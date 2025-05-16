<template>
    <Navbar />
    <main class="p-5">
        <div>
            <h1>{{ list?.nombre_lista }}</h1>
            <p>{{ list?.descripcion }}</p>
        </div>
        <div>
            <ListBookTable :books="books" />
        </div>
    </main>
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getList, getListBooks } from '@/api/api';
import type { Book, List } from '@/types/types';
import ListBookTable from '@/components/table/ListBookTable.vue';

// Definir variables de datos
const list = ref<List | null>(null);
const books = ref<Book[]>([]);

// Obtener el ID de la lista desde la ruta
const route = useRoute();
const listID = Number(route.params.id_lista);

// Obtener los datos de la lista desde API
async function fetchList() {
    try {
        const res = await getList(listID);
        list.value = res.data;
    } catch (err) {
        console.error('Error fetching list:', err);
    }
}

// Obtener los libros de la lista desde API
async function fetchListBooks() {
    try {
        const res = await getListBooks(listID);
        books.value = res.data;
    } catch (err) {
        console.error('Error fetching list books:', err);
    }
}

onMounted(async() => {
    await fetchList();
    await fetchListBooks();
});
</script>

<style scoped>

</style>