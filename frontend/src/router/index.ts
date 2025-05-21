import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/token';

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
      component: () => import('../views/SearchView.vue'),
    },
    {
      path: '/addBook',
      name: 'addBook',
      component: () => import('../views/AddBook.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/my-profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
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
      meta: { requiresAuth: true }
    },
    {
      path: '/my-lists/:id_lista',
      name: 'my-lists',
      component: () => import('../views/ListView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/book/:id',
      name: 'bookView',
      component: () => import('../views/BookView.vue'),
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isTokenValid()) {
    alert('Su token ha caducado. Por favor inicie sesión nuevamente.');
    authStore.logout();
    return;
  }
  next();
});

export default router
