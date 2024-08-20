from pymongo import MongoClient

# Connect to MongoDB server
client = MongoClient('mongodb+srv://sachinparmar0246:2nGATJVDEwDZzaA8@cluster0.c25rmsz.mongodb.net')  # Update with your MongoDB connection string if needed

# Create database
db = client.virtual_rooms

# List of collection names
collections = [
    "Doctor",
    "3D Printing Technician",
    "App Developer",
    "Archivist",
    "Business Analyst",
    "Computer Games Developer",
    "Computer Games Tester",
    "Cyber Intelligence Officer",
    "Data Entry Clerk",
    "Data Scientist",
    "Database Administrator",
    "Digital Delivery Manager",
    "Digital Product Owner",
    "E-learning Developer",
    "Forensic Computer Analyst",
    "IT Project Manager",
    "IT Security Coordinator",
    "IT Support Technician",
    "IT Trainer",
    "Information Scientist",
    "Network Engineer",
    "Network Manager",
    "Operational Researcher",
    "Pre-press Operator",
    "Robotics Engineer",
    "Social Media Manager",
    "Software Developer",
    "Solutions Architect",
    "Systems Analyst",
    "Technical Architect",
    "Technical Author",
    "Telephonist",
    "Test Lead",
    "UI/UX Designer",
    "User Researcher",
    "Web Content Editor",
    "Web Content Manager",
    "Web Designer",
    "Web Developer"
]

# Sample user data for each profession
sample_users = [
    {"name": "John Doe", "gender": "Male", "status": "Active"},
    {"name": "Jane Smith", "gender": "Female", "status": "Inactive"},
    {"name": "Alice Johnson", "gender": "Female", "status": "Active"},
    {"name": "Bob Brown", "gender": "Male", "status": "Active"},
    {"name": "Carol White", "gender": "Female", "status": "Inactive"}
]

# Insert sample user data into each collection
for collection_name in collections:
    collection = db[collection_name]
    for user in sample_users:
        user["profession"] = collection_name  # Set profession to match collection name
        collection.insert_one(user)

print("Sample user data inserted into each collection.")
