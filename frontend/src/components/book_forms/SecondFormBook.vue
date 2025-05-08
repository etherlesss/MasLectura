<template>
    <h6>
        2. Ingresar datos del libro
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
            <label for="inputEditorial" class="form-label mb-1">Editorial</label>
            <input v-model="editorial" class="form-control" id="inputEditorial" required>
        </div>
       
        <div class="col-md-6">
            <label for="inputIdioma" class="form-label mb-1">Idioma</label>
            <select id="inputIdioma" class="form-select">
                <option selected>Ninguno</option>
                <option value="Espanol">Español</option>
                <option value="Ingles">Inglés</option>
                <option value="Otro">Otro</option>
            </select>
        </div>
        <div class="col-md-6">
            <label for="fecha" class="form-label mb-1">Fecha de publicacion</label>
            <input v-model="fecha" type="date" class="form-control" id="fecha" required>
        </div>
         <div class="mb-6">
            <label for="basic-url" class="form-label mb-1">Enlace de compra</label>
            <div class="input-group">
                <span class="input-group-text" id="basic-addon3">URL</span>
                <input  v-model="url"  type="text" class="form-control" id="url" aria-describedby="basic-addon3 basic-addon4" required>
            </div>
        </div>
        <div class="mb-6">
            <label for="formFile" class="form-label mb-1">Portada</label>
            <input class="form-control" type="file" id="formFile">
        </div>
        <div class="select-serie"> El libro es parte de una saga:
            <br>
            <br>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option1" value="si" v-model="esSaga">
                <label class="form-check-label" for="option1">
                    Si
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option2" value="no" v-model="esSaga">
                <label class="form-check-label" for="option2">
                    No
                </label>
            </div>
        </div>
        <div class="col-md-6">
            <label for="inputSerie" class="form-label mb-1">Titulo de serie o saga</label>
            <input v-model="tituloSaga" class="form-control" type="text"  id="inputSerie" :disabled="esSaga !== 'si'">
        </div>
        <div class="col-md-6">
            <label for="inputBookNumber" class="form-label mb-1">Numero del libro</label>
            <input v-model="numeroLibro" class="form-control" type="number" id="inputBookNumber" :disabled="esSaga !== 'si'">
        </div>
        <div class="mb-3">
            <label for="sinopsis" class="form-label mb-1">Sinopsis</label>
            <textarea  class="form-control" id="sinopsis" rows="3" v-model="sinopsis"></textarea>
        </div>
        <div class="save-button">
            <button type="button" alt = " " aria-label="" @click="guardarFormulario">
            Guardar
            </button>
        </div>
        
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits(['guardar']);

const titulo = ref('');
const autor = ref('');
const editorial = ref('');
const idioma = ref('');
const fecha = ref('');
const url = ref('');
const tituloSaga = ref('');
const numeroLibro = ref('');
const esSaga = ref('');
const sinopsis= ref('');

function guardarFormulario() {
  const datos = {
    titulo: titulo.value,
    autor: autor.value,
    editorial: editorial.value,
    fechaPublicacion: fecha.value,
    idioma: idioma.value,
    esSaga: esSaga.value,
    url: url.value,
    tituloSaga: tituloSaga.value,
    numeroLibro: numeroLibro.value,
    sinopsis: sinopsis.value
  };
  emit('guardar', datos);  
}
</script>

<style scoped>
.save-button {
  display: flex;
  justify-content: center;
  margin-top: 2rem; 
}
</style>