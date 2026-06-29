# Diagram Skills Load Test Plan

## Purpose
Test the diagram generation skills against multiple real-world scenarios to validate market readiness.

## Test Scenarios

### Test 1: Serverless API (from scratch — common pattern)
- API Gateway → Lambda → DynamoDB
- CloudFront CDN, Cognito auth, S3 static hosting
- CloudWatch monitoring
- Tests: basic flow, 1-to-many fan-out from API GW to multiple Lambdas

### Test 2: ECS Blue-Green Deployment (complex networking)
- ALB with weighted target groups
- ECS Fargate tasks in private subnets
- CodePipeline → CodeBuild → ECR → ECS deploy
- Tests: CI/CD pipeline flow, multi-AZ, blue/green split arrows

### Test 3: Data Lake (many-to-many connections)
- S3 raw/curated/analytics buckets
- Glue ETL jobs, Glue Catalog
- Athena, Redshift, QuickSight
- Kinesis ingestion
- Tests: complex data flow with multiple paths, lake zones as containers

### Test 4: Multi-Region DR (cross-region arrows)
- Primary region: full stack
- DR region: minimal (pilot light)
- Route53 failover, S3 cross-region replication, RDS read replica
- Tests: cross-region arrows, dotted lines for replication

### Test 5: Hybrid Cloud (on-premise + AWS)
- On-premise DC with VMware
- AWS Direct Connect + VPN backup
- Transit Gateway hub
- Migration path arrows (MGN)
- Tests: on-prem to cloud arrows, dual connectivity paths

## Validation Criteria Per Test
- [ ] Zero resource omission from description
- [ ] All arrows follow style decision logic (straight/zigzag)
- [ ] Many-to-1 uses merge pattern
- [ ] 1-to-many uses bus pattern  
- [ ] No arrow overlaps containers
- [ ] Arrows enter containers from top/bottom (not side)
- [ ] 20px+ clearance from all borders
- [ ] Legend panel present
- [ ] Render to PNG and visual verify

## Sanitization Checklist
- [ ] No real IPs (use 10.x.x.x generic)
- [ ] No real account IDs (use 123456789012)
- [ ] No client names
- [ ] No real ARNs
- [ ] No real domain names

## Location
Generate all test outputs to:
```
C:\Users\ykchin\Documents\Axrail-Project\General\aws-architecture-patterns\
```

Push only after security scan passes.
