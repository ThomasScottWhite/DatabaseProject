import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy all requests starting with "/api" to the backend
      '/api': {
        target: 'http://localhost:8080', // Backend server URL
        changeOrigin: true,             // Changes the origin of the request to the target
        rewrite: (path) => path.replace(/^\/api/, ''), // Optional: remove "/api" prefix when forwarding
      },
    },
  },
});

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

