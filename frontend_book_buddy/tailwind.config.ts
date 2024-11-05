import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#D5B895", // Custom background color
        foreground: "#43270F", // Custom foreground color
      },
      fontFamily: {
        lora: ['Lora', 'serif'], // Define the Lora font
      },
    },
  },
  plugins: [],
};
export default config;
