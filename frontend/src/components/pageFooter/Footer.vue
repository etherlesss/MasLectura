<template>
    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <!-- Información -->
            <div class="info">
                <b>Información</b>
                <ul class="info-list">
                    <li class="info-links">
                        <RouterLink to="/about">Sobre nosotros</RouterLink>
                    </li>
                    <li class="info-links">
                        <RouterLink to="/contact">Contacto</RouterLink>
                    </li>
                </ul>
            </div>
            <!-- Reglas -->
            <div class="rules">
                <b>Reglas de la comunidad</b>
                <ul class="rules-list">
                    <li class="rules-links">
                        <RouterLink to="/terms">Términos y condiciones</RouterLink>
                    </li>
                    <li class="rules-links">
                        <RouterLink to="/policy">Política de privacidad</RouterLink>
                    </li>
                </ul>
            </div>
            <!-- Redes sociales -->
            <div class="social">
                <b>Nuestras redes sociales</b>
                <ul class="social-list">
                    <li class="social-links">
                        <RouterLink to="#">
                            <img src="@/assets/social/icon-facebook.png" alt="Facebook">
                        </RouterLink>
                    </li>
                    <li class="social-links">
                        <RouterLink to="#">
                            <img src="@/assets/social/icon-instagram.png" alt="Instagram">
                        </RouterLink>
                    </li>
                    <li class="social-links">
                        <RouterLink to="#">
                            <img src="@/assets/social/icon-tiktok.png" alt="TikTok">
                        </RouterLink>
                    </li>
                    <li class="social-links">
                        <RouterLink to="#">
                            <img src="@/assets/social/icon-youtube.png" alt="YouTube">
                        </RouterLink>
                    </li>
                    <li class="social-links">
                        <RouterLink to="#">
                            <img src="@/assets/social/icon-twitter.png" alt="Twitter">
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
        <!-- Derechos de autor -->
        <div class="copyrights">
            <p> © 2025 +Lectura, Inc.</p>
        </div>
    </footer>
</template>

<script setup lang="ts">
    
</script>

<style scoped>
footer {
    background-color: #262322;
    color: white;
}

.footer-content {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 2rem 0;
}

.footer-content div ul {
    list-style: none;
    font-size: .8rem;
    padding: 0;
}

.footer-content b {
    display: block;
    margin-bottom: 0.5rem;
}

.footer-content div {
    font-size: .871rem;
    text-align: center;
    padding: 0;
}

.footer-content div ul li a {
    color: white;
    text-decoration: none;
}

.footer-content div ul li a:hover {
    text-decoration: underline;
}

.social-list {
    display: flex;
}

.social-links img {
    width: 35px;
    object-fit: contain;
} 

.copyrights {
    text-align: center;
    padding: 1rem 0;
    font-size: .8rem;
}

@media (max-width: 576px) {
    .footer-content {
        flex-direction: column;
        align-items: center;
    }
}
</style>