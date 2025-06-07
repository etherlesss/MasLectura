<template>
    <h6 v-if="!ocultar">
        2. Ingresar datos de la novela
    </h6>
    <br>
    <form @submit.prevent class="row g-3">
        <div class="col-md-6">
            <label for="inputTittle" class="form-label mb-1">Título</label>
            <input  v-model="titulo" type = "text" class="form-control" id="inputTittle" required>
        </div>
        <div class="col-md-6">
            <label for="inputAutor" class="form-label mb-1">Autor</label>
            <input v-model="autor" type="text" class="form-control" id="inputAutor" required>
        </div>
        <div class="col-md-6">
            <label for="inputEditorial" class="form-label mb-1">Editorial</label>
            <input  v-model="editorial" type="text" class="form-control" id="inputEditorial" required>
        </div>
        <div class="col-md-6">
            <label for="anio" class="form-label mb-1">Año de publicación</label>
            <input 
                v-model="anio" 
                type="number" 
                class="form-control" 
                id="anio" 
                min="1000" 
                max="9999"
                required
            >
        </div>
        <div class="col-md-6">
            <label for="inputIdioma" class="form-label mb-1">Idioma</label>
            <select  v-model="idioma" id="inputIdioma" class="form-select" required>
                <option selected>Ninguno</option>
                <option value="Español">Español</option>
                <option value="Inglés">Inglés</option>
                <option value="Otro">Otro</option>
            </select>
        </div>
        <div class="col-md-6">
            <label for="inputChapters" class="form-label mb-1">Número de capitulos</label>
            <input v-model="numeroCapitulos" type="number" class="form-control" id="inputChapters">
        </div>
        <div class="mb-6">
            <label for="basic-url" class="form-label mb-1">Enlace de compra</label>
            <div class="input-group">
                <span class="input-group-text" id="basic-addon3">URL</span>
                <input v-model="urlCompra" type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3 basic-addon4">
            </div>
        </div>
        <div class="select-status"> La serie se encuentra finalizada:
            <br>
            <br>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option1" value="si" v-model="serieFinalizada">
                <label class="form-check-label" for="option1">
                    Si
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="sagaOption" id="option2" value="no" v-model="serieFinalizada" >
                <label class="form-check-label" for="option2">
                    No
                </label>
            </div>
        </div>

        <div class="mb-6">
            <label for="portada" class="form-label mb-1">Portada</label>
            <input @change="onFileChange" type="file" class="form-control" id="portada" accept="image/*">
        </div>
        <div class="mb-3">
            <label for="sinopsis" class="form-label mb-1">Sinopsis</label>
            <textarea class="form-control" id="sinopsis" rows="3" v-model="sinopsis"></textarea>
        </div>
        <div class="save-button">
            <button class = "btn ml-primary-btn mt-2 " type="button" @click="guardarFormulario" aria-label="Guardar" >
            Confirmar
            </button>
        </div>
        <div v-if="mensaje" :class="mensaje === '¡Guardado correctamente!' ? 'mensaje-guardado' : 'mensaje-error'">
            {{ mensaje }}
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { uploadImage } from '@/api/api';

const props = defineProps<{
  initialData?: Record<string, any>;
  ocultar: boolean;
}>();

const titulo = ref(props.initialData?.titulo || '');
const autor = ref(props.initialData?.autor || '');
const editorial = ref(props.initialData?.editorial || '');
const anio = ref(props.initialData?.anio || '');
const idioma = ref(props.initialData?.idioma || '');
const numeroCapitulos = ref(props.initialData?.num_capitulos || '');
const urlCompra = ref(props.initialData?.link_compra || '');
const portadaFile = ref<File|null>(null);
const urlPortada = ref(props.initialData?.portada || '');
const serieFinalizada = ref(props.initialData?.estado || '');
const sinopsis = ref(props.initialData?.sinopsis || '');
const mensaje = ref(props.initialData?.mensaje || '');
const emit = defineEmits(['guardar']);



// Computed para validar campos requeridos
const camposRequeridosCompletos = computed(() =>
    titulo.value.trim() !== '' &&
    autor.value.trim() !== '' &&
    idioma.value.trim() !== '' &&
    sinopsis.value.trim() !== '' &&
    portadaFile.value !== null
);

function onFileChange(event: Event) {
    const files = (event.target as HTMLInputElement).files;
    console.log('onFileChange triggered');
    if (files && files.length > 0) {
        portadaFile.value = files[0];
        console.log('Archivo seleccionado:', portadaFile.value);
    } else {
        console.log('No se seleccionó ningún archivo');
    }
}
async function subirImagen() {
    console.log('Entrando a subirImagen');
    if (!portadaFile.value) {
        console.log('No hay archivo de portada para subir');
        return;
    }
    const formData = new FormData();
    formData.append('imagen', portadaFile.value);
    console.log('FormData preparado para enviar:', formData);

    try {
        console.log('Enviando axios a /api/upload_image...');
        const response = await uploadImage(formData);
        console.log('Respuesta recibida de /api/upload_image:', response);

        if (!response || response.status !== 201) {
            console.error('Error al subir la imagen. Status:', response?.status);
            alert('Error al subir la imagen');
            return;
        }
        const data = response.data;
        console.log('Respuesta JSON de la subida:', data);
        urlPortada.value = data.url;
        console.log('URL de portada guardada:', urlPortada.value);
    } catch (error) {
        console.error('Excepción en subirImagen:', error);
        alert('Error inesperado al subir la imagen');
    }
}
async function guardarFormulario() {
    try{
        if (!camposRequeridosCompletos.value) {
            mensaje.value = 'Por favor, completa todos los campos requeridos.';
            setTimeout(() => {
             mensaje.value = '';
            }, 2500);
            return;
        }
    await subirImagen();
    const datos = {
        titulo: titulo.value,
        autor: autor.value,
        anio_publicacion: anio.value,
        portada: urlPortada.value,
        estado: serieFinalizada.value,
        link_compra: urlCompra.value,
        editorial: editorial.value,
        idioma: idioma.value,
        num_capitulos: numeroCapitulos.value === '' ? null : Number(numeroCapitulos.value),
        sinopsis: sinopsis.value,
        es_saga: 'N/A'
    };
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
  margin-top: 2rem; 
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

.mensaje-error {
  text-align: center;
  margin-top: 1rem;
  color: #721c24;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  transition: opacity 0.3s;
}
</style>