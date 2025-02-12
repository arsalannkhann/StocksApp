/**
 * Tailwind CSS Configuration
 * Defines content sources, theme extensions, and plugins
 */
module.exports = {
  // Specify file patterns for scanning and purging unused styles
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    // Optional: Add more paths to scan for classes
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}"
  ],

  // Theme customization and extension
  theme: {
    // Extend default theme with custom values
    extend: {
      // Example: Custom color palette
      colors: {
        'brand-primary': '#3B82F6',
        'brand-secondary': '#10B981'
      },
      // Example: Custom spacing
      spacing: {
        '128': '32rem',
        '144': '36rem'
      }
    }
  },

  // Add Tailwind plugins
  plugins: [
    // Example: Add a plugin for form styling
    require('@tailwindcss/forms'),
    // Example: Add typography plugin
    require('@tailwindcss/typography')
  ]
};