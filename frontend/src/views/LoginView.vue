<template>
    <form @submit.prevent="submitForm" class="w-50 mx-auto">
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input
                type="text"
                class="form-control"
                v-model="formData.username"
                placeholder="Enter username"
                :class="{ 'is-invalid': verification && !formData.username}"
            />
            <p class="invalid-feedback" v-if="verification && !formData.username">Username required</p>
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input 
                type="password" 
                class="form-control" 
                v-model="formData.password" 
                placeholder="Enter password"
                :class="{ 'is-invalid': verification && !formData.password}"
            />
            <p class="invalid-feedback" v-if="verification &&!formData.password">Password required</p>
        </div>
        <button type="submit" class="btn btn-success" @click="getPermission">Submit</button>
    </form>
    <p class="m-3">Don't have an account? <RouterLink class="fw-bold link-success" to="/register">Sign up</RouterLink></p>
</template>


<script>
    import router from '@/router/routes';
    import { login } from '@/services/apiService';

    export default {
        name: 'LoginView',

        data() {
            return {
                verification: null,
                formData: {
                    username: null,
                    password: null
                },
                baseUrl: "http://127.0.0.1:8000/bets/"
            };
        },

        methods: {
            inputVerification() {
                this.verification = true;
                return this.formData.username && this.formData.password;
            },

            getPermission() {
                const url = `${this.baseUrl}api-auth-token/`;
                if (!this.inputVerification()) {
                    console.error("field required");
                    return
                }
                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                };
                login(url, options);
                // TODO: Session authentication
                const isLoggedIn = localStorage.getItem('token') !== null;
                if (isLoggedIn) {
                    router.push("/");
                }
                this.formData.username = null;
                this.formData.password = null;
            },
        }   
    }
</script>
