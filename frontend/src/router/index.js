import Vue from 'vue'
import Router from 'vue-router'
import viewLogin from '@/components/login'
import viewReg from '@/components/register'
import viewQuery from '@/components/query'
import viewUpload from '@/components/upload'
import viewAdmin from '@/components/admin'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: { template: "<div></div>" }
    },
    {
      path: '/login',
      component: viewLogin
    },
    {
      path: '/register',
      component: viewReg
    },
    {
      path: '/query',
      component: viewQuery
    },
    {
      path: '/upload',
      component: viewUpload
    },
    {
      path: '/admin',
      component: viewAdmin
    },
  ]
})
