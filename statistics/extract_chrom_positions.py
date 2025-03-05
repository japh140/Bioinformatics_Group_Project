import pandas as pd

# List of CSV files
snp_csv_files = [
    "DIAMANTE2022T2DGWASassociations.csv",
    "Genes&HealthT2D2022GWASassociations.csv",
    "T2DGGI2024T2DGWASassociations.csv",
    "Type2diabetes2022GWASassociations.csv",
    "EU_T2DGGI2024T2DGWASassociations.csv"
]


# Merge all CSV files
dataset = pd.concat([pd.read_csv(f) for f in snp_csv_files], ignore_index=True)

# Extract chromosome and position
chrom_pos = dataset[['chromosome', 'position']].dropna().drop_duplicates()



# Save to a text file
chrom_pos.to_csv('t2d_chrom_position.txt', sep='\t', index=False, header=False)

print("Chromosome positions extracted and saved")
