import chromadb

# 1. Connect to the folder
client = chromadb.PersistentClient(path="./chroma_memory")

# 2. Use 'get_or_create' so it doesn't crash if empty
collection = client.get_or_create_collection(name="market_research")

# 3. Fetch data
all_data = collection.get()

# 4. Check if we actually have data
if not all_data['ids']:
    print("📭 The database is currently empty.")
    print("Try running 'fact_checker.py' and successfully completing a research task first!")
else:
    print(f"📊 Total memories stored: {len(all_data['ids'])}\n")
    for i in range(len(all_data['ids'])):
        print(f"ID:   {all_data['ids'][i]}")
        print(f"Fact: {all_data['documents'][i]}")
        print("-" * 50)