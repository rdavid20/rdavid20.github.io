import csv
import json
import os

# CONFIG
folder = 'book_lists'
input_file = os.path.join(folder, 'books.csv')
output_files = {
    'currently-reading': os.path.join(folder, 'currently_reading.json'),
    'read': os.path.join(folder, 'read.json'),
    'to-read': os.path.join(folder, 'to_read.json')
}

# Columns to include
keep_columns = [
    'Title', 'Author', 'ISBN', 'ISBN13', 'My Rating',
    'Average Rating', 'Exclusive Shelf', 'Date Read', 'Date Added'
]

def clean_isbn(raw_value):
    """Fix Excel-formatted ISBNs like =\"1234567890\"."""
    if raw_value.startswith('="') and raw_value.endswith('"'):
        return raw_value[2:-1]
    return raw_value.strip()

def clean_row(row):
    cleaned = {}
    for key in keep_columns:
        value = row.get(key, '').strip()
        if key in ['ISBN', 'ISBN13']:
            cleaned[key] = clean_isbn(value)
        else:
            cleaned[key] = value
    return cleaned

def convert_csv_to_multiple_json(csv_path):
    shelves = {
        'currently-reading': [],
        'read': [],
        'to-read': []
    }

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            shelf = row['Exclusive Shelf'].strip()
            if shelf in shelves:
                shelves[shelf].append(clean_row(row))

    for shelf, books in shelves.items():
        output_path = output_files[shelf]
        with open(output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(books, jsonfile, indent=2, ensure_ascii=False)
        print(f"✅ Wrote {len(books)} books to {output_path}")

# Run the script
if __name__ == '__main__':
    os.makedirs(folder, exist_ok=True)
    convert_csv_to_multiple_json(input_file)
