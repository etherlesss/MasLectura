import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/token';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { title: 'Inicio' }
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LogInView.vue'),
      meta: { title: 'Iniciar sesión' }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUpView.vue'),
      meta: { title: 'Crear cuenta' }
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue'),
      meta: { title: 'Buscar lecturas' }
    },
    {
      path: '/addBook',
      name: 'addBook',
      component: () => import('../views/AddBook.vue'),
      meta: { requiresAuth: true, title: 'Agregar libro' }
    },
    {
      path: '/my-profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true, title: 'Mi perfil' }
    },
    {
      path: '/recover-password/token=:token',
      name: 'recover-password',
      component: () => import('../views/PwdRecoveryView.vue'),
      meta: { title: 'Recuperar contraseña' }
    },
    {
      path: '/my-profile/edit',
      name: 'edit-profile',
      component: () => import('../views/ProfileEditView.vue'),
      meta: { requiresAuth: true, title: 'Editar mi perfil' }
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
    },
    {
      path: '/book/edit/:id',
      name: 'bookEdit', 
      component: () => import('../views/BookEdit.vue'),
    },
    {
      path: '/user-profile/:id',
      name: 'user-profile',
      component: () => import('../views/OtherUserProfile.vue'),
      meta: { requiresAuth: true }
    },
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

// Settear el título de la página a aquellas menos especificas
router.afterEach((to) => {
  const defaultTitle = '+Lectura';
  document.title = (typeof to.meta.title === 'string' ? to.meta.title : defaultTitle);
});

export default router
