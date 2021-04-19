import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/components/Home.vue'
import Upload from '@/components/Upload.vue'
import Download from '@/components/Download.vue'
import HomeRoutes from './HomeRoutes.js'

Vue.use(VueRouter)

const mainPages = [
  {
    path: '/',
    redirect: '/Home'
  },
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  {
    path: '/Upload',
    name: 'Upload',
    component: Upload
  },
  {
    path: '/Download',
    name: 'Download',
    component: Download
  }
]

let SumRoutes = []
SumRoutes = SumRoutes.concat(mainPages).concat(HomeRoutes)
const routes = SumRoutes

const router = new VueRouter({
  // 这个只适用于服务器端
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
