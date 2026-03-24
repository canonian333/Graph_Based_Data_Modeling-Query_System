import pandas as pd
import glob
import os

def df_to_markdown(df):
    try:
        return df.to_markdown(index=False)
    except ImportError:
        # Fallback if tabulate is not installed
        header = "| " + " | ".join(map(str, df.columns)) + " |"
        separator = "| " + " | ".join(["---"] * len(df.columns)) + " |"
        rows = []
        for _, row in df.iterrows():
            rows.append("| " + " | ".join(map(str, row.values)) + " |")
        return "\n".join([header, separator] + rows)

base_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\data\sap-o2c-data"
report_dir = r"f:\Projects\Graph_Based_Data_Modeling-Query_System\reports"
os.makedirs(report_dir, exist_ok=True)
report_file = os.path.join(report_dir, "EDA.md")

print(f"Generating EDA report at {report_file}...")

with open(report_file, "w", encoding='utf-8') as f:
    f.write("# Exploratory Data Analysis Report\n\n")

    for folder in sorted(os.listdir(base_dir)):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        print(f"Processing folder: {folder}")
        f.write(f"## Dataset: `{folder}`\n\n")

        # Load all jsonl files in the folder
        jsonl_files = glob.glob(os.path.join(folder_path, "*.jsonl"))
        if not jsonl_files:
            f.write("No `.jsonl` files found in this directory.\n\n")
            continue

        df_list = []
        for file in jsonl_files:
            try:
                df_part = pd.read_json(file, lines=True)
                df_list.append(df_part)
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        if not df_list:
            f.write("Failed to read any `.jsonl` files successfully.\n\n")
            continue
            
        df = pd.concat(df_list, ignore_index=True)

        # Convert dicts/lists to strings to avoid unhashable type errors
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                df[col] = df[col].astype(str)

        # 1. Info / Shape
        f.write("### 1. Basic Information\n")
        f.write(f"- **Rows**: {len(df):,}\n")
        f.write(f"- **Columns**: {len(df.columns):,}\n\n")

        # 2. Datatypes
        f.write("### 2. Data Types\n")
        f.write("```markdown\n")
        dtypes_df = df.dtypes.to_frame("Type").reset_index().rename(columns={"index": "Column"})
        dtypes_df['Type'] = dtypes_df['Type'].astype(str)
        f.write(df_to_markdown(dtypes_df))
        f.write("\n```\n\n")

        # 3. Description
        f.write("### 3. Statistical Description\n")
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            f.write("```markdown\n")
            desc_df = numeric_df.describe().reset_index().rename(columns={"index": "Statistic"})
            # Truncate some precision
            desc_df = desc_df.round(4)
            f.write(df_to_markdown(desc_df))
            f.write("\n```\n\n")
        else:
            f.write("No numeric columns available to describe.\n\n")

        # 4. Nulls
        f.write("### 4. Missing Values (Nulls)\n")
        null_counts = df.isnull().sum()
        null_counts = null_counts[null_counts > 0]
        if not null_counts.empty:
            f.write("```markdown\n")
            null_df = null_counts.to_frame("Null Count").reset_index().rename(columns={"index": "Column"})
            null_df['Percentage'] = (null_df['Null Count'] / len(df) * 100).round(2).astype(str) + "%"
            f.write(df_to_markdown(null_df))
            f.write("\n```\n\n")
        else:
            f.write("No missing values found in any columns.\n\n")

        # 5. Duplicates
        duplicate_count = df.duplicated().sum()
        f.write("### 5. Duplicates\n")
        f.write(f"- **Number of fully duplicated rows**: {duplicate_count}\n\n")

        # 6. Inconsistent IDs
        f.write("### 6. Inconsistent IDs / Anomalies\n")
        id_cols = [c for c in df.columns if any(sw in str(c).lower() for sw in ['id', 'key', 'number']) or str(c).lower().endswith('_no')]
        
        inconsistencies = []
        for col in id_cols:
            col_series = df[col]
            # Check nulls
            null_id = col_series.isnull().sum()
            if null_id > 0:
                inconsistencies.append(f"- **`{col}`**: Contains {null_id} missing values.")
            
            # Check negatives if numeric
            if pd.api.types.is_numeric_dtype(col_series):
                neg_ids = (col_series < 0).sum()
                if neg_ids > 0:
                    inconsistencies.append(f"- **`{col}`**: Contains {neg_ids} negative values.")
            
            # Uniqueness check
            unique_ratio = col_series.nunique() / len(df) if len(df) > 0 else 0
            if 0.9 < unique_ratio < 1.0:
                inconsistencies.append(f"- **`{col}`**: High cardinality ({unique_ratio*100:.1f}%) but not fully unique, possibly indicating duplicate IDs or unexpected 1:N relations.")

        if inconsistencies:
            for inc in inconsistencies:
                f.write(f"{inc}\n")
            f.write("\n")
        else:
            f.write("No obvious inconsistencies detected in ID columns based on basic heuristics.\n\n")

        f.write("---\n\n")

print("EDA report generated successfully.")
