from app.services import aws_service, azure_service

def main():
    print("AWS idle resources:")
    for r in aws_service.list_idle_resources():
        print(" -", r)
    print("\nAzure idle resources:")
    for r in azure_service.list_idle_resources():
        print(" -", r)

if __name__ == "__main__":
    main()