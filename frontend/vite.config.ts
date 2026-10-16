import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'

const protectPublicInquiry = (): Plugin => ({
  name: 'protect-public-inquiry',
  configureServer(server) {
    server.middlewares.use('/api/inquiries/', (request, response, next) => {
      const hostname = request.headers.host?.split(':')[0]
      const isLocal = hostname === '127.0.0.1' || hostname === 'localhost'
      if (request.method === 'POST' && !isLocal) {
        response.statusCode = 403
        response.setHeader('Content-Type', 'application/json; charset=utf-8')
        response.end(JSON.stringify({detail: 'Отправка заявок отключена в публичном режиме просмотра.'}))
        return
      }
      next()
    })
  },
})

export default defineConfig({
  plugins: [react(), protectPublicInquiry()],
  server: {
    port: 5173,
    allowedHosts: true,
    proxy: {'/api': {target: 'http://127.0.0.1:8000', changeOrigin: true}},
  },
})

