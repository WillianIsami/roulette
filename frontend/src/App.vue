<template>
  <img class="w-25" alt="Roulette image" src="./assets/roulette_wheel.jpg">
  <RouletteComponent msg="Welcome to Our Game"/>
  <ApiData />
</template>

<script>
import RouletteComponent from './components/Welcome.vue';
import ApiData from './components/Api.vue';

export default {
  name: 'App',
  components: {
    RouletteComponent,
    ApiData,
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
  margin-top: 60px;
}

</style>./components/Welcome.vue
