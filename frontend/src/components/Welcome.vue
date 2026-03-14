<template>
  <section class="welcome glass-card p-4 p-md-5">
    <div class="welcome-content">
      <p class="pill-label mb-3">Nova identidade visual</p>
      <h1 class="page-title">Roulette com carteira virtual e fluxo real de aposta</h1>
      <p class="page-lead mb-0">
        Monte sua estratégia, escolha fichas, faça depósito de moedas e acompanhe cada resultado da roleta com histórico de transações em tempo real.
      </p>
    </div>
    <img src="@/assets/branding/brand-banner.svg" alt="Roulette Royale" class="welcome-art" />
  </section>
</template>

<script>
export default {
  name: "WelcomeComponent",
};
</script>

<style scoped>
.welcome {
  display: grid;
  gap: 1.4rem;
  align-items: center;
  grid-template-columns: 1.15fr 1fr;
}

.welcome-art {
  width: 100%;
  border-radius: 16px;
  border: 1px solid rgba(232, 191, 101, 0.45);
  box-shadow: 0 14px 30px rgba(10, 42, 28, 0.25);
}

@media (max-width: 980px) {
  .welcome {
    grid-template-columns: 1fr;
  }
}
</style>
