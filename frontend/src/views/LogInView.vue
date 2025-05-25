<template>
    <main>
        <!-- Large screens -->
        <div class="login-container d-none d-lg-flex">
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
        <!-- Small screens -->
        <div class="login-container d-flex d-lg-none flex-column justify-content-center align-items-center">
            <div class="brand d-flex flex-column align-items-center">
                <img src="../assets/logo/logo-dark-big.png" alt="Logo" class="logo-sm">
                <p>Tus próximas lecturas en un solo lugar.</p>
                <hr class="w-75">
            </div>
            <div class="px-5">
                <LogInForm />
            </div>
        </div>
    </main>
    <RecoveryMailModal />
</template>

<script setup lang="ts">
import LogInForm from '@/components/forms/LogInForm.vue';
import RecoveryMailModal from '@/components/modal/RecoveryMailModal.vue';
</script>

<style scoped>
.login-container {
    height: 100vh;
}

.logo {
    width: 350px;
}

.logo-sm {
    width: 250px;
}

.login-left {
    background-color: #262322;
    color: white;
    border-radius: 10px;
}
</style>