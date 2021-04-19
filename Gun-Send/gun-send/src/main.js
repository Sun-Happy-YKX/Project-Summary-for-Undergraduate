import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Gun from 'gun'
import VueGun from 'vue-gun'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import Axios from 'axios'
import VueBus from 'vue-bus'
import clipboard from 'clipboard'
import VideoPlayer from 'vue-video-player'
import 'vue-video-player/src/custom-theme.css'
import 'video.js/dist/video-js.css'
import 'gun/lib/radix'
import 'gun/lib/radisk'
import 'gun/lib/store'
import 'gun/lib/rindexed'
import 'gun/lib/webrtc'
import 'gun/lib/path'
import 'gun/lib/open'
import 'gun/lib/load'
import '@/assets/style/scroll.css'

Vue.use(VideoPlayer)
Vue.use(VueBus)
Vue.use(ElementUI)
Vue.use(VueGun, {
  peers: ['http://39.106.193.116:8765/gun'],
  radisk: true,
  localStorage: false
})

Vue.config.productionTip = false
Vue.prototype.axios = Axios
Vue.prototype.clipboard = clipboard
Vue.component('User')

new Vue({
  router,
  store,
  Gun,
  VueGun,
  render: h => h(App)
}).$mount('#app')
