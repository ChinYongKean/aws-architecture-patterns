# Multi-Account Organization with Hub-Spoke Networking

## Architecture Pattern

Enterprise-grade AWS multi-account structure with centralized network security via Transit Gateway and FortiGate HA pair. Supports 15+ workload accounts across 4 business units.

## When to Use

- Enterprise with multiple business units needing network isolation
- Regulatory requirement for centralized security inspection (firewall)
- On-premise connectivity via Site-to-Site VPN
- Centralized identity management (IAM Identity Center)
- Shared services (Active Directory, DNS) across accounts

## Components

| Layer | Service | Purpose |
|-------|---------|---------|
| On-Premise | VPN Connection | Site-to-site connectivity to COLO/DC |
| Network Hub | FortiGate HA (EC2) | Centralized firewall, traffic inspection |
| Network Hub | Transit Gateway | Hub for all VPC attachments |
| Shared Services | Active Directory (EC2) | Domain services for all accounts |
| Shared Services | VPC Peering | AD connectivity to legacy account |
| Identity | IAM Identity Center | SSO for all accounts via MFA |
| Access | Systems Manager | Session Manager for RDP/SSH (no bastion) |
| Security | KMS, Secrets Manager | Encryption keys, secret rotation |
| Monitoring | CloudTrail, CloudWatch | Centralized logging |
| Storage | S3, AWS Backup | Centralized backup vault |
| Workloads | EC2 in private subnets | App tier + DB tier per account |

## Design Decisions

1. **FortiGate over AWS Network Firewall** — client had existing Fortinet licensing and expertise
2. **Transit Gateway over VPC Peering** — scales to 15+ accounts without N² peering mesh
3. **Separate Network Account** — isolates blast radius, single point for security controls
4. **No bastion hosts** — Session Manager provides audited access without open ports
5. **Private subnets only for workloads** — all internet egress through FortiGate NAT
6. **OU-based grouping** — maps to business units for SCPs and billing separation

## Scaling

- Add new workload: create account in OU → TGW attachment → VPC with standard template
- Add new business unit: create OU → same pattern replicates
- Current: 15 accounts. Tested pattern supports 100+ without TGW route table limits.

## Files

- `multi-account-organization.drawio` — Full architecture diagram
- `README.md` — This file
