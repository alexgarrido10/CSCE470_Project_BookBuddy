# CSCE470_Project_BookBuddy
Repository for CSCE 470 Class project with Gabriel Floreslovo

## Set-up and testing
As of release v0.0.1, BookBuddy is a functioning implementation of the BM25 document ranking algorithm applied to document retrieval. This section details how to test the functionality based on the source code in this repository. 

1. Clone this repository onto your machine
```console
$ git clone git@github.com:alexgarrido10/CSCE470_Project_BookBuddy.git
```

2. Set up a Python virtual environment
The source code in this repository and the virtual environment it runs in was built with Python 3.12. No earlier versions have been tested. The packages may still be compatible, but use different versions at your own discretion (Note: The commands shown here are for unix shells; specifically bash. You may need to make some alterations based on your shell)
```console
$ cd <path/to/BookBuddy/repo>
$ python3 -m venv bookbuddy
$ source bookbuddy/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements10-29-24-6pm.txt
$ python -m spacy download en_core_web_sm
```

3. Usage
As the project continues, the repository of books being serached through will increase in size. For now, there are ~1,700 books in our database. (Note: In pre-deployment, you need to have a copy of the .env file to access our supabase API key. Contact us about this.)
```console
$ python3 bm25.py "your query"
```