<template>
  <div class="select-list">
  <label for="inputList" class="form-label mb-1">Añadir a lista:</label>
  <select v-model="listaSeleccionada" id="inputLista" class="form-select" @change="onListaSeleccionada" :disabled="idUsuario === null || listasUsuario.length === 0">
    <option disabled value="">Selecciona una lista</option>
    <option v-for="lista in listasUsuario" :key="lista.id_lista" :value="lista.id_lista">
      {{ lista.nombre_lista }}
    </option>
  </select>
</div>

<!-- Modal de confirmación -->
<div v-if="mostrarModal" class="modal-mask">
  <div class="modal-wrapper">
    <div class="modal-container">
      <h5>¿Estás seguro de añadir este libro a la lista?</h5>
      <p>Lista: <strong>{{ nombreListaSeleccionada }}</strong></p>
      <div class="modal-footer d-flex gap-2">
        <button class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
        <button class="btn btn-success" @click="guardarLibroEnLista">Guardar</button>
      </div>
    </div>
  </div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getUserLists, addBookToList } from '@/api/api';

const props = defineProps<{ idLibro: number }>();

const userRaw = localStorage.getItem('user');
const idUsuario = userRaw ? JSON.parse(userRaw).id : null;

const listasUsuario = ref<{ id_lista: number, nombre_lista: string }[]>([]);
const listaSeleccionada = ref('');
const mostrarModal = ref(false);
const nombreListaSeleccionada = ref('');

async function cargarListas() {
  if (!idUsuario) return;
  const res = await getUserLists(idUsuario);
  if (res && res.status === 200) {
    listasUsuario.value = res.data;
  }
}

function onListaSeleccionada() {
  const lista = listasUsuario.value.find(l => l.id_lista === Number(listaSeleccionada.value));
  nombreListaSeleccionada.value = lista ? lista.nombre_lista : '';
  mostrarModal.value = true;
}

function cerrarModal() {
  mostrarModal.value = false;
  listaSeleccionada.value = '';
}

async function guardarLibroEnLista() {
  await addBookToList({ id_lista: Number(listaSeleccionada.value), id_libro: props.idLibro });
  mostrarModal.value = false;
  alert('¡Libro guardado en la lista!');
}

onMounted(cargarListas);
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, .5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-wrapper {
  box-shadow: 0 2px 8px rgba(0,0,0,0.33);
}
.modal-container {
  background: white;
  padding: 20px 30px;
  border-radius: 8px;
  min-width: 300px;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}
</style>
