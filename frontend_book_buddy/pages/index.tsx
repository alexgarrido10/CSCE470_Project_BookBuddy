// frontend/pages/index.tsx
import React, { useEffect, useState } from 'react';
import Layout from '../components/layout';
import SearchBar from '../components/search_bar';
import BookList from '../components/book_list';

function Home() {
  const [message, setMessage] = useState("Loading");

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <Layout>
      <div className="flex flex-col items-center min-h-screen px-4 mt-40"> {/* Center everything */}
        <h2 className="text-foreground text-4xl font-lora font-bold my-1 text-center">
          Find Your Next Great Read.
        </h2>
        <SearchBar />
        <p>{message}</p>
      </div>
    </Layout>
  );
}

export default Home;
