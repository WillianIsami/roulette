<template>
    <div>
        <button class="m-4 btn btn-secondary" @click="getData">Show bets</button>
        <div v-if="responseData == 1">
            <p class="fw-bold">Bets avaliable:</p>
            <ul class="list-unstyled">
                <li v-for="(item, index) in responseData" :key="index">{{ index }} - {{ item.bet }}</li>
            </ul>
        </div>
        <div v-else-if="responseData == 0">
            <p>Login with your account <RouterLink class="fw-bold link-success" to="/login">here</RouterLink> to see all bets avaliable</p>
        </div>
    </div>
</template>

<script>
    import { fetchData } from '@/services/apiService';

    export default {
        name: 'ApiData',

        data() {
            return {
                responseData: null
            };
        },
        methods: {
            getData() {
                fetchData().then(data => {
                    this.responseData = data
                });
            },
        }
    };
</script>