import pandas as pd

# Define list of Populations name and chromosomes (1-22)
populations = ["PJL", "BEB", "ITU", "GIH"]
chromosomes = range(1, 23)  

# Load the T2D chromosomes positions file into one DataFrame
t2d_df = pd.read_csv("t2d_chrom_position.txt", sep="\t", header=None, names=["chr", "position"])

# Convert chromosome to string to avoid errors
t2d_df["chr"] = t2d_df["chr"].astype(str)

# Process Each Population one at a time
for pp in populations:
    for chrm_no in chromosomes:
        nsl_file = f"{pp}_chr{chrm_no}_nSL_score.xlsx"
        nsl_df = pd.read_excel(nsl_file) 

        nsl_df["chr"] = nsl_df["chr"].astype(str)

        # Merge nSL data with T2D positions
        filtered_nsl = nsl_df.merge(t2d_df, on=["chr", "position"])

        # Save filtered nSL results file
        output_file = f"{pp}_chr{chrm_no}_nSL_score_filtered.xlsx"
        filtered_nsl.to_excel(output_file, index=False)
