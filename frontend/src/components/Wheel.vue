<template>
  <section class="play-area glass-card p-3 p-md-4">
    <div class="d-flex flex-column flex-lg-row gap-4 align-items-start">
      <aside class="wheel-panel">
        <div class="panel-head mb-3">
          <h2 class="section-title">Mesa ao vivo</h2>
          <p class="mb-0">Clique em apostas, gire e acompanhe seu saldo.</p>
        </div>

        <div class="roulette mt-2 mb-3">
          <div class="arrow">
            <img src="https://i.imgur.com/k6g31Sg.png" alt="arrow" />
          </div>
          <div class="wheel">
            <img
              src="@/assets/imgs/wheel.png"
              alt="roulette wheel"
              :style="{ transform: `rotate(-${currentLength}deg)` }"
              @transitionend="onWheelTransitionEnd"
            />
          </div>
        </div>

        <div class="result-chip">
          <p class="mb-1">{{ isSpinning ? "Roleta girando..." : "Último número" }}</p>
          <strong>{{ isSpinning ? "?" : latestNumber === null ? "-" : latestNumber }}</strong>
        </div>
      </aside>

      <div class="table-panel flex-grow-1">
        <RouletteBorder
          :is-spinning="isSpinning"
          :resolved-spin-data="resolvedSpinData"
          @spin="spin"
        />
      </div>
    </div>
  </section>
</template>

<script>
import RouletteBorder from "./RouletteBorder.vue";

export default {
  name: "WheelComponent",
  components: {
    RouletteBorder,
  },
  data() {
    return {
      numbers: [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,
        5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
      ],
      currentLength: -4.86,
      completeCircle: 0,
      latestNumber: null,
      isSpinning: false,
      pendingSpinData: null,
      resolvedSpinData: null,
    };
  },
  methods: {
    spin(spinData) {
      if (!spinData || this.isSpinning) {
        return;
      }

      const parsedNumber = Number(spinData.drawn_number);
      const positionArrNum = this.numbers.indexOf(parsedNumber);
      if (positionArrNum < 0) {
        return;
      }

      this.isSpinning = true;
      this.pendingSpinData = spinData;
      this.resolvedSpinData = null;
      this.currentLength += 1080 + this.completeCircle + positionArrNum * 9.729;
      this.completeCircle = 1080 + Math.abs(37 - positionArrNum) * 9.729;
    },
    onWheelTransitionEnd(event) {
      if (!this.isSpinning || event.propertyName !== "transform") {
        return;
      }

      this.isSpinning = false;
      if (!this.pendingSpinData) {
        return;
      }

      this.latestNumber = Number(this.pendingSpinData.drawn_number);
      this.resolvedSpinData = this.pendingSpinData;
      this.pendingSpinData = null;
    },
  },
};
</script>

<style scoped>
.play-area {
  overflow: hidden;
}

.wheel-panel {
  width: min(100%, 420px);
  background: linear-gradient(165deg, #143f2d 0%, #0d2d20 100%);
  border-radius: 18px;
  color: #f6edd9;
  padding: 1rem;
  box-shadow: inset 0 0 0 1px rgba(244, 205, 126, 0.32);
}

.panel-head p {
  color: #d7cbb0;
  font-size: 0.92rem;
}

.roulette {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.wheel {
  display: flex;
  align-items: center;
  justify-content: center;
}

.wheel img {
  transition: transform 10s cubic-bezier(0.19, 1, 0.22, 1);
  border-radius: 50%;
  box-shadow: 0 0 22px rgba(0, 0, 0, 0.45);
  width: 100%;
  max-width: 290px;
}

.arrow {
  margin-bottom: -15px;
  z-index: 2;
  filter: drop-shadow(0 0 8px black);
}

.arrow img {
  width: 32px;
}

.result-chip {
  background: rgba(251, 230, 181, 0.14);
  border: 1px solid rgba(245, 217, 147, 0.35);
  border-radius: 14px;
  padding: 0.7rem;
  text-align: center;
}

.result-chip p {
  margin: 0;
  color: #d3c3a0;
  font-size: 0.82rem;
}

.result-chip strong {
  font-family: "Racing Sans One", sans-serif;
  color: #fbe7bc;
  font-size: 1.8rem;
  line-height: 1;
}

.table-panel {
  width: 100%;
}

@media (max-width: 1100px) {
  .wheel-panel {
    width: 100%;
  }
}
</style>
