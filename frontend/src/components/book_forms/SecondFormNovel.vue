<template>
    <h6>
        2. Ingresar datos de la novela
    </h6>
    <br>
    <form class="row g-3">
        <div class="col-md-6">
            <label for="inputTittle" class="form-label mb-1">Titulo</label>
            <input type="text" class="form-control" id="inputTittle">
        </div>
        <div class="col-md-6">
            <label for="inputAutor" class="form-label mb-1">Autor</label>
            <input type="text" class="form-control" id="inputAutor">
        </div>
        <div class="col-md-6">
            <label for="inputEditorial" class="form-label mb-1">Editorial</label>
            <input type="text" class="form-control" id="inputEditorial">
        </div>
        <div class="col-md-6">
            <label for="inputPublication" class="form-label mb-1">Fecha de publicacion</label>
            <input v-model="birthdate" type="date" class="form-control" id="inputPublication" required>
        </div>
        <div class="col-md-6">
            <label for="inputIdioma" class="form-label mb-1">Idioma</label>
            <select id="inputIdioma" class="form-select">
                <option selected>Ninguno</option>
                <option value="1">Español</option>
                <option value="2">Inglés</option>
                <option value="3">Otro</option>
            </select>
        </div>
        <div class="col-md-6">
            <label for="inputChapters" class="form-label mb-1">Numero de capitulos</label>
            <input type="number" class="form-control" id="inputChapters">
        </div>
        <div class="mb-6">
            <label for="basic-url" class="form-label mb-1">Enlace de compra</label>
            <div class="input-group">
                <span class="input-group-text" id="basic-addon3">URL</span>
                <input type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3 basic-addon4">
            </div>
        </div>
        <div class="select-status"> La serie se encuentra finalizada:
            <br>
            <br>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option1" >
                <label class="form-check-label" for="option1">
                    Si
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option2" >
                <label class="form-check-label" for="option2">
                    No
                </label>
            </div>
        </div>
        <div class="mb-3">
            <label for="formFile" class="form-label">Portada</label>
            <input class="form-control" type="file" id="formFile">
        </div>
        <div class="save-button">
            <button type="button" alt = " " aria-label="">
            Guardar
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const birthdate = ref('');
</script>

<style scoped>
.save-button {
  display: flex;
  justify-content: center;
  margin-top: 2rem; 
}
</style>