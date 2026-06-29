#!/usr/bin/env python3
"""Generate multi-account organization architecture diagram."""
import xml.etree.ElementTree as ET

# Style constants - AWS official colors
ICON = 'sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.{service};'
GEN = 'sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3E;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{service};'
AWS_CLOUD = 'points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;'
ACCOUNT = 'points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;strokeColor=#CD2264;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#CD2264;dashed=1;'
VPC = 'points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=10;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;'
PUB_SUBNET = 'points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=10;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#7AA116;fillColor=#E9F3E6;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;'
PRI_SUBNET = 'points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=10;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;'
OU_BOX = 'fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;fontStyle=1;fontColor=#5A6C86;whiteSpace=wrap;html=1;fontSize=11;'
EDGE = 'html=1;strokeColor=#232F3E;strokeWidth=1;'
EDGE_TGW = 'edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#232F3E;strokeWidth=1;'

cells = []
cell_id = [2]  # mutable counter

def add(value, style, x, y, w, h, parent="1"):
    cid = str(cell_id[0]); cell_id[0] += 1
    cells.append(f'        <mxCell id="{cid}" value="{value}" style="{style}" vertex="1" parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>')
    return cid

def edge(src, tgt, style=EDGE):
    cid = str(cell_id[0]); cell_id[0] += 1
    cells.append(f'        <mxCell id="{cid}" style="{style}" edge="1" source="{src}" target="{tgt}" parent="1"><mxGeometry relative="1" as="geometry" /></mxCell>')

# Title
add('<b>Enterprise Multi-Account Architecture</b><br><span style="font-size:10px;color:#666">Hub-Spoke Networking with Centralized Security</span>', 'text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=14;spacing=8;', 40, 30, 450, 50)

# On-premise
onprem = add('On-Premise DC', GEN.format(service='traditional_server'), 600, 80, 40, 40)
users_icon = add('HQ &amp;amp; Subsidiaries', GEN.format(service='users'), 500, 80, 40, 40)
vpn = add('VPN', ICON.format(fill='#8C4FFF', service='vpn_connection'), 700, 80, 40, 40)

# AWS Cloud boundary
add('AWS Cloud', AWS_CLOUD, 40, 160, 1520, 1100)

# Network Account
add('Network Account', ACCOUNT, 60, 200, 500, 280)
add('VPC (10.220.0.0/16)', VPC, 80, 240, 460, 220)
add('Public Subnet', PUB_SUBNET, 100, 280, 200, 160)
fgt1 = add('FortiGate 1', ICON.format(fill='#ED7100', service='ec2'), 120, 330, 40, 40)
fgt2 = add('FortiGate 2', ICON.format(fill='#ED7100', service='ec2'), 200, 330, 40, 40)
add('HA', 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#ED7100;fontSize=9;', 110, 310, 150, 80)
tgw = add('Transit Gateway', ICON.format(fill='#8C4FFF', service='transit_gateway'), 380, 330, 40, 40)

# Shared Services Account
add('Shared Services Account', ACCOUNT, 600, 200, 300, 200)
add('Private Subnet', PRI_SUBNET, 620, 260, 260, 120)
ad1 = add('AD01', ICON.format(fill='#ED7100', service='ec2'), 650, 300, 40, 40)
ad2 = add('AD02', ICON.format(fill='#ED7100', service='ec2'), 750, 300, 40, 40)

# Security & Monitoring (right sidebar)
add('Security &amp;amp; Monitoring', OU_BOX, 960, 200, 580, 120)
add('S3 &amp;amp; Backup', ICON.format(fill='#3F8624', service='s3'), 990, 250, 40, 40)
add('CloudTrail', ICON.format(fill='#E7157B', service='cloudtrail'), 1070, 250, 40, 40)
add('CloudWatch', ICON.format(fill='#E7157B', service='cloudwatch'), 1150, 250, 40, 40)
add('KMS', ICON.format(fill='#DD344C', service='key_management_service'), 1230, 250, 40, 40)
add('Secrets Mgr', ICON.format(fill='#DD344C', service='secrets_manager'), 1310, 250, 40, 40)
add('GuardDuty', ICON.format(fill='#DD344C', service='guardduty'), 1390, 250, 40, 40)

# Identity (left sidebar)
add('IAM Identity Center', ICON.format(fill='#DD344C', service='single_sign_on'), 60, 520, 40, 40)
add('Systems Manager', ICON.format(fill='#E7157B', service='systems_manager'), 60, 620, 40, 40)
add('CloudWatch Logs', ICON.format(fill='#E7157B', service='cloudwatch'), 60, 720, 40, 40)

# OU container
add('Organization Unit = Grouping of Business Unit', OU_BOX, 180, 520, 1360, 720)

# Create 4 OU workload columns
ous = ['BU-Alpha', 'BU-Beta', 'BU-Gamma', 'BU-Delta']
ou_x = [200, 540, 880, 1220]

for i, (name, x) in enumerate(zip(ous, ou_x)):
    # Account box
    add(f'{name} Production', ACCOUNT, x, 560, 300, 320)
    add(f'VPC', VPC, x+10, 600, 280, 260)
    
    # TGW attachment icon
    tgw_att = add('TGW Attach', ICON.format(fill='#8C4FFF', service='transit_gateway'), x+130, 610, 30, 30)
    edge(tgw_att, tgw, EDGE_TGW)
    
    # App subnet
    add('Private Subnet (App)', PRI_SUBNET, x+20, 660, 260, 80)
    add('EC2', ICON.format(fill='#ED7100', service='ec2'), x+100, 685, 35, 35)
    
    # DB subnet  
    add('Private Subnet (DB)', PRI_SUBNET, x+20, 760, 260, 80)
    add('EC2', ICON.format(fill='#ED7100', service='ec2'), x+100, 785, 35, 35)

# Edge: VPN to TGW
edge(vpn, tgw, EDGE)

# Build XML
xml = f'''<mxfile host="app.diagrams.net">
  <diagram id="multi-acct" name="Multi-Account Organization">
    <mxGraphModel dx="1800" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1300" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

out = '/mnt/c/Users/ykchin/Documents/Axrail-Project/General/aws-architecture-patterns/01-multi-account-organization/multi-account-organization.drawio'
with open(out, 'w') as f:
    f.write(xml)

# Validate
tree = ET.parse(out)
all_cells = tree.findall('.//mxCell')
edges_count = len([c for c in all_cells if c.get('edge')=='1'])
print(f'✓ Generated: {out}')
print(f'  Cells: {len(all_cells)} | Edges: {edges_count}')
