<template>
    <h6 v-if="!ocultar">
        3. Seleccionar género y etiquetas
    </h6>
    <br>
    
    <form @submit.prevent class="row g-3">
        <!-- Sección Género -->
        <div class="col-md-12">
            <h6>Generos</h6>
            <label class="form-label mb-1"></label>
            <div class="genre d-flex flex-wrap justify-content-center gap-3">
                <div class="form-check" v-for="genero in generosFiltrados":key="genero.nombre" :title="genero.descripcion">
                    <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'genero-' + genero.nombre"
                    :value="genero.nombre"
                    v-model="generosSeleccionados"
                    />
                    <label class="form-check-label" :for="'genero-' + genero.nombre">
                    {{ genero.nombre }}
                    </label>
                </div>
            </div>
        </div>

        <!-- Sección Etiquetas -->
        <div class="col-md-12">
            <h6>Etiquetas</h6>
            <!-- Input para buscar etiquetas -->
            <input 
                v-model="busquedaEtiqueta" 
                type="text" 
                class="form-control"
                placeholder="Escribe para buscar etiquetas..."
            />

            <!-- Mostrar etiquetas filtradas como opciones -->
            <div class="tags-container d-flex flex-wrap">
                <div 
                    v-for="etiqueta in etiquetasFiltradas" 
                    :key="etiqueta.id"  
                    @click="agregarEtiqueta(etiqueta.nombre)"  
                    class="form-check tag-item"
                    :title="etiqueta.descripcion"
                >
                    <span class="tag-option">{{ etiqueta.nombre }}</span>
                </div>
            </div>

            <!-- Mostrar etiquetas seleccionadas con opción de eliminar -->
            <div class="selected-tags">
                <h6>Etiquetas seleccionadas:</h6>
                <ul>
                    <li v-for="(etiqueta, index) in etiquetasSeleccionadas" :key="index" class="selected-tag-item">
                        {{ etiqueta }}
                        <button type="button"
                            @click="eliminarEtiqueta(etiqueta)" 
                            class="btn btn-danger btn-sm ms-2"
                            aria-label="Eliminar etiqueta"
                        >
                            &times;
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        <div  class="save-button">
            <button class = "btn ml-primary-btn mt-2 " type="button" @click="guardarFormulario" aria-label="Guardar">
            Confirmar
            </button>
        </div>
        <div v-if="mensaje" :class="mensaje === '¡Guardado correctamente!' ? 'mensaje-guardado' : 'mensaje-error'">
            {{ mensaje }}
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { getGenres, getGenresById, getTags, getTagsIdBook } from '@/api/api';

// Datos para géneros y etiquetas
const propsIdLibro = defineProps<{ idLibro?: number; 
    ocultar?: boolean;
 }>();
const generos = ref<{ nombre: string, descripcion: string }[]>([]);
const etiquetas = ref<{ id: number, nombre: string, descripcion: string }[]>([]);
const busquedaEtiqueta = ref('');
const mensaje = ref('');
const generosSeleccionados = ref<string[]>([]);
const etiquetasSeleccionadas = ref<string[]>([]);


// Al montar, cargar todos los géneros y etiquetas, y si hay idLibro, cargar los seleccionados
onMounted(async () => {
    // Cargar todos los géneros y etiquetas
    try {
        const resGeneros = await getGenres();
        if (resGeneros.status === 200) generos.value = resGeneros.data;
    } catch (e) { console.error('Error al cargar géneros:', e); }

    try {
        const resEtiquetas = await getTags();
        if (resEtiquetas.status === 200) etiquetas.value = resEtiquetas.data;
    } catch (e) { console.error('Error al cargar etiquetas:', e); }

    // Si hay idLibro, cargar los seleccionados
    if (propsIdLibro.idLibro) {
    try {
        const resSelGeneros = await getGenresById(propsIdLibro.idLibro);
        if (resSelGeneros.status === 200) {
            console.log('Respuesta de getGenresById:', resSelGeneros.data);
            generosSeleccionados.value = resSelGeneros.data;
        }
    } catch (e) { console.error('Error al cargar géneros seleccionados:', e); }

    try {
        const resSelEtiquetas = await getTagsIdBook(propsIdLibro.idLibro);
        if (resSelEtiquetas.status === 200) {
            console.log('Respuesta de getTagsIdBook:', resSelEtiquetas.data);
            etiquetasSeleccionadas.value = resSelEtiquetas.data;
        }
    } catch (e) { console.error('Error al cargar etiquetas seleccionadas:', e); }
}
    console.log('Todos los géneros:', generos.value.map(g => g.nombre));
    console.log('Seleccionados:', generosSeleccionados.value);
    console.log('Todas las etiquetas:', etiquetas.value.map(e => e.nombre));
    console.log('Seleccionadas:', etiquetasSeleccionadas.value);
});

