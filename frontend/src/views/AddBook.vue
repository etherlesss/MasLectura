<template>
    <div>
        <Navbar />
        <div class="addBook-container">
            <!-- Sección 1: Tipo de lectura -->
            <div class="section-container">
                <div class="button-container">
                    <button type="button" aria-label="Tipo de lectura" @click="toggleSeccion('tipoLectura')">
                        Tipo de lectura
                    </button>
                </div>
                <div class="message-container">
                    <div class="message-box" v-if="!secciones.tipoLectura">
                        <h6>Seleccionar el tipo de lectura que desea agregar</h6>
                    </div>
                    <div class="form-container" v-show="secciones.tipoLectura">
                        <FirstForm 
                            @guardar="guardarFirstForm" 
                            @tipoSeleccionado="tipoSeleccionado = $event" />
                    </div>
                </div>
                
                <div class ="message-info-container">
                    <div class="message-info" v-show="secciones.tipoLectura">
                        <p>Información adicional sobre esta sección.</p>
                    </div>
                </div>
            </div>

            <!-- Sección 2: Ingresar datos -->
            <div class="section-container">
                <div class="button-container">
                    <button  type="button" aria-label="Ingresar datos" @click="toggleSeccion('ingresarDatos')" :disabled="!tipoSeleccionado || !secciones.tipoLecturaGuardado">
                        Ingresar datos
                    </button>
                </div>
                <div class="message-container">
                    <div class="message-box" v-if="!secciones.ingresarDatos">
                        <h6>Ingresar los datos del libro</h6>
                    </div>
                    <div class="form-container" v-show="secciones.ingresarDatos">
                        <SecondFormBook v-if="tipoSeleccionado === 'libro'" @guardar="guardarSecondForm" />
                        <SecondFormNovel v-if="tipoSeleccionado === 'novel'"  @guardar="guardarSecondForm" />
                        <SecondFormManga v-if="tipoSeleccionado === 'manga'"  @guardar="guardarSecondForm" />
                    </div>
                </div>
                <div class ="message-info-container">
                    <div class="message-info" v-show="secciones.ingresarDatos">
                        <p>Información adicional sobre esta sección.</p>
                    </div>
                </div>
            </div>

            <!-- Sección 3: Seleccionar categorías -->
            <div class="section-container">
                <div class="button-container">
                    <button 
                        type="button" 
                        aria-label="Seleccionar categorías" 
                        @click="toggleSeccion('seleccionarCategorias')" 
                        :disabled="!secciones.ingresarDatosGuardado"
                    >
                        Seleccionar categorías
                    </button>
                </div>
                <div class="message-container">
                    <div 
                        class="message-box" 
                        v-if="!secciones.seleccionarCategorias"
                    >
                        <h6>Seleccionar género y etiquetas</h6>
                    </div>
                    <div 
                        class="form-container" 
                        v-show="secciones.seleccionarCategorias"
                    >
                        <ThirdForm @guardar="guardarThirdForm" />
                    </div>
                </div>
                <div class ="message-info-container">
                    <div class="message-info" v-show="secciones.seleccionarCategorias">
                        <p>Información adicional sobre esta sección.</p>
                    </div>
                </div>
            </div>

            <!-- Botón final -->
            <div class="save-button">
                <button 
                    @click="enviarTodo" 
                    :disabled="!secciones.seleccionarCategoriasGuardado"
                >
                    Enviar
                </button>
            </div>
        </div>
        <Footer />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { getGenres } from '@/api/api';
import { getTags } from '@/api/api';
import { addBook } from '@/api/api';
import { addBookTag } from '@/api/api';
import { addBookGenre } from '@/api/api';
import Navbar from '@/components/nav/Navbar.vue';
import FirstForm from '@/components/book_forms/FirstForm.vue';
import SecondFormBook from '@/components/book_forms/SecondFormBook.vue';
import SecondFormNovel from '@/components/book_forms/SecondFormNovel.vue';
import SecondFormManga from '@/components/book_forms/SecondFormManga.vue';
import ThirdForm from '@/components/book_forms/ThirdForm.vue';
import Footer from '@/components/pageFooter/Footer.vue';

const tipoSeleccionado = ref('');
const firstFormData = ref<Record<string, any>>({});
const secondFormData = ref<Record<string, any>>({});
const thirdFormData = ref<Record<string, any>>({});

// Estados de las secciones
const secciones = ref({
    tipoLectura: false, // Ahora la primera sección también está oculta al principio
    tipoLecturaGuardado: false,
    ingresarDatos: false,
    ingresarDatosGuardado: false,
    seleccionarCategorias: false,
    seleccionarCategoriasGuardado: false,
});

// Define un tipo para las claves de 'secciones'
type SeccionKey = keyof typeof secciones.value;

// Alternar visibilidad de las secciones (solo una abierta a la vez)
function toggleSeccion(seccion: SeccionKey) {
    // Cierra todas las secciones
    Object.keys(secciones.value).forEach((key) => {
        if (!key.endsWith('Guardado')) {
            secciones.value[key as SeccionKey] = false;
        }
    });
    secciones.value[seccion] = true;
}
function guardarFirstForm(data: any) {
    // Guardar los datos del primer formulario
    firstFormData.value = data;
    tipoSeleccionado.value = data.tipo;
    secciones.value.tipoLecturaGuardado = true;

    // Restablecer las demás secciones
    secciones.value.ingresarDatosGuardado = false;
    secciones.value.seleccionarCategorias = false;
    secciones.value.seleccionarCategoriasGuardado = false;

    // Limpiar los datos de las demás secciones
    secondFormData.value = {};
    thirdFormData.value = {};

    // Mostrar un mensaje de éxito
    console.log('Datos del primer formulario guardados:', firstFormData.value);
}

