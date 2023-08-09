import {createRouter, createWebHistory} from 'vue-router';

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
            path: '/view/prompt/:key/advance',
            name: 'prompt (advance)',
            component: () => import('../views/AdvanceView.vue'),
            props: route => ({key: route.query.key}),

        },
        {
            path: '/view/test',
            name: 'prompt test',
            component: () => import('../views/TestingView.vue'),
            props: true,
        },
        {
            path: '/view/prompt/:key',
            name: 'prompt dev',
            component: () => import('../views/CommitView.vue'),
            props: route => ({key: route.query.key})
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
