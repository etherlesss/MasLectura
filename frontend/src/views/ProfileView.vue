<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <div class="d-flex align-items-center gap-2">
                <h1>Mi perfil</h1>
                <router-link to="/my-profile/edit" class="subtle-link-styled">
                    <p>[Editar]</p>
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
            <div class="d-flex align-items-center gap-2">
                <h2>Mis Listas</h2>
                <CreateListModal :userID="authStore.user.id" />
            </div>
            <ListCard :lists="lists" />
        </div>
    </main>
    <ChangePwdModal />
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import ChangePwdModal from '@/components/modal/ChangePwdModal.vue';
import { onMounted, ref } from 'vue';
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
</style>