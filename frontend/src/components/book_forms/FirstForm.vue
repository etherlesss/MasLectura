<template>
    <h6>
        1. Seleccionar el tipo de lectura que desea agregar
    </h6>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="Book" value = "libro" v-model = "tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="Book">
            Libro
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="AssianNovel" value = "novel" v-model = "tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="AssianNovel">
            Novela Asiatica
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="selectOption" id="Manga" value = "manga" v-model = "tipo" @change="emitirSeleccion">
        <label class="form-check-label" for="Manga">
            Manga
        </label>
    </div>
    
   
</template>

<script setup lang="ts">
    import { ref } from 'vue';
    const emit = defineEmits(['tipoSeleccionado', 'guardar']);
    const tipo = ref('');

    function emitirSeleccion() {
        emit('tipoSeleccionado', tipo.value);
        emitirDatos();
    }
    function emitirDatos() {
        emit('guardar', { tipo: tipo.value }); 
    }
    


</script>

<style scoped>


    

</style>