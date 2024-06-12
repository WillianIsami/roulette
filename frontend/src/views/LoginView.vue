<template>
  <form @submit.prevent="submitForm" class="w-50 mx-auto">
    <div class="mb-3">
      <label class="form-label">Username</label>
      <input
        type="text"
        class="form-control"
        v-model="formData.username"
        placeholder="Enter username"
        :class="{ 'is-invalid': verification && !formData.username }"
      />
      <p class="invalid-feedback" v-if="verification && !formData.username">
        Username required
      </p>
    </div>
    <div class="mb-3">
      <label class="form-label">Password</label>
      <input
        type="password"
        class="form-control"
        v-model="formData.password"
        placeholder="Enter password"
        :class="{ 'is-invalid': verification && !formData.password }"
      />
      <p class="invalid-feedback" v-if="verification && !formData.password">
        Password required
      </p>
    </div>
    <button type="submit" class="btn btn-success" @click="getPermission">
      Submit
    </button>
  </form>
  <p class="m-3">
    Don't have an account?
    <RouterLink class="fw-bold link-success" to="/register">Sign up</RouterLink>
  </p>
</template>

<script>
import auth from '@/store/auth';

export default {
  name: "LoginView",

  data() {
    return {
      verification: null,
      formData: {
        username: null,
        password: null,
      },
    };
  },

  methods: {
    inputVerification() {
      this.verification = true;
      return this.formData.username && this.formData.password;
    },

    async getPermission() {
      if (!this.inputVerification()) {
        console.error("field required");
        return;
      }
      try {
        // const options = {
        //   method: "POST",
        //   headers: {
        //     "Accept": "application/json",
        //     "Content-Type": "application/json",
        //   },
        //   credentials: 'include',
        //   body: JSON.stringify(this.formData),
        // };
        // const response = await fetch(url, options)
        const response = await auth.actions.login(this.formData)
        this.$router.push("/")
        console.log(await response.data)
      } catch (error) {
        console.error("Error: ", error)
      }
      this.formData.username = null;
      this.formData.password = null;
    },
  },
};
</script>
