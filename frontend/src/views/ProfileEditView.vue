<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <h1>Mi perfil</h1>
            <!-- Formulario -->
            <form @submit.prevent="handleSubmit" class="w-25" autocomplete="off">
                <!-- Nombre de usuario -->
                <div class="mb-3">
                    <label for="username" class="form-label mb-1"><b>Nombre de usuario</b></label>
                    <input v-model="user.nombre_usuario" type="text" class="form-control" id="username" placeholder="jsmith" required>
                </div>
                <!-- Correo electrónico -->
                <div class="mb-3">
                    <label for="mail" class="form-label mb-1"><b>Correo electrónico</b></label>
                    <input v-model="user.mail_usuario" type="email" class="form-control" id="mail" placeholder="jsmith@gmail.com" disabled>
                </div>
                <!-- Género -->
                <div class="mb-3">
                    <label for="gender" class="form-label mb-1">Género</label>
                    <select class="form-select" v-model="user.genero_usuario" id="gender" required>
                        <option selected disabled>Seleccionar...</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                        <option value="No binario">No binario</option>
                        <option value="Prefiero no decirlo">Prefiero no decirlo</option> 
                    </select>
                </div>
                <!-- Fecha de nacimiento -->
                <div class="mb-3">
                    <label for="birthdate" class="form-label mb-1">Fecha de nacimiento</label>
                    <input v-model="user.fecha_nacimiento" type="date" class="form-control" id="birthdate" required>
                </div>
                <!-- Botón de guardar cambios -->
                <button type="submit" class="btn ml-primary-btn float-end">Guardar cambios</button>
            </form>
        </div>
    </main>
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import { onMounted, ref } from 'vue';
import { getProfile, updateProfile } from '@/api/api';
import { useAuthStore } from '@/stores/token';
import { formatDateHTML } from '@/util/formatters';

// Definir variables de datos
const user = ref<any>({
    nombre_usuario: '',
    mail_usuario: '',
    genero_usuario: '',
    fecha_nacimiento: ''
});

// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

// Obtener los datos del usuario desde API
async function fetchUser() {
    try {
        const res = await getProfile(authStore.user.id);
        user.value = res.data;
        // Formatear la fecha de nacimiento al formato HTML
        user.value.fecha_nacimiento = formatDateHTML(user.value.fecha_nacimiento || '');
    } catch (err) {
        console.error('Error fetching user:', err);
    }
}

const handleSubmit = async () => {
    try {
        // Actualizar los datos del usuario
        const res = await updateProfile(authStore.user.id, user.value);

        if (res.status === 200) {
            console.log('Usuario actualizado correctamente');
            alert('Usuario actualizado correctamente');
            window.location.href = '/my-profile';
        } else {
            console.error('Error al actualizar el usuario:', res);
        }
    } catch (err) {
        console.error('Error actualizando usuario:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(async () => {
    await fetchUser();
});

</script>

<style scoped>

</style>