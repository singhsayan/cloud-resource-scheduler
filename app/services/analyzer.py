def generate_recommendations(cost_data: dict[str, float]) -> list[str]:
    recs: list[str] = []

    aws = cost_data.get("aws", 0.0)
    az  = cost_data.get("azure", 0.0)

    if aws > 400:
        recs.append("AWS: Consider Reserved Instances/Savings Plans for steady workloads.")
    if aws > 300:
        recs.append("AWS: Move non-prod EC2 to schedule-based stop/start.")
    if az > 350:
        recs.append("Azure: Explore Reserved VM Instances and Hybrid Benefit.")
    if az > 250:
        recs.append("Azure: Use Spot VMs for fault-tolerant workloads.")
    if aws < 200 and az < 200:
        recs.append(" Costs look healthy. Keep monitoring utilization & rightsizing.")

    # Generic
    recs.append("Cross-cloud: Right-size VMs, delete unattached disks/volumes, and set lifecycle policies for storage.")
    return recs