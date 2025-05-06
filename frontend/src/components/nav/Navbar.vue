<template>

    <nav class="navbar">
        <div class = 'logo'>
            <img src= "@/assets/logo/logo-big.png" alt="Logo" class="logo">
        </div>
        <div class = "search-bar">
            <input type="text" placeholder="Buscar nueva lectura...">
            <button type="button">
                <img src="@/assets/icon-search.png">
            </button>
        </div>

        <div class = 'options'>
            <ul class="nav-list">
                <li class = "nav-links">
                    <RouterLink to="/">Inicio</RouterLink>
                </li>
                <li class = "nav-links">
                    <RouterLink to="/search">Lecturas</RouterLink>
                </li>

                <!--Si el usuario NO  esta autenticado-->
                <li class = "nav-links" v-if="!isLoggedIn">
                    <RouterLink to="/login">Iniciar Sesion</RouterLink>
                </li>
                <li class = "nav-links" v-if="!isLoggedIn">
                    <RouterLink to="/signup">Crear Cuenta</RouterLink>
                </li>
                <!--Si el usuario SI esta autenticado-->
                <li class="nav-links user-dropdown" v-else>
                    <img :src="avatarUser" alt="" class="avatar" />
                    <div @click="toggleDropdown" class="user-dropdown-toggle">
                        <span>{{ userName }}</span>
                        <span class="arrow">▼</span>
                    </div>
                    <ul v-if="dropdownOpen" class="dropdown-menu">
                        <li><RouterLink to="/profile">Perfil</RouterLink></li>
                        <li><RouterLink to="/addBook">Agregar lectura</RouterLink></li>
                        <li><button @click="logout" class="logout-btn">Cerrar sesión</button></li>
                      
                    </ul>
                </li>
            </ul>
        </div>
      
    </nav>

</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

interface Usuario {
  id: number;
  name: string;
  email: string;
  foto: string;
}

const user = ref<Usuario | null>(null);
const defaultAvatar = new URL('@/assets/foto-default.png', import.meta.url).href;
const avatarUser = ref(defaultAvatar);
const isLoggedIn = computed(() => user.value !== null);
const userName = computed(() => user.value?.name ?? '');
const dropdownOpen = ref(false);
const router = useRouter();

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  user.value = null;
  avatarUser.value = defaultAvatar;
  router.push('/'); // Redirige al home u otra ruta
}

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value;
}

function handleClickOutside(event: MouseEvent) {
  const dropdown = document.querySelector('.user-dropdown');
  if (dropdown && !dropdown.contains(event.target as Node)) {
    dropdownOpen.value = false;
  }
}

function obtenerFotoPerfil() {
  const token = localStorage.getItem('token');
  if (token) {
    fetch('http://localhost:3000/api/usuario', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        user.value = data;  // Almacena los datos del usuario
        avatarUser.value = data.foto || defaultAvatar;  // Asigna la foto del usuario
      })
      .catch((err) => {
        console.error('Error al obtener datos del usuario:', err);
      });
  }
}

onMounted(() => {
  const userData = localStorage.getItem('user');
  console.log('Contenido en localStorage:', userData);
  if (userData) {
    try {
      user.value = JSON.parse(userData);
      console.log('Usuario cargado:', user.value);
      obtenerFotoPerfil();
    } catch (e) {
      console.error('Error al parsear JSON de usuario:', e);
    }
  }
});

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>

.navbar{
    background-color: #262322;
    display:flex;
    align-items: center;
}

.logo{
    height: auto;
    width: 300px;
}

.nav-list{
    display: flex;
    list-style: none;   
    align-items: center;

}

.nav-links a {
  padding: 20px;
  color: white;
  text-decoration: none;
  align-items: center;
}
.nav-links span {
    padding: 20px;
    color: white;
}
.nav-links img {
    height: 35px;
    margin: 2px;
}

.search-bar{
    padding:auto;
}

.search-bar input{
    width: 300px;
    padding: 3px;
    font-size: 16px;
}

.search-bar button{
    height: 35px;
    margin: 2px;
    background-color: #262322;
    border-color: rgb(155, 154, 154);
}

.user-dropdown {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1px;
  cursor: pointer;
  color: white;
}

.user-dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 3px;
}

.user-dropdown-toggle span{
  padding: 6px;
}

.arrow {
  font-size: 12px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #262322;
  border: 1px solid #444;
  border-radius: 5px;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 100;
  min-width: 130px;
  display: block;
}

.dropdown-menu li {
  text-align: left;
  color: white;
  width: 100%;
  white-space: nowrap;
  border-bottom: 1px solid rgb(117, 117, 117);
  padding: 10px 10px;
  
}
.dropdown-menu a {
  padding: 10px;
  
  
}

.dropdown-menu li:hover {
  background-color: #3a3736;
  
}

.logout-btn {
  padding-left: 5px 5px;
  background: none;
  border: none;
  color: white;
  width: 100%;
  text-align: left;
  
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #3a3736;
}

*{
    margin: 0;
}


</style>