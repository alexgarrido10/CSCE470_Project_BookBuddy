# CSCE470_Project_BookBuddy
Repository for CSCE 470 Class project with Gabriel Floreslovo

## Set-up and testing
As of release v0.0.1, BookBuddy is a functioning implementation of the BM25 document ranking algorithm applied to document retrieval. This guide will help you test its functionality. 

1. Clone this repository onto your machine
```console
$ git clone git@github.com:alexgarrido10/CSCE470_Project_BookBuddy.git
```

2. Set up a Python virtual environment
BookBuddy was built with Python 3.12. No other versions of Python have been tested. The packages may still be compatible, but use different versions at your own discretion and use 3.12 for best results.
> **Note:** The commands shown here assume a UNIX shell (e.g. bash). You may need to make some alterations based on your shell.
```console
$ cd <path/to/BookBuddy/repo>
$ python3 -m venv bookbuddy
$ source bookbuddy/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements10-29-24-6pm.txt
$ python -m spacy download en_core_web_sm
```
> **NoteL** 
Alternatively, you can run our setup shell script.However, if problems arise it might be easier to run each command separately to debug.
```console
$ cd <path/to/BookBuddy/repo>
$ source setupEnv.sh
```

3. Usage
As the project continues, our database of books being serached through will be expanded. For now, there are ~1,700 books in our database. 
> **Note:** Note: In pre-deployment, you need to have a copy of the .env file to access our supabase API key. Contact us to request access to this file.
```console
$ python3 bm25.py "your query"
```

4. Backend Setup
> **Note:** The backend is Flask (Python)
```console
$ cd /backend_book_buddy
$ python3.12 -m venv backend_env
$ source backend_env/bin/activate
$ pip3 install flask
$ pip install flask_cors
$ python3.12 server.py # runs program

view on browser my putting http://127.0.0.1:8080/api/home into url bar
```
5. Frontend Setup
> **Note** The frontend is using Next.js (React)
```console
$ cd /frontend_book_buddy
$ npm run dev