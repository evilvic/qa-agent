import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './assets/tokens.css'

import RootApp from './RootApp.vue'

const app = createApp(RootApp)

app.use(createPinia())
app.use(router)

app.mount('#app')
