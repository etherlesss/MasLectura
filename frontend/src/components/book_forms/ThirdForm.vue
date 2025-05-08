<template>
    <h6>
        3. Seleccionar género y etiquetas
    </h6>
    <br>
    
    <form class="row g-3">
        <!-- Sección Género -->
        <div class="col-md-12">
            <h6>Generos</h6>
            <label class="form-label mb-1"></label>
            <div class="genre d-flex flex-wrap gap-3">
                <div class="form-check" v-for="genero in generos" :key="genero.id">
                    <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'genero-' + genero.id"
                    :value="genero.nombre"
                    v-model="generosSeleccionados"
                    />
                    <label class="form-check-label" :for="'genero-' + genero.id">
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

            <!-- Select con etiquetas filtradas -->
            <select v-model="etiquetasSeleccionadas" multiple class="form-control">
                <option 
                    v-for="etiqueta in etiquetasFiltradas" 
                    :key="etiqueta.id" 
                    :value="etiqueta.nombre"
                >
                    {{ etiqueta.nombre }}
                </option>
            </select>

            <!-- Mostrar etiquetas seleccionadas -->
            <div class="selected-tags">
                <h6>Etiquetas seleccionadas:</h6>
                <ul>
                    <li v-for="(etiqueta, index) in etiquetasSeleccionadas" :key="index">
                        {{ etiqueta }}
                    </li>
                </ul>
            </div>
        </div>

        <!-- Botón de Guardar -->
        <div class="save-button">
            <button type="button" @click="guardarFormulario">
                Guardar
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

// Datos para géneros y etiquetas
const generos = ref<{ id: number; nombre: string }[]>([]);
const generosSeleccionados = ref<string[]>([]);
const etiquetas = ref<{ id: number; nombre: string }[]>([]);
const etiquetasSeleccionadas = ref<string[]>([]);
const busquedaEtiqueta = ref('');

// Cargar géneros y etiquetas desde la API al montar el componente
onMounted(async () => {
    try {
        // Cargar géneros
        const resGeneros = await fetch('/api/generos');
        generos.value = await resGeneros.json();

        // Cargar etiquetas
        const resEtiquetas = await fetch('/api/etiquetas');
        etiquetas.value = await resEtiquetas.json();
    } catch (error) {
        console.error('Error al cargar los géneros o etiquetas:', error);
    }
});

// Filtrar etiquetas basadas en la búsqueda del usuario
const etiquetasFiltradas = computed(() => {
    return etiquetas.value.filter((etiqueta) =>
        etiqueta.nombre.toLowerCase().includes(busquedaEtiqueta.value.toLowerCase())
    );
});

// Emitir evento con los géneros y etiquetas seleccionados
const emit = defineEmits(['guardar']);

function guardarFormulario() {
    const datos = {
        generosSeleccionados: generosSeleccionados.value,
        etiquetasSeleccionadas: etiquetasSeleccionadas.value,
    };
    emit('guardar', datos); // Emitir los datos al componente padre
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
</style>
