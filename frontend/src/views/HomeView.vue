
<template>
  <div>
    <Navbar />
  
  
  <div class = "body">
    <h1>Welcome to the Home Page</h1>
    <p>This is a simple home page for our application.</p>
    <div class="test">
      <img src="../assets/test/Angel4.jpg" alt="foto-prueba">
    </div>
  </div>

    <Footer/>

</div>
</template>
<script setup lang="ts">
import Navbar from '@/components/nav/Navbar.vue';
import Footer from '@/components/pageFooter/Footer.vue';
</script>

<style scoped>

.test img{
  width: 100%  ;
  height: 100% ;
}

.body{
  height: 100%;
  margin: 0px;
  min-height: 100vh;
}


</style>