import React from 'react';

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex flex-col min-h-screen bg-background"> {/* Use custom background color */}
      <header className="text-foreground p-4 shadow-md"> {/* Use custom foreground color */}
        <h1 className="text-6xl font-bold font-lora">Book Buddy</h1> {/* Apply Lora font */}
      </header>
      <main className="flex-grow p-8">{children}</main>
      <footer className="bg-gray-800 text-white p-4 text-center">
        © 2024 Book Buddy
      </footer>
    </div>
  );
};

export default Layout;
