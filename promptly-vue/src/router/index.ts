import PromptViewVue from '@/views/PromptView.vue'
import {createRouter, createWebHistory} from 'vue-router'
import DebugView from "@/views/DebugView.vue";
import IterationView from "@/views/IterationView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'index',
            redirect: '/view/profile',
        },
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
            props: true

        },
        {
            path: '/view/debug',
            name: 'debug',
            component: DebugView,
            props: true,
        },
        {
            path: '/view/iteration',
            name: 'iteration',
            component: IterationView,
            // props: true,
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
