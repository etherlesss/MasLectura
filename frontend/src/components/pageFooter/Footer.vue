<template>
    <footer class = "endPage">
        <div class = "info"> 
            <p>Información</p>
            <ul class="info-list">
                <li class = "info-links">
                    <RouterLink to="/about">Sobre nosotros</RouterLink>
                </li>
                <li class = "info-links">
                    <RouterLink to="/contact">Contacto</RouterLink>
                </li>
                
            </ul>
        </div>
        <div class = "rules"> 
            <p>Reglas de la comunidad</p>
            <ul class="rules-list">
                <li class = "rules-links">
                        <RouterLink to="/terms">Términos y concidiciones</RouterLink>
                </li>
                <li class = "rules-links">
                        <RouterLink to="/privacity">Política de privacidad</RouterLink>
                </li>
            </ul>
        </div>
        <div class = "social"> 
            <p>Nuestras redes sociales</p>
            <ul class="social-list">
                <li class = "social-links">
                        <RouterLink to=#>
                            <img src="@/assets/social/icon-facebook.png">
                        </RouterLink>
                </li>
                <li class = "social-links">
                        <RouterLink to=#>
                            <img src="@/assets/social/icon-instagram.png">
                        </RouterLink>
                </li>
                <li class = "social-links">
                        <RouterLink to=#>
                            <img src="@/assets/social/icon-tiktok.png">
                        </RouterLink>
                </li>
                <li class = "social-links">
                        <RouterLink to=#>
                            <img src="@/assets/social/icon-youtube.png">
                        </RouterLink>
                </li>
                <li class = "social-links">
                        <RouterLink to=#>
                            <img src="@/assets/social/icon-twitter.png">
                        </RouterLink>
                </li>
                
            </ul>
        </div>
        <div class = "copyrights">
            <p> © 2025 +Lectura, Inc.</p>
        </div>
    </footer>
</template>

<script setup lang="ts">
    
</script>

<style scoped>

.endPage{
    display: flex;
    background-color: #262322;
    margin-top: auto;
}

.info, .rules, .social, .copyrights{
    margin: auto;
    color: white;
    text-align: center;
    padding-top: 15px;
    font-size: 14px;
    
}

.info-list, .rules-list, .social-list{
    list-style: none;
    padding-left: 0;
    margin-left: 0;
    font-size: 13px;
    
}

.info-list, .rules-list, .social-list{
    text-align: center;
}

.info-links a, .rules-links a, .social-links a {
    color: white;
    text-decoration: none;
}

.social-list{
    display: flex;
    margin-bottom: 20px;
}

.copyrights{
    margin-top: 15px;
    padding-top: 0px;
}

.social-links img {
    width: 35x;
    height: 35px;
    object-fit: contain;
}

</style>