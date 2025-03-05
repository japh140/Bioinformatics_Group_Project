import pandas as pd

# lists of all T2D SNP dataset csv files
snp_csv_files = [
    "DIAMANTE2022T2DGWASassociations.csv",
    "Genes&HealthT2D2022GWASassociations.csv",
    "EU_T2DGGI2024T2DGWASassociations.csv",
    "Type2diabetes2022GWASassociations.csv",
    "T2DGGI2024T2DGWASassociations.csv"
]

# Load all SNP dataset csv files and create a dictionary for chromosome position: snps id
snps_dataset = pd.concat([pd.read_csv(f) for f in snp_csv_files], ignore_index=True)
print (snps_dataset.columns)

dictionary = {(str(row['chromosome']), int(row['position'])): row['dbSNP'] for index, row in snps_dataset.iterrows()}


# Path to input and oputput files
input_file = "all_chromosomes.vcf"
output_file = "snps_anotated_all_chromosomes.vcf"



# Read and update the VCF file

with open(input_file, 'r') as inp_file, open(output_file, 'w') as out_file:
    for line in inp_file:
        if line.startswith("#"):  
            out_file.write(line)
        else:
            colmn = line.strip().split("\t")
            chromosome, position = str(colmn[0]), int(colmn[1])
            
            # Replace ID with the snp rsid 
            snp_id = dictionary.get((chromosome, position), colmn[2])
            colmn[2] = str(snp_id)
            
            out_file.write("\t".join(colmn) + "\n")



print( "VCF file annotated with snps ids")
