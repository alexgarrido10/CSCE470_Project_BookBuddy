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
authorsWeight = 0.1
descriptionWeight = 0.3
genreWeight = 0.15
titleB = 0.75
genreB = 0.75
authorsB = 0.75
descriptionB = 0.75

# BM-25 hyperparameter K1
k1 = 1.4

# Implementation of the BM-25 ranking algorithm
def weighted_bm25(query, bookData, avLens):
    scores = []
    numDocs = len(bookData)

    termDfs = {term: sum(1 for book in bookData if term in book['norm_title'] 
                     or book['norm_categories'] 
                     or book['norm_authors']
                     or book['description'])

                     for term in query}

    for book in bookData:
        bookScore = 0
        for term in query:
            # Get term frequencies for each field
            titleTf = book['norm_title'].count(term)
            authorsTf = book['norm_authors'].count(term)
            genreTf = book['norm_categories'].count(term)
            descriptionTf = book['description'].count(term)

            # Get field lengths for document
            titleLen = len(book['norm_title'].split())
            authorsLen = len(book['norm_authors'].split())
            genreLen = len(book['norm_categories'].split())
            descriptionLen = len(book['description'].split())

            # Calculate normalized term frequencies for each field
            titleNormTf = titleTf / ((1 - titleB) + titleB * (titleLen / avLens['title']))
            authorsNormTf = authorsTf / ((1 - authorsB) + authorsB * (authorsLen / avLens['authors']))
            genreNormTf = genreTf / ((1 - genreB) + genreB * (genreLen / avLens['genre']))
            descriptionNormTf = descriptionTf / ((1 - descriptionB) + descriptionB * (descriptionLen / avLens['description']))

            # Weight individual norm tfs and sum to get total 'weight' of term accross all fields
            termWeight = (titleNormTf * titleWeight) + (authorsNormTf * authorsWeight) + \
                (genreNormTf * genreWeight) + (descriptionNormTf * descriptionWeight)
            
            # Calculate df and then idf for the term
            idf = math.log((numDocs - termDfs[term] + 0.5) / (termDfs[term] + 0.5)) 

            # Include K1 and multiply by idf of the term
            termFinal = (termWeight / (k1 + termWeight)) * idf
            
            # Add term's final contribution to the current doc's score
            bookScore += termFinal
            # print(termFinal)
        
        # Add the total doc score to scores
        scores.append((book['id'], book['norm_title'], bookScore))

    return sorted(scores, key= lambda x: x[2])[:20]

def main():

    parser = argparse.ArgumentParser(
        prog = "bm25",
        description = "Retrieve the top 20 most relevant documents to a given query based on "
        "a text collection pulled from Google Books"
    )
    parser.add_argument("query", help="Your search query on the collection")
    args = parser.parse_args()

    # Pull the collection from Supabase
    bookResponse = supabase.table('books').select('id, norm_title, norm_authors, norm_categories, description', count='exact').execute()
    if bookResponse.data:
        print(f"Good pull: {bookResponse.count} rows returned")
    bookData = bookResponse.data

    # Get the average lengths for each field / zone
    averageLengths = {
        'title': sum(len(book['norm_title'].split()) for book in bookData) / len(bookData),
        'authors': sum(len(book['norm_authors'].split()) for book in bookData) / len(bookData),
        'genre': sum(len(book['norm_categories'].split()) for book in bookData) / len(bookData),
        'description': sum(len(book['description'].split()) for book in bookData) / len(bookData)
    }

    # Turn user query into list of terms
    queryTerms = args.query.split()

    # Get the top 20 most relevant results based on BM25
    # for book in bookData[:25]:
    #     print(book['norm_title'])

    top20 = weighted_bm25(queryTerms, bookData, averageLengths)

    
    for ind, result in enumerate(top20,1): # Print out the top 20 ranked results
        print(f"{ind}. {result[1]} - Score:{result[2]:.9f}")

if __name__ == "__main__":
    main()