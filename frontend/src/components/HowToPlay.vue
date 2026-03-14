<template>
  <section class="glass-card p-4 p-md-5">
    <h1 class="page-title">Como jogar (modo iniciante)</h1>
    <p class="page-lead mb-4">
      Em menos de 2 minutos você consegue entender tudo: onde clicar, quanto pode ganhar e como ler o resultado líquido da rodada.
    </p>

    <div class="quick-steps mb-4">
      <article class="step-card">
        <h3>1. Abasteça sua carteira</h3>
        <p>Use os botões de depósito rápido para colocar moedas e começar sem travar no saldo.</p>
      </article>
      <article class="step-card">
        <h3>2. Escolha o valor da ficha</h3>
        <p>A ficha define quanto cada clique adiciona na aposta: 5, 10, 25, 50 ou 100 moedas.</p>
      </article>
      <article class="step-card">
        <h3>3. Monte sua combinação</h3>
        <p>Aposte interno (mais risco, maior retorno) ou externo (mais chance, retorno menor).</p>
      </article>
      <article class="step-card">
        <h3>4. Gire e aguarde parar</h3>
        <p>O número é revelado só quando a roleta para. Depois disso, você vê lucro, perdas e saldo final.</p>
      </article>
    </div>

    <section class="formula-box mb-4">
      <h2 class="section-title mb-2">Como ler retorno e lucro</h2>
      <p class="mb-2">
        <strong>Retorno líquido ao acertar</strong> é o lucro da aposta vencedora, sem contar o valor da ficha.
      </p>
      <p class="mb-2"><strong>Retorno total recebido</strong> = ficha + lucro.</p>
      <p class="mb-0">
        <strong>Resultado líquido da rodada</strong> = soma dos lucros vencedores - soma das apostas perdidas.
      </p>
    </section>

    <h2 class="section-title mb-2">Pagamentos por cobertura</h2>
    <div class="table-responsive mb-4">
      <table class="table table-sm table-striped mb-0 payout-table">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Números cobertos</th>
            <th>Lucro líquido (acerto)</th>
            <th>Retorno total (ficha 5)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Straight-up</td>
            <td>1</td>
            <td>35:1</td>
            <td>180.00</td>
          </tr>
          <tr>
            <td>Split</td>
            <td>2</td>
            <td>17:1</td>
            <td>90.00</td>
          </tr>
          <tr>
            <td>Street</td>
            <td>3</td>
            <td>11:1</td>
            <td>60.00</td>
          </tr>
          <tr>
            <td>Corner / Basket</td>
            <td>4</td>
            <td>8:1</td>
            <td>45.00</td>
          </tr>
          <tr>
            <td>Two Street</td>
            <td>6</td>
            <td>5:1</td>
            <td>30.00</td>
          </tr>
          <tr>
            <td>Line / Dozens</td>
            <td>12</td>
            <td>2:1</td>
            <td>15.00</td>
          </tr>
          <tr>
            <td>Cor / Paridade / Faixa</td>
            <td>18</td>
            <td>1:1</td>
            <td>10.00</td>
          </tr>
        </tbody>
      </table>
    </div>

    <section class="result-example mb-4">
      <h2 class="section-title mb-2">Exemplo real de resultado líquido</h2>
      <p class="mb-1">Você apostou 45.00 no total.</p>
      <p class="mb-1">Apostas vencedoras geraram +25.00 de lucro.</p>
      <p class="mb-1">Apostas perdedoras somaram -25.00.</p>
      <p class="mb-0"><strong>Resultado líquido = 0.00</strong> (nem ganhou, nem perdeu no giro).</p>
    </section>

    <div class="cta-box d-flex flex-wrap align-items-center justify-content-between gap-2">
      <p class="mb-0 fw-semibold">Pronto para testar uma estratégia na mesa?</p>
      <RouterLink to="/" class="btn btn-brand">Ir para a roleta</RouterLink>
    </div>
  </section>
</template>

<script>
export default {
  name: "HowToPlay",
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
