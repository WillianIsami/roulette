<template>
  <div
    class="container d-flex flex-column justify-content-center disable-select rounded-pill"
  >
    <div class="d-flex flex-row justify-content-center">
      <div
        class="d-flex align-items-center bg-green me-3 p-2 border border-white col0"
        @click="inList(0)"
      >
        <div
          v-if="selectedBets[0]"
          class="chip bg-primary"
        >
          <span class="chipSpan">{{ selectedBets[0][0] }}</span>
        </div>
        <p class="fs-1 mb-0 text-center">0</p>
      </div>
      <div>
        <div class="row" v-for="row in 3" :key="row">
          <div
            class="col nbs border border-white d-flex justify-content-center align-items-center"
            v-for="col in 12"
            :key="col"
            :id="`num${col * 3 - row + 1}`"
            :style="{ backgroundColor: getColor(col * 3 - row + 1) }"
          >
            {{ col * 3 - row + 1 }}
          </div>
        </div>
      </div>
      <div class="two_to_one">
        <div
          class="col nbs border border-white ms-3 d-flex align-items-center justify-content-center"
          v-for="row in 3"
          :key="row"
          @click="twoToOne(row)"
        >
          <div
            v-if="selectedBets[`line${row}`]"
            class="chip bg-primary"
          >
            <span class="chipSpan">{{ selectedBets[`line${row}`][0] }}</span>
          </div>
          <p class="text-center">2:1</p>
        </div>
      </div>
      <div class="position-absolute parent">
        <div class="medium" v-for="row in 6" :key="row">
          <div
            class="nbs-transparent child d-flex justify-content-center align-items-center"
            v-for="col in 25"
            :key="col"
            @click="inList(col * 6 - row + 1)"
          >
            <div
              v-if="selectedBets[col*6-row+1]"
              class="chip bg-primary"
            >
              <span class="chipSpan">{{ selectedBets[col*6-row+1][0] }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="bets-container">
      <div class="d-flex justify-content-center">
        <div class="row w-100">
          <div
            class="col mt-1 border border-white bet-text"
            v-for="(col, index) in bet_dozens"
            :key="col"
            @click="genDozens(index, col)"
          >
            <div class="p-3">
              <div
                v-if="selectedBets[col]"
                class="chip bg-primary"
              >
                <span class="chipSpan">{{ selectedBets[col][0] }}</span>
              </div>
              <p class="text-center m-0">{{ col }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex justify-content-center">
        <div class="row w-100">
          <div
            class="col border border-white bet-text"
            v-for="col in bets"
            :key="col"
            @click="generalBets(col)"
          >
            <div class="p-1">
              <div
                v-if="selectedBets[col]"
                class="chip bg-primary"
              >
                <span class="chipSpan">{{ selectedBets[col][0] }}</span>
              </div>
              <p class="text-center m-0">{{ col }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <button class="m-4 btn btn-danger" @click="clearBets">Clear bets</button>
  <button class="m-4 btn btn-success" @click="sendAllBets">Spin</button>
  <p class="text-danger" v-if="betNotSelected">Select a bet</p>
  <p class="fw-bold text-danger" v-if="drawnNum !== 0">Drawn Number: {{ drawnNum }}</p>
</template>

<script>
import { sendBets } from '@/services/apiService';

export default {
  name: "RouletteComponent",
  data() {
    return {
      roulette: {
        1: "red",
        2: "black",
        3: "red",
        4: "black",
        5: "red",
        6: "black",
        7: "red",
        8: "black",
        9: "red",
        10: "black",
        11: "black",
        12: "red",
        13: "black",
        14: "red",
        15: "black",
        16: "red",
        17: "black",
        18: "red",
        19: "red",
        20: "black",
        21: "red",
        22: "black",
        23: "red",
        24: "black",
        25: "red",
        26: "black",
        27: "red",
        28: "black",
        29: "black",
        30: "red",
        31: "black",
        32: "red",
        33: "black",
        34: "red",
        35: "black",
        36: "red",
      },
      bet_dozens: ["1st 12", "2nd 12", "3rd 12"],
      bets: ["1-18", "Even", "Red", "Black", "Odd", "19-36"],
      straightUpBetArr: [0],
      splitHorizontalArr: [],
      splitVerticalArr: [],
      streetArr: [],
      twoStreetArr: [],
      cornerArr: [],
      sixLineArr: [],
      zeroBetArr: [1, 2, 3, 4, 5, 6],
      selectedBets: {},
      baseUrl: process.env.VUE_APP_BASE_URL,
      betNotSelected: false,
      drawnNum: 0,
    };
  },

  mounted() {
    this.genArrBet(this.straightUpBetArr, 8, 144, 3);
    this.genArrBet(this.splitHorizontalArr, 14, 138, 3);
    this.genArrBet(this.splitVerticalArr, 9, 143, 2);
    this.genArrBet(this.cornerArr, 15, 137, 2);
    this.genArrBet(this.streetArr, 7, 139, 1);
    this.genArrBet(this.twoStreetArr, 13, 133, 1);
  },

  methods: {
    emitSpin() {
      this.$emit('spin');
    },

    clearBets() {
      this.selectedBets = {};
    },

    getColor(number) {
      return this.roulette[number];
    },

    sendAllBets() {
      if (Object.keys(this.selectedBets).length !== 0) {
        const url = `${this.baseUrl}/spin/`;
        const options = {
          method: 'POST',
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",  
          },
          credentials: 'include',
          body: JSON.stringify(this.selectedBets)
        }
        this.betNotSelected = false
        const response = sendBets(url, options)
        response.then((data) => {
          localStorage.setItem("drawn_number", data["drawn_number"])
          if (data["drawn_number"]) {
            this.emitSpin()
            this.drawnNum = data["drawn_number"]
          }
        })
        .catch((error) => {
          console.error("Error: ", error)
        })
      } else {
        this.betNotSelected = true
      }
    },
    
    handleGenBets(betType, resultArr) {
      if (this.selectedBets[betType]) {
        this.selectedBets[betType][0] = parseInt(this.selectedBets[betType][0]) + 5.00
        console.log("existe" ,this.selectedBets)
        return
      }
      this.selectedBets[betType] = [5.00, betType, resultArr]
      console.log("não existe" ,this.selectedBets)
    },

    twoToOne(num) {
      let row = {
        3: 1,
        2: 2,
        1: 3,
      };
      let number = row[num];
      let resultRange = Array.from({ length: 12 }, (_, i) => number + i * 3);
      let betType = `line${num}`
      this.handleGenBets(betType, resultRange)
      console.log(`numbers: ${resultRange}`);
    },

    genDozens(num, betType) {
      // "1st 12", "2nd 12", "3rd 12"
      num = num * 12;
      let resultRange = Array.from({ length: 12 }, (_, i) => num + i + 1);
      this.handleGenBets(betType, resultRange)
      console.log(`numbers: ${resultRange}`);
    },

    generalBets(bet) {
      let cleanBet = bet.trim().toLowerCase();
      let bets = {
        "1-18": Array.from({ length: 18 }, (_, i) => i + 1),
        "19-36": Array.from({ length: 18 }, (_, i) => i + 19),
        "black": Object.keys(this.roulette).filter(
          (key) => this.roulette[key] === "black",
        ),
        "red": Object.keys(this.roulette).filter(
          (key) => this.roulette[key] === "red",
        ),
        "even": Array.from({ length: 36 }, (_, i) => i + 1).filter(
          (num) => num % 2 === 0,
        ),
        "odd": Array.from({ length: 36 }, (_, i) => i + 1).filter(
          (num) => num % 2 === 1,
        ),
      };
      let resultBet = bets[cleanBet];
      this.handleGenBets(bet, resultBet)
    },

    genArrBet(arr, start, end, leng) {
      for (let rowNumber = start; rowNumber <= end; rowNumber += 12) {
        Array.prototype.push.apply(
          arr,
          Array.from({ length: leng }, (_, i) => rowNumber + i * 2),
        );
      }
    },

    handleBet(number, betType, betArr, indexMultiplier, halfSizeArr, initialArr) {
      const index = number === 0 ? number : betArr.indexOf(number);
      let resultArr = []
      if (betType !== "straight-up") {
        resultArr = initialArr.map(
          (value) => value + index * indexMultiplier + (halfSizeArr ? Math.floor(index/2) : 0)
        )
      }
      if (this.selectedBets[number]) {
        this.selectedBets[number][0] = parseInt(this.selectedBets[number][0]) + 5.00
        console.log("existe" ,this.selectedBets)
        return
      }
      this.selectedBets[number] = [5.00, betType, resultArr.length ? resultArr : [index]]
      console.log("não existe" ,this.selectedBets)
    },

    inList(number) {
      // let example = {
      //    "num1": [0, "straight-up", [1]]
      // }
      if (number === 0) {
        this.handleBet(number, "straight-up", number, 1, false, [])
      } 
      else if (this.straightUpBetArr.includes(number)) {
        this.handleBet(number, "straight-up", this.straightUpBetArr, 1, false, [])
      } 
      else if (this.splitHorizontalArr.includes(number)) {
        this.handleBet(number, "split", this.splitHorizontalArr, 1, false, [1,4])
      } 
      else if (this.splitVerticalArr.includes(number)) {
        this.handleBet(number, "split", this.splitVerticalArr, 1, true, [1,2])
      } 
      else if (this.streetArr.includes(number)) {
        this.handleBet(number, "street", this.streetArr, 3, false, [1,2,3])
      } 
      else if (this.twoStreetArr.includes(number)) {
        this.handleBet(number, "two_street", this.twoStreetArr, 3, false, [1,2,3,4,5,6])
      } 
      else if (this.cornerArr.includes(number)) {
        this.handleBet(number, "corner", this.cornerArr, 1, true, [1,2,4,5])
      } else if (this.zeroBetArr.includes(number)) {
        let zeroBets = {
          1: [0, 1, 2, 3],
          2: [0, 1],
          3: [0, 1, 2],
          4: [0, 2],
          5: [0, 2, 3],
          6: [0, 3],
        };
        if (this.selectedBets[number]) {
          this.selectedBets[number][0] = parseInt(this.selectedBets[number][0]) + 5
          console.log("exist" ,this.selectedBets)
          return
        }
        this.selectedBets[number] = [5, "zero_bets", zeroBets[number]]
        console.log("don't exist" ,this.selectedBets)
      }
    },
  },
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

.chip {
  width: 16px;
  height: 16px;
  background-color: #fff;
  border: 1px solid white;
  border-radius: 100%;
  position: absolute;
}

.chipSpan {
  color: #000;
  font-weight: bold;
  font-size: 10px;
  position: relative;
  display: block;
  text-align: center;
}
</style>
