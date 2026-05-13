import chromadb
import csv

# 1. Connect to your ChromaDB
client = chromadb.PersistentClient(path="./chroma_memory")
collection = client.get_collection(name="market_research")

# 2. Get all data (including embeddings)
data = collection.get(include=['embeddings', 'documents'])

if not data['embeddings']:
    print("No data found to export!")
    exit()

# 3. Save Vectors File (vectors.tsv)
with open('vectors.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for vector in data['embeddings']:
        writer.writerow(vector)

# 4. Save Metadata File (metadata.tsv)
with open('metadata.tsv', 'w', newline='') as f:
    # We add a header so the projector knows what the column is
    f.write("Fact\n")
    for doc in data['documents']:
        # Clean up newlines to prevent TSV breaking
        clean_doc = doc.replace('\n', ' ')
        f.write(f"{clean_doc}\n")

print("✅ Export complete! Created 'vectors.tsv' and 'metadata.tsv'.")