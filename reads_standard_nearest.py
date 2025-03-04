import pymongo
import random
import time
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection URI
username = os.getenv("username")
password = os.getenv("password")
uri = f"mongodb+srv://{username}:{password}@cluster0.j5mfx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Sample restaurant data
sample_data = [
    {"name": f"Restaurant {i}", "cuisine": "Cuisine Type", "rating": random.randint(1, 5)}
    for i in range(100)
]

# Function to measure average read latency
def measure_read_latency(collection, attempts=10):
    latencies = []
    for _ in range(attempts):
        start_time = time.time()
        collection.find_one({"name": f"Restaurant {random.randint(0, 99)}"})
        end_time = time.time()
        latencies.append((end_time - start_time) * 1000)  # Convert to milliseconds
    return sum(latencies) / len(latencies)

# Connect to MongoDB and insert sample data
client = pymongo.MongoClient(uri)
db = client.get_database("restaurant_db")
collection = db.get_collection("recommendations")

nearest_client = pymongo.MongoClient(uri, read_preference=pymongo.ReadPreference.NEAREST)
nearest_db = nearest_client.get_database("restaurant_db")
nearest_collection = nearest_db.get_collection("recommendations")

# Insert sample documents
collection.insert_many(sample_data)

while True:
    sleep(5)
    # Measure average read latency with default connection
    default_latency = measure_read_latency(collection)
    print(f"Average read latency with default connection: {default_latency:.6f} ms")

    # Measure average read latency with "nearest" connection
    nearest_latency = measure_read_latency(nearest_collection)
    print(f"Average read latency with 'nearest' connection: {nearest_latency:.6f} ms")