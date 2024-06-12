<template>
  <div class="mt-3 mb-5 roulette">
    <div class="arrow">
      <img src="https://i.imgur.com/k6g31Sg.png">
    </div>
    <div class="wheel">
      <img src="../assets/imgs/wheel.png" :style="{ transform: `rotate(-${currentLength}deg)` }">
    </div>
  </div>
  <RouletteBorder @spin="spin" />
</template>
  
<script>
  import RouletteBorder from './RouletteBorder.vue';

  export default {
    name: "WheelComponent",
    components: {
      RouletteBorder
    },
    data() {
      return {
        numbers: [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22,18, 29, 7, 28, 12, 35, 3, 26],
        currentLength: -4.86,
        completeCircle: 0,
      };
    },
    methods: {
      spin() {
        let random = parseInt(localStorage.getItem("drawn_number"))
        let positionArrNum = this.numbers.indexOf(random)
        this.currentLength += 1080 + this.completeCircle + positionArrNum * 9.729
        this.completeCircle = 1080 + Math.abs(37-positionArrNum) * 9.729
      },
    },
  };
</script>
  
<style scoped>
body {
  margin: 0;
  background: #1B1B21;
}

.roulette {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.wheel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.wheel img {
  transition: transform 10s cubic-bezier(0.19, 1, 0.22, 1);
  border-radius: 50%;
  box-shadow: 0 0 15px black;
  width: 60%;
  max-width: 500px;
  transform: rotate(0deg);
}

.arrow {
  margin-bottom: -15px;
  z-index: 99;
  filter: drop-shadow(0 0 8px black)
}
</style>
