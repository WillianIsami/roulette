<template>
    <form @submit.prevent="submitForm" class="w-50 mx-auto">
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type="text" class="form-control" v-model="formData.username" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" v-model="formData.password" required>
        </div>
        <button type="submit" class="btn btn-primary" @click="getPermission">Submit</button>
    </form>
    <p class="m-3">Don't have an account? <RouterLink class="fw-bold" to="/register">Sign up</RouterLink></p>
</template>


<script>
    import { login } from '@/services/apiService';

    export default {
        name: 'LoginView',

        data() {
            return {
                responseData: null,
                formData: {
                    username: '',
                    password: ''
                },
                baseUrl: "http://127.0.0.1:8000/bets/"
            };
        },

        methods: {
            getPermission() {
                const url = `${this.baseUrl}api-auth-token/`;
                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData)
                };
                login(url, options);
                this.formData.username = '';
                this.formData.password = '';
            },
        }   
    }
</script>
