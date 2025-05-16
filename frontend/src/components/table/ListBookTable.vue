<template>
    <div class="book-table">
        <table class="table table-responsive">
            <thead>
                <tr>
                    <th scope="col">Portada</th>
                    <th scope="col">Título</th>
                    <th scope="col">Autor</th>
                    <th scope="col">Agregado</th>
                    <th scope="col">Quitar</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="props.books.length === 0">
                    <td colspan="5" class="text-center" style="opacity: .5;">No hay libros en esta lista.</td>
                </tr>
                <tr v-else v-for="book in props.books" :key="book.id_libro" class="align-middle">
                    <td>
                        <img :src="book.portada" alt="Portada del libro" class="img-fluid" />
                    </td>
                    <td>
                        {{ book.titulo }}
                    </td>
                    <td>
                        {{ book.autor }}
                    </td>
                    <td>
                        {{ formatDateText(book.fecha) }}
                    </td>
                    <td>
                        <i class="bi bi-x-lg"></i>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { formatDateText } from '@/util/formatters';
import type { Book } from '@/types/types';

// Definir props
const props = defineProps<{ books: Book[] }>();
</script>

<style scoped>
td img {
    height: 6rem;
    object-fit: contain;
    aspect-ratio: 1/1.6;
}
</style>