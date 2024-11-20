import math
from supabase import create_client, Client
import os
import sys
import argparse
import re

from dotenv import load_dotenv

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Weights and parameters assigned to books' fields
# Our product is meant to be more exploratory, i.e. users will be searching for genre and integrating mood
titleWeight = 0.4
authorsWeight = 0.5
descriptionWeight = 0.2
genreWeight = 0.7

titleB = 0.75
genreB = 0.75
authorsB = 0.75
descriptionB = 0.5

# Non-textual sentiment feature weight; works more as a percentage of text vs non-text feature importance
sentimentWeight = 0.5

# BM-25 hyperparameter K1
k1 = 1.4

# List of generic terms to penalize generic titles
# GENERIC_TERMS= {'fiction', 'fantasy', ''}

# def set_weights(slection):
    

# Get all of the current entries in our database by pagination (too many entries for simple select query)
def pull_books():
    # Get total rows
    response = supabase.table('books').select('id', count='exact').execute()
    totalRows = response.count

    bookData = []
    pageSize = 500
    begin = 0

    while begin < totalRows:
        response = supabase.table('books').select('id, norm_title, norm_authors, norm_categories, description, '
                    'sentiment_score, title, authors', 
                    count='exact').range(begin, min(totalRows - 1, begin + pageSize -1)).execute()

        if not response.data:
            break

        bookData.extend(response.data)
        begin += pageSize

    return bookData


# Implementation of the BM-25 ranking algorithm
def weighted_bm25(query, bookData, avLens, sentimentBias):
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
        
        # Adjustments 
        # Reward exact title match
        if " ".join(query) == book['norm_title']:
            bookScore -= 4

        # Reward exact author match
        if " ".join(query) == book['norm_authors']:
            bookScore -= 4

        if sentimentBias != None:
            # Include sentiment scores
            alpha = 1
            # A higher alpha punishes less similar sentiments harder, lower alpha punishes less and thus rewards 
            # more similar sentiments less as well
            sentimentFeature = math.exp(-alpha * abs(book['sentiment_score'] - sentimentBias)) * 2
            bookScore = (1 - sentimentWeight) * bookScore - sentimentFeature * sentimentWeight

        # Add the total doc score to scores
        scores.append((book['id'], book['title'], bookScore, book['authors']))

    return sorted(scores, key= lambda x: x[2])[:20]

def main():

    parser = argparse.ArgumentParser(
        prog = "bm25",
        description = "Retrieve the top 20 most relevant documents to a given query based on "
        "a text collection pulled from Google Books"
    )
    parser.add_argument("query", help="Your search query on the collection")
    parser.add_argument("-s", "--sentiment", type=float, help="What kind of feeling you're searching for in the book (float in [-1,1] \
                        where -1 is negative, 0 is neutral, and 1 is positive)")
    args = parser.parse_args()

    # Pull the collection from Supabase
    bookData = pull_books()

    # Get the average lengths for each field / zone
    averageLengths = {
        'title': sum(len(book['norm_title'].split()) for book in bookData) / len(bookData),
        'authors': sum(len(book['norm_authors'].split()) for book in bookData) / len(bookData),
        'genre': sum(len(book['norm_categories'].split()) for book in bookData) / len(bookData),
        'description': sum(len(book['description'].split()) for book in bookData) / len(bookData)
    }

    # Normalize user query
    normQuery = args.query.lower()
    normQuery = re.sub(r'\d+','',normQuery)
    normQuery = re.sub(r'[^\w\s]','',normQuery)
    normQuery = normQuery.strip()

    # Turn user query into list of terms
    queryTerms = normQuery.split()

    # Get the top 20 most relevant results based on BM25
    # for book in bookData[:25]:
    #     print(book['norm_title'])

    top20 = weighted_bm25(queryTerms, bookData, averageLengths, args.sentiment)

    
    for ind, result in enumerate(top20,1): # Print out the top 20 ranked results
        print(f"{ind}. {result[1]}, by {result[3]} - Score:{result[2]:.9f}")

if __name__ == "__main__":
    main()