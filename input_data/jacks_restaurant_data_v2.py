import json
import pandas as pd

# Read menu items from CSV
menu_items_df = pd.read_csv('final_data.csv')

# Read questions from JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Convert DataFrame to list of dictionaries (each representing a menu item)
menu_items = menu_items_df.to_dict(orient='records')

# Function to create a single entry based on a menu item
def create_entry(menu_item):
    documents = []
    for q in questions:
        field_value = menu_item.get(q['field'], None)  # Use .get() to handle missing fields
        if isinstance(field_value, str) and q['field'] == 'ingredients':
            field_value = field_value.split(', ')
        documents.append({
            "question": q["question"],
            "section": q["section"],
            "text": field_value if field_value is not None else "N/A"  # Provide default if field is missing
        })
    return {
        "course": "menu-items",
        "documents": documents
    }

# Generate the dataset for all menu items
data = []
for item in menu_items:
    data.append(create_entry(item))

# Write to JSON file
with open('jacks_restaurant_data.json', 'w') as f:  # Adjust filename as needed
    json.dump(data, f, indent=2)
