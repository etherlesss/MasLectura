<template>
    <div class="edit-record-container">
        <template v-if="rolUsuario === 'Administrador' && historial.length > 0">
            <button class="btn ml-primary-btn mt-2" @click="abrirModal">Ver historial de ediciones</button>
            <div v-if="mostrarModal" class="modal-backdrop">
                <div class="modal-confirm">
                    <h4>Historial de ediciones</h4>
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Hora</th>
                                <th>Usuario</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(ed, idx) in historial" :key="idx">
                                <td>{{ formatDate(ed.tiempo) }}</td>
                                <td>{{ formatTime(ed.tiempo) }}</td>
                                <td>{{ ed.nombre_usuario }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <button class="btn btn-secondary" @click="cerrarModal">Cerrar</button>
                </div>
            </div>
        </template>
        <template v-else>
            <span v-if="ultimaEdicion">
                Última edición: {{ formatDate(ultimaEdicion.tiempo) }}
                <template v-if="ultimaEdicion.nombre_usuario"> por <b>{{ ultimaEdicion.nombre_usuario }}</b></template>
            </span>
            <span v-else>
                Sin ediciones registradas
            </span>
        </template>
    </div>
</template>

<script setup lang="ts">
import { defineProps, onMounted, ref } from 'vue';
import { getEditHistory, getUserRole } from '@/api/api';
import { useAuthStore } from '@/stores/token';

const authStore = useAuthStore();
const idUsuario = authStore.user.id;
const rolUsuario = ref<string | null>(null);
const props = defineProps<{
    idLibro: number;
}>();

async function cargarRolUsuario() {
    
}
const historial = ref<{ tiempo: string, nombre_usuario: string }[]>([]);
const mostrarModal = ref(false);
const ultimaEdicion = ref<{ tiempo: string, nombre_usuario: string } | null>(null);

function formatDate(datetime: string) {
    const date = new Date(datetime);
    return date.toLocaleDateString('es-CL', { day: '2-digit', month: '2-digit', year: 'numeric' });
}
function formatTime(datetime: string) {
    const date = new Date(datetime);
    return date.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

async function abrirModal() {
    mostrarModal.value = true;
    // El historial ya se carga en onMounted, pero puedes recargarlo aquí si lo deseas
}

function cerrarModal() {
    mostrarModal.value = false;
}

onMounted(async () => {
    if (idUsuario) {
        const res = await getUserRole(idUsuario);
        if (res && res.status === 200) {
            rolUsuario.value = res.data.rol;
        }
    }
    const res = await getEditHistory(props.idLibro);
    if (res && res.status === 200 && res.data.historial.length > 0) {
        historial.value = res.data.historial;
        ultimaEdicion.value = res.data.historial[0]; // El primero es el más reciente
    } else {
        historial.value = [];
        ultimaEdicion.value = null;
    }
});
</script>

<style scoped>
.edit-record-container {
    font-size: 0.95rem;
    color: #555;
    margin-top: 0.5rem;
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
    min-width: 350px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.table {
    margin-bottom: 1rem;
}
</style>