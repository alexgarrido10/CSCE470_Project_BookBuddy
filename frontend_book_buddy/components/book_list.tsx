import React from 'react';

// type Book = {
//   rank: number;
//   title: string;
//   score: string;
// };

type BookListProps = {
  books: Book[];
};

const BookList: React.FC<BookListProps> = ({ books }) => {

// just return a list of the results i would usually get from bm25.py
  return (
    <div className="mt-10">
      {books.length === 0 ? (
        <p>No books found. Try a different search!</p>
      ) : (
        <ul>
          {books.map((book) => (
            <li key={book.rank} className="my-4 p-2 border-b">
              <h3 className="text-xl">{book.title}</h3>
              <p>Score: {book.score}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BookList;
