import pandas as pd

# lists of all T2D SNP dataset csv files
snp_csv_files = [
    "DIAMANTE2022T2DGWASassociations.csv",
    "Genes&HealthT2D2022GWASassociations.csv",
    "T2DGGI2024T2DGWASassociations.csv",
    "EU_T2DGGI2024T2DGWASassociations.csv",
    "Type2diabetes2022GWASassociations.csv"
]

# Load all SNP dataset csv files into one DataFrame
snps_dataset = pd.concat([pd.read_csv(f) for f in snp_csv_files], ignore_index=True)

# Rename the colmumn to ensure the correct name in place 
snps_dataset.rename(columns={"chromosome": "CHROM", "position": "POS", "dbSNP": "SNP_ID"}, inplace=True)

# Convert chromosome to string to avoid error
snps_dataset["CHROM"] = snps_dataset["CHROM"].astype(str)

# Define list of Populations name
populations = ["PJL", "BEB", "ITU", "GIH"]

# Process Each Population one at a time
for pp in populations:
    nsl_file = f"{pp}_combined_nSL_scores.xlsx"  # # this brings nSL results file for all populations

    # Load nSL data 
    nsl_df = pd.read_excel(nsl_file, engine="openpyxl")

    # Rename columns if needed to match the SNP dataset
    nsl_df.rename(columns={"chr": "CHROM", "position": "POS"}, inplace=True)
    
    # Convert chromosome to string to avoid errors 
    nsl_df["CHROM"] = nsl_df["CHROM"].astype(str)

    # Merge nSL results with rsIDs
    annotated_nsl_df = nsl_df.merge(snps_dataset[["CHROM", "POS", "SNP_ID"]], on=["CHROM", "POS"], how="left")

    # Save Annotated nSL Results files
    output_file = f"{pp}_nSL_scores.xlsx"
    annotated_nsl_df.to_excel(output_file, index=False, engine="openpyxl")

    print(f"nSL results files are annorated with rsIDs)
