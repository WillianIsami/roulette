<template>
    <HeaderComponent />
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
    <FooterComponent />
</template>


<script>
    import { getToken } from '@/services/apiService';
    import HeaderComponent from '../components/Header.vue';
    import FooterComponent from '../components/Footer.vue'

    export default {
        name: 'App',
        components: {
            HeaderComponent,
            FooterComponent,
        }, 

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
                getToken(url, options);
                this.formData.username = '';
                this.formData.password = '';
            },
        }   
    }
</script>
