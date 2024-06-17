import App from './App'
// #ifndef VUE3
import Vue from 'vue';
// Vue.use(i18n);
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
import i18n from './common/i18n.js';
export function createApp() {
  const app = createSSRApp(App)
  app.use(i18n);
  return {
    app
  }
}
// #endif