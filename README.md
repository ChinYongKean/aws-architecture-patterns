# AWS Architecture Patterns

Production-grade AWS architecture diagrams from real enterprise deployments. Each pattern includes an editable `.drawio` diagram, design decisions, and scaling guidance.

## Patterns

| # | Pattern | Key Services | Accounts |
|---|---------|-------------|----------|
| 01 | [Multi-Account Organization](./01-multi-account-organization/) | Organizations, Transit Gateway, FortiGate HA, IAM Identity Center | 15+ |
| 02 | Hub-Spoke Network *(coming soon)* | Transit Gateway, FortiGate, cross-account ALBs | 6+ |
| 03 | Serverless + PrivateLink *(coming soon)* | Lambda, API GW, DynamoDB, NLB, PrivateLink | 3 |
| 04 | Multi-Tier Workload *(coming soon)* | ALB, ASG, EC2, RDS, NAT Gateway | 1 |
| 05 | Data Analytics Pipeline *(coming soon)* | S3, SageMaker, QuickSight, ETL | 1 |

## How to Use

1. Open any `.drawio` file in [draw.io](https://app.diagrams.net/) or VS Code with the draw.io extension
2. Read the pattern's `README.md` for design decisions and when to use
3. Adapt to your project — rename accounts, adjust CIDRs, add services

## Design Principles

- **No client names** — all patterns are sanitized and genericized
- **Real-world tested** — every pattern was deployed in production
- **Opinionated** — includes design decisions and trade-offs, not just boxes and arrows
- **Scalable** — each pattern documents how to scale beyond the shown components

## Author

Chin Yong Kean — AWS 12x Certified Solutions Architect
