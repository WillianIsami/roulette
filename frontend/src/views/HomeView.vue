<template>
  <div class="d-flex flex-column gap-4">
    <WelcomeComponent />
    <WheelComponent />
  </div>
</template>

<script>
import WelcomeComponent from "@/components/Welcome.vue";
import WheelComponent from "@/components/Wheel.vue";

export default {
  name: "HomeView",
  components: {
    WelcomeComponent,
    WheelComponent,
  },
};
</script>
