<template>
  <div class="container">
    <NavbarComponent />
    <main>
      <RouterView />
    </main>
    <FooterComponent />
  </div>
</template>

<script>
import FooterComponent from "@/components/Footer.vue";
import NavbarComponent from "@/components/Navbar.vue";

export default {
  name: "App",
  components: {
    FooterComponent,
    NavbarComponent,
  },
  data() {
    return {
      activeLink: "/",
    };
  },
  methods: {
    setActiveLink(link) {
      this.activeLink = link;
    },
  },
};
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
  content: "";
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
