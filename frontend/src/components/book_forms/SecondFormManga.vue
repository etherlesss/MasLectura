<template>
    <h6>
        2. Ingresar datos del manga
    </h6>
    <br>
    <form class="row g-3">
        <div class="col-md-6">
            <label for="inputTittle" class="form-label mb-1">Titulo</label>
            <input v-model="titulo" type="text" class="form-control" id="inputTittle" required>
        </div>
        <div class="col-md-6">
            <label for="inputAutor" class="form-label mb-1">Autor</label>
            <input v-model="autor" type="text" class="form-control" id="inputAutor" required>
        </div>
        <div class="col-md-6">
            <label for="inputArtist" class="form-label mb-1">Artista</label>
            <input v-model="artista" type="text" class="form-control" id="inputArtist" required>
        </div>
        <div class="col-md-6">
            <label for="inputEditorial" class="form-label mb-1">Editorial</label>
            <input v-model="editorial" type="text" class="form-control" id="inputEditorial" required>
        </div>
        <div class="col-md-6">
            <label for="inputPublication" class="form-label mb-1">Fecha de publicacion</label>
            <input v-model="fechaPublicacion" type="date" class="form-control" id="inputPublication" required>
        </div>
        <div class="col-md-6">
            <label for="inputIdioma" class="form-label mb-1">Idioma</label>
            <select v-model="idioma" id="inputIdioma" class="form-select" required>
                <option value="1">Español</option>
                <option value="2">Inglés</option>
                <option value="3">Otro</option>
            </select>
        </div>
        <div class="col-md-6">
            <label for="inputChapters" class="form-label mb-1">Número de capítulos</label>
            <input v-model="numeroCapitulos" type="number" class="form-control" id="inputChapters" required>
        </div>
        <div class="mb-6">
            <label for="basic-url" class="form-label mb-1">Enlace de compra</label>
            <div class="input-group">
                <span class="input-group-text" id="basic-addon3">URL</span>
                <input v-model="url" type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3 basic-addon4" required>
            </div>
        </div>
        <div class="select-status">
            La serie se encuentra finalizada:
            <br><br>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="serieFinalizada" id="option1" value="si" v-model="serieFinalizada">
                <label class="form-check-label" for="option1">
                    Sí
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="serieFinalizada" id="option2" value="no" v-model="serieFinalizada">
                <label class="form-check-label" for="option2">
                    No
                </label>
            </div>
        </div>
        <div class="mb-3">
            <label for="formFile" class="form-label">Portada</label>
            <input class="form-control" type="file" id="formFile" required>
        </div>
        <div class="save-button">
            <!-- Asegúrate de que el evento @click dispare la función de guardar correctamente -->
            <button type="button" @click="guardarFormulario" aria-label="Guardar">
                Guardar
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Variables para los campos del formulario
const titulo = ref('');
const autor = ref('');
const artista = ref('');
const editorial = ref('');
const fechaPublicacion = ref('');
const idioma = ref('');
const numeroCapitulos = ref('');
const url = ref('');
const serieFinalizada = ref('');
const portada = ref('');

// Emitir evento al guardar los datos
const emit = defineEmits(['guardar']);

function guardarFormulario() {
  const datos = {
    titulo: titulo.value,
    autor: autor.value,
    artista: artista.value,
    editorial: editorial.value,
    fechaPublicacion: fechaPublicacion.value,
    idioma: idioma.value,
    numeroCapitulos: numeroCapitulos.value,
    url: url.value,
    serieFinalizada: serieFinalizada.value,
    portada: portada.value,
  };
  emit('guardar', datos); // Emitir los datos al componente padre
}
</script>

<style scoped>
.save-button {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}
</style>
