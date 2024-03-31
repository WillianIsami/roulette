<template>
    <div class="container">
        <WelcomeComponent msg="Welcome to Our Game"/>
        <RouletteComponent />
        <ApiComponent />
        <FooterComponent />
    </div>
</template>

<script>
  import WelcomeComponent from '../components/Welcome.vue';
  import ApiComponent from '../components/Api.vue';
  import FooterComponent from '../components/Footer.vue';
  import RouletteComponent from '../components/RouletteBorder.vue';

  export default {
    name: 'App',
    components: {
      WelcomeComponent,
      RouletteComponent,
      ApiComponent,
      FooterComponent,
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
