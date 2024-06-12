<template>
  <div>
    <div v-if="responseData === true">
      <ul class="list-unstyled">
        <li v-for="(bet, index) in bets.bets" :key="index">
          {{ index + 1 }} - {{ bet }}
        </li>
      </ul>
    </div>
    <div v-else-if="responseData === false">
      <p>
        Login with your account
        <RouterLink class="fw-bold link-success" to="/login">here</RouterLink>
        to see all bets available
      </p>
    </div>
    <button class="m-4 btn btn-success" @click="getData">Show bets</button>
  </div>
</template>

<script>
export default {
  name: "ListBets",

  data() {
    return {
      responseData: null,
      bets: [],
      baseUrl: process.env.VUE_APP_BASE_URL
    };
  },
  methods: {
    async getData() {
      try {
        const response = await fetch(`${this.baseUrl}/api/`, {
          method: 'GET',
          credentials: 'include',
        })
        if (!response.ok) {
          throw new Error('Protected resources error')
        }
        const data = await response.json();
        this.responseData = true
        this.bets = data
      } catch (error) {
        console.error("Error: ", error)
      }
    },
  },
};
</script>
