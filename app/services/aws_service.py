import boto3
import pandas as pd
import random
from datetime import datetime, timedelta, timezone
from config import settings

# -----------------------------
# Config
# -----------------------------
DEMO_MODE = True  # ✅ Toggle this: True = mock data, False = real AWS data

# -----------------------------
# 1. Get summary (single number)
# -----------------------------
def get_cost_summary():
    if DEMO_MODE:
        today = datetime.now(timezone.utc).date()
        random.seed(today.toordinal())  # stable per day
        return round(random.uniform(50, 500), 2)

    ce = boto3.client("ce", region_name=settings.AWS_REGION)

    end = datetime.today().date()
    start = end - timedelta(days=30)

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start.strftime("%Y-%m-%d"),
            "End": end.strftime("%Y-%m-%d"),
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
    )

    return float(response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"])

# -----------------------------
# 2. Cost breakdown (per service + daily)
# -----------------------------
def get_cost_breakdown():
    if DEMO_MODE:
        end = datetime.now(timezone.utc).replace(day=1)
        days = [(end - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(30))]

        services = ["EC2", "S3", "Lambda", "EBS", "CloudWatch"]
        rows = []
        for d in days:
            for s in services:
                cost = round(random.uniform(0.1, 5.0), 2)
                month = d[:7]
                rows.append([s, cost, d, month])
        return pd.DataFrame(rows, columns=["service", "cost", "date", "month"])

    ce = boto3.client("ce", region_name=settings.AWS_REGION)

    end = datetime.today().date()
    start = end - timedelta(days=30)   # last 30 days

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start.strftime("%Y-%m-%d"),
            "End": end.strftime("%Y-%m-%d"),
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    rows = []
    for result in response["ResultsByTime"]:
        date = result["TimePeriod"]["Start"]
        month = date[:7]  # YYYY-MM
        for group in result["Groups"]:
            service = group["Keys"][0]
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            rows.append([service, amount, date, month])

    return pd.DataFrame(rows, columns=["service", "cost", "date", "month"])

# -----------------------------
# 3. Idle resources
# -----------------------------
def list_idle_resources():
    if DEMO_MODE:
        return [
            "ec2-demo",
            "vol-123",
            "eip-demo-789",
            "my-s3-practice-bucket-sayan",
            "test-function"
        ]

    idle_resources = []

    ec2 = boto3.client("ec2", region_name=settings.AWS_REGION)
    cloudwatch = boto3.client("cloudwatch", region_name=settings.AWS_REGION)
    s3 = boto3.client("s3", region_name=settings.AWS_REGION)
    lam = boto3.client("lambda", region_name=settings.AWS_REGION)

    # --- EC2 instances idle check ---
    instances = ec2.describe_instances()
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            metrics = cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=datetime.utcnow() - timedelta(days=7),
                EndTime=datetime.utcnow(),
                Period=3600,
                Statistics=["Average"],
            )

            datapoints = metrics.get("Datapoints", [])
            if datapoints:
                avg_cpu = sum(dp["Average"] for dp in datapoints) / len(datapoints)
                if avg_cpu < 2:  # idle threshold
                    idle_resources.append(
                        f"EC2 instance {instance_id} (CPU < {round(avg_cpu,2)}% last 7d)"
                    )

    # --- Unattached EBS volumes ---
    volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])
    for vol in volumes["Volumes"]:
        idle_resources.append(f"EBS volume {vol['VolumeId']} (unattached)")

    # --- Unused Elastic IPs ---
    addresses = ec2.describe_addresses()
    for addr in addresses["Addresses"]:
        if "InstanceId" not in addr:
            idle_resources.append(f"Elastic IP {addr['AllocationId']} (unused)")

    # --- S3 buckets with no requests ---
    buckets = s3.list_buckets()
    for bucket in buckets["Buckets"]:
        name = bucket["Name"]
        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/S3",
            MetricName="NumberOfObjects",
            Dimensions=[{"Name": "BucketName", "Value": name}, {"Name": "StorageType", "Value": "AllStorageTypes"}],
            StartTime=datetime.utcnow() - timedelta(days=30),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=["Average"],
        )
        datapoints = metrics.get("Datapoints", [])
        if not datapoints:
            idle_resources.append(f"S3 bucket {name} (no objects/requests last 30d)")

    # --- Lambda functions with zero invocations ---
    functions = lam.list_functions()
    for fn in functions.get("Functions", []):
        fn_name = fn["FunctionName"]
        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Invocations",
            Dimensions=[{"Name": "FunctionName", "Value": fn_name}],
            StartTime=datetime.utcnow() - timedelta(days=30),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=["Sum"],
        )
        datapoints = metrics.get("Datapoints", [])
        total_invocations = sum(dp["Sum"] for dp in datapoints) if datapoints else 0
        if total_invocations == 0:
            idle_resources.append(f"Lambda function {fn_name} (no invocations last 30d)")

    return idle_resources