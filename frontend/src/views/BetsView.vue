<template>
  <section>
    <div class="text-center mb-3">
      <h1 class="page-title">Mercado de Apostas</h1>
      <p class="page-lead">
        Confira todas as modalidades disponíveis na API e use este guia como referência antes de montar sua mesa.
      </p>
    </div>
    <BetGuideInteractive />
    <ListBets />
  </section>
</template>

<script>
import BetGuideInteractive from "@/components/BetGuideInteractive.vue";
import ListBets from "@/components/ListBets.vue";

export default {
  name: "BetsView",
  components: {
    BetGuideInteractive,
    ListBets,
  },
};
</script>
