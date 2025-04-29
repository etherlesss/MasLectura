<template>

    <nav class="navbar">
        <div class = 'logo'>
            <img src= "@/assets/logo/logo-big.png" alt="Logo" class="logo">
        </div>
        <div class = "search-bar">
            <input type="text" placeholder="Buscar nueva lectura...">
            <button type="button">
                <img src="@/assets/icon-search.png">
            </button>
        </div>

        <div class = 'options'>
            <ul class="nav-list">
                <li class = "nav-links">
                    <RouterLink to="/">Inicio</RouterLink>
                </li>
                <li class = "nav-links">
                    <RouterLink to="/login">Iniciar Sesion</RouterLink>
                </li>
                <li class = "nav-links">
                    <RouterLink to="/signup">Crear Cuenta</RouterLink>
                </li>
            </ul>
        </div>
      
    </nav>

</template>

<script setup lang="ts">
import { ref } from 'vue';
</script>

<style scoped>

.navbar{
    background-color: #262322;
    display:flex;
    align-items: center;
}

.logo{
    height: auto;
    width: 300px;
}

.nav-list{
    display: flex;
    list-style: none;   
}

.nav-links a {
    padding: 20px;
    color: white;
    text-decoration: none;
}

.search-bar{
    padding:auto;
}

.search-bar input{
    width: 300px;
    padding: 3px;
    font-size: 16px;
}

.search-bar button{
    height: 35px;
    margin: 2px;
    background-color: #262322;
    border-color: rgb(155, 154, 154);
}

*{
    margin: 0;
}
</style>