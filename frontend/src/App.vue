<template>
  <div id="app" class="app-shell">
    <NavbarComponent />
    <main class="app-main">
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
};
</script>
