"""
Pull cost data and (optionally) persist it via utils/db.py
"""
from app.services import aws_service, azure_service
from app.utils import db

def main():
    db.init()
    aws_df = aws_service.get_cost_breakdown()
    az_df  = azure_service.get_cost_breakdown()

    for _, r in aws_df.iterrows():
        db.insert_cost("aws", r["service"], r["region"], r["month"], float(r["cost"]))
    for _, r in az_df.iterrows():
        db.insert_cost("azure", r["service"], r["region"], r["month"], float(r["cost"]))
    print("Inserted costs into SQLite at cloud_costs.sqlite")

if __name__ == "__main__":
    main()