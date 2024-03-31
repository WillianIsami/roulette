<template>
    <div class="container">
        <nav class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
            <img src="./assets/icons/logo.png" alt="roulette logo" width="40" />
            <div class="nav col-12 col-md-auto mb-2 d-flex justify-content-center align-items-center mb-md-0">
                <RouterLink to="/" class="nav-link px-2 link-secondary underline-on-hover">Home</RouterLink>
                <RouterLink to="/about" class="nav-link px-2 link-dark underline-on-hover">About Us</RouterLink>
                <RouterLink to="/bets" class="nav-link px-2 link-dark underline-on-hover">Bets</RouterLink>
                <RouterLink to="/faq" class="nav-link px-2 link-dark underline-on-hover">FAQ</RouterLink>
            </div>
            <div class="col-md-3 text-end">
                <RouterLink to="/login" class="btn btn-outline-success me-2">Login</RouterLink>
                <RouterLink to="/register" class="btn btn-success">Sign-up</RouterLink>
            </div>
        </nav>
        <main>
            <RouterView />
        </main>
    </div>
</template>

<script>
  export default {
    name: 'App',
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
