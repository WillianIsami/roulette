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
    <div>
    </div>

    <div>
        <button class="m-4 btn btn-secondary" @click="getData">Show bets</button>
        <div v-if="responseData">
            <p class="fw-bold">Bets avaliable:</p>
            <ul class="list-unstyled">
                <li v-for="(item, index) in responseData" :key="index">{{ index }} - {{ item.bet }}</li>
            </ul>
        </div>
    </div>
</template>

<script>
    import { getToken, fetchData } from '@/services/apiService'

    export default {
        name: 'ApiData',

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
                console.log("testing formdata", this.formData);
                const url = `${this.baseUrl}api-token-auth/`;
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

            getData() {
                fetchData().then(data => {
                    this.responseData = data
                });
            }
        }
    };
</script>