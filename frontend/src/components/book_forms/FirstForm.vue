<template>
    <h6>
        1. Seleccionar el tipo de lectura que desea agregar
    </h6>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="Book" value="Libro" v-model="tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="Book">
            Libro
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="AssianNovel" value="Novela" v-model="tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="AssianNovel">
            Novela Asiática
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="Manga" value="Manga" v-model="tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="Manga">
            Manga
        </label>
    </div>
    <div class="save-button">
        <button type="button" alt=" " aria-label="Guardar" @click="guardarFormulario":disabled="!tipo">
            Guardar
        </button>
    </div>
    <div v-if="mensaje" class="mensaje-guardado">
        {{ mensaje }}
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const props = defineProps<{ initialData?: Record<string, any> }>();
const emit = defineEmits(['tipoSeleccionado', 'guardar']);
const tipo = ref(props.initialData?.tipo|| '');
const mensaje = ref(props.initialData?.mensaje || '');


// Emitir el tipo seleccionado
function emitirSeleccion() {
    emit('tipoSeleccionado', tipo.value);
}

// Emitir los datos al guardar
function guardarFormulario() {
    try {
        const datos = { tipo: tipo.value };
        console.log('Datos enviados:', datos);
        emit('guardar', datos);
        mensaje.value = '¡Guardado correctamente!';
    } catch (e) {
        mensaje.value = 'Ocurrió un error al guardar.';
    }
    setTimeout(() => {
        mensaje.value = '';
    }, 2500); 
}
</script>

<style scoped>
.save-button {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
}
.save-button button:disabled {
    background-color: #ccc;
    cursor: not-allowed;   
}

.mensaje-guardado {
    text-align: center;
    margin-top: 1rem;
    color: #155724;
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    transition: opacity 0.3s;
}
</style>