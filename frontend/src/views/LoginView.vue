<template>
  <section class="auth-shell glass-card p-4 p-md-5">
    <h1 class="page-title">{{ $t("auth.login.title") }}</h1>
    <p class="page-lead mb-4">{{ $t("auth.login.lead") }}</p>

    <form @submit.prevent="getPermission" class="auth-form">
      <div class="mb-3 text-start">
        <label class="form-label">{{ $t("auth.login.usernameLabel") }}</label>
        <input
          type="text"
          class="form-control"
          v-model.trim="formData.username"
          :placeholder="$t('auth.login.usernamePlaceholder')"
          :class="{ 'is-invalid': verification && !formData.username }"
        />
        <p class="invalid-feedback" v-if="verification && !formData.username">{{ $t("auth.login.usernameRequired") }}</p>
      </div>

      <div class="mb-3 text-start">
        <label class="form-label">{{ $t("auth.login.passwordLabel") }}</label>
        <input
          type="password"
          class="form-control"
          v-model.trim="formData.password"
          :placeholder="$t('auth.login.passwordPlaceholder')"
          :class="{ 'is-invalid': verification && !formData.password }"
        />
        <p class="invalid-feedback" v-if="verification && !formData.password">{{ $t("auth.login.passwordRequired") }}</p>
      </div>

      <p v-if="errorMessage" class="text-danger fw-semibold mb-3">{{ errorMessage }}</p>

      <button type="submit" class="btn btn-brand w-100" :disabled="isSubmitting">
        {{ isSubmitting ? $t("auth.login.submitting") : $t("auth.login.submit") }}
      </button>
    </form>

    <p class="m-0 mt-3 text-center">
      {{ $t("auth.login.noAccount") }}
      <RouterLink class="fw-bold text-decoration-none" to="/register">{{ $t("auth.login.registerCta") }}</RouterLink>
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
        this.errorMessage = error?.userMessage || this.$t("auth.login.fallbackError");
      } finally {
        this.isSubmitting = false;
      }
    },
  },
  mounted() {
    if (this.$route.query.reason === "session_expired") {
      this.errorMessage = this.$t("auth.sessionExpired");
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
