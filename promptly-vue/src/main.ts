// import './assets/main.css';

import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from './App.vue';
import router from './router';

import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(Antd)
app.use(router)

app.mount('#app')
