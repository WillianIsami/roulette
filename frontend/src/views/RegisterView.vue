<template>
  <form @submit.prevent="submitForm" class="w-50 mx-auto">
    <div class="mb-3">
      <label class="form-label">Username</label>
      <input
        type="text"
        class="form-control"
        v-model="username"
        placeholder="Enter Username"
        :class="{ 'is-invalid': verification && !username }"
      />
      <p class="invalid-feedback" v-if="verification && !username">
        Username required
      </p>
    </div>
    <div class="mb-3">
      <label class="form-label">Password</label>
      <input
        type="password"
        class="form-control"
        v-model="password"
        placeholder="Enter password"
        :class="{ 'is-invalid': verification && !password }"
      />
      <p class="invalid-feedback" v-if="verification && !password">
        Password required
      </p>
    </div>
    <div class="mb-3">
      <label class="form-label">Confirm Password</label>
      <input
        type="password"
        class="form-control"
        v-model="confirmPassword"
        placeholder="Confirm Password"
        :class="{
          'is-invalid':
            verification && (password !== confirmPassword || !confirmPassword),
        }"
      />
      <p
        class="invalid-feedback"
        v-if="
          verification && (password !== confirmPassword || !confirmPassword)
        "
      >
        Passwords don't match
      </p>
    </div>
    <button type="submit" class="btn btn-success" @click="getPermission">
      Submit
    </button>
  </form>
  <p class="m-3">
    Have an account?
    <RouterLink class="fw-bold link-success" to="/login">Log in</RouterLink>
  </p>
</template>

<script>
import router from "@/router/routes";
import { register } from "@/services/apiService";

export default {
  name: "RegisterView",

  data() {
    return {
      verification: null,
      username: null,
      password: null,
      confirmPassword: null,
      createdUser: null,
      baseUrl: process.env.VUE_APP_BASE_URL,
    };
  },

  methods: {
    inputVerification() {
      this.verification = true;
      return (
        this.username &&
        this.password &&
        this.confirmPassword &&
        this.password === this.confirmPassword
      );
    },

    getPermission() {
      const url = `${this.baseUrl}/api/create/`;
      if (!this.inputVerification()) {
        console.error("field required");
        return;
      }
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      };
      register(url, options).then((data) => {
        // TODO: Session authentication
        if (typeof data === typeof "str") {
          router.push("/login");
          return;
        }
        this.username = null;
        this.password = null;
        this.confirmPassword = null;
      });
    },
  },
};
</script>
