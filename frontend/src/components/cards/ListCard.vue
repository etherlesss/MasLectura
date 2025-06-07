<template>
    <div class="card-scroll">
        <div v-for="list in props.lists" class="card">
            <img :src="images[list.id_lista]" class="card-img-top pt-3 pi-3" alt="{{ list.nombre_lista }}" />
            <div class="card-body">
                <router-link :to="'/my-lists/'+list.id_lista" class="subtle-link-styled">
                    <h5 class="card-title">{{ list.nombre_lista }}</h5>
                </router-link>
                <p class="card-text">{{ list.descripcion }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { getListFirstBook } from '@/api/api';
import type { List } from '@/types/types';
import { getPortadaUrl } from '@/util/util';

// Definir props
const props = defineProps<{ lists: List[] }>();

// Mapea id_lista a la URL de la imagen
const images = ref<{ [key: number]: string }>({});

async function fetchListFirstBook(id_lista: number) {
    try {
        const res = await getListFirstBook(id_lista);
        return getPortadaUrl(res.data.portada);
    } catch (err) {
        console.error('Error fetching first book:', err);
        return 'https://demuseo.com/wp-content/uploads/woocommerce-placeholder.png';
    }
}

// Cargar imágenes al montar o cuando cambian las listas
async function loadImages() {
    // Limpiar el objeto de imágenes
    images.value = {};
    // Obtener la primera imagen de cada lista y almacenarla
    for (const list of props.lists) {
        images.value[list.id_lista] = await fetchListFirstBook(list.id_lista);
    }
}

// Ejecutar función al montar el componente
onMounted(loadImages);

// Observa cambios en las listas y vuelve a cargar imágenes
watch(() => props.lists, loadImages, { immediate: true });
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

.card img {
    height: 14rem;
    object-fit: contain;
    aspect-ratio: 1/1.6;
}

.card p {
    font-size: .871rem;
    line-height: 135%;
}

.card {
    width: 16rem;
    height: 22rem;
    flex: 0 0 auto;
}

.card-text {
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    max-height: 4.5em;
}

@media (max-width: 576px) {
    .card {
        width: 10rem;
        height: 14rem;
    }

    .card img {
        height: 8rem;
    }

    .card p {
        font-size: .75rem;
        line-height: 120%;
    }

    .card-text {
        -webkit-line-clamp: 2;
        line-clamp: 2;
        max-height: 3.5em;
    }
}
</style>