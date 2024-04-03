<template>
    <div class="container d-flex flex-column justify-content-center disable-select">
        <div class="d-flex flex-row justify-content-center">
            <div class="d-flex align-items-center bg-green me-3 p-2 border border-white col0">
                <p class="fs-1 mb-0 text-center"> 0 </p>
            </div>
            <div>
                <div class="row" v-for="row in 3" :key="row">
                    <div class="col nbs border border-white d-flex justify-content-center align-items-center" v-for="col in 12" :key="col" :id="`col${col*3-row+1}`" :style="{ backgroundColor: getColor(col * 3 - row + 1) }">
                        {{ col * 3 - row + 1 }}
                    </div>
                </div>
            </div>
            <div class="two_to_one"> 
                <div class="col nbs border border-white ms-3 d-flex align-items-center justify-content-center" v-for="row in 3" :key="row">
                    <p class="text-center">2:1</p>
                </div>
            </div>
            <div class="position-absolute parent">
                <div class="medium" v-for="row in 6" :key="row">
                    <div class="
                    nbs-transparent child border border-primary d-flex justify-content-center align-items-center " v-for="col in 25" :key="col" @click="inList(col*6-row+1)">

                    </div>
                </div>
            </div>
        </div>
        <div class="bets-container">
            <div class="d-flex justify-content-center">
                <div class="row w-100">
                    <div class="col mt-1 border border-white bet-text" v-for="col in bet_dozens" :key="col">
                        <div class="p-3">
                            <p class="text-center m-0">{{ col }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="d-flex justify-content-center">
                <div class="row w-100">
                    <div class="col border border-white bet-text" v-for="col in bets" :key="col">
                        <div class="p-1">
                            <p class="text-center m-0">{{ col }}</p>
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
                    34: "red", 35: "black", 36: "red",
                },
                bet_dozens: ["1st 12", "2nd 12", "3rd 12"],
                bets: ["1-18","Even","Red","Black","Odd","19-36"],
                straightUpBetArr: [],
                splitArr: [],
                streetArr: [],
                cornerArr: [],
                sixLineArr: [],
            };
        },

        mounted() {
            this.genArrBet(this.straightUpBetArr , 8, 144, 3);
            this.genArrBet(this.splitArr, 14, 138, 3);
            this.genArrBet(this.cornerArr, 15, 137, 2);
        },

        methods: {
            getColor(number) {
                return this.roleta[number]; 
            },

            genArrBet(arr, start, end, leng) {
                for (let rowNumber = start; rowNumber <= end; rowNumber += 12) {
                    Array.prototype.push.apply(arr, Array.from({length: leng}, (_, i) => rowNumber + i * 2));
                }
            },

            inList(number) {
                // TODO: call functions and send values instead console.log
                if (this.straightUpBetArr.includes(number)) {
                    let straightIndex = this.straightUpBetArr.indexOf(number);
                    console.log(`${straightIndex+1}: ${number}`);
                }
                else if (this.splitArr.includes(number)) {
                    let splitIndex = this.splitArr.indexOf(number);
                    this.firstSplit = [1,4];
                    this.splitResultArr = this.firstSplit.map((value) => value + splitIndex);
                    console.log(`${number}: ${this.splitResultArr}`);
                }
                else if (this.cornerArr.includes(number)) {
                    let cornerIndex = this.cornerArr.indexOf(number);
                    this.firstCorner = [1,2,4,5];
                    this.cornerResultArr = this.firstCorner.map((value) => value + cornerIndex + Math.floor(cornerIndex/2));
                    console.log(`${number}: ${this.cornerResultArr}`);
                }
            }
        }
    };
</script>

<style scoped>
    .container {
        width: 80%;
        height: 20rem;
        max-width: 50rem;
        background-color: green;
    }
    
    .col0 {
        width: 3em;
        height: 5em;
        color: white;
        border-radius: 32px 0px 0px 32px;
    }

    .bet-text {
        width: 50px;
        font-size: 0.813rem;
        font-weight: bold;
        color: white;
    }

    .text-center {
        font-size: 0.8em;
    }
    
    .nbs {
        height: 2.1em;
        width: 2.1em;
        font-size: 0.813em;
        font-weight: bold;
        color: white;
        transform: rotate(-90deg);
        -webkit-transform: rotate(-90deg);
    }

    .nbs-large {
        font-weight: bold;
        color: white;
    }
    
    .disable-select {
        user-select: none;
    }

    .nbs-transparent {
        height: 10px;
        width: 5px;
    }

    .nbs-transparent-parent {
        width: 500px;
    }

    .first {
        width: 100%;
        height: 100%;
    }

    .transparent {
        color: transparent;
    }

    .parent {
        display: flex;
        flex-direction: column;
        margin-left: 20px;
        margin-top: 5px;
    }

    .medium {
        display: flex;
        flex-direction: row;
    }

    .child {
        width: 0.855em;
        height: 0.89em;
    }

    .bets-container {
        width: 26rem;
        margin: 0 auto;
    }

</style>