<template>
    <Navbar />
    <main>
        <!-- Busqueda -->
        <section class="search d-flex flex-column align-items-center justify-content-center p-lg-5 p-3">
            <div>
                <h2>Buscar libros</h2>
            </div>
            <div class="search-bar mb-3">
                <form class="d-flex" role="search" @submit="onSearch" autocomplete="off">
                    <input class="form-control me-2" type="search" placeholder="Buscar lecturas..." aria-label="Search" v-model="searchQuery"/>
                    <button class="btn" type="submit">Buscar</button>
                </form>
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
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import SearchCard from '@/components/cards/SearchCard.vue';
import { ref, onMounted, computed, watch } from 'vue';
import { getBooks } from '@/api/api';
import { useRoute, useRouter } from 'vue-router';
import type { Book } from '@/types/types';

// Definir variables de datos
const route = useRoute();
const router = useRouter();
const searchQuery = ref<string>(route.query.q as string || '');
const books = ref<Book[]>([]);

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

// Filtrar libros según la búsqueda
const filteredBooks = computed(() => {
    if (!searchQuery.value) {
        return books.value;
    }
    return books.value.filter(book => {
        return book.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
               book.autor.toLowerCase().includes(searchQuery.value.toLowerCase());
    });
});

onMounted(async () => {
    await fetchBooks();
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
</style>