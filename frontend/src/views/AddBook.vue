<template>
    <Navbar />
    <main>
        <div class="addBook-container d-flex flex-column align-items-center gap-2 p-lg-5 pb-3">
            <!-- Sección 1: Tipo de lectura -->
            <div class="section-container">
                <div class="button-container">
                    <button @click="toggleSeccion('tipoLectura')">Tipo de Lectura</button>
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
                    <p> 
                        Existen diferentes tipos de lecturas disponibles en esta página.
                         <br>
                            <br>
                    </p>
                    <div class="message-info" v-show="secciones.tipoLectura">
                        <p>
                            <b>Libros</b> son lecturas que pueden ser de cualquier género y son el formato más común.
                            Libros como Harry Potter y El Señor de los Anillos caen en esta categoría.
                            <br>
                            <br>
                            <b>Novelas asiaticas</b> son lecturas que provienen de Asia, como novelas ligeras y novelas web.
                            Poseen un formato de capítulos, los cuales son publicados periódicamente en línea o de forma física.
                            Novelas como Re:Zero, Sword Art Online y Solo Leveling son ejemplos de novelas asiaticas.
                            <br>
                            <br>
                            <b>Manga</b> son lecturas que provienen de Japón y son un formato de cómic japonés.
                            Los mangas son publicados en formato de capítulos y volumenes, los cuales son publicados periódicamente en línea o de forma física.
                            Mangas como One Piece, Naruto y Attack on Titan son ejemplos de mangas.
                            <br>
                            <br>
                            Por favor, seleccione el tipo de lectura que desea agregar y 
                            verifique que la información es correcta ya que <b>esta información no
                            podrá ser editada una vez que el libro haya sido guardado en nuestra página.</b>
                            <br>
                            <br>
                            Una vez que se haya seleccionado el tipo de lectura,
                            se habilitarán las siguientes secciones para ingresar los datos del libro.
                        </p>
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
                        <SecondFormBook v-if="tipoSeleccionado === 'Libro'" :ocultar="false"@guardar="guardarSecondForm" />
                        <SecondFormNovel v-if="tipoSeleccionado === 'Novela'" :ocultar="false" @guardar="guardarSecondForm" />
                        <SecondFormManga v-if="tipoSeleccionado === 'Manga'"  :ocultar="false"@guardar="guardarSecondForm" />
                    </div>
                </div>
                <div class ="message-info-container">
                    <p> 
                        Datos del libro como título y autor se deben ingresar en esta sección.
                         <br>
                            <br>
                    </p>
                    <div class="message-info" v-show="secciones.ingresarDatos">
                        <p>Ciertos datos son necesarios al momento de agregar un libro.
                            Por favor, asegurarse que <b>Título, Autor, Idioma, Sinopsis, Portada,
                            Artista (si es un manga)</b> esten correctamente ingresados para que 
                            el libro pueda ser agregado.
                            <br>
                            <br>
                            Los campos que no son obligatorios pueden ser dejados en blanco si no se tiene
                            la información disponible, los cuales podrán ser editados posteriormente
                            desde la vista del libro.
                            <br>
                            <br>
                            Una vez que se hayan ingresado los datos del libro, se habilitará la siguiente sección
                            para seleccionar los géneros y etiquetas del libro.
                        </p>
                    </div>
                </div>
            </div>
            <!-- Sección 3: Seleccionar categorías -->
            <div class="section-container">
                <div class="button-container">
                    <button type="button" aria-label="Seleccionar categorías" @click="toggleSeccion('seleccionarCategorias')" :disabled="!secciones.ingresarDatosGuardado">
                        Seleccionar categorías
                    </button>
                </div>
                <div class="message-container">
                    <div class="message-box" v-if="!secciones.seleccionarCategorias">
                        <h6>Seleccionar género y etiquetas</h6>
                    </div>
                    <div class="form-container" v-show="secciones.seleccionarCategorias">
                        <ThirdForm @guardar="guardarThirdForm" />
                    </div>
                </div>
                <div class ="message-info-container">
                    <p> 
                        Géneros y etiquetas son importantes para categorizar el libro y 
                        facilitar su búsqueda en la plataforma.
                         <br>
                        <br>
                    </p>
                    <div class="message-info" v-show="secciones.seleccionarCategorias">
                        <p> Etiquetas son una forma de entregar información adicional sobre la lectura
                            sin dar datos específicos de esta. <b>Facilita el poder escoger una lectura que se ajuste a los gustos del usuario
                            y alertar sobre temas que pueden ser sensibles para el lector.</b>
                            <br>
                            <br>
                            Por favor, seleccione los géneros y etiquetas que mejor describan 
                            el libro y <b>se puede seleccionar múltiples de ellos.</b>
                            <br>
                            <br>
                            En caso de no saber de que se trata alguno de ellos, <b>mantener el 
                            cursor sobre el nombre del género o etiqueta
                            mostrará una breve descripción.</b>
                            <br>
                            <br>
                            Y si no se encuentra el género o etiqueta deseada, 
                            no se preocupe, constamente estamos agregando nuevos géneros y etiquetas a la plataforma
                            para facilitar la búsqueda de nuevas lecturas a nuestros usuarios.
                            Recordar que es posible editar la información de las lecturas una vez que estas hayan sido guardadas.
                            
                        </p>
                    </div>
                </div>
            </div>
            <!-- Botón final -->
            <div class="save-button">
                <button class = "btn ml-primary-btn mt-2 "@click="enviarTodo" :disabled="!secciones.seleccionarCategoriasGuardado">
                    Guardar todo
                </button>
            </div>
        </div>
    </main>
    <Footer />
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
import router from '@/router';

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
    const todosGeneros = await resGeneros.data;
    const resEtiquetas = await getTags();
    const todasEtiquetas = await resEtiquetas.data

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
                ...firstFormData.value,
                ...secondFormData.value,
            });

        if (responseLibro.status !== 201) {
            if (responseLibro.status === 409) {
                alert(responseLibro.data.message);
                return;
            } else {
                throw new Error(`Error al guardar el libro: ${responseLibro.status}`);
            }
        }

        // Obtener el ID del libro recién creado
        const id_libro = responseLibro.data.id_libro;
        console.log('Libro guardado con ID:', id_libro);

        // Enviar los géneros seleccionados al backend (book_genre.py)
        const responseGeneros = await addBookGenre({
            id_libro,
            generos: generosIds,
        });

       if (responseGeneros.status !== 201 && responseGeneros.status !== 200) {
            throw new Error(`Error al guardar los géneros: ${responseGeneros.status}`);
        }

        console.log('Géneros asociados correctamente.');

        // Enviar las etiquetas seleccionadas al backend (book_tag.py)
        const responseEtiquetas = await addBookTag ({
            id_libro,
            etiquetas: etiquetasIds,
        });

         if (responseEtiquetas.status !== 201 && responseEtiquetas.status !== 200) {
            throw new Error(`Error al guardar las etiquetas: ${responseEtiquetas.status}`);
        }
        console.log('Etiquetas asociadas correctamente.');

        alert('Libro, géneros y etiquetas guardados correctamente.');
        router.push({ name: 'home' }); // Redirige a Home
    } catch (error) {
        console.error('Ocurrió un error:', error);
        alert('Ocurrió un error al guardar los datos. Por favor, intente nuevamente.');
    }
}
</script>

<style scoped>
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
    text-align: justify;
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
    font-size: 14px;
    text-align: justify;
}

.message-info-container p {
    margin: 0;
}

@media (max-width: 576px) {
    .section-container {
        flex-direction: column;
        align-items: center;
        padding-block: 1rem;
        gap: 1rem;
    }

    .message-container {
        padding: 0 1rem;
    }
}
</style>