<template>
    <!-- Modal -->
    <div class="modal fade" id="recover-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Cabecera del modal -->
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Recuperar contraseña</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="clearForm"></button>
                </div>
                <!-- Cuerpo del modal -->
                <div class="modal-body">
                    <!-- Informacion -->
                    <p>Ingresa tu correo electrónico para recuperar tu contraseña.</p>
                    <!-- Formulario -->
                    <form @submit.prevent="sendRecoveryEmail" autocomplete="off">   
                        <!-- Correo -->
                        <div class="form-floating mb-3">
                            <input v-model="mail" type="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
                            <label for="floatingInput">Correo electrónico</label>
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
import { ref } from 'vue';
import { recoverPassword } from '@/api/api';

const mail = ref<string>('');

// Funcion para limpiar el formulario
function clearForm() {
    mail.value = '';
}

const sendRecoveryEmail = async () => {
    // Enviar el correo electrónico
    try {
        const res = await recoverPassword(mail.value);
        console.log("RES", res);
        if (res.status === 200) {
            alert('Correo de recuperación enviado. Por favor, revisa tu bandeja de entrada.');
            
        } else {
            alert('Error al enviar el correo de recuperación. Por favor, intenta nuevamente.');
        }
    } catch (err) {
        console.error('Error:', err);
        alert('Error al enviar el correo de recuperación. Por favor, intenta nuevamente.');
    }
};

</script>

<style scoped>

</style>