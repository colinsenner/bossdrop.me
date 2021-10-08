const colors = require('tailwindcss/colors')

module.exports = {
  mode: 'jit',
  purge: [
    './src/**/*.html',
    './src/**/*.njk',
    './src/**/*.md',
    './src/**/*.11ty.js'
  ],
  theme: {
    fontFamily: {
      sans: ['Montserrat', 'Open Sans', 'sans-serif'],
      serif: ['exocet', 'Merriweather', 'serif'],
    },
  },
}
