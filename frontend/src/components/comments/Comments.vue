<template>
    <div class="body-comments">
        <p>¡Bienvenido a la sección de comentarios! ¡Aquí puedes dejar tus opiniones y comentarios sobre el libro!</p>
        <div class="comments-section">
            <div class="comment-form pb-3">
                <h6>Deja tu comentario:</h6>
                <textarea class="form-control" rows="3" placeholder="Escribe tu comentario aquí..." v-model="comentario" :disabled="idUsuario === null"></textarea>
                <button type="button" class="btn ml-primary-btn mt-2" @click="enviarComentario" :disabled="idUsuario === null">Enviar</button>
            </div>
            <div v-for="(c, i) in comentariosLibro" :key="i" class="comment">
                <div class="d-flex align-items-center justify-content-between">
                    <router-link
                  class="user-link"
                  :to="{ name: 'user-profile', params: { id: c.id_usuario } }"
                  style="cursor:pointer"
                >
                  {{ c.nombre_usuario }}
                </router-link>
                    <br>
                    <button type="button" v-if="rolUsuario === 'Administrador'" class="delete-icon" @click="abrirModalBorrar(c)">
                        🗑️
                    </button>
                </div>
                <p>{{ c.descripcion }}</p>
            </div>
            <div v-if="mostrarModal" class="modal-backdrop">
                <div class="modal-confirm">
                    <p>¿Estás seguro de que deseas borrar este comentario?</p>
                    <div class="modal-footer d-flex gap-2">
                        <button @click="confirmarBorrado" class="btn btn-danger">Sí, borrar</button>
                        <button @click="mostrarModal = false" class="btn btn-secondary">Cancelar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, onMounted, watch } from 'vue';
import { addComment, getCommentsByBook, deleteComment, getUserRole, getProfile } from '@/api/api';

const userRaw = localStorage.getItem('user');
const idUsuario = userRaw ? JSON.parse(userRaw).id : null;
const props = defineProps<{ idLibro: number}>();
const comentario = ref('');
const comentariosLibro = ref<{nombre_usuario: string, descripcion: string, id_usuario: number, id_comentario?: number }[]>([]);
const rolUsuario = ref<string | null>(null);
const mostrarModal = ref(false);
const comentarioABorrar = ref<any>(null);


async function cargarRolUsuario() {
    if (idUsuario) {
        const res = await getUserRole(idUsuario);
        if (res && res.status === 200) {
            rolUsuario.value = res.data.rol;
        }
    }
}

async function cargarComentarios() {
    const res = await getCommentsByBook(props.idLibro);
    if (res && res.status === 200) {
        comentariosLibro.value = res.data;
    }
}
async function enviarComentario() {
    if (!comentario.value.trim()) {
        alert('Por favor, escribe un comentario antes de enviar.');
        return;
    }
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

function abrirModalBorrar(comentario: any) {
    comentarioABorrar.value = comentario;
    mostrarModal.value = true;
}

async function confirmarBorrado() {
    if (comentarioABorrar.value) {
        const res = await deleteComment(comentarioABorrar.value.id_comentario);
        if (res && res.status === 200) {
            await cargarComentarios();
        } else {
            alert('No se pudo borrar el comentario');
        }
    }
    mostrarModal.value = false;
    comentarioABorrar.value = null;
}



onMounted(async () => {
    await cargarRolUsuario();
    await cargarComentarios();
});
</script>

<style scoped>

.comment {
    background: rgba(110, 108, 108, 0.08); /* semitransparente */
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}



.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-confirm {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  min-width: 300px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.delete-icon{
    font-size: 1.2rem; 
    transition: color 0.2s, transform 0.2s; 
    border-radius: 25%;
    border-color: rgb(0, 0, 0);
    background-color: rgba(247, 247, 247, 0.1);
}

.delete-icon:hover {
    transform: scale(1.1); 
    transition: color 0.2s, transform 0.2s; 
}

.user-link {
  color: #000000;
  cursor: pointer;
}
.user-link:hover {
  color: #8a8b8b;
  text-decoration: underline;
}
</style>