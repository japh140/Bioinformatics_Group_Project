import pandas as pd
import glob

# Define list of Populations name
populations = ["PJL", "BEB", "ITU", "GIH"]


for pp in populations:
    # Get all filtered nSL results files for each population
    nSL_files = glob.glob(f"{pp}_chr*_nSL_score_filtered.xlsx")

    # Read and concatenate all files for this population
    df_list = [pd.read_excel(file) for file in nSL_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    # Save the combined file
    output_file = f"{pp}_combined_nSL_scores.xlsx"
    combined_df.to_excel(output_file, index=False, engine="openpyxl")

    print("nSL results files are merged !")
