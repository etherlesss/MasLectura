<template>
    <Navbar/>
    <div class ="book-view">
        <div class = "left-container">
            <div class ="calification-container">
                Promedio: {{ libro?.promedio || 'Desconocido' }} 
            </div>
            <div class="card">
                <img :src="getPortadaUrl(libro?.portada)" class="card-img-top" alt="Portada">
            </div>
            <div class="Information-container" v-if="libro">
                <h5 class="info">Titulo: {{ libro?.titulo || 'Desconocido'}} </h5>
                <h6 class="info">Autor: {{ libro?.autor || 'Desconocido'}}</h6>
                <h6 class="info" v-if = "libro.tipo === 'manga'">Artista: {{ libro?.artista || 'Desconocido'}}</h6>
                <div class="select-list">
                    <AddToList v-if="libro && libro.id_libro" :id-libro="libro.id_libro" />
                </div>
                <div class="tags"> 
                    <h6>Etiquetas:</h6>  
                    <ul>
                        <li v-for="etiqueta in etiquetas" :key="etiqueta">{{ etiqueta }}</li>
                    </ul>  
                </div>
                <div class ="books-details">
                    <ul v-if="libro.tipo === 'libro'">
                        <li class="details"> <h6> Tipo: {{ libro?.tipo || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Editorial: {{ libro?.editorial || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Año de publicación: {{ libro?.anio_publicacion || 'Desconocido'}}</h6></li> 
                        <li class="details"><h6>Idioma: {{ libro?.idioma || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Compra: {{ libro?.link_compra || 'Desconocido'}}</h6></li>
                        <li class="details" v-if="libro.es_saga === 'si'"><h6>Nombre de saga: {{ libro?.titulo_saga || 'Desconocido'}}</h6></li>
                        <li class="details" v-if="libro.es_saga === 'si'"><h6>Número de libro: {{ libro?.num_libro || 'Desconocido'}}</h6></li>
                    </ul>
                    <ul v-else-if="libro.tipo=== 'novel' || libro.tipo === 'manga'">
                        <li class="details" v-if="libro.tipo==='novel'"> <h6> Tipo: Novela web</h6></li>
                        <li class="details" v-if="libro.tipo==='manga'"> <h6> Tipo: Manga</h6></li>
                        <li class="details"><h6>Editorial: {{ libro?.editorial || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Año de publicación: {{ libro?.anio_publicacion || 'Desconocido'}}</h6></li> 
                        <li class="details"><h6>Idioma: {{ libro?.idioma || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Compra: {{ libro?.link_compra || 'Desconocido'}}</h6></li>
                        <li class="details"><h6>Número de capítulos: {{ libro?.num_capitulos || 'Desconocido' }}</h6></li>
                        <li class="details"><h6>Serie finalizada:{{ libro?.estado.toUpperCase() || 'Desconocido' }}</h6></li>
                    </ul>
                </div>
            </div>
        </div>
        <div class = "right-container">
            <div class= "book-edit">
                <div class="info-edit">
                    <h6>Informacion edicion</h6>
                </div>
                <div class ="button-edit">
                    <button type="button" class="btn">✏️ Editar</button>
                </div>
            </div>
            <hr class="linea-centro">
            <div class="book-description">
                <h4>Sinopsis:</h4>
                <p>{{ libro?.sinopsis || 'Desconocido' }}</p>
                <p class="description"></p>
            </div>
            <hr class="linea-centro">
            <div class ="genres">
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
            <div class ="comments">
                <h4>Comentarios</h4>
                <Comments v-if="libro && libro.id_libro" :id-libro="libro.id_libro" />
            </div>
        </div>
    </div>
    <Footer/>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { getBook } from '@/api/api';
import { useRoute } from 'vue-router';
import { getTagsIdBook } from '@/api/api';
import { getGenresById } from '@/api/api';
import Comments from '@/components/comments/Comments.vue';
import AddToList from '@/components/list/AddToList.vue';


const etiquetas = ref<string[]>([]);
const route = useRoute();
const libro = ref<any>(null);
const idLibro = 7;
const backendUrl = 'http://127.0.0.1:3307/api';
const generos = ref<string[]>([]);
//const idLibro = ref(route.params.id);

function getPortadaUrl(portada: string | undefined) {
  if (!portada) return 'https://demuseo.com/wp-content/uploads/woocommerce-placeholder.png';
  if (portada.startsWith('wwww')) return portada;
  // Si portada es "/uploads/archivo.jpg", quita el prefijo si lo deseas, o simplemente concatena

  return backendUrl + portada;
}


onMounted(async () => {
  try {
    const res = await getBook(Number(idLibro));
    if (res.status !== 200) throw new Error('No se pudo obtener el libro');
    libro.value = res.data;

    // Obtener etiquetas
    const resEtiquetas = await getTagsIdBook(Number(idLibro));
    if (resEtiquetas.status === 200) {
      etiquetas.value = resEtiquetas.data;
    }

    // Obtener géneros
    const resGeneros = await getGenresById(Number(idLibro));
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
    min-height: 600px; 
}

.left-container {
    width: 30%;
    min-height: 784px;
    background-color: #fae8d4;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.right-container {
    width: 75%;
    min-height: 784px;
}

.similar-books-row {
    display: flex;
    gap: 1rem;
    justify-content: flex-start; /* o center */
    flex-wrap: nowrap;
}

.similar-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    width: 220px; /* Ajusta el ancho según tu diseño */
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

.card{
    display: flex;
    margin: 0 auto;
    width: 80%;
    
}

.calification-container{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 15%;
}

.info{
    display: flex;
    justify-content: left;
    align-items: center;
    margin-top: 10%;
    margin-left: 10%;
}   

.select-list{
    margin-left: 10%;
    margin-right: 10%;
}

.tags{
    display: flex;
    justify-content: left;
    align-items: center;
    margin-top: 10%;
    margin-left: 10%;
}

.books-details{
    display: flex;
    justify-content: left;
    align-items: center;
    margin-top: 10%;
    margin-left: 10%;
}

.right-container{
    display: flex;
    flex-direction: column;
    margin-left: 5%;
}

.book-edit{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 5%;
    margin-right: 7%;
}
.linea-centro {
    width: auto; 
    margin-right: 7%;
    border: none;
    border-top: 2px solid #c0c0c0; /* color y grosor de la línea */
}

.books-details ul{
    list-style: none;
    padding: 0%;
}

.book-description p{
    display: flex;
    flex-direction: column;
    margin-right: 10%;
    text-align: justify;
}
</style>