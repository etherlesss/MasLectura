<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <div class="d-flex gap-2">
                <h1>Mi perfil</h1>
                <router-link to="/my-profile/edit" class="d-flex align-items-center gap-2 subtle-link-styled">
                    <i class="bi bi-pencil"></i>
                    <p>Editar</p>
                </router-link>
            </div>
            <div>
                <p><b>Nombre de usuario:</b> {{ user?.nombre_usuario }}</p>
                <p><b>Correo electrónico:</b> {{ user?.mail_usuario }}</p>
                <p><b>Género: </b> {{ user?.genero_usuario }}</p>
                <p><b>Fecha de nacimiento:</b> {{ formatDate(user?.fecha_nacimiento || '') }}</p>
                <p><b>Contraseña</b> <a href="#" class="subtle-link-styled" data-bs-toggle="modal" data-bs-target="#changepwd-modal">[Cambiar]</a></p>
            </div>
        </div>
        <div>
            <h2>Mis Listas</h2>
        </div>
    </main>
    <ChangePwdModal />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import { onMounted, ref } from 'vue';
import { getProfile } from '@/api/api';
import { useAuthStore } from '@/stores/token';
import { formatDate } from '@/util/formatters';
import type { User } from '@/types/types';
import ChangePwdModal from '@/components/modal/ChangePwdModal.vue';

// Definir variables de datos
const user = ref<User | null>(null);

// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

// Obtener los datos del usuario desde API
async function fetchUser() {
    try {
        const res = await getProfile(authStore.user.id);
        user.value = res.data;
    } catch (err) {
        console.error('Error fetching user:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(async () => {
    await fetchUser();
});
</script>

<style scoped>
p {
    margin: .5rem 0;
}
</style>