import React from 'react';

const SearchBar = () => {
  return (
    <div className="flex justify-center my-8 w-full max-w-3xl"> {/* Center and set max-width */}
      <input
        type="text"
        placeholder="Search for books by title, author, or genre"
        className="w-full p-4 text-xl border border-[#D9D9D9] bg-[#D9D9D9] rounded-lg placeholder-[#413D3D] text-center focus:outline-none focus:ring-2 focus:ring-[#D9D9D9]"
      />
    </div>
  );
};

export default SearchBar;

