<template>
    <Navbar />
    <main class="p-5">
        <!-- Recomendaciones de IA-->
        <div v-if="authStore.token">
            <h2>Sólo para ti</h2>
        </div>
        <!-- Mejores calificados -->
        <div>
            <h2>Top en calificaciones</h2>
            <div class="card-scroll">
                <HomeCard v-for="book in topRating" :key="book.id_libro" :book="book" />
            </div>
        </div>
        <!-- Descubre algo nuevo (aleatorio) -->
        <div>
            <h2>Descubre algo nuevo</h2>
            <div class="card-scroll">
                <HomeCard v-for="book in discover" :key="book.id_libro" :book="book" />
            </div>
        </div>
    </main>
    <Footer />
</template>

<script setup lang="ts">
import HomeCard from '@/components/cards/HomeCard.vue';
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/token';
import { getBooks } from '@/api/api';
import type { Book } from '@/types/types';

// Definir variables de datos
const authStore = useAuthStore();
const books = ref<Book[]>([]);
const topRating = ref<Book[]>([]);
const discover = ref<Book[]>([]);

// Obtener 10 libros mejor calificados
function getTopRatedBooks(books: Book[]) {
    topRating.value = books.sort((a, b) => b.promedio - a.promedio).slice(0, 10);
}

// Obtener 10 libros aleatorios
function getRandomBooks(books: Book[]) {
    const shuffled = books.sort(() => 0.5 - Math.random());
    discover.value = shuffled.slice(0, 10);
}


// Obtener los libros desde la API
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

// Ejecutar funciones al montar el componente
onMounted(async() => {
    await fetchBooks();
    getTopRatedBooks(books.value);
    getRandomBooks(books.value);
});
</script>

<style scoped>
.card-scroll {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    gap: 1rem;
    padding-bottom: 1rem;
    scrollbar-width: thin;
    scrollbar-color: #ccc #f5f5f5;
}
</style>