<template>
  <section class="glass-card p-4 p-md-5">
    <h1 class="page-title">{{ $t("howToPlay.title") }}</h1>
    <p class="page-lead mb-4">{{ $t("howToPlay.lead") }}</p>

    <div class="quick-steps mb-4">
      <article class="step-card">
        <h3>{{ $t("howToPlay.steps.walletTitle") }}</h3>
        <p>{{ $t("howToPlay.steps.walletDescription") }}</p>
      </article>
      <article class="step-card">
        <h3>{{ $t("howToPlay.steps.chipTitle") }}</h3>
        <p>{{ $t("howToPlay.steps.chipDescription") }}</p>
      </article>
      <article class="step-card">
        <h3>{{ $t("howToPlay.steps.comboTitle") }}</h3>
        <p>{{ $t("howToPlay.steps.comboDescription") }}</p>
      </article>
      <article class="step-card">
        <h3>{{ $t("howToPlay.steps.spinTitle") }}</h3>
        <p>{{ $t("howToPlay.steps.spinDescription") }}</p>
      </article>
    </div>

    <section class="formula-box mb-4">
      <h2 class="section-title mb-2">{{ $t("howToPlay.formulaTitle") }}</h2>
      <p class="mb-2"><strong>{{ $t("howToPlay.formulaProfit") }}</strong></p>
      <p class="mb-2"><strong>{{ $t("howToPlay.formulaTotal") }}</strong></p>
      <p class="mb-0"><strong>{{ $t("howToPlay.formulaNet") }}</strong></p>
    </section>

    <h2 class="section-title mb-2">{{ $t("howToPlay.payoutTitle") }}</h2>
    <div class="table-responsive mb-4">
      <table class="table table-sm table-striped mb-0 payout-table">
        <thead>
          <tr>
            <th>{{ $t("howToPlay.payoutHeaders.type") }}</th>
            <th>{{ $t("howToPlay.payoutHeaders.coveredNumbers") }}</th>
            <th>{{ $t("howToPlay.payoutHeaders.netProfit") }}</th>
            <th>{{ $t("howToPlay.payoutHeaders.totalReturn") }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in payoutRows" :key="row.typeKey">
            <td>{{ $t(row.typeKey) }}</td>
            <td>{{ row.covered }}</td>
            <td>{{ row.net }}</td>
            <td>{{ row.total }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <section class="result-example mb-4">
      <h2 class="section-title mb-2">{{ $t("howToPlay.resultExampleTitle") }}</h2>
      <p class="mb-1">{{ $t("howToPlay.resultExampleStake") }}</p>
      <p class="mb-1">{{ $t("howToPlay.resultExampleWins") }}</p>
      <p class="mb-1">{{ $t("howToPlay.resultExampleLosses") }}</p>
      <p class="mb-0"><strong>{{ $t("howToPlay.resultExampleNet") }}</strong></p>
    </section>

    <div class="cta-box d-flex flex-wrap align-items-center justify-content-between gap-2">
      <p class="mb-0 fw-semibold">{{ $t("howToPlay.cta") }}</p>
      <RouterLink to="/" class="btn btn-brand">{{ $t("howToPlay.ctaButton") }}</RouterLink>
    </div>
  </section>
</template>

<script>
export default {
  name: "HowToPlay",
  computed: {
    payoutRows() {
      return [
        { typeKey: "howToPlay.payoutRows.straightUp", covered: "1", net: "35:1", total: "180.00" },
        { typeKey: "howToPlay.payoutRows.split", covered: "2", net: "17:1", total: "90.00" },
        { typeKey: "howToPlay.payoutRows.street", covered: "3", net: "11:1", total: "60.00" },
        { typeKey: "howToPlay.payoutRows.corner", covered: "4", net: "8:1", total: "45.00" },
        { typeKey: "howToPlay.payoutRows.twoStreet", covered: "6", net: "5:1", total: "30.00" },
        { typeKey: "howToPlay.payoutRows.lineDozen", covered: "12", net: "2:1", total: "15.00" },
        { typeKey: "howToPlay.payoutRows.evenMoney", covered: "18", net: "1:1", total: "10.00" },
      ];
    },
  },
};
</script>

<style scoped>
.quick-steps {
  display: grid;
  gap: 0.7rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.step-card,
.formula-box,
.result-example,
.cta-box {
  border: 1px solid #e0d2b1;
  border-radius: 12px;
  background: #fffdf8;
  padding: 0.8rem;
}

.step-card h3 {
  font-size: 1rem;
  margin-bottom: 0.35rem;
  color: #214733;
}

.step-card p,
.formula-box p,
.result-example p {
  margin: 0;
  color: #375548;
}

.payout-table {
  background: #fffdf7;
}

.cta-box {
  background: linear-gradient(135deg, #fff8e3 0%, #f3e4bf 100%);
}
</style>
