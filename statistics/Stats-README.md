Statistical Analysis for T2D Susceptibility Project

Description
This file contains statistical analyses and data processing steps related to population genetics. It includes statistical tests such as nSL (number of Segregating sites by Length) and FST (Fixation Index) to detect selection signals. Additionally, it covers data filtering, permutation tests, and normalisation, ensuring high-quality genomic analysis.

Overview
This project focuses on identifying genetic variants associated with Type 2 Diabetes (T2D) and analysing positive selection signals in South Asian populations. The statistical components involve various filtering, validation, and statistical tests applied to genomic data.

Statistical Components
1. Population-Based VCF Filtering
Purpose: Extracts population-specific VCFs to analyze T2D genetic variants.
Script: Population filter.txt
Method:
Filters variants for BEB, GIH, ITU, STU populations.
Uses bcftools and htslib to subset samples and compress/index VCFs.
Parallelised across chromosomes 1-22.
2. Integrity Checks for VCF Data
Purpose: Ensures data quality by validating and cleaning VCF files.
Script: Integrity VCF checks.txt
Method:
Biallelic Check: Filters out non-biallelic SNPs.
Duplicate Removal: Ensures unique SNPs using bcftools norm.
VCF Compliance Validation: Detects format inconsistencies.
Sorting Check: Ensures SNPs are correctly ordered.
X Chromosome Removal: Restricts analysis to autosomal SNPs.
3. Filtering SNPs by Genomic Positions
Purpose: Selects SNPs located in predefined T2D-associated genomic regions.
Script: Filter by SNP positions.txt ( Liftover was utilised to make sure postions from another reference genome mathched our
GrCh37 genome
Method:
###BURHAN ADD HERE
.
5. Permutation Test for Positive Selection Signals
Purpose: Generates a null distribution by randomly shuffling nSL scores to assess statistical significance.
Script: permutation test code.txt
Method:
Performs 1000 permutations of nSL scores.
Computes a test statistic (e.g., mean or max) for each permutation.
Used to evaluate whether observed selection signals are significant.
Dependencies: numpy
6. Normalisation of Selection Signals
Purpose: Standardises selection statistics to improve the visibility of selection signals.
Method:
Applies Z-score transformation to nSL.
Ensures comparability across different populations.
Enhances visualisation of selection signals.
Requirements
bcftools
htslib
numpy
