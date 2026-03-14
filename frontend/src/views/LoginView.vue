<template>
  <section class="auth-shell glass-card p-4 p-md-5">
    <h1 class="page-title">Entrar</h1>
    <p class="page-lead mb-4">Acesse sua conta para liberar a mesa e apostar com carteira.</p>

    <form @submit.prevent="getPermission" class="auth-form">
      <div class="mb-3 text-start">
        <label class="form-label">Usuário</label>
        <input
          type="text"
          class="form-control"
          v-model.trim="formData.username"
          placeholder="Digite seu usuário"
          :class="{ 'is-invalid': verification && !formData.username }"
        />
        <p class="invalid-feedback" v-if="verification && !formData.username">Usuário obrigatório.</p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">Senha</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="formData.password"
          placeholder="Digite sua senha"
          :class="{ 'is-invalid': verification && !formData.password }"
        />
        <p class="invalid-feedback" v-if="verification && !formData.password">Senha obrigatória.</p>
      </div>

      <p v-if="errorMessage" class="text-danger fw-semibold mb-3">{{ errorMessage }}</p>

      <button type="submit" class="btn btn-brand w-100" :disabled="isSubmitting">
        {{ isSubmitting ? "Entrando..." : "Entrar" }}
      </button>
    </form>

    <p class="m-0 mt-3 text-center">
      Não tem conta?
      <RouterLink class="fw-bold text-decoration-none" to="/register">Cadastre-se</RouterLink>
    </p>
  </section>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      verification: false,
      isSubmitting: false,
      errorMessage: "",
      formData: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    inputVerification() {
      this.verification = true;
      return Boolean(this.formData.username && this.formData.password);
    },

    async getPermission() {
      if (!this.inputVerification()) {
        return;
      }

      this.errorMessage = "";
      this.isSubmitting = true;
      try {
        await this.$store.dispatch("login", this.formData);
        this.verification = false;
        this.$router.push("/");
      } catch (error) {
        this.errorMessage = error?.userMessage || "Não foi possível entrar agora. Tente novamente.";
      } finally {
        this.isSubmitting = false;
      }
    },
  },
  mounted() {
    if (this.$route.query.reason === "session_expired") {
      this.errorMessage = "Sua sessão expirou. Faça login novamente para continuar.";
    }
  },
};
</script>

<style scoped>
.auth-shell {
  width: min(520px, 100%);
  margin: 0 auto;
}

.auth-form {
  max-width: 420px;
  margin: 0 auto;
}
</style>
