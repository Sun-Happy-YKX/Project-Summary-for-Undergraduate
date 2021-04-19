import Vue from 'vue'
import VueRouter from 'vue-router'
import About from '@/components/Home/About.vue'
import Help from '@/components/Home/Help.vue'
import TeamIntroduction from '@/components/Home/TeamIntroduction.vue'
import Feedback from '@/components/Home/Feedback.vue'

Vue.use(VueRouter)

const HomeRoutes = [
  {
    path: '/Home/About',
    name: 'About',
    component: About
  },
  {
    path: '/Home/TeamIntroduction',
    name: 'TeamIntroduction',
    component: TeamIntroduction
  },
  {
    path: '/Home/Help',
    name: 'Help',
    component: Help
  },
  {
    path: '/Home/Feedback',
    name: 'Feedback',
    component: Feedback
  }
]
export default HomeRoutes
