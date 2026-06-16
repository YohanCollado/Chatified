import Vue from 'vue'
import Router from 'vue-router'
import Chat from '@/components/Chat'
import UserAuth from '@/components/UserAuth'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/chats'
    },
    {
      path: '/chats',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/chats/:uri',
      name: 'ChatSession',
      component: Chat
    },
    {
      path: '/auth',
      name: 'UserAuth',
      component: UserAuth
    }
  ]
})
