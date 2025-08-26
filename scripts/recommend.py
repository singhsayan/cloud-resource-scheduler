from app.services import aws_service, azure_service, analyzer

def main():
    aws = aws_service.get_cost_summary()
    az  = azure_service.get_cost_summary()
    recs = analyzer.generate_recommendations({"aws": aws, "azure": az})
    print(f"AWS Cost: ${aws:,.2f}")
    print(f"Azure Cost: ${az:,.2f}\n")
    print("Recommendations:")
    for r in recs:
        print(" -", r)

if __name__ == "__main__":
    main()