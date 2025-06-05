<template>
    <main class="p-5 d-flex flex-column align-items-center">
        <p class="not-found">
            <span v-for="(char, i) in '404'" :key="i" class="wave-letter" :style="{ animationDelay: (i * 0.3) + 's' }">
                {{ char }}
            </span>
        </p>
        <h1>Página no encontrada</h1>
        <p class="mb-4">
            Lo sentimos, la página que estás buscando no existe. Puede que haya sido eliminada, su nombre haya cambiado o que esté temporalmente fuera de servicio.
        </p>
        <p>
            Por favor, verifica la URL o vuelve a la <router-link to="/" class="link-styled">página de inicio</router-link>.
        </p>
    </main>
</template>

<script setup lang="ts">
</script>

<style scoped>
.not-found {
    font-size: 3rem;
    text-shadow: 2px 4px 12px rgba(0,0,0,0.15);
    letter-spacing: 0.1em;
    user-select: none;
}

.wave-letter {
    display: inline-block;
    text-shadow: 2px 4px 12px rgba(0,0,0,0.15);
    animation: wave 1.6s infinite ease-in-out;
    font-weight: bold;
}

@keyframes wave {
    0%   { transform: translateY(0); }
    25%  { transform: translateY(-2px); }
    75%  { transform: translateY(2px); }
    100% { transform: translateY(0); }
}
</style>