<template>
    <Navbar />
    <main class="p-5">
        <div class="mb-5">
            <h1>Mi perfil</h1>
            <!-- Formulario -->
            <form @submit.prevent="handleSubmit" autocomplete="off">
                <!-- Nombre de usuario -->
                <div class="mb-3">
                    <label for="username" class="form-label mb-1"><b>Nombre de usuario</b></label>
                    <input v-model="user.nombre_usuario" type="text" class="form-control" id="username" placeholder="jsmith" required>
                </div>
                <!-- Correo electrónico -->
                <div class="mb-3">
                    <label for="mail" class="form-label mb-1"><b>Correo electrónico</b></label>
                    <input v-model="user.mail_usuario" type="email" class="form-control" id="mail" placeholder="jsmith@gmail.com" disabled>
                </div>
                <!-- Género -->
                <div class="mb-3">
                    <label for="gender" class="form-label mb-1">Género</label>
                    <select class="form-select" v-model="user.genero_usuario" id="gender" required>
                        <option selected disabled>Seleccionar...</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                        <option value="No binario">No binario</option>
                        <option value="Prefiero no decirlo">Prefiero no decirlo</option> 
                    </select>
                </div>
                <!-- Fecha de nacimiento -->
                <div class="mb-3">
                    <label for="birthdate" class="form-label mb-1">Fecha de nacimiento</label>
                    <input v-model="user.fecha_nacimiento" type="date" class="form-control" id="birthdate" required>
                </div>
                <!-- Imagen de perfil -->
                <div class="mb-3">
                    <label for="profilePic" class="form-label mb-1">Imagen de perfil</label>
                    <input type="file" class="form-control" id="profilePic" accept="image/*" @change="onFileChange">
                    <div v-if="previewImg" class="mt-2 d-flex d-lg-block flex-column align-items-center">
                        <img :src="previewImg" alt="Vista previa" style="max-width: 120px; max-height: 120px; border-radius: 12px;">
                    </div>
                </div>
                <!-- Botón de guardar cambios -->
                <button type="submit" class="btn ml-primary-btn float-end">Guardar cambios</button>
            </form>
        </div>
    </main>
    <Footer />
</template>

<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
import { onMounted, ref } from 'vue';
import { getProfile, updateProfile, uploadFotoPerfil } from '@/api/api';
import { useAuthStore } from '@/stores/token';
import { formatDateHTML } from '@/util/formatters';

// Definir variables de datos
const user = ref<any>({
    nombre_usuario: '',
    mail_usuario: '',
    genero_usuario: '',
    fecha_nacimiento: ''
});

//Variable para la vista previa de la imagen
const selectedFile = ref<File | null>(null);
const previewImg = ref<string | null>(null);

// Obtener el ID del usuario desde el almacenamiento local
const authStore = useAuthStore();

// Obtener los datos del usuario desde API
async function fetchUser() {
    try {
        const res = await getProfile(authStore.user.id);
        user.value = res.data;
        // Formatear la fecha de nacimiento al formato HTML
        user.value.fecha_nacimiento = formatDateHTML(user.value.fecha_nacimiento || '');
    } catch (err) {
        console.error('Error fetching user:', err);
    }
}

//Subir imagen de perfil
function onFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile.value = target.files[0];
        previewImg.value = URL.createObjectURL(target.files[0]);
    }
}

const handleSubmit = async () => {
    try {
        let foto_perfil = user.value.foto_perfil;

        // Si hay imagen seleccionada, súbela primero
        if (selectedFile.value) {
            const formData = new FormData();
            formData.append('image', selectedFile.value);

            const resImg = await uploadFotoPerfil(formData);
            if (resImg.status === 201 && resImg.data.filename) {
                // Construye la URL completa
                foto_perfil = foto_perfil = resImg.data.url;
            } else {
                alert('Error al subir la imagen de perfil');
                return;
            }
        }
        // Actualizar los datos del usuario
        const res = await updateProfile(authStore.user.id, {
            ...user.value,
            foto_perfil
        });
        
        if (res.status === 200) {
            console.log('Usuario actualizado correctamente');
            alert('Usuario actualizado correctamente');
            window.location.href = '/my-profile';
        } else {
            console.error('Error al actualizar el usuario:', res);
        }
    } catch (err) {
        console.error('Error actualizando usuario:', err);
    }
}

// Ejecutar funciones al montar el componente
onMounted(async () => {
    await fetchUser();
});

</script>

<style scoped>
form {
    width: 25%;
}

@media (max-width: 576px) {
    form {
        width: 100%;
    }
}
</style>