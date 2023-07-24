import PromptViewVue from '@/views/PromptView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    {
        path: '/view/profile',
        name: 'profile',
        props: true,
        component: () => import('../views/ProfileView.vue')
      },
      {
        path: '/view/prompt/:key',
        name: 'prompt',
        component: PromptViewVue,
        // props: route => ({ key: route.query.key }),
        props:true

      },
      {
        path: '/test',
        name: 'test',
        component: () => import('../views/DebugView.vue')
      },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
