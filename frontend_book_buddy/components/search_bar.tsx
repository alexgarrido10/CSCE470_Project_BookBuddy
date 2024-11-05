// frontend/components/search_bar.tsx
import React, { useState } from 'react';

type SearchBarProps = {
  onSearchResults: (results: any[]) => void;
};

const SearchBar: React.FC<SearchBarProps> = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();

    if (query.trim()) {
      try {
        const response = await fetch(`http://localhost:8080/api/search?query=${encodeURIComponent(query)}`);
        const results = await response.json();

        if (response.ok) {
          onSearchResults(results); // Pass search results to Home component
        } else {
          console.error("Error fetching search results:", results.error);
        }
      } catch (error) {
        console.error("Error during search:", error);
      }
    }
  };

  return (
    <div className="flex justify-center my-8 w-full">
      <form onSubmit={handleSearch} className="w-full max-w-3xl">
        <input
          type="text"
          placeholder="Search for books by title, author, or genre"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-4 text-xl border border-[#D9D9D9] bg-[#D9D9D9] rounded-lg placeholder-[#413D3D] text-center focus:outline-none focus:ring-2 focus:ring-[#D9D9D9]"
        />
      </form>
    </div>
  );
};

export default SearchBar;
