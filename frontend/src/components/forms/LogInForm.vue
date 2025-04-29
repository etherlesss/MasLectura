<template>
    <form>
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
                <p class="mt-2 float-end">Olvidaste tu contraseña? Recupérala <a href="#" class="link-styled">aquí</a>.</p>
            </div>
        </div>
        <!-- Boton de inicio de sesion -->
        <button type="submit" class="btn ml-primary-btn float-end">Iniciar sesión</button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { login } from '@/api/api';

const mail = ref<string>('');
const pwd = ref<string>('');

</script>

<style scoped>

</style>