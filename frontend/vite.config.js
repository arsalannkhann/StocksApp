// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Explicitly define entry point
  build: {
    rollupOptions: {
      input: {
        main: './src/main.tsx'  // Adjust path to your main entry file
      }
    }
  },
  optimizeDeps: {
    include: ['recharts']
  }
});