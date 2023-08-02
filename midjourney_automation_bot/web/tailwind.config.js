/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/*.{html,js}"],
  darkMode: false, // or 'media' or 'class'
  purge: {
    enabled: true,
    content: ["**/*.{html,js}"],
  },
  theme: {
    extend: {},
  },
  plugins: [],
}
