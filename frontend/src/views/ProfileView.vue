<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <h1>Mi perfil</h1>
            <div>
                <p><b>Nombre de usuario:</b> {{ user?.nombre_usuario }}</p>
                <p><b>Correo electrónico:</b> {{ user?.mail_usuario }}</p>
                <p><b>Género: </b> {{ user?.genero_usuario }}</p>
                <p><b>Fecha de nacimiento:</b> {{ formatDate(user?.fecha_nacimiento || '') }}</p>
            </div>
        </div>
        <div>
            <h2>Mis Listas</h2>
        </div>
    </main>
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import { onMounted, ref } from 'vue';
import { getProfile } from '@/api/api';
import { useAuthStore } from '@/stores/token';
import { formatDate } from '@/util/formatters';
import type { User } from '@/types/types';

// Definir variables de datos
const user = ref<User | null>(null);

// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

// Obtener los datos del usuario desde API
async function fetchUser() {
    try {
        user.value = await getProfile(authStore.user.id);
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