**Description:**  
This file contains statistical analyses and data processing steps related to population genetics. It includes statistical tests such as **nSL (number of Segregating sites by Length) and FST (Fixation Index)** to detect selection signals. Additionally, it covers **data filtering, normalisation, and permutations tests **, ensuring high-quality genomic analysis.

# Statistical Analysis for T2D Susceptibility Project

## Overview
This project focuses on identifying genetic variants associated with Type 2 Diabetes (T2D) and analysing positive selection signals in South Asian populations. The statistical components involve various filtering, validation, and statistical tests applied to genomic data.

## Statistical Components

### 1. **Permutation Test for Positive Selection Signals**
   - **Purpose**: Generates a null distribution by randomly shuffling nSL scores to assess statistical significance.
   - **Script**: `permutation test code.txt`
   - **Method**:
     - Performs **1000 permutations** of nSL scores.
     - Computes a test statistic (e.g., mean or max) for each permutation.
     - Used to evaluate whether observed selection signals are significant.
   - **Dependencies**: `numpy`

### 2. **Population-Based VCF Filtering**
   - **Purpose**: Extracts population-specific VCFs to analyze T2D genetic variants.
   - **Script**: `Population filter.txt`
   - **Method**:
     - Filters variants for **BEB, GIH, ITU, STU** populations.
     - Uses `bcftools` and `htslib` to subset samples and compress/index VCFs.
     - Parallelized across **chromosomes 1-22**.

### 3. **Integrity Checks for VCF Data**
   - **Purpose**: Ensures data quality by validating and cleaning VCF files.
   - **Script**: `Integrity VCF checks.txt`
   - **Method**:
     - **Biallelic Check**: Filters out non-biallelic SNPs.
     - **Duplicate Removal**: Ensures unique SNPs using `bcftools norm`.
     - **VCF Compliance Validation**: Detects format inconsistencies.
     - **Sorting Check**: Ensures SNPs are correctly ordered.
     - **X Chromosome Removal**: Restricts analysis to **autosomal** SNPs.

### 4. **Filtering SNPs by Genomic Positions**
   - **Purpose**: Selects SNPs located in predefined T2D-associated genomic regions.
   - **Script**: `Filter by SNP positions.txt`
   - **Method**:
     - Uses a **BED file** to extract SNPs in specific genomic regions.
     - Processes **seven populations** in parallel.
     - Utilises `bcftools view -R` for targeted filtering.
     - Ensures efficient indexing of output files.

## Requirements
- `bcftools`
- `htslib`
- `numpy`
- Unix environment with **SGE job scheduling** (for batch processing).

## Execution Instructions
Run each script in a Unix terminal or HPC environment following the provided comments within the scripts.
