<template>
  <HeaderComponent />
  <img src="./assets/imgs/roulette.png" class="w-75" />
  <RouletteComponent msg="Welcome to Our Game"/>
  <ApiData />
  <FooterComponent />
</template>

<script>
import RouletteComponent from './components/Welcome.vue';
import ApiData from './components/Api.vue';
import HeaderComponent from './components/Header.vue';
import FooterComponent from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
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

</style>./components/Welcome.vue
