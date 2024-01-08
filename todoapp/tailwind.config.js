/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/**/*.{html, }",
  ],
  theme: {
    extend: {
      zIndex :{
        "1000":"999",
        "1024":"1000"
      }

    },
  },
  plugins: [],
}

