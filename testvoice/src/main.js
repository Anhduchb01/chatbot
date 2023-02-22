import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false
import VueRecord from '@codekraft-studio/vue-record'
Vue.use(VueRecord)
new Vue({
  render: h => h(App),
}).$mount('#app')