// Guardar datos de la segunda sección
function guardarSecondForm(data: any) {
    secondFormData.value = data;
    secciones.value.ingresarDatosGuardado = true;
    console.log('Datos del segundo formulario guardados:', secondFormData.value);
}

// Guardar datos de la tercera sección
function guardarThirdForm(data: any) {
    thirdFormData.value = data; // Aquí se guardan los IDs de géneros y etiquetas
    secciones.value.seleccionarCategoriasGuardado = true;
    console.log('Datos del tercer formulario guardados:', thirdFormData.value);
}

async function buscarIdsPorNombres() {
    const generosSeleccionadosNombres = [...(thirdFormData.value.generosSeleccionados || [])];
    const etiquetasSeleccionadasNombres = [...(thirdFormData.value.etiquetasSeleccionadas || [])];
    const resGeneros = await getGenres();
    const todosGeneros = await resGeneros.json();
    const resEtiquetas = await getTags();
    const todasEtiquetas = await resEtiquetas.json();

    // Buscar los IDs correspondientes a los nombres seleccionados
    const generosIds = generosSeleccionadosNombres.map((nombre: string) => {
        const genero = todosGeneros.find((g: any) => {
            return g.nombre.trim().toLowerCase() === nombre.trim().toLowerCase();
        });
        return genero ? genero.id : null;
    }).filter((id: number | null) => id !== null);

    const etiquetasIds = etiquetasSeleccionadasNombres.map((nombre: string) => {
        const etiqueta = todasEtiquetas.find((e: any) => {
            return e.nombre.trim().toLowerCase() === nombre.trim().toLowerCase();
        });
        return etiqueta ? etiqueta.id : null;
    }).filter((id: number | null) => id !== null);

    console.log('Datos enviados:', {
        generosIds,
        etiquetasIds,
    });

    return { generosIds, etiquetasIds };
}
// Enviar todos los datos
async function enviarTodo() {
    try {
        // Buscar los IDs de géneros y etiquetas
        const { generosIds, etiquetasIds } = await buscarIdsPorNombres();
        // Enviar los datos del primer y segundo formulario al backend (book.py)
        const responseLibro = await addBook({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...firstFormData.value,
                ...secondFormData.value,
            }),
        });

        if (!responseLibro.ok) {
            if (responseLibro.status === 409) {
                const data = await responseLibro.json();
                alert(data.message);
                return;
            }
            else throw new Error(`Error al guardar el libro: ${responseLibro.status}`);
        }

        // Obtener el ID del libro recién creado
        const { id_libro } = await responseLibro.json();
        console.log('Libro guardado con ID:', id_libro);

        // Enviar los géneros seleccionados al backend (book_genre.py)
        const responseGeneros = await addBookGenre({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_libro,
                generos: generosIds, // IDs de géneros
            }),
        });

        if (!responseGeneros.ok) {
            throw new Error(`Error al guardar los géneros: ${responseGeneros.status}`);
        }

        console.log('Géneros asociados correctamente.');

        // Enviar las etiquetas seleccionadas al backend (book_tag.py)
        const responseEtiquetas = await addBookTag ({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id_libro,
                etiquetas: etiquetasIds, // IDs de etiquetas
            }),
        });

        if (!responseEtiquetas.ok) {
            throw new Error(`Error al guardar las etiquetas: ${responseEtiquetas.status}`);
        }

        console.log('Etiquetas asociadas correctamente.');

        alert('Libro, géneros y etiquetas guardados correctamente.');
    } catch (error) {
        console.error('Ocurrió un error:', error);
        alert('Ocurrió un error al guardar los datos. Por favor, intente nuevamente.');
    }
}
</script>

<style scoped>
.addBook-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    gap: 2rem; 
    padding: 2rem;
    max-width: 100%;
    width: 100%; 
}

.section-container {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    justify-content: center;
    width: 100%;           
    max-width: 1300px;
    margin: 0 auto;   
}

.message-container {
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 100%;
    width: 100%;
    padding: 0 2rem;
    
}

.message-box {
    text-align: center;
    max-width: 800px;
    width: 100%;
    box-sizing: border-box;
    background-color: #f9f9f9; 
    border: 2px solid #444;    
    border-radius: 8px;        
    padding: 0.5rem 1rem;
}

.form-container {
    padding: 1.5rem;
    border: 2px solid #444;
    border-radius: 8px;
    background-color: #f9f9f9;
    max-width: 800px;
    width: 100%;
    box-sizing: border-box;
}

.button-container {
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 200px;
}

.button-container button {
    width: 100%;
    height: 40px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.message-info-container {
    background-color: bisque;
    max-width: 200px;   
    width: 100%; 
    box-sizing: border-box;
    border-radius: 8px; 
    padding: 1.5rem;
}
.message-info {
    background-color: bisque;
    max-width: 300px;   
    width: 100%; 
    box-sizing: border-box;
    border-radius: 8px; 
    padding: 1.5rem;
}
</style>