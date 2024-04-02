<template>
    <div class="container">
        <nav class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between me-3 py-3 mb-4 border-bottom">
            <RouterLink to="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
                <img src="./assets/icons/logo.png" alt="roulette logo" width="40" />
            </RouterLink>
            <div class="nav col-12 col-md-auto mb-2 d-flex justify-content-center align-items-center mb-md-0">
                <RouterLink to="/" class="nav-link px-2 underline-on-hover" :class="{ 'link-secondary': activeLink === '/', 'link-dark': activeLink !== '/' }" @click="setActiveLink('/')">Home</RouterLink>
                <RouterLink to="/about" class="nav-link px-2 underline-on-hover" :class="{ 'link-secondary': activeLink === '/about', 'link-dark': activeLink !== '/about' }" @click="setActiveLink('/about')">About Us</RouterLink>
                <RouterLink to="/bets" class="nav-link px-2 underline-on-hover" :class="{ 'link-secondary': activeLink === '/bets', 'link-dark': activeLink !== '/bets' }" @click="setActiveLink('/bets')">Bets</RouterLink>
                <RouterLink to="/faq" class="nav-link px-2 underline-on-hover" :class="{ 'link-secondary': activeLink === '/faq', 'link-dark': activeLink !== '/faq' }" @click="setActiveLink('/faq')">FAQ</RouterLink>
            </div>
            <div class="col-md-3 text-end">
                <RouterLink to="/login" class="btn btn-outline-success me-2" @click="setActiveLink('/login')">Login</RouterLink>
                <RouterLink to="/register" class="btn btn-success" @click="setActiveLink('/register')">Sign-up</RouterLink>
            </div>
        </nav>
        <main>
            <RouterView />
        </main>
        <FooterComponent />
    </div>
</template>

<script>
    import FooterComponent from './components/Footer.vue';

    export default {
        name: 'App',
        components: {
            FooterComponent,
        },
        data() {
            return {
                activeLink: '/'
            };
        },
        methods: {
            setActiveLink(link) {
                this.activeLink = link;
            }
        }
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    .underline-on-hover {
        position: relative;
        text-decoration: none;
    }

    .underline-on-hover::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: -2px;
        width: 100%;
        height: 2px;
        background-color: green;
        transition: width 0.3s;
        transform: scaleX(0);
    }

    .underline-on-hover:hover::after {
        transform: scaleX(1);
    }
</style>
