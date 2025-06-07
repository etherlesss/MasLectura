<template>
    <Navbar />
    <main>
        <div class="book-view">
            <!-- Contenedor izquierdo-->
            <div class="left-container">
                <div class="calification-container d-flex align-items-baseline">
                    <span>Promedio: {{ libro?.promedio || 'Desconocido' }}</span>
                    <span style="font-size: .8rem;">/{{ ratingCount }} Calificaciones</span>
                </div>
                <div class="card cover">
                    <img :src="getPortadaUrl(libro?.portada)" class="cover-img-top" alt="Portada">
                </div>
                <div class="information-container" v-if="libro">
                    <h5 class="info">Titulo: {{ libro?.titulo || 'Desconocido'}} </h5>
                    <h6 class="info">Autor: {{ libro?.autor || 'Desconocido'}}</h6>
                    <h6 class="info" v-if="libro.tipo === 'manga'">Artista: {{ libro?.artista || 'Desconocido'}}</h6>
                    <!-- Calificar -->
                    <div class="rating mt-3">
                        <h6>Califica este libro:</h6>
                        <div class="input-group">
                            <select v-model="calificacion" class="form-select" :disabled="!authStore.token">
                                <option disabled :value="null">Selecciona una calificación</option>
                                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
                            </select>
                            <button @click="calificarLibro" class="btn ml-primary-btn" :disabled="!authStore.token">Calificar</button>
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
                                <h6>Serie finalizada: {{ libro?.estado.toUpperCase() || 'Desconocido' }}</h6>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- Contenedor derecho -->
            <div class="right-container">
                <div class="book-edit">
                    <div class="info-edit">
                        <h6><EditRecord
                        v-if="libro && libro.id_libro"
                        :id-libro="libro.id_libro"
                        /></h6>
                    </div>
                    <div class="button-edit" v-if="authStore.token">
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
                    <div class="card-scroll">
                        <HomeCard v-for="book in similares" :key="book.id_libro" :book="book" />
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
import EditRecord from '@/components/edit/EditRecord.vue';
import HomeCard from '@/components/cards/HomeCard.vue';
import { ref, onMounted, watch } from 'vue';
import { getBook, getTagsIdBook, getGenresById, rateBook, getSimilarBooks, getUserRating, getBookRatingCount } from '@/api/api';
import { getPortadaUrl } from '@/util/util';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/token';
import type { Book } from '@/types/types';

// Definir variables
const etiquetas = ref<string[]>([]);
const generos = ref<string[]>([]);
const route = useRoute();
const libro = ref<Book | null>(null);
const router = useRouter();
const calificacion = ref<number | null>(null);
const authStore = useAuthStore();
const similares = ref<Book[]>([]);
const ratingCount = ref<number>(0);

// Obtener el ID del libro desde la ruta
const idLibro = ref(Number(route.params.id));

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

async function loadBook() {
    try {
        // Obtener el libro
        const resLibro = await getBook(idLibro.value);
        if (resLibro.status !== 200) throw new Error('No se pudo obtener el libro');
        libro.value = resLibro.data;

        // Settear el título de la pagina como el libro obtenido
        document.title = libro.value && libro.value.titulo ? `Libro - ${libro.value.titulo}` : 'Libro';

        // Obtener cantidad de calificaciones
        const resCantidad = await getBookRatingCount(idLibro.value);
        if (resCantidad.status === 200) {
            ratingCount.value = resCantidad.data.count;
        }

        // Obtener etiquetas del libro
        const resEtiquetas = await getTagsIdBook(idLibro.value);
        if (resEtiquetas.status === 200) {
            etiquetas.value = resEtiquetas.data;
        }

        // Obtener géneros del libro
        const resGeneros = await getGenresById(idLibro.value);
        if (resGeneros.status === 200) {
            generos.value = resGeneros.data;
        }

        // Obtener libros similares
        const resSimilares = await getSimilarBooks(idLibro.value);
        if (resSimilares.status === 200) {
            // Mostrar 10 aleatorios
            const shuffled = resSimilares.data.sort(() => 0.5 - Math.random());
            similares.value = shuffled.slice(0, 10);
        }
        
        // Obtener calificacion del usuario
        calificacion.value = null;
        if (authStore.token && libro.value?.id_libro) {
            const resRating = await getUserRating(libro.value.id_libro, authStore.user.id);
            if (resRating.status === 200) {
                calificacion.value = Number(resRating.data.puntaje);
            }
        }
    } catch (err) {
        console.error('Error al cargar el libro:', err);
    }
}

onMounted(async () => {
    await loadBook();
});

watch(() => route.params.id, async newId => {
    if (newId) {
        idLibro.value = Number(newId);
        await loadBook();
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

.cover {
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

.card-scroll {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    gap: 1rem;
    padding-bottom: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #ccc #f5f5f5;
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
}
</style>