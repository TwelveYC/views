import Vue from 'vue'
import VueRouter from 'vue-router'
import SF from '../views/scaleFreeNetworks'

Vue.use(VueRouter)

const routes = [
  {
    path: '/sf',
    name: 'SF',
    component: SF
  },
  {
    path: '/ev',
    name: 'EV',
    component: function () {
      return import("../views/evolutionNetworks")
    }
  },
  {
    path: '/map',
    name: 'map',
    component: function () {
      return import("../views/mapNetworks")
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
