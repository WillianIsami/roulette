<template>
  <section>
    <div class="text-center mb-3">
      <h1 class="page-title">{{ $t("betsPage.title") }}</h1>
      <p class="page-lead">{{ $t("betsPage.lead") }}</p>
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
