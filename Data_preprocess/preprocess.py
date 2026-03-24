import pandas as pd
import glob
import os

base_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\sap-o2c-data"
output_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\preprocesed_data"
report_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)

report_file = os.path.join(report_dir, "preprocess.md")

# ID mapping configurations for stable node IDs
# We will identify ID columns based on heuristics or explicit mapping and prefix them
id_prefixes = {
    'billingDocument': 'BILL_',
    'cancelledBillingDocument': 'BILL_',
    'accountingDocument': 'ACC_',
    'clearingAccountingDocument': 'ACC_',
    'referenceDocument': 'REF_',
    'soldToParty': 'CUST_',
    'businessPartner': 'BP_',
    'customer': 'CUST_',
    'deliveryDocument': 'DEL_',
    'referenceSdDocument': 'SO_',
    'salesOrder': 'SO_',
    'salesDocument': 'SO_',
    'plant': 'PLANT_',
    'shippingPoint': 'SHIP_',
    'product': 'PROD_',
    'material': 'PROD_',
    'glAccount': 'GL_',
    'reconciliationAccount': 'GL_',
    'companyCode': 'COMP_'
}

def clean_id(val):
    if pd.isna(val):
        return None
    if isinstance(val, float):
        return str(int(val))
    return str(val).strip()

def preprocess_and_save():
    with open(report_file, "w", encoding='utf-8') as f:
        f.write("# Data Preprocessing Report\n\n")
        f.write("This report details the transformations applied to the O2C dataset, including foreign key normalisation, stable node IDs, and data quality mitigations based on EDA.\n\n")
        
        for folder in sorted(os.listdir(base_dir)):
            folder_path = os.path.join(base_dir, folder)
            if not os.path.isdir(folder_path):
                continue
                
            jsonl_files = glob.glob(os.path.join(folder_path, "*.jsonl"))
            if not jsonl_files:
                continue
                
            df_list = []
            for file in jsonl_files:
                try:
                    df_part = pd.read_json(file, lines=True)
                    df_list.append(df_part)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            if not df_list:
                continue
                
            df = pd.concat(df_list, ignore_index=True)
            original_rows = len(df)
            original_cols = len(df.columns)
            
            f.write(f"## Dataset: `{folder}`\n")
            f.write(f"- **Original Shape**: {original_rows} rows, {original_cols} columns\n")
            
            # Convert dicts/lists to strings to avoid unhashable type errors
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                    df[col] = df[col].astype(str)

            # Data Quality & Mitigations
            # 1. Drop duplicates
            df = df.drop_duplicates()
            dedup_rows = len(df)
            f.write(f"- **Duplicates Removed**: {original_rows - dedup_rows}\n")
            
            # 2. Drop columns with > 90% missing values as identified in EDA
            missing_ratio = df.isnull().mean()
            cols_to_drop = missing_ratio[missing_ratio > 0.90].index.tolist()
            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)
                f.write(f"- **Dropped sparse columns (>90% null)**: {', '.join(cols_to_drop)}\n")
            
            # 3. Handle missing values in remaining columns
            # For categorical strings, fill with 'UNKNOWN' config or simply leave null
            # Wait, replacing with UNKNOWN might be bad for Graph DBs where null properties are omitted.
            # We will leave normal nulls, but ensure ID columns are cleaned up.
            
            # Foreign Key Normalization and Stable Node IDs
            transformed_cols = []
            for col in df.columns:
                if col in id_prefixes:
                    # Clean the ID (remove .0, convert to string)
                    df[col] = df[col].apply(clean_id)
                    
                    # Context-aware logic for referenceSdDocument
                    if col == 'referenceSdDocument' and folder == 'billing_document_items':
                        prefix = 'DEL_'
                    else:
                        prefix = id_prefixes[col]
                    
                    # Apply prefix for stable node ID
                    df[col] = df[col].apply(lambda x: prefix + x if x else x)
                    transformed_cols.append(col)
                # Some IDs might not be in the prefix list, but we should make sure they are strings if they end with ID, Document, etc.
                elif any(sw in str(col).lower() for sw in ['id', 'key', 'number']) or str(col).lower().endswith('_no'):
                     df[col] = df[col].apply(clean_id)
                    
            if transformed_cols:
                f.write(f"- **Normalised IDs & Assigned Stable Prefixes**: {', '.join(transformed_cols)}\n")
                
            f.write(f"- **Final Shape**: {len(df)} rows, {len(df.columns)} columns\n\n")
            
            # Save to preprocesed_data
            out_folder = os.path.join(output_dir, folder)
            os.makedirs(out_folder, exist_ok=True)
            out_file = os.path.join(out_folder, f"{folder}_preprocessed.jsonl")
            
            # Convert dict/list columns to string so json serialization doesn't fail if nested
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                    df[col] = df[col].astype(str)
                    
            df.to_json(out_file, orient='records', lines=True)
            print(f"Processed {folder} -> {out_file}")

if __name__ == "__main__":
    print("Starting preprocessing...")
    preprocess_and_save()
    print(f"Preprocessing complete. Report saved to {report_file}")
