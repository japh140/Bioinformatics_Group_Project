import pandas as pd

# Define list of Populations name
populations = ["PJL", "BEB", "ITU", "GIH"]  

# Process Each Population one at a time
for pop in populations:
    file_path = f"Fst_results_{pop}_CEU_annotated.xlsx"  # this brings Fst results file for all populations
    
    # Load the Fst results Excel file
    df = pd.read_excel(file_path, engine="openpyxl")

    # Remove duplicate rows
    df_cleaned = df.drop_duplicates()

    # Save cleaned Fst results files
    output_file = f"Fst_results_{pop}_CEU_cleaned.xlsx"
    df_cleaned.to_excel(output_file, index=False, engine="openpyxl")

    print("Duplicates removed from Fst results files")
