import React, { useState } from 'react';

type SearchBarProps = {
  onSearchResults: (results: any[]) => void;
};

const SearchBar: React.FC<SearchBarProps> = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [mood, setMood] = useState(0); // Default mood value
  const [showMoodSlider, setShowMoodSlider] = useState(false); // State to control slider visibility

  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();

    if (query.trim()) {
      try {
        // Only use the mood parameter if the slider is shown and mood is not the default value
        // if we left it default value of 0 it would still affect the query

        // connection to the backend (flask)
        let url = `http://localhost:8080/api/search?query=${encodeURIComponent(query)}`;
        if (showMoodSlider) {
          url += `&mood=${mood}`;
        }

        const response = await fetch(url);
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
    <div className="flex flex-col items-center my-8 w-full">
      <form onSubmit={handleSearch} className="w-full max-w-3xl">
        <input
          type="text"
          placeholder="Search for books by title, author, or genre"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-4 text-xl border border-[#D9D9D9] bg-[#D9D9D9] rounded-lg placeholder-[#413D3D] text-center focus:outline-none focus:ring-2 focus:ring-[#D9D9D9]"
        />

        <div className="mt-4 flex justify-center items-center">
          <button
            type="button"
            onClick={() => setShowMoodSlider(!showMoodSlider)}
            className="px-4 py-2 bg-gray-700 text-white text-s rounded-lg"
          >
            {showMoodSlider ? 'Hide Mood Slider' : 'Feeling a certain mood? Click this to adjust your query based on how you are feeling!'}
          </button>
        </div>

        {showMoodSlider && (
          <div className="flex flex-col items-center mt-4">
            <p>The scale is from -1 to 1</p>
            <p>-1 is negative/dark mood and 1 is positive/lighter mood</p>
            <label htmlFor="mood-slider" className="text-lg font-bold">
              Select Mood Sentiment: {mood.toFixed(1)}
            </label>
            <input
              id="mood-slider"
              type="range"
              min="-1"
              max="1"
              step="0.1"
              value={mood}
              onChange={(e) => setMood(Number(e.target.value))}
              className="w-full max-w-sm"
            />
          </div>
        )}
      </form>
    </div>
  );
};

export default SearchBar;
