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

# Convert chromosome to string to avoid errors 
snps_dataset["CHROM"] = snps_dataset["CHROM"].astype(str)

# Define list of Populations name
populations = ["PJL", "BEB", "ITU", "GIH"]  

# Process Each Population one at a time
for pop in populations:
    fst_file = f"Fst_results_{pop}_CEU.xlsx"  # this brings Fst results file for all populations
    
    # Load Fst results
    fst_df = pd.read_excel(fst_file, engine="openpyxl")
    
    # Convert chromosome to string to avoid errors 
    fst_df["CHROM"] = fst_df["CHROM"].astype(str)

    # Merge Fst results with rsIDs
    annotated_fst_df = fst_df.merge(snps_dataset[["CHROM", "POS", "SNP_ID"]], on=["CHROM", "POS"], how="left")

    # Save annotated Fst Results files
    output_file = f"Fst_results_{pop}_CEU_annotated.xlsx"
    annotated_fst_df.to_excel(output_file, index=False, engine="openpyxl")

    print("Fst results files are annorated with rsIDs)
