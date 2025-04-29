<template>
    <form>
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
                <input v-model="username" type="text" class="form-control" id="username" placeholder="jsmith1992" required autocomplete="off">
            </div>
            <!-- Correo electronico -->
            <div class="mb-3">
                <label for="mail" class="form-label mb-1">Correo electrónico</label>
                <input v-model="mail" type="email" class="form-control" id="mail" placeholder="jsmith@gmail.com" required autocomplete="off">
            </div>
            <div class="d-flex gap-3">
                <!-- Contraseña -->
                <div class="mb-3 w-50">
                    <label for="pwd" class="form-label mb-1">Contraseña</label>
                    <input v-model="pwd" type="password" class="form-control" id="pwd" placeholder="contraseña" required autocomplete="off">
                </div>
                <!-- Confirmar contraseña -->
                <div class="mb-3 w-50">
                    <label for="pwdconfirm" class="form-label mb-1">Confirmar contraseña</label>
                    <input v-model="pwdconfirm" type="password" class="form-control" id="pwdconfirm" placeholder="contraseña" required autocomplete="off">
                </div>
            </div>
            <div class="d-flex gap-3">
                <!-- Fecha de nacimiento -->
                <div class="mb-3 w-50">
                    <label for="birthdate" class="form-label mb-1">Fecha de nacimiento</label>
                    <input v-model="birthdate" type="date" class="form-control" id="birthdate" required autocomplete="off">
                </div>
                <!-- Genero -->
                <div class="mb-3 w-50">
                    <label for="gender" class="form-label mb-1">Género</label>
                    <select class="form-select" id="gender" required>
                        <option selected disabled>Seleccionar...</option>
                        <option value="1">Masculino</option>
                        <option value="2">Femenino</option>
                        <option value="3">No binario</option>
                        <option value="4">Prefiero no decirlo</option> 
                    </select>
                </div>
            </div>
        </div>
        <!-- Boton de inicio de sesion -->
        <button type="submit" class="btn ml-primary-btn float-end">Crear cuenta</button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const username = ref<string>('');
const mail = ref<string>('');
const pwd = ref<string>('');
const pwdconfirm = ref<string>('');
const birthdate = ref<string>('');
const gender = ref<string>('');

</script>

<style scoped>

</style>