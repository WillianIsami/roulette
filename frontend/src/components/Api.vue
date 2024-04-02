<template>
    <div>
        <button class="m-4 btn btn-success" @click="getData">Show bets</button>
        <div v-if="responseData === true">
            <p class="fw-bold">Bets avaliable:</p>
            <ul class="list-unstyled">
                <li v-for="(item, index) in users" :key="index">{{ index }} - {{ item.bet }}</li>
            </ul>
        </div>
        <div v-else-if="responseData === false">
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
                responseData: null,
                users: []
            };
        },
        methods: {
            async getData () {
                this.responseData = true;
                const response = await fetchData();
                this.users = response;
            },
        }
    };
</script>