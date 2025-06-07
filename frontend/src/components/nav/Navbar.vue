<template>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container-fluid">
            <!-- Brand large screens -->
            <router-link to="/" class="navbar-brand d-none d-lg-block">
                <img class="logo" src="@/assets/logo/logo-big.png" alt="Logo" style="pointer-events: none;" />
            </router-link>
            <!-- Brand small screens -->
            <router-link to="/" class="navbar-brand d-block d-lg-none">
                <img class="short-logo" src="@/assets/logo/logo-sm.png" alt="Logo" style="pointer-events: none;" />
            </router-link>
            <!-- Search bar -->
            <div class="search-bar mx-auto" @submit="handleSearch">
                <form class="d-flex" role="search">
                    <input class="form-control form-control-sm me-2" type="search" placeholder="Buscar lecturas..." aria-label="Search" v-model="searchQuery"/>
                    <button class="btn btn-outline-light" type="submit"><i class="bi bi-search"></i></button>
                </form>
            </div>
            <!-- Toggler/collapsible Button -->
            <button class="navbar-toggler p-1" type="button" data-bs-toggle="collapse" data-bs-target="#toggler" aria-controls="toggler" aria-expanded="false" aria-label="Toggle navigation" style="border-color: #fff;">
                <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
            </button>
            <!-- Links -->
            <div class="collapse navbar-collapse flex-grow-0" id="toggler">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Inicio</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/search">Lecturas</router-link>
                    </li>
                    <!-- No auth only -->
                    <li class="nav-item" v-if="!authStore.token">
                        <router-link class="nav-link" to="/login">Iniciar Sesion</router-link>
                    </li>
                    <li class="nav-item" v-if="!authStore.token">
                        <router-link class="nav-link" to="/signup">Crear Cuenta</router-link>
                    </li>
                    <!-- Auth only -->
                    <li class="nav-item dropdown" v-else>
                        <div class="nav-link dropdown-toggle d-flex align-items-center" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <img :src="profilePicUrl" alt="Avatar" class="avatar" />
                            <p class="m-0">{{ authStore.user.name }}</p>
                        </div>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><router-link class="dropdown-item" to="/my-profile">Mi perfil</router-link></li>
                            <li><router-link class="dropdown-item" to="/addBook">Agregar lectura</router-link></li>
                            <li><button class="dropdown-item" @click="authStore.logout()">Cerrar sesión</button></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/token';
import { getProfile } from '@/api/api';

// Definir variables
const authStore = useAuthStore();
const searchQuery = ref<string>('');
const router = useRouter();
const API_BASE_URL = 'http://127.0.0.1:3307/api';
import defaultProfilePic from '@/assets/foto-default.png';
const userProfile = ref<any>(null);

const profilePicUrl = computed(() => {
    if (userProfile.value && userProfile.value.foto_perfil) {
        return API_BASE_URL + userProfile.value.foto_perfil;
    }
    return defaultProfilePic;
});

onMounted(async () => {
    if (authStore.user?.id) {
        const res = await getProfile(authStore.user.id);
        userProfile.value = res.data;
    }
});

function handleSearch(event: Event) {
    event.preventDefault();
    if (searchQuery.value.trim()) {
        // Redirigir a la página de búsqueda con la consulta
        router.push({ path: '/search', query: { q: searchQuery.value } });
        // Limpiar el campo de búsqueda
        searchQuery.value = '';
    }
}
</script>

<style scoped>
.navbar {
    background-color: #262322;
}

.logo {
    width: 16rem;
}

.nav-item:hover .nav-link {
    text-decoration: underline;
}

.nav-link {
    color: #fff !important;
}

.navbar-nav .nav-item {
    display: flex;
    align-items: center;
}

.avatar {
    width: 2.5rem;
    height: 2.5rem;
    object-fit: cover;
    border-radius: 50%; 
    margin-right: 0.75rem; 

}
.short-logo {
    width: 3rem;
}
</style>