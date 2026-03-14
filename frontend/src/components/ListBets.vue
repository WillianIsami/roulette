<template>
  <section class="glass-card p-4">
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
      <h2 class="section-title mb-0">Tipos de apostas disponíveis</h2>
      <button class="btn btn-brand-outline" type="button" @click="getData" :disabled="loading">
        {{ loading ? "Carregando..." : "Atualizar" }}
      </button>
    </div>

    <p v-if="errorMessage" class="text-danger fw-semibold">{{ errorMessage }}</p>

    <div v-if="responseData" class="bet-grid">
      <div class="bet-card" v-for="(bet, index) in bets.bets" :key="index">
        <p class="mb-1 small text-muted">Aposta {{ index + 1 }}</p>
        <strong>{{ bet }}</strong>
      </div>
    </div>

    <div v-else-if="!loading" class="text-muted">
      Faça login para visualizar e apostar.
      <RouterLink class="fw-bold text-decoration-none" to="/login">Entrar</RouterLink>
    </div>
  </section>
</template>

<script>
import { fetchBets } from "@/services/apiService";
import { isAuthError } from "@/services/errorService";

export default {
  name: "ListBets",
  data() {
    return {
      responseData: false,
      loading: false,
      errorMessage: "",
      bets: { bets: [] },
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    async handleError(error) {
      const message = error?.userMessage || "Não foi possível carregar os tipos de aposta agora.";
      this.errorMessage = message;

      if (!isAuthError(error)) {
        return;
      }

      this.errorMessage = "Sua sessão expirou. Redirecionando para login...";
      try {
        await this.$store.dispatch("logout");
      } catch (_) {
        this.$store.commit("SET_AUTHENTICATED", false);
      }

      setTimeout(() => {
        this.$router.push({ name: "Login", query: { reason: "session_expired" } });
      }, 900);
    },

    async getData() {
      this.loading = true;
      this.errorMessage = "";
      try {
        const data = await fetchBets();
        this.responseData = true;
        this.bets = data;
      } catch (error) {
        this.responseData = false;
        await this.handleError(error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.bet-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.65rem;
}

.bet-card {
  border: 1px solid #e0d2b0;
  border-radius: 12px;
  padding: 0.75rem;
  background: #fffdf8;
}
</style>
