import json
import pandas as pd
import random

# Read menu items from Excel or CSV
menu_items_df = pd.read_csv('final_data.csv')

# Read questions from JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Convert DataFrame to list of dictionaries
menu_items = menu_items_df.to_dict(orient='records')

# Function to create a single entry
def create_entry(menu_item):
    documents = []
    for q in questions:
        field_value = menu_item[q['field']]
        if isinstance(field_value, str) and q['field'] == 'ingredients':
            field_value = field_value.split(', ')
        documents.append({
             "question": q["question"],
             "section": q["section"],
            "text": f"The {menu_item['name']} contains {', '.join(field_value) if isinstance(field_value, list) else field_value}"
        })
    return {
        "course": "menu-items",
        "documents": documents
    }

# Generate the dataset
data = []
for _ in range(1000):
    item = random.choice(menu_items)
    data.append(create_entry(item))

# Write to JSON file
with open('jacks_restaurant_data2.json', 'w') as f:
    json.dump(data, f, indent=2)
