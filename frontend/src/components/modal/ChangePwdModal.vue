<template>
    <!-- Modal -->
    <div class="modal fade" id="changepwd-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Cabecera del modal -->
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Cambiar contraseña</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <!-- Cuerpo del modal -->
                <div class="modal-body">
                    <!-- Formulario -->
                    <form @submit.prevent="handleSubmit" autocomplete="off">
                        <!-- Contraseña actual -->
                        <div>
                            <label for="pwd-current" class="form-label mb-1">Contraseña actual</label>
                            <input
                                v-model="pwdCurrent"
                                :type="showPassword ? 'text' : 'password'"
                                class="form-control"
                                id="pwd-current"
                                placeholder="Tu contraseña actual"
                                pattern='^(?=.*[!@#$%^&*(),.?\":{}|<>])[^\s]{6,30}$'
                                title="La contraseña debe tener entre 6 y 30 caracteres y al menos un carácter especial"
                                required
                            >
                        </div>
                        <!-- Contraseña -->
                        <div>
                            <label for="pwd" class="form-label mb-1">Contraseña</label>
                            <input
                                v-model="pwd"
                                :type="showPassword ? 'text' : 'password'"
                                class="form-control"
                                id="pwd"
                                placeholder="Tu nueva contraseña"
                                pattern='^(?=.*[!@#$%^&*(),.?\":{}|<>])[^\s]{6,30}$'
                                title="La contraseña debe tener entre 6 y 30 caracteres y al menos un carácter especial"
                                required
                            >
                        </div>
                        <!-- Repetir contraseña -->
                        <div class="mt-3">
                            <label for="pwd-repeat" class="form-label mb-1">Repetir contraseña</label>
                            <input
                                v-model="pwdRepeat"
                                :type="showPassword ? 'text' : 'password'"
                                class="form-control"
                                id="pwd-repeat"
                                placeholder="Vuelve a escribir tu nueva contraseña"
                                pattern='^(?=.*[!@#$%^&*(),.?\":{}|<>])[^\s]{6,30}$'
                                title="La contraseña debe tener entre 6 y 30 caracteres y al menos un carácter especial"
                                required
                            >
                        </div>
                        <!-- Checkbox para mostrar/ocultar contraseñas -->
                        <div class="form-check mt-3">
                            <input class="form-check-input" type="checkbox" id="show-password" v-model="showPassword">
                            <label class="form-check-label" for="show-password">
                                Mostrar contraseñas
                            </label>
                        </div>

                        <!-- Boton de envío -->
                        <div class="float-end mt-3">
                            <button type="submit" class="btn ml-primary-btn">Enviar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import { useAuthStore } from '@/stores/token';
import { updatePassword } from '@/api/api';

// Definir variables de datos
const pwdCurrent = ref<string>('');
const pwd = ref<string>('');
const pwdRepeat = ref<string>('');
const showPassword = ref<boolean>(false);

// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

// Funcion para limpiar el formulario
function clearForm() {
    pwd.value = '';
    pwdRepeat.value = '';
}

const handleSubmit = async () => {
    try {
        // Validar que las contraseñas coincidan
        if (pwd.value !== pwdRepeat.value) {
            alert('Las contraseñas no coinciden');
            return;
        }

        // Validar que las contraseñas cumplan con el patrón
        const passwordPattern = /^(?=.*[!@#$%^&*(),.?":{}|<>])[^\s]{6,30}$/;
        if (!passwordPattern.test(pwd.value)) {
            alert('La contraseña debe tener entre 6 y 30 caracteres, incluir al menos un carácter especial y no contener espacios.');
            return;
        }

        // Actualizar los datos del usuario
        const res = await updatePassword(authStore.user.id, { pwd: pwd.value, pwdCurrent: pwdCurrent.value });

        if (res.status === 200) {
            console.log('Contraseña actualizada correctamente');
            alert('Contraseña actualizada correctamente, por favor vuelve a iniciar sesión');
            // Desloguear al usuario y redirigir a inicio de sesión
            authStore.logout();
            window.location.href = '/login';
        } else if (res.status === 401) {
            alert('Contraseña actual incorrecta');
        } else {
            console.error('Error al actualizar el usuario:', res);
        }
    } catch (err) {
        console.error('Error actualizando usuario:', err);
    }
}

// Escuchar el evento de cierre del modal para limpiar el formulario
onMounted(() => {
    const modalElement = document.getElementById('changepwd-modal');
    if (modalElement) {
        modalElement.addEventListener('hidden.bs.modal', clearForm);
    }
});

onUnmounted(() => {
    const modalElement = document.getElementById('changepwd-modal');
    if (modalElement) {
        modalElement.removeEventListener('hidden.bs.modal', clearForm);
    }
});
</script>

<style scoped>

</style>