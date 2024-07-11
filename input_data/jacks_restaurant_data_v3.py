import json
import pandas as pd

# Read menu items from CSV
menu_items_df = pd.read_csv('dish_data.csv')

# Read questions from JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Convert DataFrame to list of dictionaries (each representing a menu item)
menu_items = menu_items_df.to_dict(orient='records')

# Function to create a single entry based on a menu item
def create_entry(menu_item):
    documents = []
    for q in questions:
        field_value = menu_item.get(q['field'], "N/A")  # Use .get() with default "N/A"
        if isinstance(field_value, str) and q['field'] == 'ingredients':
            field_value = field_value.split(', ')
            text = f"The {menu_item['name']} contains {', '.join(field_value)}"
        else:
            text = f"The {menu_item['name']} contains {field_value}"
        
        documents.append({
            "question": q["question"],
            "section": q["section"],
            "text": text
        })
    return {
        "dish name": menu_item['name'],
        "documents": documents
    }

# Generate the dataset for all menu items
data = []
for item in menu_items:
    data.append(create_entry(item))

# Write to JSON file
with open('jacks_restaurant_data.json', 'w') as f:  # Adjust filename as needed
    json.dump(data, f, indent=2)
