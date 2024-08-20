import streamlit as st
from openai import OpenAI
from pymongo import MongoClient
from datetime import datetime
import pytz
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize MongoDB client
mongo_client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))
db = mongo_client.virtual_rooms  # Access the virtual_rooms database

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Unknown Agents", "Users"])

if page == "Home":
    st.title("Find Suitable Professional")

    # Custom CSS for the text area
    st.markdown("""
        <style>
        .input_area {
            width: auto;
            height: 150px;
            padding: 16px;
            border-radius: 9px;
            outline: none;
            background-color: #F2F2F2;
            border: 1px solid #e5e5e500;
            transition: all 0.3s cubic-bezier(0.15, 0.83, 0.66, 1);
        }

        .input_area:focus {
            border: 1px solid transparent;
            box-shadow: 0px 0px 0px 2px #242424;
            background-color: transparent;
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to get the most suitable profession
    def get_suitable_profession(query):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that recommends the most suitable profession or expert to answer a query. Respond with only the profession or expert type."},
                {"role": "user", "content": f"Who is best suited to answer this question or request: {query}"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()

    # Function to find the correct collection name (case-insensitive)
    def find_collection(profession):
        collections = db.list_collection_names()
        for collection in collections:
            if collection.lower() == profession.lower():
                return collection
        return None

    # Function to store the question in the appropriate collection
    def store_question_in_collection(profession, question):
        collection = db[profession]  # Access the appropriate collection based on the profession

        # Get the current date and time
        tz = pytz.timezone('Asia/Kolkata')  # Replace with your timezone
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        # First, update documents where 'questions' is not an array or doesn't exist
        collection.update_many(
            {'$or': [
                {'questions': {'$exists': False}},
                {'questions': {'$not': {'$type': 'array'}}}
            ]},
            {'$set': {'questions': []}}
        )

        # Now, push the new question to the 'questions' array
        result = collection.update_many(
            {},  # Updates all documents in the collection
            {'$push': {'questions': {current_time: question}}},
            upsert=True  # Create the document if it does not exist
        )
        
        if result.modified_count > 0:
            st.write(f"Question successfully stored in the {profession} collection for all users.")
        else:
            st.write(f"No existing users found in the {profession} collection. A new document was created with the question.")

    # Function to store question in unknown_agents collection
    def store_in_unknown_agents(profession, question):
        unknown_agents = db.unknown_agents
        tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        
        unknown_agents.insert_one({
            'timestamp': current_time,
            'question': question,
            'suggested_agent': profession
        })
        
        st.write(f"The suggested agent '{profession}' was not found in the database. The question has been stored in the unknown_agents collection.")

    # Text area for user input
    user_input = st.text_area("", key="text_input", placeholder="Enter your question here", help="Input your question here")

    # Button to submit the text area input
    if st.button("Find Suitable Professional"):
        if user_input.strip():
            # Get the suitable profession
            suggested_profession = get_suitable_profession(user_input)
            
            # Find the correct collection name (case-insensitive)
            correct_profession = find_collection(suggested_profession)
            
            if correct_profession:
                # Store the question in the appropriate collection
                store_question_in_collection(correct_profession, user_input)
            else:
                # Store in unknown_agents collection
                store_in_unknown_agents(suggested_profession, user_input)
        else:
            st.write("Please enter a question before submitting.")

elif page == "Unknown Agents":
    st.title("Unknown Agents")

    # Fetch data from unknown_agents collection
    unknown_agents = db.unknown_agents
    data = list(unknown_agents.find({}, {'_id': 0}))  # Exclude the MongoDB _id field

    if data:
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Display as table
        st.table(df)
    else:
        st.write("No data found in the unknown_agents collection.")

elif page == "Users":
    st.title("User Profiles")

    # Fetch all collection names (professions)
    collections = db.list_collection_names()
    
    # Remove 'unknown_agents' from the list if it exists
    if 'unknown_agents' in collections:
        collections.remove('unknown_agents')

    # Create a dropdown to select profession
    selected_profession = st.selectbox("Select a profession", collections)

    if selected_profession:
        # Fetch data for the selected profession
        collection = db[selected_profession]
        users_data = list(collection.find({}, {'_id': 0}))  # Exclude MongoDB _id field

        if users_data:
            # Convert to DataFrame
            df = pd.DataFrame(users_data)
            
            # Display as table
            st.table(df)
        else:
            st.write(f"No users found for {selected_profession}.")
