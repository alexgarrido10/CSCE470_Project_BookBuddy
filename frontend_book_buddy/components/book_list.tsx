// frontend/components/BookList.tsx
import React from 'react';

const books = [
  { title: "Book One", author: "Author One" },
  { title: "Book Two", author: "Author Two" },
  // Sample data; replace with dynamic data as you build out API calls.
];

const BookList = () => {
  return (
    <div style={{ display: "grid", gap: "20px", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))" }}>
      {books.map((book, index) => (
        <div key={index} style={{
          border: "1px solid #ddd",
          padding: "10px",
          borderRadius: "4px",
          boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.1)"
        }}>
          <h3>{book.title}</h3>
          <p>{book.author}</p>
        </div>
      ))}
    </div>
  );
};

export default BookList;
