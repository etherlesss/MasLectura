<template>
    <Navbar />
    <main>
        <!-- Busqueda -->
        <section class="search d-flex flex-column align-items-center justify-content-center p-lg-5 p-3">
            <div>
                <h2>Buscar libros</h2>
            </div>
            <!-- Search bar -->
            <div class="search-bar mb-3">
                <form class="d-flex" role="search" @submit="onSearch" autocomplete="off">
                    <input class="form-control me-2" type="search" placeholder="Buscar lecturas..." aria-label="Search" v-model="searchQuery"/>
                    <button class="btn" type="submit">Buscar</button>
                </form>
            </div>
            <!-- Collapse -->
            <div>
                <div class="d-flex justify-content-center mb-3 mb-lg-0">
                    <button class="btn" type="button" data-bs-toggle="collapse" data-bs-target="#filters" aria-expanded="false" aria-controls="filters">
                        Expandir filtros
                    </button>
                </div>
                <div class="collapse" id="filters">
                    <form @submit.prevent="">
                        <!-- Generos -->
                        <div class="genres p-lg-5">
                            <!-- Titulo y selector-->
                            <div class="d-flex gap-2 align-items-center">
                                <b>Géneros</b>
                                <select class="form-select form-select-sm w-25" id="genres" v-model="genreMode">
                                    <option value="AND">AND</option>
                                    <option value="OR">OR</option>
                                </select>
                            </div>
                            <!-- Lista de generos -->
                            <div class="row row-cols-lg-5 row-cols-md-4 row-cols-2 p-3">
                                <div v-for="genre in genres" :key="genre.id_genero" class="form-check col">
                                    <input class="form-check-input" type="checkbox" :id="'genero-' + genre.id_genero" :value="genre.nombre" v-model="selectedGenres">
                                    <label class="form-check-label" :for="'genero-' + genre.id_genero" :title="genre.descripcion">
                                        {{ genre.nombre }}
                                    </label>
                                </div>
                            </div>
                        </div>
                        <!-- Etiquetas -->
                        <div class="tags p-lg-5">
                            <!-- Titulo y selector-->
                            <div class="d-flex gap-2 align-items-center mb-3">
                                <b>Etiquetas</b>
                                <select class="form-select form-select-sm w-25" id="genres" v-model="tagMode">
                                    <option value="AND">AND</option>
                                    <option value="OR">OR</option>
                                </select>
                            </div>
                            <!-- Lista de etiquetas -->
                            <div class="d-flex flex-column flex-lg-row gap-3">
                                <!-- Incluir -->
                                <div class="d-flex flex-column gap-2">
                                    <b>Incluir</b>
                                    <Multiselect
                                        v-model="includedTags"
                                        :options="tags"
                                        :multiple="true"
                                        :close-on-select="false"
                                        :clear-on-select="false"
                                        :preserve-search="true"
                                        placeholder="Buscar etiquetas..."
                                        label="nombre"
                                        track-by="id"
                                        :preselect-first="false"
                                    />
                                </div>
                                <!-- Excluir -->
                                <div class="d-flex flex-column gap-2 mb-3 mb-lg-0">
                                    <b>Excluir</b>
                                    <Multiselect
                                        v-model="excludedTags"
                                        :options="tags"
                                        :multiple="true"
                                        :close-on-select="false"
                                        :clear-on-select="false"
                                        :preserve-search="true"
                                        placeholder="Buscar etiquetas..."
                                        label="nombre"
                                        track-by="id"
                                        :preselect-first="false"
                                    />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </section>
        <!-- Resultados -->
        <section class="results d-flex flex-row flex-wrap justify-content-center gap-3 p-lg-5 p-3">
            <div v-if="filteredBooks.length === 0" class="d-flex flex-column align-items-center">
                <h2 class="text-center">No se encontraron resultados</h2>
                <p class="text-center">Intenta buscar algo diferente</p>
            </div>
            <div v-for="book in filteredBooks" :key="book.id_libro" v-else>
                <SearchCard :book="book" />
            </div>
        </section>
    </main>
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import SearchCard from '@/components/cards/SearchCard.vue';
import Multiselect from 'vue-multiselect';
import { ref, onMounted, computed, watch } from 'vue';
import { getBooks, getTags, getGenres, getDetailedBooks } from '@/api/api';
import { useRoute, useRouter } from 'vue-router';
import type { Book, Tag, Genre } from '@/types/types';

