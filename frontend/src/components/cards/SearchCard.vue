<template>
    <div class="card">
        <img :src="getPortadaUrl(props.book.portada)" class="card-img-top pt-3 pi-3" :alt="props.book.titulo" />
        <div class="card-body">
            <router-link :to="'/book/'+props.book.id_libro" class="subtle-link-styled">
                <h5 class="card-title">{{ props.book.titulo }}</h5>
            </router-link>
            <p class="m-0">{{ props.book.autor }}</p>
            <p class="m-0">{{ 'Calificación: ' + props.book.promedio + '/10' }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Book } from '@/types/types';
import { getPortadaUrl } from '@/util/util';

// Definir props
const props = defineProps<{ book: Book }>();
</script>

<style scoped>
.card {
    width: 16rem;
    height: 22rem;
    flex: 0 0 auto;
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

.card h5 {
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    max-height: 4.5em;
}

@media (max-width: 576px) {
    .card {
        width: 10rem;
        height: 16rem;
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

    .card h5 {
        font-size: 1rem;
    }
}
</style>