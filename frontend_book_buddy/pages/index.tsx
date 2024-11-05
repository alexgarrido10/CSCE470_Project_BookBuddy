// frontend/pages/index.tsx
import React, { useEffect, useState } from 'react';
import Layout from '../components/layout';
import SearchBar from '../components/search_bar';
import BookList from '../components/book_list';

function Home() {
  const [message, setMessage] = useState("Loading");
  const [searchResults, setSearchResults] = useState([]); // State for search results

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Function to handle search results received from SearchBar
  const handleSearchResults = (results: any[]) => {
    setSearchResults(results); // Update search results
  };

  return (
    <Layout>
      <div className="flex flex-col items-center min-h-screen px-4 mt-40">
        <h2 className="text-foreground text-4xl font-lora font-bold my-1 text-center">
          Find Your Next Great Read.
        </h2>
        <SearchBar onSearchResults={handleSearchResults} /> {/* Pass handler to SearchBar */}
        <BookList books={searchResults} /> {/* Pass search results to BookList */}
      </div>
    </Layout>
  );
}

export default Home;
