<template>
    <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
      <a href="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
        <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap"><use xlink:href="#bootstrap"></use></svg>
      </a>

      <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <li><a href="#" class="nav-link px-2 link-secondary underline-on-hover">Home</a></li>
        <li><a href="#" class="nav-link px-2 link-dark underline-on-hover">Apostas</a></li>
        <li><a href="#" class="nav-link px-2 link-dark underline-on-hover">FAQs</a></li>
        <li><a href="#" class="nav-link px-2 link-dark underline-on-hover">About Us</a></li>
      </ul>

      <div class="col-md-3 text-end">
        <button type="button" class="btn btn-outline-primary me-2">Login</button>
        <button type="button" class="btn btn-primary">Sign-up</button>
      </div>
    </header>
</template>

<script>
    export default {
        name: 'HeaderComponent',
    }
</script>

<style scoped>
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