<template>
    <form @submit.prevent="submitForm" class="w-50 mx-auto">
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input
                type="text"
                class="form-control"
                v-model="username"
                placeholder="Enter Username"
                required
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input
                type="password"
                class="form-control"
                v-model="password"
                placeholder="Enter password"
                required
            />
        </div>
        <div class="mb-3">
            <label class="form-label">Confirm Password</label>
            <input
                type="password"
                class="form-control"
                v-model="confirmPassword"
                placeholder="Confirm Password"
                required
            />
        </div>
        <button type="submit" class="btn btn-success" @click="getPermission">Submit</button>
    </form>
    <p class="m-3">Have an account? <RouterLink class="fw-bold link-success" to="/login">Log in</RouterLink></p>
</template>


<script>
    import { register } from '@/services/apiService';

    export default {
        name: 'RegisterView',

        data() {
            return {
                responseData: null,
                username: null,
                password: null,
                confirmPassword: null,
                baseUrl: "http://127.0.0.1:8000/bets/"
            };
        },

        methods: {
            getPermission() {
                const url = `${this.baseUrl}api/create/`;
                // TODO: Create an element (toast?) on the page intead console.error()
                if (!this.username || !this.password || !this.confirmPassword) {
                    console.error("Field empty");
                    return
                }  
                else if (this.password !== this.confirmPassword) {
                    console.error("Passwords don't match");
                    return 
                }
                const options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password
                    })
                };
                register(url, options);
                this.username = null;
                this.password = null;
                this.confirmPassword = null;
            },
        }   
    }
</script>
