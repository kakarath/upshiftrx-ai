import pandas as pd
import os
from pathlib import Path

def combine_results(results_dir="results", output_file="results/master_results.csv"):
    # Validate and sanitize paths
    path = Path(results_dir).resolve()
    output_path = Path(output_file).resolve()
    
    # Ensure output directory exists
    os.makedirs(output_path.parent, exist_ok=True)
    
    all_files = list(path.glob("*.csv"))
    print(f"Found {len(all_files)} CSV files")

    dfs = []
    for f in all_files:
        try:
            df = pd.read_csv(f)
            if not df.empty:
                dfs.append(df)
        except (pd.errors.EmptyDataError, FileNotFoundError) as e:
            print(f"Skipping {f}: {e}")
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if dfs:
        try:
            master = pd.concat(dfs, ignore_index=True)
            master.to_csv(output_path, index=False)
            print(f"✅ Combined {len(dfs)} files into {output_path}")
        except Exception as e:
            print(f"Error saving combined file: {e}")
    else:
        print("⚠️ No valid CSV files found to combine.")

if __name__ == "__main__":
    combine_results()
