import pandas as pd

# Define list of Populations name
populations = ["PJL", "BEB", "ITU", "GIH"]

# Process Each Population one at a time
for pp in populations:
    file_path = f"{pp}_nSL_scores.xlsx"  # this brings nSL results file for all populations

    # Load the Fst results file
    df = pd.read_excel(file_path, engine="openpyxl")

    # Remove Duplicate Rows
    df_cleaned = df.drop_duplicates()

    # Save cleaned nSL results files
    output_file = f"{pp}_nSL_scores_cleaned.xlsx"
    df_cleaned.to_excel(output_file, index=False, engine="openpyxl")

    print("Duplicates removed from nSL results files")
