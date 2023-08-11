// vue.config.js
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
    devServer: {
        proxy: {
            '/api/*': {
                target: 'http://localhost:8000/',
                ws: true,
                changeOrigin: true
            },
        }
    }
})