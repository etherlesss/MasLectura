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
                    <div class="d-flex align-items-center">
                        <img
                            v-if="c.foto_perfil"
                            :src="getProfilePicUrl(c.foto_perfil)"
                            alt="Foto de perfil"
                            class="comment-profile-pic me-2"/>
                        <router-link
                            class="user-link"
                            :to="{ name: 'user-profile', params: { id: c.id_usuario } }"
                            style="cursor:pointer">
                            {{ c.nombre_usuario }}
                        </router-link>
                        <span v-if="c.fecha" class="comment-date ms-2">{{ formatDate(c.fecha) }}</span>
                    </div>
                    <button type="button" v-if="rolUsuario === 'Administrador'" class="delete-icon btn" @click="abrirModalBorrar(c)">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
                <p class="comment-description">{{ c.descripcion }}</p>
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
import { addComment, getCommentsByBook, deleteComment, getUserRole, API_URL } from '@/api/api';

const userRaw = localStorage.getItem('user');
const idUsuario = userRaw ? JSON.parse(userRaw).id : null;
const props = defineProps<{ idLibro: number}>();
const comentario = ref('');
const comentariosLibro = ref<{nombre_usuario: string, descripcion: string, id_usuario: number, id_comentario?: number, fecha?: string, foto_perfil?: string }[]>([]);
const rolUsuario = ref<string | null>(null);
const mostrarModal = ref(false);
const comentarioABorrar = ref<any>(null);
const defaultProfilePic = 'https://ui-avatars.com/api/?name=Usuario&background=cccccc&color=555555&size=256';

async function cargarRolUsuario() {
    if (idUsuario) {
        const res = await getUserRole(idUsuario);
        if (res && res.status === 200) {
            rolUsuario.value = res.data.rol;
        }
    }
}

function getProfilePicUrl(foto_perfil?: string) {
    if (foto_perfil) {
        if (foto_perfil.startsWith('http')) return foto_perfil;
        return API_URL + foto_perfil;
    }
    return defaultProfilePic;
}

function formatDate(fecha: string) {
    if (!fecha) return '';
    const d = new Date(fecha);
    return d.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' });
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

.comment-date {
    font-size: 0.85rem;
    color: #4b4949;
    margin-left: 0.5rem;
}

.user-link {
  color: #000000;
  cursor: pointer;
}

.user-link:hover {
  color: #8a8b8b;
  text-decoration: underline;
}

.comment-profile-pic {
    width: 2.5rem;
    height: 2.5rem;
    object-fit: cover;
    border-radius: 50%; 
    margin-right: 0.75rem; 
    border: 1px solid #5f5d5d;
}

.comment-description {
    margin-top: 1rem;
}
</style>