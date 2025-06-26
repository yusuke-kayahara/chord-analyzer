const plugin = require('tailwindcss/plugin');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
        },
        accent: {
          500: '#f59e0b',
          600: '#d97706',
        }
      },
      fontFamily: {
        'music': ['Georgia', 'serif'],
      }
    },
  },
  plugins: [
    plugin(function({ addUtilities, theme }) {
      addUtilities({
        '.slider-track': {
          '--tw-gradient-from': theme('colors.blue.500', '#3b82f6'),
          '--tw-gradient-to': theme('colors.blue.500', '#3b82f6'),
          'background-image': `linear-gradient(to right, var(--tw-gradient-from) var(--value, 0%), ${theme('colors.gray.300', '#d1d5db')} var(--value, 0%))`,
        },
      });
    }),
  ],
};