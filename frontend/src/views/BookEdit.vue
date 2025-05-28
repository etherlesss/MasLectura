<template>
    <Navbar />
    <main>
        <div class="addBook-container d-flex flex-column align-items-center gap-2 p-lg-5 pb-3">
            <div class=" instructions">
                <h4 class = 'center'>Editar lectura</h4>
            <h6 >
                <p>En esta sección es posible editar los datos de las lecturas. Por favor, 
                    ser consciente de que los cambios realizados
                    serán visibles para todos los usuarios de la plataforma.
                    Asegúrate de que la información es correcta y está actualizada.
                    <br>
                    
                    Para editar una lectura, es necesario completar los siguientes pasos:
                    <br>   
                    <br>
                    1. Editar los datos principales de la lectura (título, autor, etc.).
                    <br>    
                    2. Editar los géneros y etiquetas de la lectura.
                    <br>
                    3. Guardar los cambios realizados.
                    <br>
                    <br>
                    Una vez que se guarden los cambios, la lectura se actualizará en la plataforma.
                    Guardar todos los cambios en los datos principales, géneros y etiquetas solo será posibles 
                    una vez que se hayan confirmado los cambios en cada sección.
                    <br>
                </p>
            </h6>
            </div>
            <!-- Formulario de datos principales -->
            <div class="top form-container mb-4">
                <h6>Editar información de la lectura</h6>
                <SecondFormBook
                  v-if="tipoSeleccionado === 'Libro'"
                  :initialData="secondFormData"
                  :ocultar="true"
                  @guardar="guardarSecondForm"
                />
                <SecondFormNovel
                  v-if="tipoSeleccionado === 'Novela'"
                  :initialData="secondFormData"
                  :ocultar="true"
                  @guardar="guardarSecondForm"
                />
                <SecondFormManga
                  v-if="tipoSeleccionado === 'Manga'"
                  :initialData="secondFormData"
                  :ocultar="true"
                  @guardar="guardarSecondForm"
                />
            </div>
            <!-- Formulario de géneros y etiquetas -->
            <div class="bottom form-container mb-4">
                <h6>Editar géneros y etiquetas de la lectura</h6>
                <ThirdForm
                  :idLibro="idLibro"
                  :ocultar="true"
                  @guardar="guardarThirdForm"
                />
            </div>
            <!-- Botón final -->
            <div class=save-button>
                <button class="btn ml-primary-btn mt-2 " @click="enviarTodo"
                :disabled="!puedeGuardarTodo">
                    Guardar todo
                </button>
            </div>
            <!-- Modal de confirmación -->
            <div v-if="mostrarModal" class="modal-backdrop">
              <div class="modal-confirm">
                <p>¿Estás seguro de que deseas guardar los cambios?</p>
                <button @click="confirmarGuardar" class="btn btn-primary">Sí, guardar</button>
                <button @click="mostrarModal = false" class="btn btn-secondary">Cancelar</button>
              </div>
            </div>
        </div>
    </main>
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import FirstForm from '@/components/book_forms/FirstForm.vue';
import SecondFormBook from '@/components/book_forms/SecondFormBook.vue';
import SecondFormNovel from '@/components/book_forms/SecondFormNovel.vue';
import SecondFormManga from '@/components/book_forms/SecondFormManga.vue';
import ThirdForm from '@/components/book_forms/ThirdForm.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/token';
import { ref, onMounted, computed} from 'vue';
import { getBook, getGenresById, getTagsIdBook, updateBook, updateBookGenres,updateBookTags } from '@/api/api';


// Recibe los datos enviados desde BookView
const route = useRoute();
const idLibro = Number(route.params.id);

const tipoSeleccionado = ref('');
const firstFormData = ref<Record<string, any>>({});
const secondFormData = ref<Record<string, any>>({});
const thirdFormData = ref<Record<string, any>>({});
const libro = ref<Record<string, any>>({});
const etiquetas = ref<any[]>([]);
const generos = ref<any[]>([]);

const mostrarModal = ref(false);

onMounted(async () => {
    try {
        // Obtener el libro
        const resLibro = await getBook(idLibro);
        if (resLibro.status !== 200) throw new Error('No se pudo obtener el libro');
        libro.value = resLibro.data;

        // Asignar tipoSeleccionado y datos iniciales
        tipoSeleccionado.value = libro.value.tipo || '';
        secondFormData.value = { ...libro.value };

        // Obtener etiquetas del libro
        const resEtiquetas = await getTagsIdBook(idLibro);
        if (resEtiquetas.status === 200) {
            etiquetas.value = resEtiquetas.data;
        }

        // Obtener géneros del libro
        const resGeneros = await getGenresById(idLibro);
        if (resGeneros.status === 200) {
            generos.value = resGeneros.data;
        }

         console.log('Datos del libro:', libro.value)
    } catch (e) {
        console.error(e);
    }
});
const seccionGuardada = ref({
  datosPrincipales: false,
  categorias: false,
});
function guardarSecondForm(data: Record<string, any>) {
    secondFormData.value = data;
    seccionGuardada.value.datosPrincipales = true;
    
}
function guardarThirdForm(data: Record<string, any>) {
    thirdFormData.value = data;
    seccionGuardada.value.categorias = true;
    console.log('Datos recibidos de ThirdForm:', data);
}

// Computed para habilitar/deshabilitar el botón
const puedeGuardarTodo = computed(() =>
  seccionGuardada.value.datosPrincipales && seccionGuardada.value.categorias
);

function enviarTodo() {
    mostrarModal.value = true;
}


async function confirmarGuardar() {
  mostrarModal.value = false;
  try {

    // 1. Actualizar libro
    const responseLibro = await updateBook(idLibro, {
      ...secondFormData.value,
    });
    console.log('Datos del libro a actualizar:', secondFormData.value);
    if (responseLibro.status !== 200) throw new Error('Error al actualizar el libro');

    // 2. Actualizar géneros
    await updateBookGenres(idLibro, {
      generos: thirdFormData.value.generosSeleccionados,
    });
    console.log('Etiquetas a guardar', generos.value);
    // 3. Actualizar etiquetas
    await updateBookTags(idLibro, {
      etiquetas: thirdFormData.value.etiquetasSeleccionadas,
    });
    console.log('Etiquetas a guardar', etiquetas.value);
    alert('¡Cambios guardados correctamente!');
  } catch (e) {
    alert('Ocurrió un error al guardar los cambios.');
    console.error(e);
  }
}

</script>

<style scoped>

.addBook-container {
    max-width: 1200px;
    margin: 0 auto;
}

.form-container {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-confirm {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  min-width: 300px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.instructions h4{
    text-align: center;
    margin-bottom: 1rem;
}

.instructions h6 {
    text-align: justify;
    margin-bottom: 1rem;
}


</style>
