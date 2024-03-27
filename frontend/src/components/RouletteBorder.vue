<template>
    <div class="container d-flex flex-row justify-content-center">
        <div class="grid-container p-3">
            <div class="d-flex flex-row justify-content-center">
                <div class="d-flex align-items-center bg-green m-1 me-3 p-2 border border-white col0">
                    <p class="fs-1 mb-0 text-center bet-text"> 0 </p>
                </div>
                <div>
                    <div class="row" v-for="(row, index) in rows" :key="index">
                        <div class="col nbs border border-white border-3 d-flex justify-content-center align-items-center" v-for="col in 12" :key="col" :class="`col${col*3-row+1}`" :style="{ backgroundColor: getColor(col * 3 - row + 1) }">
                            {{ col * 3 - row + 1 }}
                        </div>
                    </div>
                </div>
                <div class="two_to_one"> 
                    <div class="col nbs border border-white border-3 ms-2 d-flex align-items-center justify-content-center" v-for="row in 3" :key="row">
                        <p class="text-center m-0">2 to 1</p>
                    </div>
                </div>
            </div>
            <div>
                <div class="d-flex justify-content-center">
                    <div class="row bets-container">
                        <div class="col m-1 bg-green border border-white" v-for="col in bet_dozens" :key="col">
                            <div class="p-3">
                                <h3 class="text-center m-0 bet-text">{{ col }}</h3>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-center">
                    <div class="row bets-container">
                        <div class="col m-1 bg-green border border-white" v-for="col in bets" :key="col">
                            <div class="p-1">
                                <h3 class="text-center m-0 bet-text">{{ col }}</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
    export default {

        name: 'RouletteComponent',
        data() {
            return {
                roleta: {
                    1: "red", 2: "black", 3: "red",
                    4: "black", 5: "red", 6: "black",
                    7: "red", 8: "black", 9: "red",
                    10: "black", 11: "black", 12: "red",
                    13: "black", 14: "red", 15: "black",
                    16: "red", 17: "black", 18: "red",
                    19: "red", 20: "black", 21: "red",
                    22: "black", 23: "red", 24: "black",
                    25: "red", 26: "black", 27: "red",
                    28: "black", 29: "black", 30: "red",
                    31: "black", 32: "red", 33: "black", 
                    34: "red", 35: "black", 36: "red"
                },
                bet_dozens: ["1st 12", "2nd 12", "3rd 12"],
                bets: ["1 to 18","Even","Red","Black","Odd","19 to 36"]
                // rouletteWheelNumbers = [ 
                //     0, 32, 15, 19, 4, 21, 2, 25,
                //     17, 34, 6, 27, 13, 36, 11,
                //     30, 8, 23,10, 5, 24, 16, 33,
                //     1, 20, 14, 31, 9, 22, 18, 29,
                //     7, 28, 12, 35, 3, 26
                // ];
            };
        },
        computed: {
            rows() {
                return Math.ceil(Object.keys(this.roleta).length / 12);
        }
        },
        methods: {
            getColor(number) {
                return this.roleta[number]; 
            }
        }
    };
</script>

<style scoped>
    .grid-container {
        width: 750px;
        background-color: green;
    }
    
    .col0 {
        border-bottom-left-radius: 100%;
        border-top-left-radius: 100%;
    }

    .bet-text {
        font-size: 13px;
        font-weight: bold;
        color: white;
    }

    .nbs {
        height: 50px;
        width: 50px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        transform: rotate(-90deg);
        -webkit-transform: rotate(-90deg);
    }

    .two_to_one .nbs {
        font-size: 13px;
    }

    .bets-container {
        width: 44rem;
    }

</style>