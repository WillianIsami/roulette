<template>
  <section class="glass-card p-4 p-md-5">
    <h1 class="page-title">Sobre a plataforma</h1>
    <p class="page-lead mb-4">
      Este projeto simula uma roleta com carteira virtual e fluxo completo de apostas, incluindo validação de regras no backend,
      histórico de transações e autenticação baseada em JWT com cookies HTTP only.
    </p>

    <div class="about-grid">
      <article class="about-item">
        <h3>Backend sólido</h3>
        <p>
          API em Django REST com validação de tipos de aposta, bloqueio por saldo insuficiente e rastreabilidade de cada ganho/perda na carteira.
        </p>
      </article>
      <article class="about-item">
        <h3>UX de aposta</h3>
        <p>
          Interface responsiva inspirada em mesas de cassino, com seleção de fichas, status de giro e feedback imediato do resultado líquido.
        </p>
      </article>
      <article class="about-item">
        <h3>Qualidade</h3>
        <p>
          Cobertura por testes automatizados e workflow CI para executar lint/build no frontend e testes completos no backend.
        </p>
      </article>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutView",
};
</script>

<style scoped>
.about-grid {
  display: grid;
  gap: 0.8rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.about-item {
  border: 1px solid #e1d5b8;
  border-radius: 14px;
  padding: 0.9rem;
  background: #fffdf8;
}

.about-item h3 {
  font-family: "Racing Sans One", sans-serif;
  color: #214a34;
  margin-bottom: 0.4rem;
  font-size: 1.15rem;
}

.about-item p {
  margin: 0;
  color: #3a5448;
}
</style>
