<template>
    <Navbar />
    <main class="p-3 p-lg-5">
        <div>
            <div class="d-flex align-items-center gap-2">
                <h1>{{ list?.nombre_lista }}</h1>
                <div v-if="list && list.nombre_lista !== 'Leído' && list.nombre_lista !== 'Quiero leer' && list.nombre_lista !== 'Leyendo'" class="d-flex align-items-center gap-2">
                    <EditListModal :list="list" />
                    <a href="#" class="subtle-link-styled" @click="removeList(list?.id_lista)">[Eliminar]</a>
                </div>
            </div>
            <p>{{ list?.descripcion }}</p>
        </div>
        <div>
            <ListBookTable :books="books" :listID="listID" />
        </div>
    </main>
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { deleteList, getList, getListBooks } from '@/api/api';
import type { Book, List } from '@/types/types';
import ListBookTable from '@/components/table/ListBookTable.vue';
import EditListModal from '@/components/modal/EditListModal.vue';

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
        if (res.status === 200) {
            books.value = res.data;
        }
    } catch (err) {
        console.error('Error fetching list books:', err);
    }
}

// Eliminar la lista
async function removeList(listID: number) {
    try {
        const res = await deleteList(listID);
        if (res.status !== 200) {
            alert('Ocurrió un error al eliminar la lista.');
        }
        window.location.href = '/my-profile';
    } catch (err) {
        console.error('Error removing list:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(async() => {
    await fetchList();
    await fetchListBooks();
    
    // Settear el título de la pagina como la lista obtenida
    document.title = `Lista - ${list.value?.nombre_lista}` || 'Lista';
});
</script>

<style scoped>

</style>