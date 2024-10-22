import requests
from supabase import create_client, Client
import os


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

# Add book data to Supabase
def add_books_to_supabase(books):
    for book in books:
        volume_info = book.get('volumeInfo', {})
        title = volume_info.get('title', 'Unknown Title')
        authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
        published_date = volume_info.get('publishedDate', 'Unknown')
        categories = ', '.join(volume_info.get('categories', []))
        description = volume_info.get('description', 'No description available.')
        page_count = volume_info.get('pageCount', 0)

        # Prepare data to insert into Supabase
        book_data = {
            "title": title,
            "authors": authors,
            "published_date": published_date,
            "categories": categories,
            "description": description,
            "page_count": page_count
        }

        # Insert into Supabase
        response = supabase.table('books').insert(book_data).execute()
        if response.data:
            print(f"Successfully added book: {title}")
        else:
            print(f"Error adding book: {title}, Status Code: {response.status_code}")

# Main function to fetch and store books for different genres
def main():
    genres = ["Fiction", "Mystery", "Science Fiction", "Biography", "Fantasy", "History", "Romance"]
    for genre in genres:
        print(f"Fetching books for genre: {genre}")
        maxBooks = 300
        startIndex = 0
        maxResults = 40
        while startIndex <= maxBooks:
            books = get_books_by_genre(genre, startIndex, min(maxResults, maxBooks - startIndex))
            if books:
                add_books_to_supabase(books)
                startIndex += 40
            else:
                break

if __name__ == "__main__":
    main()