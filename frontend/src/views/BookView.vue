<template>
    <Navbar />
    <main>
        <div class="book-view">
            <!-- Contenedor izquierdo-->
            <div class="left-container">
                <div class ="calification-container">
                    Promedio: {{ libro?.promedio || 'Desconocido' }} 
                </div>
                <div class="card">
                    <img :src="getPortadaUrl(libro?.portada)" class="card-img-top" alt="Portada">
                </div>
                <div class="information-container" v-if="libro">
                    <h5 class="info">Titulo: {{ libro?.titulo || 'Desconocido'}} </h5>
                    <h6 class="info">Autor: {{ libro?.autor || 'Desconocido'}}</h6>
                    <h6 class="info" v-if="libro.tipo === 'manga'">Artista: {{ libro?.artista || 'Desconocido'}}</h6>
                    <!-- Calificar -->
                    <div class="rating mt-3">
                        <h6>Califica este libro:</h6>
                        <div class="input-group">
                            <select v-model="calificacion" class="form-select">
                                <option disabled value="">Selecciona una calificación</option>
                                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
                            </select>
                            <button @click="calificarLibro" class="btn ml-primary-btn">Calificar</button>
                        </div>
                    </div>
                    <div class="select-list">
                        <AddToList v-if="libro && libro.id_libro" :id-libro="libro.id_libro" />
                    </div>
                    <div class="tags"> 
                        <h6>Etiquetas:</h6>  
                        <ul v-if="etiquetas.length > 0">
                            <li v-for="etiqueta in etiquetas" :key="etiqueta">{{ etiqueta }}</li>
                        </ul>
                        <p class="p-0" v-else>No hay etiquetas disponibles</p>
                    </div>
                    <div class="books-details">
                        <ul v-if="libro.tipo.toLowerCase() === 'libro'">
                            <li class="details">
                                <h6>Tipo: {{ libro?.tipo || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Editorial: {{ libro?.editorial || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Año de publicación: {{ libro?.anio_publicacion || 'Desconocido'}}</h6>
                            </li> 
                            <li class="details">
                                <h6>Idioma: {{ libro?.idioma || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Compra: {{ libro?.link_compra || 'Desconocido'}}</h6>
                            </li>
                            <li class="details" v-if="libro.es_saga.toLowerCase() === 'si'">
                                <h6>Nombre de saga: {{ libro?.titulo_saga || 'Desconocido'}}</h6>
                            </li>
                            <li class="details" v-if="libro.es_saga.toLowerCase() === 'si'">
                                <h6>Número de libro: {{ libro?.num_libro || 'Desconocido'}}</h6>
                            </li>
                        </ul>
                        <ul v-else-if="libro.tipo.toLowerCase() === 'novel' || libro.tipo.toLowerCase() === 'manga'">
                            <li class="details" v-if="libro.tipo.toLowerCase()==='novel'">
                                <h6>Tipo: Novela web</h6>
                            </li>
                            <li class="details" v-if="libro.tipo.toLowerCase()==='manga'">
                                <h6>Tipo: Manga</h6>
                            </li>
                            <li class="details">
                                <h6>Editorial: {{ libro?.editorial || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Año de publicación: {{ libro?.anio_publicacion || 'Desconocido'}}</h6>
                            </li> 
                            <li class="details">
                                <h6>Idioma: {{ libro?.idioma || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Compra: {{ libro?.link_compra || 'Desconocido'}}</h6>
                            </li>
                            <li class="details">
                                <h6>Número de capítulos: {{ libro?.num_capitulos || 'Desconocido' }}</h6>
                            </li>
                            <li class="details">
                                <h6>Serie finalizada:{{ libro?.estado.toUpperCase() || 'Desconocido' }}</h6>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- Contenedor derecho -->
            <div class="right-container">
                <div class="book-edit">
                    <div class="info-edit">
                        <h6>Informacion edicion</h6>
                    </div>
                    <div class="button-edit">
                        <button type="button" class="btn" @click="irAEditar">✏️ Editar</button>
                    </div>
                </div>
                <hr class="linea-centro">
                <div class="book-description">
                    <h4>Sinopsis:</h4>
                    <p>{{ libro?.sinopsis || 'Desconocido' }}</p>
                    <p class="description"></p>
                </div>
                <hr class="linea-centro">
                <div class="genres">
                    <h4>Géneros</h4>
                    <ul>
                        <li v-for="genero in generos" :key="genero">{{ genero }}</li>
                    </ul>
                </div>
                <hr class="linea-centro">
                <div class ="similar-books">
                    <h4>Libros similares</h4>
                    <div class="similar-books-row">
                        <div class="similar-card" v-for="n in 5" :key="n">
                            <img src="https://demuseo.com/wp-content/uploads/woocommerce-placeholder.png" alt="Portada" class="similar-card-img">
                            <div class="similar-card-title">Libro {{ n }}</div>
                        </div>
                    </div>
                </div>
                <hr class="linea-centro">
                <div class="comments">
                    <h4>Comentarios</h4>
                    <Comments v-if="libro && libro.id_libro" :id-libro="libro.id_libro" />
                </div>
            </div>
        </div>
    </main>
    <Footer />
</template>

<script setup lang="ts">
import Comments from '@/components/comments/Comments.vue';
import AddToList from '@/components/list/AddToList.vue';
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { ref, onMounted } from 'vue';
import { getBook, getTagsIdBook, getGenresById, rateBook } from '@/api/api';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/token';
import type { Book } from '@/types/types';

// Definir variables
const etiquetas = ref<string[]>([]);
const generos = ref<string[]>([]);
const route = useRoute();
const libro = ref<Book | null>(null);
const backendUrl = 'http://127.0.0.1:3307/api/';
const router = useRouter();
const calificacion = ref<number | null>(null);
const authStore = useAuthStore();

// Obtener el ID del libro desde la ruta
const idLibro = Number(route.params.id);

function getPortadaUrl(portada: string | undefined): string {
  if (!portada) return 'https://demuseo.com/wp-content/uploads/woocommerce-placeholder.png';
  if (portada.startsWith('http')) return portada;
  // Si portada es "/uploads/archivo.jpg", concatena el backendUrl
  return backendUrl + portada;
}

function irAEditar() {
  if (libro.value && libro.value.id_libro) {
    router.push({
      name: 'bookEdit',
      params: {
        id: libro.value.id_libro
      }
    });
  }
}

// Calificar el libro
async function calificarLibro() {
    try {
        // Validar que la calificación sea un número entre 1 y 10
        if (calificacion.value === null || calificacion.value < 1 || calificacion.value > 10) {
            alert('Por favor, selecciona una calificación válida entre 1 y 10.');
            return;
        }

        // Validar que el libro tenga un ID
        if (!libro.value || !libro.value.id_libro) {
            alert('No se pudo calificar el libro. Por favor, intenta nuevamente.');
            return;
        }

        // Calificar el libro
        const res = await rateBook({
            puntaje: calificacion.value,
            id_usuario: authStore.user.id
        }, libro.value.id_libro);

        if (res.status === 200) {
            alert('Libro calificado exitosamente');
            window.location.reload();
        } else {
            alert('Error al calificar el libro. Por favor, intenta nuevamente.');
        }
    } catch (error) {
        console.error('Error al calificar el libro:', error);
        alert('Ocurrió un error al calificar el libro. Por favor, intenta nuevamente.');
    }
}

onMounted(async () => {
    try {
        // Obtener el libro
        const resLibro = await getBook(idLibro);
        if (resLibro.status !== 200) throw new Error('No se pudo obtener el libro');
        libro.value = resLibro.data;

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
        
    } catch (e) {
        console.error(e);
    }

    
});
</script>

<style scoped>
.book-view {
    display: flex;
}

.left-container {
    width: 30%;
    padding: 2rem;
    background-color: #fae8d4;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.right-container {
    width: 70%;
    padding: 2rem;
    background-color: #f0f0f0;
}

.similar-books-row {
    display: flex;
    gap: 1rem;
    justify-content: flex-start;
    flex-wrap: nowrap;
}

.similar-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    width: 16rem;
    padding: 0.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.similar-card-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 4px;
}

.similar-card-title {
    margin-top: 0.5rem;
    font-size: 1rem;
    font-weight: bold;
}

.card {
    display: flex;
    margin: 0 auto;
    width: 80%;
}

.calification-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.information-container {
    padding: 2rem;
}

.info {
    display: flex;
    justify-content: left;
    align-items: center;
}

.select-list {
    padding-block: 1rem;
}

.books-details {
    display: flex;
    justify-content: left;
    align-items: center;
}

.books-details ul {
    list-style-type: none;
    padding: 0;
}

.right-container {
    display: flex;
    flex-direction: column;
}

.book-edit{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.linea-centro {
    border-top: 2px solid #c0c0c0;
}

.book-description p{
    display: flex;
    flex-direction: column;
    text-align: justify;
}

@media (max-width: 576px) {
    .book-view {
        flex-direction: column;
    }

    .left-container, .right-container {
        width: 100%;
    }

    .information-container {
        padding: 2rem 1rem;
    }

    .similar-books-row {
        flex-wrap: wrap;
    }
}
</style>