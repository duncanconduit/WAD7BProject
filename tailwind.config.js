/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
  './templates/**/*.html',
  './static/js/**/*.js',
  ],
  safelist: [
  'bg-red-300 dark:bg-red-500',
  'bg-blue-300 dark:bg-blue-500',
  'bg-green-300 dark:bg-green-500',
  'bg-yellow-300 dark:bg-yellow-500',
  'bg-purple-300 dark:bg-purple-500',
    ],
  darkMode: 'media',
  theme: {
  extend: {
    colors: {
    brand: {
      primary: '#3339f1',
      dark: '#1F365F',
      light: '#93C5FD',
      lightest: '#DBEAFE',
      darkest: '#1E3A8A',
      background: '#1e1e1e',

    },
    darktextbox: '#292929',
    darkinputlabel: '#949494',
    inputborder: '#cccccc',
    light_secondary_action: '#888888',
    dark_secondary_action: '#a8a8a8',
    dark_important: '#84484b'
    },
    boxShadow: {
      'brand-glow': '0 0 18px rgba(51, 57, 241, 0.4)',
    },
    fontFamily: {
    marlinSquare: ['MarlinSoftSquare', 'sans-serif'],
    },
  },
  },
  variants: {
  extend: {},
  },
  plugins: [],
};