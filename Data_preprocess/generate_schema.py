import os
import json
import glob

base_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\preprocesed_data"
report_file = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports\schema.md"

def generate_schema():
    schema_stats = {}
    
    # Gather schema for all folders
    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue
            
        jsonl_files = glob.glob(os.path.join(folder_path, "*.jsonl"))
        if not jsonl_files:
            continue
            
        # Read the first line of the first file to get schema
        try:
            with open(jsonl_files[0], 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line:
                    record = json.loads(first_line)
                    schema_stats[folder] = list(record.keys())
        except Exception as e:
            print(f"Error reading {folder}: {e}")
            
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# O2C Preprocessed Data Schema\n\n")
        
        # Mermaid Graph
        f.write("## Entity Relationship Graph\n\n")
        f.write("This subgraph illustrates the relationships between core entities based on foreign keys.\n\n")
        f.write("```mermaid\n")
        f.write("erDiagram\n")
        f.write("    CUSTOMER ||--o{ SALES_ORDER : \"places\"\n")
        f.write("    CUSTOMER ||--o{ BILLING_DOCUMENT : \"receives\"\n")
        f.write("    CUSTOMER ||--o{ ACCOUNTING_DOCUMENT : \"has\"\n")
        f.write("    CUSTOMER ||--|| BUSINESS_PARTNER : \"is\"\n")
        f.write("    CUSTOMER }o--|| COMPANY_CODE : \"interacts_with\"\n")
        f.write("    CUSTOMER }o--|| GL_ACCOUNT : \"reconciliation_account\"\n")
        f.write("\n")
        f.write("    COMPANY_CODE ||--o{ ACCOUNTING_DOCUMENT : \"owns\"\n")
        f.write("    COMPANY_CODE ||--o{ BILLING_DOCUMENT : \"owns\"\n")
        f.write("\n")
        f.write("    SALES_ORDER ||--|{ PRODUCT : \"contains\"\n")
        f.write("    DELIVERY_DOCUMENT }o--|| SALES_ORDER : \"fulfills\"\n")
        f.write("    BILLING_DOCUMENT }o--|| DELIVERY_DOCUMENT : \"bills_for\"\n")
        f.write("\n")
        f.write("    DELIVERY_DOCUMENT }o--|| PLANT : \"shipped_from\"\n")
        f.write("    DELIVERY_DOCUMENT }o--|| SHIPPING_POINT : \"uses\"\n")
        f.write("\n")
        f.write("    BILLING_DOCUMENT ||--|{ PRODUCT : \"contains\"\n")
        f.write("    BILLING_DOCUMENT ||--|| ACCOUNTING_DOCUMENT : \"generates\"\n")
        f.write("\n")
        f.write("    ACCOUNTING_DOCUMENT }o--o| ACCOUNTING_DOCUMENT : \"cleared_by\"\n")
        f.write("    ACCOUNTING_DOCUMENT }o--|| GL_ACCOUNT : \"posts_to\"\n")
        f.write("\n")
        f.write("    PRODUCT }o--|| PLANT : \"stocked_in\"\n")
        f.write("```\n\n")
        
        # Tables schema
        f.write("## Tables Structure\n\n")
        f.write("Below is the schema (columns) for each dataset in the preprocessed data output.\n\n")
        for table, cols in schema_stats.items():
            f.write(f"### `{table}`\n")
            f.write("```markdown\n")
            f.write("| Column Name |\n")
            f.write("| :--- |\n")
            for col in cols:
                f.write(f"| {col} |\n")
            f.write("```\n\n")

if __name__ == "__main__":
    generate_schema()
    print(f"Schema report generated at {report_file}")
