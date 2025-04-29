<template>
    <main>
        <div class="login-container d-flex">
            <div class="login-left p-5 w-50 m-1 d-flex flex-column align-items-center">
                <div class="brand d-flex flex-column justify-content-center align-items-center m-5">
                    <img src="../assets/logo/logo-big.png" alt="Logo" class="logo">
                    <p>Tus próximas lecturas en un solo lugar.</p>
                </div>
                <div class="illust">

                </div>
            </div>
            <div class="login-right p-5 w-50 d-flex flex-column justify-content-center align-items-center">
                <LogInForm />
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import LogInForm from '@/components/forms/LogInForm.vue';


</script>

<style scoped>
.login-container {
    height: 100vh;
}

.logo {
    width: 350px;
}

.login-left {
    background-color: #262322;
    color: white;
    border-radius: 10px;
}
</style>