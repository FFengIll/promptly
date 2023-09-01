import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'index',
            redirect: '/view/index',
        },
        {
            path: '/view/index',
            name: 'prompt index',
            props: true,
            component: () => import('../views/IndexView.vue')
        },
        {
            path: '/view/prompt/:key',
            name: 'prompt',
            component: () => import('../views/PromptView.vue'),
            props: route => ({ key: route.params.key }),

        },
        {
            path: '/view/testing',
            name: 'prompt testing',
            component: () => import('../views/TestingView.vue'),
            props: true,
        },
        {
            path: '/view/commit/:key',
            name: 'prompt commit',
            component: () => import('../views/CommitView.vue'),
            props: route => ({ key: route.params.key })
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
