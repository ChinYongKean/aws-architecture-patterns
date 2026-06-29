# NLB + Auto Scaling Group with Active Directory Domain Join Automation

## Architecture Pattern

Internal Network Load Balancer fronting a Windows Auto Scaling Group with automated Active Directory domain join/unjoin via Lambda lifecycle hooks. Zero manual intervention for server provisioning.

## System Flow

```
                        ┌─────────────────────────────────────────────────┐
                        │  VPC (Private Subnet)                           │
                        │                                                 │
  On-Premise ──────────►│  ┌─────────┐     ┌──────────────────────────┐  │
  (FortiGate)           │  │   NLB   │────►│  ASG (min:1, max:3)      │  │
                        │  │ internal │     │  ┌─────┐ ┌─────┐        │  │
                        │  │10.54.x.88│     │  │ EC2 │ │ EC2 │ ...    │  │
                        │  │          │     │  │Win  │ │Win  │        │  │
                        │  │ 8 TCP    │     │  └──┬──┘ └──┬──┘        │  │
                        │  │listeners │     └─────┼───────┼────────────┘  │
                        │  └─────────┘            │       │               │
                        │                         │       │               │
                        │  ┌──────────────────────┼───────┼────────────┐  │
                        │  │ Lambda (VPC)         ▼       ▼            │  │
                        │  │ ┌────────────┐  ┌────────────┐           │  │
                        │  │ │Domain Join │  │Domain Unjoin│           │  │
                        │  │ └─────┬──────┘  └─────┬──────┘           │  │
                        │  └───────┼───────────────┼───────────────────┘  │
                        └──────────┼───────────────┼──────────────────────┘
                                   │               │
                    ┌──────────────┼───────────────┼──────────────┐
                    │              ▼               ▼              │
                    │  ┌──────────────┐  ┌─────────────────┐     │
                    │  │Secrets Mgr   │  │SSM Parameter     │     │
                    │  │AD Credentials│  │Hostname Pool(99) │     │
                    │  └──────────────┘  └─────────────────┘     │
                    │                                             │
                    │  ┌──────────────┐  ┌─────────────────┐     │
                    │  │EventBridge   │  │CloudWatch Alarms │     │
                    │  │Lifecycle Hook│  │CPU >40%: +1      │     │
                    │  │Triggers      │  │CPU <25%: -1      │     │
                    │  └──────────────┘  └─────────────────┘     │
                    └─────────────────────────────────────────────┘
                                   │
                                   ▼ LDAP 389/636
                    ┌──────────────────────────┐
                    │  Active Directory DC      │
                    │  10.52.62.42 (ql.group)   │
                    └──────────────────────────┘
```

## When to Use

- Windows workloads requiring Active Directory domain membership
- Scaling servers that need unique hostnames in AD
- Internal services accessed via TCP (not HTTP) — requires NLB over ALB
- Automated provisioning with zero manual domain join steps

## Components

| Layer | Resource | Config |
|-------|----------|--------|
| Load Balancing | NLB (internal) | IP: 10.54.64.88, 8 TCP listeners (7045-7048, 8045-8048) |
| Compute | Primary EC2 | m6a.2xlarge, 10.54.64.91, Windows, 150GB+50GB EBS |
| Compute | ASG | Min 1, Max 3, lifecycle hooks (launch + terminate) |
| Compute | Launch Template | Same as primary: m6a.2xlarge, 2 EBS volumes |
| Automation | Lambda (Join) | Python 3.12, VPC-attached, 600s timeout |
| Automation | Lambda (Unjoin) | Python 3.12, VPC-attached, 300s timeout |
| Events | EventBridge | Triggers on EC2_INSTANCE_LAUNCHING / TERMINATING |
| Scaling | CloudWatch Alarms | CPU >40% → scale out, CPU <25% → scale in |
| Secrets | Secrets Manager | AD credentials (ql.group domain) |
| Config | SSM Parameter | Hostname pool (FMWEB-ASG-01 to FMWEB-ASG-99) |
| Security | 3 Security Groups | NLB SG, Lambda SG (LDAP), EC2 SGs |
| IAM | Lambda Role | SSM, Secrets, ASG, EC2, CloudWatch permissions |
| External | Active Directory | 10.52.62.42, LDAP 389/636 |

## Lifecycle Flow

### Instance Launch (Domain Join)
```
1. ASG launches new instance
2. Lifecycle hook pauses launch (600s timeout)
3. EventBridge triggers Domain Join Lambda
4. Lambda:
   a. Allocates hostname from SSM pool (e.g., FMWEB-ASG-07)
   b. Tags EC2 with hostname
   c. Reads AD creds from Secrets Manager
   d. Waits for SSM agent online
   e. Executes PowerShell via SSM Run Command:
      - Remove-Computer (unjoin if stale)
      - Add-Computer (join domain with new hostname)
      - Restart
   f. Completes lifecycle action → CONTINUE
5. Instance joins target groups, starts receiving traffic
```

### Instance Terminate (Domain Unjoin)
```
1. ASG terminates instance (scale-in or unhealthy)
2. Lifecycle hook pauses termination (300s timeout)
3. EventBridge triggers Domain Unjoin Lambda
4. Lambda:
   a. Reads hostname from EC2 tags
   b. Removes computer object from AD
   c. Returns hostname to SSM pool
   d. Completes lifecycle action → CONTINUE
5. Instance terminates cleanly
```

## Design Decisions

1. **NLB over ALB** — application uses raw TCP on custom ports (7045-8048), not HTTP
2. **Lifecycle hooks** — prevents instance serving traffic before domain join completes (ABANDON on failure)
3. **SSM hostname pool** — atomic allocation prevents duplicate hostnames across concurrent launches
4. **Lambda in VPC** — required for LDAP connectivity to on-premise AD (via FortiGate)
5. **Primary EC2 separate from ASG** — stable instance for baseline, ASG handles burst
6. **600s launch timeout** — domain join + restart takes ~3-5 minutes
7. **Scale thresholds 40%/25%** — conservative to avoid flapping (6 evaluation periods for scale-in)

## Security

- No public IPs — all traffic via internal NLB
- Lambda SG restricts egress to AD (LDAP 389/636) + HTTPS (443 for AWS APIs)
- EC2 managed via SSM Session Manager (no SSH/RDP ports open)
- AD credentials in Secrets Manager (not hardcoded)
- IAM role follows least privilege per action

## Files

- `fm-prod-web.drawio` — Architecture diagram
- `README.md` — This file
