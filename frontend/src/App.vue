<template>
  <HeaderComponent />
  <WelcomeComponent msg="Welcome to Our Game"/>
  <RouletteComponent />
  <ApiData />
  <FooterComponent />
</template>

<script>
  import WelcomeComponent from './components/Welcome.vue';
  import ApiData from './components/Api.vue';
  import HeaderComponent from './components/Header.vue';
  import FooterComponent from './components/Footer.vue';
  import RouletteComponent from './components/RouletteBorder.vue';

  export default {
    name: 'App',
    components: {
      HeaderComponent,
      WelcomeComponent,
      RouletteComponent,
      ApiData,
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
</style>
