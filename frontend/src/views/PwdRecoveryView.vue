<template>
    <main class="login-container">
        <div>
            <!-- Contenedor de titulo y mensaje -->
            <div class="text-center">
                <h1>
                   :( 
                </h1>
                <p>¿Olvidaste tu contraseña? Ingresa tu nueva contraseña y repítela para cambiarla.</p>
            </div>
            <!-- Contenedor de formulario -->
            <div class="d-flex flex-column">
                <form @submit.prevent="handleResetPassword" autocomplete="off">
                    <!-- Contraseña -->
                    <div>
                        <label for="pwd" class="form-label mb-1">Contraseña</label>
                        <input v-model="pwd" :type="showPassword ? 'text' : 'password'" class="form-control" id="pwd" placeholder="Tu nueva contraseña" required>
                    </div>
                    <!-- Repetir contraseña -->
                    <div class="mt-3">
                        <label for="pwd-repeat" class="form-label mb-1">Repetir contraseña</label>
                        <input v-model="pwdRepeat" :type="showPassword ? 'text' : 'password'" class="form-control" id="pwd-repeat" placeholder="Vuelve a escribir tu nueva contraseña" required>
                    </div>
                    <!-- Checkbox para mostrar/ocultar contraseñas -->
                    <div class="form-check mt-3">
                        <input class="form-check-input" type="checkbox" id="show-password" v-model="showPassword">
                        <label class="form-check-label" for="show-password">
                            Mostrar contraseñas
                        </label>
                    </div>
                    <!-- Boton de recuperar contraseña -->
                    <button type="submit" class="btn ml-primary-btn mt-3 float-end">Recuperar contraseña</button>
                </form>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { resetPassword } from '@/api/api';

const pwd = ref<string>('');
const pwdRepeat = ref<string>('');
const showPassword = ref<boolean>(false);

// Obtener el token de la URL
const route = useRoute();
const token = route.params.token as string;

const handleResetPassword = async () => {
    if (pwd.value !== pwdRepeat.value) {
        alert('Las contraseñas no coinciden. Por favor, verifica e intenta nuevamente.');
        return;
    }

    try {
        const res = await resetPassword(token, pwd.value );
        if (res.status === 200) {
            alert('Contraseña recuperada exitosamente. Puedes iniciar sesión con tu nueva contraseña.');
            // Redirigir al inicio de sesión
            window.location.href = '/login';
        } else {
            alert('Error al recuperar la contraseña. Por favor, intenta nuevamente.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al recuperar la contraseña. Por favor, intenta nuevamente.');
    }
};
</script>

<style scoped>
.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    width: 100%;
}
</style>