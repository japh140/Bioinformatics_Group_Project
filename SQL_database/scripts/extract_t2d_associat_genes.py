import pandas 

dataset= pandas.read_csv("t2d.hugeamp_dataset/South Asian/DIAMANTE 2022 T2D GWAS_associations.csv")

#print(dataset.columns)


#extract the genes name from the datasets in a dataframe
#if 'nearest' in dataset.columns:
    #genes_list = dataset["nearest"].unique().tolist()
     
    #print (genes_list)
#else:
   # print("Error: 'nearest' column not found in the dataset.")
genes_list = pandas.DataFrame(dataset["nearest"].unique(), columns=["genes"])

#save it in csv file 

genes_list.to_csv("t2d.hugeamp_dataset/t2d_associated_genes_list.csv", index=False)



