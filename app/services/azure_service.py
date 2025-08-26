import random
import pandas as pd
from datetime import datetime, timedelta, timezone

# -----------------------------
# Config
# -----------------------------
DEMO_MODE = True  # ✅ Toggle this: True = mock data, False = real Azure data

# -----------------------------
# 1. Cost Summary
# -----------------------------
def get_cost_summary() -> float:
    if DEMO_MODE:
        today = datetime.now(timezone.utc).date()
        random.seed(today.toordinal())  # stable mock per day
        return round(random.uniform(200, 1200), 2)

    # Real Azure Cost API (requires subscription + billing setup)
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.consumption import ConsumptionManagementClient
    from azure.mgmt.resource import SubscriptionClient

    credential = DefaultAzureCredential()
    subscription_client = SubscriptionClient(credential)
    subscription_id = next(subscription_client.subscriptions.list()).subscription_id

    client = ConsumptionManagementClient(credential, subscription_id)
    end = datetime.utcnow().date()
    start = end - timedelta(days=30)

    usage = client.usage_details.list(
        scope=f"/subscriptions/{subscription_id}",
        expand="properties/meterDetails",
        filter=f"properties/usageStart ge '{start}' and properties/usageEnd le '{end}'"
    )

    total = sum(float(item.pretax_cost) for item in usage)
    return round(total, 2)

# -----------------------------
# 2. Cost Breakdown
# -----------------------------
def get_cost_breakdown() -> pd.DataFrame:
    if DEMO_MODE:
        end = datetime.now(timezone.utc).replace(day=1)
        months = [(end - timedelta(days=30*i)).strftime("%Y-%m") for i in reversed(range(6))]

        services = [
            "Virtual Machines",
            "Storage Accounts",
            "SQL Database",
            "Functions",
            "AKS (Kubernetes)",
            "Application Gateway",
            "Monitor"
        ]
        regions = ["eastus"]  # keep single common region for mock clarity

        rows = []
        for m in months:
            for s in services:
                cost = round(random.uniform(20, 300), 2)
                rows.append([m, s, regions[0], cost])

        return pd.DataFrame(rows, columns=["month", "service", "region", "cost"])

    # Real implementation would query Azure Cost Management API
    raise NotImplementedError("Azure cost breakdown requires billing API setup.")

# -----------------------------
# 3. Idle / Underutilized Resources
# -----------------------------
def list_idle_resources():
    if DEMO_MODE:
        return [
            "vm-prod-01",
            "disk-backup-02",
            "ip-staging-33",
            "gateway-test"
        ]

    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.resource import SubscriptionClient

    credential = DefaultAzureCredential()
    subscription_client = SubscriptionClient(credential)
    subscription_id = next(subscription_client.subscriptions.list()).subscription_id

    compute_client = ComputeManagementClient(credential, subscription_id)
    vms = compute_client.virtual_machines.list_all()

    idle_resources = []
    for vm in vms:
        # Placeholder: real idle check would need Azure Monitor metrics
        idle_resources.append(vm.name)

    return idle_resources