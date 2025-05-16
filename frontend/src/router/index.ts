import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LogInView.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUpView.vue'),
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/Search.vue'),
    },
    {
      path: '/addBook',
      name: 'addBook',
      component: () => import('../views/AddBook.vue'),
    },
    {
      path: '/my-profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
    },
    {
      path: '/recover-password/token=:token',
      name: 'recover-password',
      component: () => import('../views/PwdRecoveryView.vue'),
    },
    {
      path: '/my-profile/edit',
      name: 'edit-profile',
      component: () => import('../views/ProfileEditView.vue'),
    },
    {
      path: '/my-lists/:id_lista',
      name: 'my-lists',
      component: () => import('../views/ListView.vue'),
    }
  ],
})

export default router
