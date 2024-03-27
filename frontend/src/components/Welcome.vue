<template>
  <div class="container">
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to play<br>
      check out the
      <a href="#">rules</a>.
    </p>
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