// Definir variables de datos
const route = useRoute();
const router = useRouter();
const searchQuery = ref<string>(route.query.q as string || '');
const books = ref<Book[]>([]);
const tags = ref<Tag[]>([]);
const genres = ref<Genre[]>([]);
const genreMode = ref<string>('AND');
const tagMode = ref<string>('AND');
const selectedGenres = ref<string[]>([]);
const includedTags = ref<Tag[]>([]);
const excludedTags = ref<Tag[]>([]);
const detailedBooks = ref<any[]>([]);

// Obtener la consulta de búsqueda desde la URL
watch (
    () => route.query.q,
    (newQuery) => {
        if (newQuery) {
            searchQuery.value = newQuery as string || '';
        }
    }
);

// Actualizar la consulta de búsqueda cuando cambie
function onSearch(e: Event) {
    e.preventDefault();
    router.replace({ query: { query: searchQuery.value } });
}

// Obtener los libros desde API
async function fetchBooks() {
    try {
        const res = await getBooks();
        if (res.status === 200) {
            books.value = res.data;
        }
    } catch (err) {
        console.error('Error fetching books:', err);
    }
}

// Obtener las etiquetas desde la API
async function fetchTags() {
    try {
        const res = await getTags();
        if (res.status === 200) {
            tags.value = res.data;
        }
    } catch (err) {
        console.error('Error fetching tags:', err);
    }
}

// Obtener los generos desde la API
async function fetchGenres() {
    try {
        const res = await getGenres();
        if (res.status === 200) {
            genres.value = res.data;
        }
    } catch (err) {
        console.error('Error fetching genres:', err);
    }
}

// Obtener los libros con generos y etiquetas
async function fetchDetailedBooks() {
    try {
        const res = await getDetailedBooks();
        if (res.status === 200) {
            detailedBooks.value = res.data;
            console.log('Detailed books fetched:', detailedBooks.value);
        }
    } catch (err) {
        console.error('Error fetching detailed books:', err);
    }
}

// Filtrar libros según la búsqueda
const filteredBooks = computed(() => {
    return books.value.filter(book => {
        // Filtrar por título o autor
        const matchesSearch =
            book.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            book.autor.toLowerCase().includes(searchQuery.value.toLowerCase());

        // Buscar el libro detallado correspondiente
        const detailedBook = detailedBooks.value.find(db => db.id_libro === book.id_libro);
        if (!detailedBook) return false;

        // Filtrar por géneros
        const bookGenres = detailedBook.generos.map((g: any) => g.nombre_genero);
        const genreMatch =
            selectedGenres.value.length === 0 ||
            (genreMode.value === 'AND'
                ? selectedGenres.value.every(genre => bookGenres.includes(genre))
                : selectedGenres.value.some(genre => bookGenres.includes(genre)));

        // Filtrar por etiquetas
        const bookTags = detailedBook.etiquetas.map((t: any) => t.nombre_etiqueta);
        const includedMatch =
            includedTags.value.length === 0 ||
            (tagMode.value === 'AND'
                ? includedTags.value.every(tag => bookTags.includes(tag.nombre))
                : includedTags.value.some(tag => bookTags.includes(tag.nombre)));

        // Excluir etiquetas
        const excludedMatch =
            excludedTags.value.length === 0 ||
            !excludedTags.value.some(tag => bookTags.includes(tag.nombre));

        return matchesSearch && genreMatch && includedMatch && excludedMatch;
    });
});

onMounted(async () => {
    await fetchBooks();
    await fetchGenres();
    await fetchTags();
    await fetchDetailedBooks();
});
</script>

<style scoped>
.search {
    background-color: #F2E5D7;
}

.search button {
    outline: 1px solid #262322;
}

.search button:hover {
    background-color: #262322;
    color: #F2E5D7;
}

#filters label {
    font-size: .871rem;
}
</style>