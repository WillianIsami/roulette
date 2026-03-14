<template>
  <section class="auth-shell glass-card p-4 p-md-5">
    <h1 class="page-title">{{ $t("auth.register.title") }}</h1>
    <p class="page-lead mb-4">{{ $t("auth.register.lead") }}</p>

    <form @submit.prevent="getPermission" class="auth-form">
      <div class="mb-3 text-start">
        <label class="form-label">{{ $t("auth.register.usernameLabel") }}</label>
        <input
          type="text"
          class="form-control"
          v-model.trim="username"
          :placeholder="$t('auth.register.usernamePlaceholder')"
          :class="{ 'is-invalid': verification && !usernameIsValid }"
        />
        <p class="invalid-feedback" v-if="verification && !usernameIsValid">
          {{ $t("auth.register.usernameMinLength") }}
        </p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">{{ $t("auth.register.passwordLabel") }}</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="password"
          :placeholder="$t('auth.register.passwordPlaceholder')"
          :class="{ 'is-invalid': verification && !passwordIsValid }"
        />
        <p class="invalid-feedback" v-if="verification && !passwordIsValid">
          {{ $t("auth.register.passwordMinLength") }}
        </p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">{{ $t("auth.register.confirmPasswordLabel") }}</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="confirmPassword"
          :placeholder="$t('auth.register.confirmPasswordPlaceholder')"
          :class="{ 'is-invalid': verification && !passwordsMatch }"
        />
        <p class="invalid-feedback" v-if="verification && !passwordsMatch">
          {{ $t("auth.register.passwordMismatch") }}
        </p>
      </div>

      <p v-if="errorMessage" class="text-danger fw-semibold mb-3">{{ errorMessage }}</p>
      <p v-if="successMessage" class="text-success fw-semibold mb-3">{{ successMessage }}</p>

      <button type="submit" class="btn btn-brand w-100" :disabled="isSubmitting">
        {{ isSubmitting ? $t("auth.register.submitting") : $t("auth.register.submit") }}
      </button>
    </form>

    <p class="m-0 mt-3 text-center">
      {{ $t("auth.register.haveAccount") }}
      <RouterLink class="fw-bold text-decoration-none" to="/login">{{ $t("auth.register.loginCta") }}</RouterLink>
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
        this.successMessage = this.$t("auth.register.successCreated");
        this.username = "";
        this.password = "";
        this.confirmPassword = "";
        setTimeout(() => {
          this.$router.push("/login");
        }, 800);
      } catch (error) {
        this.errorMessage = error?.userMessage || this.$t("auth.register.fallbackError");
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
