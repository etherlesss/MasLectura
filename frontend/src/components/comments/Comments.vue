<template>
    <div class="body-comments">
        <p>¡Bienvenido a la sección de comentarios! ¡Aquí puedes dejar tus opiniones y comentarios sobre el libro!</p>
        <div class="comments-section">
            <div class="comment-form pb-3">
                <h6>Deja tu comentario:</h6>
                <textarea class="form-control" rows="3" placeholder="Escribe tu comentario aquí..." v-model="comentario"></textarea>
                <button type="button" class="btn ml-primary-btn mt-2" @click="enviarComentario">Enviar</button>
            </div>
            <div v-for="(c, i) in comentariosLibro" :key="i" class="comment">
                <strong>{{ c.nombre_usuario }}</strong>
                <p>{{ c.descripcion }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted, watch } from 'vue';
import { addComment, getCommentsByBook } from '@/api/api';

const userRaw = localStorage.getItem('user');
const idUsuario = userRaw ? JSON.parse(userRaw).id : null;
const props = defineProps<{ idLibro: number}>();
console.log('props:', props);
const comentario = ref('');
const comentariosLibro = ref<{nombre_usuario: string, descripcion: string }[]>([]);

async function cargarComentarios() {
    const res = await getCommentsByBook(props.idLibro);
    if (res && res.status === 200) {
        comentariosLibro.value = res.data;
    }
}
async function enviarComentario() {
    if (!comentario.value.trim()) return;
    console.log({
        id_libro: props.idLibro,
        id_usuario: idUsuario,
        descripcion: comentario.value
    });
    await addComment({ id_libro: props.idLibro, id_usuario: idUsuario, descripcion: comentario.value });
    comentario.value = '';
    console.log('Comentario enviado');
    watch(comentario, (nuevoValor) => {
    console.log('comentario.value:', nuevoValor);
    });
    await cargarComentarios();
}

onMounted(cargarComentarios);
</script>

<style scoped>

</style>