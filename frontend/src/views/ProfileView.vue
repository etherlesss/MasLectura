<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <div >
                <div class="d-flex align-items-center gap-2 mb-4">
                    <h1>Mi perfil</h1>
                    <router-link to="/my-profile/edit" class="subtle-link-styled">
                        <p>[Editar]</p>
                    </router-link>
                </div>
                <div class="d-flex align-items-start gap-4">
                    <div class="profile-pic-container">
                        <img
                            :src="profilePicUrl"
                            alt="Foto de perfil"
                            class="profile-pic" />
                    </div>
                <div>
                    <p><b>Nombre de usuario:</b> {{ user?.nombre_usuario }}</p>
                    <p><b>Correo electrónico:</b> {{ user?.mail_usuario }}</p>
                    <p><b>Género: </b> {{ user?.genero_usuario }}</p>
                    <p><b>Fecha de nacimiento:</b> {{ formatDate(user?.fecha_nacimiento || '') }}</p>
                    <p><b>Contraseña</b> <a href="#" class="subtle-link-styled" data-bs-toggle="modal" data-bs-target="#changepwd-modal">[Cambiar]</a></p>
                </div>
                </div>
                
            </div>
            <div class ="mt-5">
                <div class="d-flex align-items-center gap-2">
                    <h2>Mis Listas</h2>
                    <CreateListModal :userID="authStore.user.id" />
                </div>
                <ListCard :lists="lists" />
            </div>
        </div>
    </main>
    <ChangePwdModal />
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import ChangePwdModal from '@/components/modal/ChangePwdModal.vue';
import { onMounted, ref, computed } from 'vue';
import { getProfile, getUserLists } from '@/api/api';
import { useAuthStore } from '@/stores/token';
import { formatDate } from '@/util/formatters';
import type { User, List } from '@/types/types';
import ListCard from '@/components/cards/ListCard.vue';
import CreateListModal from '@/components/modal/CreateListModal.vue';
import { useRoute, useRouter } from 'vue-router';

// Definir variables de datos
const user = ref<User | null>(null);
const lists = ref<List[]>([]);
const router = useRouter();
const route = useRoute();
// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

//Base URL para las fotos de perfil
const API_BASE_URL = 'http://127.0.0.1:3307/api';

//Foto default de perfil
const defaultProfilePic = 'https://ui-avatars.com/api/?name=Usuario&background=cccccc&color=555555&size=256';

const profilePicUrl = computed(() => {
    if (user.value && user.value.foto_perfil) {
        // Si la URL ya incluye http, úsala tal cual (por compatibilidad)
        if (user.value.foto_perfil.startsWith('http')) {
            return user.value.foto_perfil;
        }
        return API_BASE_URL + user.value.foto_perfil;
    }
    return defaultProfilePic;
});

if (Number(route.params.id) === Number(authStore.user.id)) {
  router.replace('/my-profile');
}
// Obtener los datos del usuario desde API
async function fetchUser() {
    try {
        const res = await getProfile(authStore.user.id);
        user.value = res.data;
    } catch (err) {
        console.error('Error fetching user:', err);
    }
}

// Obtener las listas del usuario desde API
async function fetchUserLists() {
    try {
        const res = await getUserLists(authStore.user.id);
        lists.value = res.data;
    } catch (err) {
        console.error('Error fetching user lists:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(async () => {
    await fetchUser();
    await fetchUserLists();
});
</script>

<style scoped>
p {
    margin: .5rem 0;
}


.profile-pic-container {
    min-width: 160px;
    min-height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-pic {
    width: 160px;
    height: 160px;
    object-fit: cover;
    border-radius: 12px; /* Bordes levemente redondeados, pero cuadrado */
    border: 2px solid #e0e0e0;
    background: #fafafa;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: box-shadow 0.2s;
}


</style>