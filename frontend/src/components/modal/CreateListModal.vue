<template>
    <!-- Boton del modal -->
    <a href="#" class="subtle-link-styled" data-bs-toggle="modal" data-bs-target="#create-list-modal">
        [Crear lista]
    </a>
    <!-- Modal -->
    <div class="modal fade" id="create-list-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Cabecera del modal -->
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Crear lista</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <!-- Cuerpo del modal -->
                <div class="modal-body">
                    <!-- Formulario -->
                    <form @submit.prevent="handleSubmit" autocomplete="off">   
                        <!-- Nombre lista -->
                        <div class="form-floating mb-3">
                            <input v-model="listName" type="text" class="form-control" id="floatingInput" placeholder="Romance" required>
                            <label for="floatingInput">Nombre</label>
                        </div>
                        <!-- Descripcion -->
                        <div class="form-floating">
                            <textarea v-model="listDesc" class="form-control" placeholder="Mis favoritos de romance." id="floatingTextarea" maxlength="1024"></textarea>
                            <small>{{ listDesc.length }}/1024 caracteres</small>
                            <label for="floatingTextarea">Descripcion</label>
                        </div>

                        <!-- Boton de envío -->
                        <div class="float-end mt-3">
                            <button type="submit" class="btn ml-primary-btn">Crear</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { createList } from '@/api/api';
import { ref, onMounted, onUnmounted } from 'vue';

// Definir variables
const listName = ref<string>('');
const listDesc = ref<string>('');

// Definir prop
const props = defineProps({ userID: Number });

// Funcion para limpiar el formulario
function clearForm() {
    listName.value = '';
    listDesc.value = '';
}

const handleSubmit = async () => {
    try {
        // Crear lista
        const res = await createList({id_usuario: props.userID, nombre_lista: listName.value, descripcion: listDesc.value});

        // Recargar la página en caso de éxito
        if (res.status === 201) {
            window.location.reload();
        } else {
            alert('Ocurrió un error al crear la lista');
        }
    } catch (err) {
        console.error('Error creating list:', err);
    }
}

// Escuchar el evento de cierre del modal para limpiar el formulario
onMounted(() => {
    const modalElement = document.getElementById('create-list-modal');
    if (modalElement) {
        modalElement.addEventListener('hidden.bs.modal', clearForm);
    }
});

onUnmounted(() => {
    const modalElement = document.getElementById('create-list-modal');
    if (modalElement) {
        modalElement.removeEventListener('hidden.bs.modal', clearForm);
    }
});
</script>

<style scoped>

</style>