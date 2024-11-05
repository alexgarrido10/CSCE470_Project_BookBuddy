import math
from supabase import create_client, Client
import os
import sys
import argparse

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Weights and parameters assigned to books' fields
titleWeight = 0.45
authorWeight = 0.1
descriptionWeight = 0.3
genreWeight = 0.15
titleB = 0.75
genreB = 1 # Completely normalize zone length
authorB = 1
descriptionB = 1

# BM-25 hyperparameter K1
k = 1.4

# Implementation of the BM-25 ranking algorithm
def wieghted_bm25(query, bookData, avLens):
    scores = []
    numDocs = len()

    for book in bookData:
        for term in query:
            # Get term frequencies for each field
            titleTf = book['title']

    return 0

def main():

    parser = argparse.ArgumentParser(
        prog = "bm25",
        description = "Retrieve the top 20 most relevant documents to a given query based on "
        "a text collection pulled from Google Books"
    )
    parser.add_argument("query", help="Your serach query on the collection")
    args = parser.parse_args()

    # Pull the collection from Supabase
    bookResponse = supabase.table('books').select('id, norm_title, norm_authors, norm_categories, description').execute()
    if bookResponse.error:
        print(f"Error {bookResponse.status_code} fetching collection: {bookResponse.error}")
        sys.exit(1)
    bookData = bookResponse.data

    queryTerms = args.query.split()

    print(f"")

    # print("Not yet implemented")

if __name__ == "__main__":
    main()