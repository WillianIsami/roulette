<template>
  <img alt="Roulette image" src="./assets/roulette_wheel.jpg">
  <Roulette msg="Welcome to Our Game"/>
</template>

<script>
import Roulette from './components/Welcome.vue'

export default {
  name: 'App',
  components: {
    Roulette
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

img {
  width: 400px;
}
</style>./components/Welcome.vue
