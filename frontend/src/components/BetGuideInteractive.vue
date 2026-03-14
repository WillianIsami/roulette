<template>
  <section class="glass-card p-4 mb-3">
    <div class="guide-header mb-3">
      <h2 class="section-title mb-1">{{ $t("betGuide.title") }}</h2>
      <p class="mb-0 text-muted">{{ $t("betGuide.lead") }}</p>
    </div>

    <div class="type-grid mb-3">
      <button
        v-for="item in betExamples"
        :key="item.id"
        type="button"
        class="type-btn"
        :class="{ active: selectedBetId === item.id }"
        @click="selectedBetId = item.id"
      >
        <span>{{ betTypeLabel(item.id) }}</span>
      </button>
    </div>

    <div class="guide-layout">
      <div class="guide-summary">
        <p class="pill-label mb-2">{{ $t(selectedExample.categoryKey) }}</p>
        <h3 class="mb-2">{{ betTypeLabel(selectedExample.id) }}</h3>
        <p class="mb-2">{{ $t(selectedExample.hintKey) }}</p>
        <p class="mb-2"><strong>{{ $t("betGuide.coverage") }}:</strong> {{ selectedExample.numbers.length }}</p>
        <p class="mb-2"><strong>{{ $t("betGuide.payout") }}:</strong> {{ selectedExample.payout }}</p>
        <p class="mb-2">
          <strong>{{ $t("betGuide.stakeExample", { stake: stakeExample.toFixed(2) }) }}:</strong>
          +{{ hitProfit.toFixed(2) }}
        </p>
        <p class="mb-0 text-muted">{{ $t("betGuide.lossExample", { stake: stakeExample.toFixed(2) }) }}</p>
      </div>

      <div class="guide-board-wrap">
        <div class="guide-board">
          <div class="guide-main-row">
            <div class="guide-zero" :class="{ covered: isCovered(0) }">
              <span>0</span>
              <div v-if="showZeroMarker" class="guide-marker marker-zero" />
            </div>

            <div class="guide-grid-wrap">
              <div class="guide-grid">
                <template v-for="(row, rowIndex) in numberRows" :key="`row-${rowIndex}`">
                  <div
                    v-for="number in row"
                    :key="`g-num-${number}`"
                    class="guide-number"
                    :class="[`number-${roulette[number]}`, { covered: isCovered(number) }]"
                  >
                    <span>{{ number }}</span>
                    <div v-if="isCovered(number) && selectedExample.numbers.length <= 6" class="coverage-dot" />
                  </div>
                </template>
              </div>

              <div v-if="showGridMarker" class="guide-marker" :style="gridMarkerStyle" />
            </div>

            <div class="guide-line-col">
              <div
                v-for="line in [1, 2, 3]"
                :key="`line-${line}`"
                class="guide-line-cell"
                :class="{ active: selectedExample.lineCell === line }"
              >
                2:1
              </div>
            </div>
          </div>

          <div class="guide-outside">
            <div class="outside-row three">
              <div
                v-for="label in outsideDozens"
                :key="label"
                class="outside-cell"
                :class="{ active: selectedExample.outsideCell === label }"
              >
                {{ betTypeLabel(label) }}
              </div>
            </div>
            <div class="outside-row six">
              <div
                v-for="label in outsideSimple"
                :key="label"
                class="outside-cell"
                :class="{ active: selectedExample.outsideCell === label }"
              >
                {{ betTypeLabel(label) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { translateBetType } from "@/utils/betType";

export default {
  name: "BetGuideInteractive",
  data() {
    return {
      stakeExample: 5,
      selectedBetId: "straight-up",
      outsideDozens: ["1st 12", "2nd 12", "3rd 12"],
      outsideSimple: ["1-18", "even", "red", "black", "odd", "19-36"],
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
      betExamples: [
        {
          id: "straight-up",
          categoryKey: "betGuide.categoryInside",
          payout: "35:1",
          multiplier: 35,
          numbers: [17],
          hintKey: "betGuide.hints.straightUp",
        },
        {
          id: "split",
          categoryKey: "betGuide.categoryInside",
          payout: "17:1",
          multiplier: 17,
          numbers: [14, 17],
          hintKey: "betGuide.hints.split",
        },
        {
          id: "street",
          categoryKey: "betGuide.categoryInside",
          payout: "11:1",
          multiplier: 11,
          numbers: [16, 17, 18],
          hintKey: "betGuide.hints.street",
        },
        {
          id: "two street",
          categoryKey: "betGuide.categoryInside",
          payout: "5:1",
          multiplier: 5,
          numbers: [16, 17, 18, 19, 20, 21],
          hintKey: "betGuide.hints.twoStreet",
        },
        {
          id: "corner",
          categoryKey: "betGuide.categoryInside",
          payout: "8:1",
          multiplier: 8,
          numbers: [17, 18, 20, 21],
          hintKey: "betGuide.hints.corner",
        },
        {
          id: "line",
          categoryKey: "betGuide.categoryOutside",
          payout: "2:1",
          multiplier: 2,
          numbers: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
          lineCell: 1,
          hintKey: "betGuide.hints.line",
        },
        {
          id: "1st 12",
          categoryKey: "betGuide.categoryOutside",
          payout: "2:1",
          multiplier: 2,
          numbers: Array.from({ length: 12 }, (_, i) => i + 1),
          outsideCell: "1st 12",
          hintKey: "betGuide.hints.first12",
        },
        {
          id: "2nd 12",
          categoryKey: "betGuide.categoryOutside",
          payout: "2:1",
          multiplier: 2,
          numbers: Array.from({ length: 12 }, (_, i) => i + 13),
          outsideCell: "2nd 12",
          hintKey: "betGuide.hints.second12",
        },
        {
          id: "3rd 12",
          categoryKey: "betGuide.categoryOutside",
          payout: "2:1",
          multiplier: 2,
          numbers: Array.from({ length: 12 }, (_, i) => i + 25),
          outsideCell: "3rd 12",
          hintKey: "betGuide.hints.third12",
        },
        {
          id: "1-18",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: Array.from({ length: 18 }, (_, i) => i + 1),
          outsideCell: "1-18",
          hintKey: "betGuide.hints.low",
        },
        {
          id: "even",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: Array.from({ length: 36 }, (_, i) => i + 1).filter((n) => n % 2 === 0),
          outsideCell: "even",
          hintKey: "betGuide.hints.even",
        },
        {
          id: "red",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
          outsideCell: "red",
          hintKey: "betGuide.hints.red",
        },
        {
          id: "black",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
          outsideCell: "black",
          hintKey: "betGuide.hints.black",
        },
        {
          id: "odd",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: Array.from({ length: 36 }, (_, i) => i + 1).filter((n) => n % 2 === 1),
          outsideCell: "odd",
          hintKey: "betGuide.hints.odd",
        },
        {
          id: "19-36",
          categoryKey: "betGuide.categoryOutside",
          payout: "1:1",
          multiplier: 1,
          numbers: Array.from({ length: 18 }, (_, i) => i + 19),
          outsideCell: "19-36",
          hintKey: "betGuide.hints.high",
        },
      ],
    };
  },
  computed: {
    selectedExample() {
      return this.betExamples.find((item) => item.id === this.selectedBetId) || this.betExamples[0];
    },
    hitProfit() {
      return this.stakeExample * this.selectedExample.multiplier;
    },
    numberRows() {
      return Array.from({ length: 3 }, (_, row) =>
        Array.from({ length: 12 }, (_, col) => this.numberAt(row, col)),
      );
    },
    showGridMarker() {
      return !this.selectedExample.outsideCell && !this.selectedExample.lineCell && !this.selectedExample.numbers.includes(0);
    },
    showZeroMarker() {
      return this.selectedExample.numbers.includes(0);
    },
    gridMarkerStyle() {
      const positions = this.selectedExample.numbers.map((number) => this.numberPosition(number));
      const avgCol = positions.reduce((acc, point) => acc + point.col, 0) / positions.length;
      const avgRow = positions.reduce((acc, point) => acc + point.row, 0) / positions.length;
      return {
        left: `${((avgCol + 0.5) / 12) * 100}%`,
        top: `${((avgRow + 0.5) / 3) * 100}%`,
      };
    },
  },
  methods: {
    betTypeLabel(type) {
      return translateBetType((key, params) => this.$t(key, params), type);
    },
    numberAt(row, col) {
      const rowOffset = [3, 2, 1];
      return col * 3 + rowOffset[row];
    },
    numberPosition(number) {
      const idx = number - 1;
      const col = Math.floor(idx / 3);
      const rowOrder = idx % 3;
      const map = {
        2: 0,
        1: 1,
        0: 2,
      };
      return {
        col,
        row: map[rowOrder],
      };
    },
    isCovered(number) {
      return this.selectedExample.numbers.includes(number);
    },
  },
};
</script>

<style scoped>
.guide-header p {
  max-width: 70ch;
}

.type-grid {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
}

.type-btn {
  border: 1px solid #dbc59a;
  border-radius: 10px;
  background: #fffdf7;
  color: #244434;
  font-weight: 700;
  font-size: 0.83rem;
  padding: 0.5rem 0.6rem;
  transition: 0.2s ease;
}

.type-btn:hover {
  border-color: #b38a3e;
  transform: translateY(-1px);
}

.type-btn.active {
  border-color: #a7791f;
  background: #f2e3bf;
  color: #123223;
}

.guide-layout {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(250px, 340px) minmax(0, 1fr);
}

.guide-summary {
  border: 1px solid #e1d5bb;
  border-radius: 14px;
  background: #fffdf8;
  padding: 0.9rem;
}

.guide-summary h3 {
  font-family: "Racing Sans One", sans-serif;
  color: #1d4631;
}

.guide-board-wrap {
  overflow-x: auto;
  text-align: center;
}

.guide-board {
  --cell: clamp(1.95rem, 2.75vw, 2.45rem);
  --zero-w: calc(var(--cell) * 1.22);
  --gap: 0.45rem;
  display: inline-block;
  width: auto;
  min-width: fit-content;
  border: 1px solid #d5ba84;
  border-radius: 14px;
  background: linear-gradient(180deg, #0f6a40 0%, #0d5635 100%);
  padding: 0.6rem;
  text-align: left;
}

.guide-main-row {
  display: flex;
  gap: var(--gap);
}

.guide-zero {
  width: var(--zero-w);
  height: calc(var(--cell) * 3);
  border: 1px solid rgba(255, 255, 255, 0.72);
  border-radius: 18px 0 0 18px;
  background: #137f4f;
  color: #fff;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.guide-zero.covered {
  box-shadow: inset 0 0 0 2px #ffd373;
}

.guide-grid-wrap {
  position: relative;
}

.guide-grid {
  display: grid;
  grid-template-columns: repeat(12, var(--cell));
  grid-template-rows: repeat(3, var(--cell));
}

.guide-number {
  border: 1px solid rgba(255, 255, 255, 0.72);
  color: #fff;
  font-weight: 700;
  font-size: 0.76rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.number-red {
  background: #be2d33;
}

.number-black {
  background: #181f24;
}

.guide-number.covered {
  box-shadow: inset 0 0 0 2px #ffcf64;
}

.coverage-dot {
  position: absolute;
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 999px;
  background: #fbd786;
  box-shadow: 0 0 0 1px #3f2a0f;
}

.guide-marker {
  position: absolute;
  width: 0.62rem;
  height: 0.62rem;
  border-radius: 999px;
  background: rgba(255, 235, 184, 0.25);
  border: 1px solid #f5d28f;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 0 1px rgba(39, 25, 7, 0.35);
}

.marker-zero {
  top: 50%;
  left: 50%;
}

.guide-line-col {
  display: grid;
  grid-template-rows: repeat(3, var(--cell));
}

.guide-line-cell {
  width: calc(var(--cell) * 1.25);
  border: 1px solid rgba(255, 255, 255, 0.72);
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
  font-weight: 700;
  font-size: 0.78rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.guide-line-cell.active {
  box-shadow: inset 0 0 0 2px #ffd373;
}

.guide-outside {
  margin-left: calc(var(--zero-w) + var(--gap));
  margin-top: var(--gap);
  width: calc(var(--cell) * 12);
}

.outside-row {
  display: grid;
}

.outside-row.three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.outside-row.six {
  grid-template-columns: repeat(6, minmax(0, 1fr));
}

.outside-cell {
  border: 1px solid rgba(255, 255, 255, 0.72);
  min-height: calc(var(--cell) * 0.8);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.12);
}

.outside-cell.active {
  box-shadow: inset 0 0 0 2px #ffd373;
}

@media (max-width: 980px) {
  .guide-layout {
    grid-template-columns: 1fr;
  }

  .guide-board-wrap {
    text-align: left;
  }
}
</style>
