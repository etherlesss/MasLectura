<template>
    <main>
        <!-- Large screens -->
        <div class="signup-container d-none d-lg-flex">
            <div class="signup-left p-5 w-50 m-1 d-flex flex-column align-items-center">
                <div class="brand d-flex flex-column justify-content-center align-items-center mx-5 mt-5">
                    <img src="../assets/logo/logo-big.png" alt="Logo" class="logo">
                    <p>Tus próximas lecturas en un solo lugar.</p>
                </div>
                <div class="illust d-flex justify-content-center align-items-center">
                    <img src="../assets/illust.png" alt="Illustration">
                </div>
            </div>
            <div class="login-right p-5 w-50 d-flex flex-column justify-content-center align-items-center">
                <SignUpForm />
            </div>
        </div>
        <!-- Small screens -->
        <div class="signup-container d-flex d-lg-none flex-column justify-content-center align-items-center">
            <div class="brand d-flex flex-column align-items-center">
                <img src="../assets/logo/logo-dark-big.png" alt="Logo" class="logo-sm">
                <p>Tus próximas lecturas en un solo lugar.</p>
                <hr class="w-75">
            </div>
            <div class="px-5">
                <SignUpForm />
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import SignUpForm from '@/components/forms/SignUpForm.vue';


</script>

<style scoped>
.signup-container {
    height: 100vh;
}

.logo {
    width: 350px;
}

.logo-sm {
    width: 250px;
}

.signup-left {
    background-color: #262322;
    color: white;
    border-radius: 10px;
}

.illust img {
    display: block;
    max-width: 100%;
    width: 75%;
    height: auto;
    margin: 0 auto;
}

@media (max-width: 1200px) {
    .illust img {
        width: 90%;
    }
}
</style>