import sqlite3
import random

# Connect to SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('snp_associations.db')
cursor = conn.cursor()

# Create the SNP_Associations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SNP_Associations (
        snp_id TEXT,
        chromosome TEXT,
        position INTEGER,
        p_value REAL,
        mapped_gene TEXT,
        phenotype TEXT,
        population TEXT
    )
''')

# Function to generate mock data
def generate_mock_data():
    snp_ids = ['rs12345', 'rs23456', 'rs34567', 'rs45678', 'rs56789']
    chromosomes = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5']
    mapped_genes = ['TCF7L2', 'FTO', 'GCK', 'INS', 'PPARG']
    phenotypes = ['Type 2 Diabetes']
    populations = ['Pakistani', 'Bangladesh', 'South Asian']

    # Generate random records
    for _ in range(10):  # Generate 10 mock records
        snp_id = random.choice(snp_ids)
        chromosome = random.choice(chromosomes)
        position = random.randint(1000, 1000000)
        p_value = round(random.uniform(0.00001, 0.05), 5)
        mapped_gene = random.choice(mapped_genes)
        phenotype = random.choice(phenotypes)
        population = random.choice(populations)

        # Insert data into SNP_Associations table
        cursor.execute('''
            INSERT INTO SNP_Associations (snp_id, chromosome, position, p_value, mapped_gene, phenotype, population)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (snp_id, chromosome, position, p_value, mapped_gene, phenotype, population))

    # Commit changes to the database
    conn.commit()

# Generate and insert mock data
generate_mock_data()

# Verify by fetching some records
cursor.execute('SELECT * FROM SNP_Associations LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()