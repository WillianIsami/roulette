<template>
  <section class="auth-shell glass-card p-4 p-md-5">
    <h1 class="page-title">Criar conta</h1>
    <p class="page-lead mb-4">Cadastre-se para usar carteira, roleta e histórico de apostas.</p>

    <form @submit.prevent="getPermission" class="auth-form">
      <div class="mb-3 text-start">
        <label class="form-label">Usuário</label>
        <input
          type="text"
          class="form-control"
          v-model.trim="username"
          placeholder="Escolha um usuário"
          :class="{ 'is-invalid': verification && !usernameIsValid }"
        />
        <p class="invalid-feedback" v-if="verification && !usernameIsValid">
          Usuário deve ter ao menos 3 caracteres.
        </p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">Senha</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="password"
          placeholder="Crie uma senha"
          :class="{ 'is-invalid': verification && !passwordIsValid }"
        />
        <p class="invalid-feedback" v-if="verification && !passwordIsValid">
          Senha deve ter pelo menos 8 caracteres.
        </p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">Confirmar senha</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="confirmPassword"
          placeholder="Repita a senha"
          :class="{ 'is-invalid': verification && !passwordsMatch }"
        />
        <p class="invalid-feedback" v-if="verification && !passwordsMatch">
          As senhas precisam ser iguais.
        </p>
      </div>

      <p v-if="errorMessage" class="text-danger fw-semibold mb-3">{{ errorMessage }}</p>
      <p v-if="successMessage" class="text-success fw-semibold mb-3">{{ successMessage }}</p>

      <button type="submit" class="btn btn-brand w-100" :disabled="isSubmitting">
        {{ isSubmitting ? "Cadastrando..." : "Cadastrar" }}
      </button>
    </form>

    <p class="m-0 mt-3 text-center">
      Já tem conta?
      <RouterLink class="fw-bold text-decoration-none" to="/login">Entrar</RouterLink>
    </p>
  </section>
</template>

<script>
import { register } from "@/services/apiService";

export default {
  name: "RegisterView",
  data() {
    return {
      verification: false,
      isSubmitting: false,
      username: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    usernameIsValid() {
      return this.username.length >= 3;
    },
    passwordIsValid() {
      return this.password.length >= 8;
    },
    passwordsMatch() {
      return Boolean(this.confirmPassword) && this.password === this.confirmPassword;
    },
  },
  methods: {
    inputVerification() {
      this.verification = true;
      return Boolean(this.usernameIsValid && this.passwordIsValid && this.passwordsMatch);
    },

    async getPermission() {
      if (!this.inputVerification()) {
        return;
      }

      this.errorMessage = "";
      this.successMessage = "";
      this.isSubmitting = true;
      try {
        await register({
          username: this.username,
          password: this.password,
        });
        this.verification = false;
        this.successMessage = "Conta criada com sucesso. Redirecionando para login...";
        this.username = "";
        this.password = "";
        this.confirmPassword = "";
        setTimeout(() => {
          this.$router.push("/login");
        }, 800);
      } catch (error) {
        this.errorMessage = error?.userMessage || "Não foi possível criar a conta.";
      } finally {
        this.isSubmitting = false;
      }
    },
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
