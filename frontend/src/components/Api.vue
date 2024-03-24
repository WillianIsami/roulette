<template>
    <div>
        <button @click="getPermission">Get permission to get data</button>
    </div>

    <div>
      <button @click="getData">Show data</button>
      <div v-if="responseData">
        <h2>Data Received:</h2>
        <pre>{{ responseData }}</pre>
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
            };
        },
        methods: {
            getPermission() {
                getToken();
            },

            getData() {
                fetchData();
            }
        }
    };
    </script>
