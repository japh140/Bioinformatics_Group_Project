GWAS Catalog
File:		gwas_catalog_v1.0-associations_e113_r2025-01-08.tsv
Site:		https://www.ebi.ac.uk/gwas/
Download From:	https://www.ebi.ac.uk/gwas/docs/file-downloads  (All associations v1.0)

CREATE TABLE "SNP_Associations" (
	"snp_id"	TEXT,
	"chromosome"	TEXT,
	"position"	INTEGER,
	"p_value"	REAL,
	"mapped_gene"	TEXT,
	"phenotype"	TEXT,
	"population"	TEXT,
);


Project Field	GWAS Field		DIAMANTE_SAS Field
snp_id		SNPs			rsID
chromosome	CHR_ID			chromosome_b37
position	CHR_POS			position_b37
p_value		P_VALUE			Fixedeffectspvalue
mapped_gene	MAPPED_GENE		missimg
phenotype	DISEASE_TRAIT(*)	"Type 2 Diabetes"
population	INITIAL_SAMPLE_SIZE	

(*) Searches on DISEASE_TRAIT Like '%Type 2 Diabetes%'


SELECT SNPs,CHR_ID,CHR_POS,P_VALUE,MAPPED_GENE,DISEASE_TRAIT,INITIAL_SAMPLE_SIZE FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%Pakistani%'
142 Rows

INSERT INTO SNP_Associations 
SELECT SNPS, CHR_ID, CHR_POS, P_VALUE, MAPPED_GENE, DISEASE_TRAIT, 'Pakistani' FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%Pakistani%'
142 Rows

SELECT SNPs,CHR_ID,CHR_POS,P_VALUE,MAPPED_GENE,DISEASE_TRAIT,INITIAL_SAMPLE_SIZE FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%Bangladesh%'
3 Rows

INSERT INTO SNP_Associations 
SELECT SNPs,CHR_ID,CHR_POS,P_VALUE,MAPPED_GENE,DISEASE_TRAIT,'Bangladesh' FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%Bangladesh%'
3 Rows

SELECT SNPs,CHR_ID,CHR_POS,P_VALUE,MAPPED_GENE,DISEASE_TRAIT,INITIAL_SAMPLE_SIZE FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%South Asian%'
1052 Rows

INSERT INTO SNP_Associations 
SELECT SNPs,CHR_ID,CHR_POS,P_VALUE,MAPPED_GENE,DISEASE_TRAIT,'South Asian' FROM GWAS WHERE DISEASE_TRAIT LIKE '%Type 2 Diabetes%' AND INITIAL_SAMPLE_SIZE Like '%South Asian%'
1052 Rows
