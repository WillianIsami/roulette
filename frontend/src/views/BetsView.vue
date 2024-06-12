<template>
  <h1>Bets</h1>
  <ListBets />
</template>

<script>
import ListBets from "@/components/ListBets.vue";

export default {
  name: "BetsView",
  components: {
    ListBets,
  },
};
</script>
