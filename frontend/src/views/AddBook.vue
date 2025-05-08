<template>
    <div>
        <Navbar />
        <div class="addBook-container">
            <div class="section-container">
                <div class="button-container">
                    <button type="button" alt = " " aria-label="">
                    Tipo de lectura
                    </button>
                </div>
                <div class="form-container">
                    <FirstForm @guardar="guardarFirstForm" @tipoSeleccionado="tipoSeleccionado = $event" />
                </div>
            </div>
            <div class="section-container">
                <div class="button-container">
                    <button type="button" alt = " " aria-label="">
                    Ingresar datos
                    </button>
                </div>
                <div class="form-container">
                    <SecondFormBook v-if="tipoSeleccionado === 'libro'" @guardar="guardarSecondForm" />
                    <SecondFormNovel v-if="tipoSeleccionado === 'novel'"  @guardar="guardarSecondForm"/>
                    <SecondFormManga v-if="tipoSeleccionado === 'manga'"  @guardar="guardarSecondForm"/>
                    
                </div>
            </div>
            <div class="section-container">
                <div class="button-container">
                    <button type="button" alt = " " aria-label="">
                    Seleccionar categorias
                    </button>
                </div>
                <div class="form-container">
                    <ThirdForm @guardar="guardarThirdForm" />
                
                </div>
            </div>
            <div class="save-button">
                <button @click="enviarTodo">Enviar</button>
            </div>
        </div>
        <Footer/>
    </div>
</template>
<script setup lang="ts">
    import { ref } from 'vue';
    import Navbar from '@/components/nav/Navbar.vue';
    import FirstForm from '@/components/book_forms/FirstForm.vue';
    import SecondFormBook from '@/components/book_forms/SecondFormBook.vue';
    import SecondFormNovel from '@/components/book_forms/SecondFormNovel.vue';
    import SecondFormManga from '@/components/book_forms/SecondFormManga.vue';
    import ThirdForm from '@/components/book_forms/ThirdForm.vue';
    import Footer from '@/components/pageFooter/Footer.vue';

    const tipoSeleccionado = ref('');
    const firstFormData = ref<Record<string, any>>({});
    const secondFormData = ref<Record<string, any>>({});
    const thirdFormData = ref<Record<string, any>>({});


    function guardarFirstForm(data: any) {
  firstFormData.value = data;
}

function guardarSecondForm(data: any) {
  secondFormData.value = data;
}

function guardarThirdForm(data: any) {
  thirdFormData.value = data;
}

function enviarTodo() {
  const datosCompletos = {
    ...firstFormData.value,
    ...secondFormData.value,
    ...thirdFormData.value
  };

  
  async function enviarTodo() {
  try {
    const response = await fetch('/api/libros', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datosCompletos)
    });

    // Verificar si la respuesta fue exitosa
    if (!response.ok) {
      throw new Error(`Error en la petición: ${response.status}`);
    }

    const data = await response.json();
    console.log("Guardado correctamente", data);
  } catch (error) {
    console.error("Ocurrió un error:", error);
    alert("Ocurrió un error al guardar los datos. Por favor, intente nuevamente.");
  }
    }
}
</script>
    
<style scoped>

.addBook-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    gap: 2rem; 
    padding: 2rem;
}

.section-container{
    display: flex;
  gap: 1rem;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
  max-width: 900px;
}


.form-container{
  padding: 1.5rem;
  border: 2px solid #444;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-width: 800px;
  width: 100%;
  box-sizing: border-box;
}
.button-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 200px;
}

.button-container button {
  width: 100%;
  height: 40px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>