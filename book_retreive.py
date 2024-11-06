import requests
from supabase import create_client, Client
import os
import re
import spacy


# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Google Books API setup
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

# Query and add books by genre
def get_books_by_genre(genre, start_index=0, max_results=40):
    params = {
        'q': f'subject:{genre}',
        'key': API_KEY,
        'maxResults': max_results,
        'startIndex': start_index
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error fetching books for genre {genre}: {response.status_code}")
        return []

# Add book data to Supabase database
def add_books_to_supabase(books, genre):
    # Loading natural language processing kit (spaCy) for more complex processing
    nlp = spacy.load("en_core_web_sm")
    for book in books:
        # Initialize variables to hold json info
        volume_info = book.get('volumeInfo', {})
        title = volume_info.get('title', 'Unknown Title')
        authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
        published_date = volume_info.get('publishedDate', 'Unknown')
        categories = ', '.join(volume_info.get('categories', [genre]))
        description = volume_info.get('description', 'No description available.')
        page_count = volume_info.get('pageCount', 0)

        # Pre-processing the description
        description = description.lower() # Make all words lower case
        description = re.sub(r'\d+','',description) # Remove all digits 
        description = re.sub(r'[^\w\s]','',description) # Remove punctuation
        description = description.strip() # Remove all whitespace
        descriptionDoc = nlp(description) # Turn description into spaCy doc object
        # Remove all stop words from description and concatenate back into a string with spaces between tokens
        description = " ".join([token.text for token in descriptionDoc if not token.is_stop])
        # Description done

        # Pre-process the genres
        categories_normal = categories.lower()
        categories_normal = re.sub(r'\d+', '', categories_normal)
        categories_normal = re.sub(r'[^\w\s]', '', categories_normal)
        categories_normal = categories_normal.strip()

        # Pre-process the authors
        authors_normal = authors.lower()
        authors_normal = re.sub(r'\d+', '', authors_normal)
        authors_normal = re.sub(r'[^\w\s]', '', authors_normal)
        authors_normal = authors_normal.strip()

        # Pre-process the title
        title_normal = title.lower() 
        title_normal = re.sub(r'\d+', '', title_normal)
        title_normal = re.sub(r'[^\w\s]', '', title_normal)
        title_normal = title_normal.strip()

        # Prepare data to insert into Supabase database
        book_data = {
            "title": title,
            "norm_title": title_normal,
            "authors": authors,
            "norm_authors": authors_normal,
            "published_date": published_date,
            "categories": categories,
            "norm_categories": categories_normal,
            "description": description,
            "page_count": page_count
        }

        # Insert into Supabase
        response = supabase.table('books').insert(book_data).execute()
        if response.data:
            print(f"Successfully added book: {title}")
        else:
            print(f"Error adding book: {title}, Status Code: {response.status_code}")

# Removes duplicate entries from Supabase database
def remove_supabase_duplicates():
    res = supabase.rpc('remove_duplicate_rows').execute()

    if res.data:
        print(f"Removed {res.data} duplicates")
    else:
        print(f"Error: {res.status}: {res.error}")

# Main function to fetch and store books for different genres
def main():
    genres = ["Fiction", "Mystery", "Science Fiction", "Biography", "Fantasy", "History", "Romance", "Philosophy", "Self Help"]
    for genre in genres:
        print(f"Fetching books for genre: {genre}")
        maxBooks = 500
        startIndex = 0
        maxResults = 40
        while startIndex <= maxBooks:
            books = get_books_by_genre(genre, startIndex, min(maxResults, maxBooks - startIndex))
            if books:
                add_books_to_supabase(books, genre)
                startIndex += 40
            else:
                break

    # Now delete all duplicate data in the database by calling custom function
    remove_supabase_duplicates()

if __name__ == "__main__":
    main()