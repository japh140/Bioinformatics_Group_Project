
import pandas as pd

# Load 1000genome population metadata
pop_dataset = pd.read_csv("population_metadata_from_1000Genome.csv", sep="\t")



# Subpopulations in the datasets
sub_south_asian = ["Bengali", "Punjabi", "Gujarati", "Telugu", "CEPH"]



# loop through each sub populations and save sample ID listsin sepearte txt file
for sp in sub_south_asian:
    SA_population = pop_dataset[pop_dataset["Population name"].str.contains(sp, case=False, na=False)]
    sample_ids = SA_population["Sample name"]

    # Save in a text file
    txtfile = f"{sp}_sampleID.txt"
    with open(txtfile, "w") as txt:
        for ID in sample_ids:
            txt.write(ID + "\n")



print("Sample ID lists are extracted and saved")
