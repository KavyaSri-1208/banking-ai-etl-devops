# Architecture notes

## Four-server learning layout

1. EC2 Server 1: DevOps master — Jenkins, Git, Docker, SonarQube, Terraform, KOPS and kubectl.
2. KOPS control-plane EC2: Kubernetes control plane.
3. KOPS worker EC2 1: ETL and API workloads.
4. KOPS worker EC2 2: Streamlit and supporting workloads.

KOPS creates/manages the control plane and worker EC2 instances. These are separate from the DevOps master. A single control plane is for learning only and is not highly available.

## Data flow

Synthetic CSV -> legacy Python ETL and PySpark ETL -> processed/excluded/summary outputs -> reconciliation -> tests -> Docker images -> ECR -> Kubernetes.

## Environment model

Namespaces `banking-dev`, `banking-uat` and `banking-prod` are logical separation for this demonstration. Namespace separation alone is not sufficient for real production isolation.
