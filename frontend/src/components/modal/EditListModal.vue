<template>
    <!-- Boton del modal -->
    <a href="#" class="subtle-link-styled" data-bs-toggle="modal" data-bs-target="#edit-list-modal">
        [Editar]
    </a>
    <!-- Modal -->
    <div class="modal fade" id="edit-list-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Cabecera del modal -->
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Editar lista</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <!-- Cuerpo del modal -->
                <div class="modal-body">
                    <!-- Formulario -->
                    <form @submit.prevent="handleSubmit" autocomplete="off">   
                        <!-- Nombre lista -->
                        <div class="form-floating mb-3">
                            <input v-model="listTemp.nombre_lista" type="text" class="form-control" id="floatingInput" placeholder="Romance" required>
                            <label for="floatingInput">Nombre</label>
                        </div>
                        <!-- Descripcion -->
                        <div class="form-floating">
                            <textarea v-model="listTemp.descripcion" class="form-control" placeholder="Mis favoritos de romance." id="floatingTextarea" maxlength="1024"></textarea>
                            <small>{{ listTemp.descripcion.length }}/1024 caracteres</small>
                            <label for="floatingTextarea">Descripcion</label>
                        </div>

                        <!-- Boton de envío -->
                        <div class="float-end mt-3">
                            <button type="submit" class="btn ml-primary-btn">Guardar cambios</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { List } from '@/types/types';
import { updateList } from '@/api/api';

// Definir props
const props = defineProps<{ list: List }>();

// Definir variables de datos
const listTemp = ref<any>({
    id_lista: 0,
    nombre_lista: '',
    descripcion: ''
});

const handleSubmit = async () => {
    try {
        // Actualizar los datos de la lista
        const res = await updateList(props.list.id_lista, listTemp.value);

        // Enviar alerta si se intenta editar las listas predeterminadas
        if (res.status === 401) {
            alert('No puedes editar las listas predeterminadas');
            return;
        }

        if (res.status !== 200) {
            alert('Error al actualizar la lista');
            return;
        }

        // Recargar la pagina
        window.location.reload();
    } catch (err) {
        console.error('Error actualizando usuario:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(() => {
    listTemp.value = JSON.parse(JSON.stringify(props.list));
});
</script>

<style scoped>

</style>