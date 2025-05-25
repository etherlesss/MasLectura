<template>
    <form @submit.prevent="handleSubmit" autocomplete="off">
        <!-- Titulo y subtitulo -->
        <div class="greet text-center">
            <h1>Crear cuenta</h1>
            <p>¡Crea tu propia cuenta y obtén tus propias recomendaciones personalizadas!</p>
        </div>
        <!-- Campos del formulario -->
        <div class="d-flex flex-column">
            <!-- Nombre de usuario -->
            <div class="mb-3">
                <label for="username" class="form-label mb-1">Nombre de usuario</label>
                <input v-model="username" type="text" class="form-control" id="username" placeholder="jsmith1992" required>
            </div>
            <!-- Correo electronico -->
            <div class="mb-3">
                <label for="mail" class="form-label mb-1">Correo electrónico</label>
                <input v-model="mail" type="email" class="form-control" id="mail" placeholder="jsmith@gmail.com" required>
            </div>
            <div class="d-flex gap-3">
                <!-- Contraseña -->
                <div class="mb-3 w-50">
                    <label for="pwd" class="form-label mb-1">Contraseña</label>
                    <input v-model="pwd" type="password" class="form-control" id="pwd" placeholder="contraseña" required>
                </div>
                <!-- Confirmar contraseña -->
                <div class="mb-3 w-50">
                    <label for="pwdconfirm" class="form-label mb-1">Confirmar contraseña</label>
                    <input v-model="pwdconfirm" type="password" class="form-control" id="pwdconfirm" placeholder="contraseña" required>
                </div>
            </div>
            <div class="d-flex gap-3">
                <!-- Fecha de nacimiento -->
                <div class="mb-3 w-50">
                    <label for="birthdate" class="form-label mb-1">Fecha de nacimiento</label>
                    <input v-model="birthdate" type="date" class="form-control" id="birthdate" required>
                </div>
                <!-- Genero -->
                <div class="mb-3 w-50">
                    <label for="gender" class="form-label mb-1">Género</label>
                    <select class="form-select" id="gender" v-model="gender" required>
                        <option selected value="" disabled>Seleccionar...</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                        <option value="No binario">No binario</option>
                        <option value="Prefiero no decirlo">Prefiero no decirlo</option> 
                    </select>
                </div>
            </div>
            <!-- Usuario ya tiene cuenta -->
            <hr>
            <p class="text-center mt-2">¿Ya tienes cuenta? Inicia sesión <a href="/login" class="link-styled">aquí</a>.</p>
        </div>
        <!-- Boton de inicio de sesion -->
        <button type="submit" class="btn ml-primary-btn float-end">Crear cuenta</button>
    </form>
</template>

<script setup lang="ts">
import { signup } from '@/api/api';
import { ref } from 'vue';

const username = ref<string>('');
const mail = ref<string>('');
const pwd = ref<string>('');
const pwdconfirm = ref<string>('');
const birthdate = ref<string>('');
const gender = ref<string>('');

const handleSubmit = async () => {
    try {
        // Validar que las contraseñas coincidan
        if (pwd.value !== pwdconfirm.value) {
            alert('Las contraseñas no coinciden. Por favor, inténtelo de nuevo.');
            return;
        }

        // Registrar al usuario
        const res = await signup({
            username: username.value,
            mail: mail.value,
            pwd: pwd.value,
            birthdate: birthdate.value,
            gender: gender.value
        });

        // Checkear si hay conflicto de existencia de usuario
        if (res.status === 409) {
            if (confirm('Este usuario ya tiene una cuenta. ¿Desea iniciar sesión?')) {
                // Redirigir a la página de inicio de sesión
                window.location.href = '/login';
            } else {
                alert('Por favor, elige otro nombre de usuario.');
                return;
            }
        }

        // Notificar al usuario que la cuenta ha sido creada exitosamente
        alert('La cuenta ha sido creada exitosamente. Por favor, inicia sesión.');
        // Redirigir a la página de inicio de sesión
        window.location.href = '/login';
    } catch (err) {
        console.error('Error al crear la cuenta:', err);
        alert('Ocurrió un error inesperado al crear la cuenta.');
    }
}

</script>

<style scoped>

</style>