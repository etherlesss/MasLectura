<template>
    <form @submit.prevent="handleSubmit">
        <!-- Titulo y subtitulo -->
        <div class="greet text-center">
            <h1>¡Bienvenido de vuelta!</h1>
            <p>Ingresa tus credenciales para recibir tus recomendaciones en un solo lugar.</p>
        </div>
        <!-- Campos del formulario -->
        <div class="d-flex flex-column">
            <!-- Correo electronico -->
            <div class="mb-3">
                <label for="mail" class="form-label mb-1">Correo electrónico</label>
                <input v-model="mail" type="email" class="form-control" id="mail" placeholder="jsmith@gmail.com" required>
            </div>
            <!-- Contraseña -->
            <div>
                <label for="pwd" class="form-label mb-1">Contraseña</label>
                <input v-model="pwd" type="password" class="form-control" id="pwd" placeholder="contraseña" required>
                <!-- Recuperar constraseña -->
                <p class="mt-2 float-end">Olvidaste tu contraseña? Recupérala <a href="#" class="link-styled" data-bs-toggle="modal" data-bs-target="#recover-modal">aquí</a>.</p>
            </div>
            <!-- Usuario no tiene cuenta -->
            <hr>
            <p class="text-center mt-2">¿No tienes cuenta? Crea la tuya <a href="/signup" class="link-styled">aquí</a>.</p>
        </div>
        <!-- Boton de inicio de sesion -->
        <button type="submit" class="btn ml-primary-btn float-end">Iniciar sesión</button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/token';
import { login } from '@/api/api';

const mail = ref<string>('');
const pwd = ref<string>('');
const authStore = useAuthStore();

const handleSubmit = async () => {
    try {
        const res = await login({ mail: mail.value, pwd: pwd.value });

        // Checkear la existencia del usuario
        if (res.status === 404) {
            alert('Usuario no encontrado. Por favor verifica tus credenciales.');
            return;
        }

        // Checkear si la contraseña es correcta
        if (res.status === 401) {
            alert('Contraseña incorrecta. Por favor verifica tus credenciales.');
            return;
        }

        // Verificar acceso
        if (res.data.token) {
            // Obtener token
            const token = res.data.token;
            // Obtener datos del usuario
            const user = res.data.user;
            // Obtener fecha de expiración del token
            const expDate = new Date(res.data.exp_date);

            // Almacenar token y datos en el store de Pinia
            authStore.setToken(token, expDate);
            authStore.setUser(user);

            // Redirigir a la página principal
            window.location.href = '/';
        }
    } catch (err) {
        console.error('Error al iniciar sesión:', err);
        alert('Ocurrió un error inesperado al iniciar sesión.');
    }
}

</script>

<style scoped>

</style>