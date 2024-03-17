<template>
  <div class="roulette">
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to play<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">rules</a>.
    </p>
    <h2>Have some fun <a href="">Play</a></h2>
  </div>
</template>

<script>
export default {
  name: 'RouletteComponent',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