// Filtrar géneros basados en la búsqueda del usuario
const generosFiltrados = computed(() => {
    return generos.value.filter(g => g.nombre && g.nombre.trim() !== "")
    .sort((a, b) => a.nombre.localeCompare(b.nombre));
});

// Filtrar etiquetas basadas en la búsqueda del usuario
const etiquetasFiltradas = computed(() => {
    return etiquetas.value
        .filter((etiqueta) =>
            etiqueta.nombre.toLowerCase().includes(busquedaEtiqueta.value.toLowerCase())
        )
        .filter((etiqueta) => !etiquetasSeleccionadas.value.includes(etiqueta.nombre)) // Excluir etiquetas seleccionadas
        .sort((a, b) => a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' })); // Orden alfabético
});

// Función para agregar etiqueta seleccionada
function agregarEtiqueta(etiqueta: string) {
    if (!etiquetasSeleccionadas.value.includes(etiqueta)) {
        etiquetasSeleccionadas.value.push(etiqueta);
        console.log('Etiquetas seleccionadas:', etiquetasSeleccionadas.value);
        console.log('Etiquetas filtradas:', etiquetasFiltradas.value);
    } else {
        console.warn(`La etiqueta "${etiqueta}" ya está seleccionada.`);
    }
}
// Función para eliminar una etiqueta seleccionada
function eliminarEtiqueta(etiqueta: string) {
    etiquetasSeleccionadas.value = etiquetasSeleccionadas.value.filter(e => e !== etiqueta);
}
// Emitir evento con los géneros y etiquetas seleccionados
const emit = defineEmits(['guardar']);

// Computed para validar campos requeridos
const camposRequeridosCompletos = computed(() =>
    generosSeleccionados.value.length > 0 &&
    etiquetasSeleccionadas.value.length > 0
);

function guardarFormulario() {
    try {
        if (!camposRequeridosCompletos.value) {
            mensaje.value = 'Por favor, selecciona al menos un género y una etiqueta.';
            setTimeout(() => {
             mensaje.value = '';
            }, 2500);
            return;
        }
        const datos = {
            generosSeleccionados: generosSeleccionados.value,
            etiquetasSeleccionadas: etiquetasSeleccionadas.value
        };
        console.log('Datos enviados:', datos);
        emit('guardar', datos); // Emitir los datos al componente padre
        mensaje.value = '¡Guardado correctamente!';
        setTimeout(() => {
        mensaje.value = '';
    }, 2500);
    } catch (e) {
        mensaje.value = 'Ocurrió un error al guardar.';
    }
}
</script>

<style scoped>
.selected-tags {
    margin-top: 1rem;
    border: 1px solid #ccc;
    padding: 0.5rem;
    border-radius: 5px;
}

.selected-tags ul {
    list-style-type: none;
    padding: 0;
}

.selected-tags li {
    margin: 0.3rem 0;
}

.save-button {
    display: flex;
    justify-content: center;
    margin-top: 2rem; 
}

.genre {
    max-width: 600px; 
    margin: 0 auto;   
}
.form-check {
    width: 150px;     
    text-align: left;
}
.selected-tags {
    margin-top: 1rem;
    border: 1px solid #ccc;
    padding: 0.5rem;
    border-radius: 5px;
}

.selected-tags ul {
    list-style-type: none;
    padding: 0;
}

.selected-tags li {
    display: inline-flex;
    align-items: center;
    margin: 0.3rem 0;
    padding: 0.3rem;
    background-color: #f1f1f1;
    border-radius: 5px;
}

.selected-tag-item button {
    background: none;
    border: none;
    color: #ff0000;
    font-size: 1.2rem;
    cursor: pointer;
}

.selected-tag-item button:hover {
    color: #d50000;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.3rem;
  max-width: 800px;
  margin: 0 auto;
  max-height: 200px; 
  overflow-y: auto;  
  padding: 0.5rem;
  border: 1px solid #ccc; 
}

.tag-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.3rem 0.5rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, text-decoration 0.3s; 
  font-size: 0.75rem;
  text-align: center;
  height: 2rem;
  
}

.selected-tag-item {

    border-radius: 5px;
    border: 1px solid #8a8a8a; /* Borde negro */
}

.tag-option {
  font-size: 0.75rem; 
}
.tag-item:hover {
  background-color: #f1f1f1;
  text-decoration: underline;
}

.form-container{
    align-items:center ;
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
