<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <div class="d-flex align-items-center gap-2">
                <h1>Perfil</h1>
                <button type="button" v-if="rolUsuario && rolUsuario === 'Administrador'" class="delete-icon" @click="abrirModalBorrarUsuario">
                        🗑️
                </button>
            </div>
            <div >
                <p><b>Nombre de usuario:</b> {{ user?.nombre_usuario }} 
                    <button
                        v-if="rolUsuario === 'Administrador'"
                        class="edit-icon"
                        @click="abrirModalEditarUsuario"
                        style="margin-left: 8px;"
                        title="Editar nombre de usuario"
                        >[Editar]
                    </button>
                </p>
                <p><b>Correo electrónico:</b> {{ user?.mail_usuario }}</p>
                <p><b>Género: </b> {{ user?.genero_usuario }}</p>
                <p><b>Fecha de nacimiento:</b> {{ formatDate(user?.fecha_nacimiento || '') }}</p>
            </div>
        </div>
        <div>
            <div class="d-flex align-items-center gap-2">
                <h2>Listas</h2>
            </div>
            <ListCard :lists="lists" />
        </div>
        <div v-if="mostrarModalBorrarUsuario" class="modal-backdrop">
            <div class="modal-confirm">
                <p>¿Estás seguro de que deseas borrar este usuario? Esta acción no se puede deshacer.</p>
                <button @click="borrarUsuario" class="btn btn-danger">Sí, borrar usuario</button>
                <button @click="mostrarModalBorrarUsuario = false" class="btn btn-secondary">Cancelar</button>
            </div>
        </div>
        <div v-if="mostrarModalEditarUsuario" class="modal-backdrop">
        <div class="modal-confirm">
            <h4>Editar nombre de usuario</h4>
            <input
            v-model="nuevoNombreUsuario"
            class="form-control"
            placeholder="Nuevo nombre de usuario"
            style="margin-bottom: 1rem;"
            />
            <button @click="editarNombreUsuario" class="btn btn-primary">Guardar</button>
            <button @click="mostrarModalEditarUsuario = false" class="btn btn-secondary" style="margin-left: 1rem;">Cancelar</button>
        </div>
        </div>
    </main>
    <ChangePwdModal />
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getProfile, getUserLists, getUserRole, deleteUser, updateUserName } from '@/api/api';
import { formatDate } from '@/util/formatters';
import type { User, List } from '@/types/types';
import ListCard from '@/components/cards/ListCard.vue';
import { useAuthStore } from '@/stores/token';

// Definir variables de datos
const user = ref<User | null>(null);
const lists = ref<List[]>([]);
const rolUsuario = ref<string | null>(null);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const idUsuario = Number(route.params.id);
const mostrarModalBorrarUsuario = ref(false);
const mostrarModalEditarUsuario = ref(false);
const nuevoNombreUsuario = ref('');

// Redirección si el usuario es el mismo que el autenticado
if (idUsuario === Number(authStore.user.id)) {
  router.replace('/my-profile');
}

async function cargarRolUsuario() {
    const res = await getUserRole(authStore.user.id); 
    rolUsuario.value = res.data.rol;
}

function abrirModalBorrarUsuario() {
  mostrarModalBorrarUsuario.value = true;
}

function abrirModalEditarUsuario() {
  nuevoNombreUsuario.value = user.value?.nombre_usuario || '';
  mostrarModalEditarUsuario.value = true;
}

async function editarNombreUsuario() {
  if (!nuevoNombreUsuario.value.trim()) {
    alert('El nombre de usuario no puede estar vacío.');
    return;
  }
  try {
    // Llama a tu API para editar el nombre de usuario
    const res = await updateUserName(idUsuario, nuevoNombreUsuario.value);
    if (res && res.status === 200) {
      if (user.value) {
        user.value = {
          id_usuario: user.value.id_usuario,
          nombre_usuario: nuevoNombreUsuario.value,
          mail_usuario: user.value.mail_usuario,
          genero_usuario: user.value.genero_usuario,
          rol: user.value.rol,
          fecha_nacimiento: user.value.fecha_nacimiento
        };
      }
      mostrarModalEditarUsuario.value = false;
      alert('Nombre de usuario actualizado');
    } else {
      alert('Error al actualizar el nombre de usuario');
    }
  } catch (err) {
    alert('Error al actualizar el nombre de usuario');
  }
}

async function borrarUsuario() {
    mostrarModalBorrarUsuario.value = false;
    if (confirm('¿Estás seguro de que deseas borrar este usuario? Esta acción no se puede deshacer.')) {
        const res = await deleteUser(idUsuario);
        if (res && res.status === 200) {
            alert('Usuario eliminado correctamente');
            router.push('/');
        } else {
            alert('Error al eliminar el usuario');
        }
    }
}
async function fetchUser() {
    try {
        const userId = Number(route.params.id);
        const res = await getProfile(userId);
        user.value = res.data;
    } catch (err) {
        console.error('Error fetching user:', err);
    }
}

async function fetchUserLists() {
    try {
        const userId = Number(route.params.id);
        const res = await getUserLists(userId);
        lists.value = res.data;
    } catch (err) {
        console.error('Error fetching user lists:', err);
    }
}

onMounted(async () => {
    await fetchUser();
    await fetchUserLists();
    await cargarRolUsuario();
});

</script>

<style scoped>
p {
    margin: .5rem 0;
}

.button{
    font-size: 1.2rem; 
    transition: color 0.2s, transform 0.2s; 
    border-radius: 25%;
    border-color: rgb(0, 0, 0);
    background-color: rgba(247, 247, 247, 0.1);
}

.button:hover {
    transform: scale(1.1); 
    transition: color 0.2s, transform 0.2s; 
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

.edit-icon {
    border: none;
    background: none;
    color: #252525;
    font-size: 0.9rem;
    padding: 0;
    margin: 0;
    cursor: pointer;
    font-family: inherit;
    vertical-align: middle;
}
.edit-icon:hover {
    text-decoration: underline;
}
</style>