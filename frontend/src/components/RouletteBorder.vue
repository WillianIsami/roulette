<template>
  <div class="roulette-border">
    <section class="info-grid mb-3">
      <div class="wallet-box">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <h3 class="section-title">{{ $t("roulette.walletTitle") }}</h3>
          <span class="pill-label">{{ $t("common.virtualCoins") }}</span>
        </div>
        <p class="wallet-value mb-2">{{ Number(wallet.balance || 0).toFixed(2) }}</p>
        <p class="wallet-note mb-3">{{ $t("roulette.walletNote") }}</p>
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="amount in quickDeposits"
            :key="amount"
            type="button"
            class="btn btn-sm btn-brand-outline"
            :disabled="loadingWallet"
            @click="deposit(amount)"
          >
            +{{ amount }}
          </button>
        </div>
      </div>

      <div class="bet-box">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <h3 class="section-title">{{ $t("roulette.currentBetTitle") }}</h3>
          <span class="pill-label">{{ $t("common.total") }}: {{ totalSelectedAmount.toFixed(2) }}</span>
        </div>
        <label class="chip-label" for="chipValue">{{ $t("roulette.chipValue") }}</label>
        <select id="chipValue" v-model.number="chipValue" class="form-select mb-3 chip-select">
          <option v-for="value in chipOptions" :key="value" :value="value">
            {{ $t("roulette.chipSuffix", { value }) }}
          </option>
        </select>

        <div class="d-flex flex-wrap gap-2">
          <button type="button" class="btn btn-outline-danger" @click="clearBets">{{ $t("roulette.clearBets") }}</button>
          <button
            type="button"
            class="btn btn-success"
            :disabled="isSubmitting || isSpinning || totalSelectedAmount <= 0"
            @click="sendAllBets"
          >
            {{ isSubmitting || isSpinning ? $t("roulette.spinning") : $t("roulette.spinWheel") }}
          </button>
        </div>
      </div>
    </section>

    <section class="table-card mb-3">
      <div class="table-scroll">
        <div class="roulette-table disable-select">
          <div class="board-row">
            <div class="board-core">
              <div
                class="zero-cell board-zone"
                role="button"
                tabindex="0"
                @click="placeDirectNumberBet(0)"
                @keydown.enter.prevent="placeDirectNumberBet(0)"
                @keydown.space.prevent="placeDirectNumberBet(0)"
              >
                <span class="zero-label">0</span>
                <div v-if="selectedBets['num-0']" class="chip number-chip bg-warning">
                  <span class="chipSpan">{{ selectedBets["num-0"][0] }}</span>
                </div>

                <button
                  v-for="marker in zeroMarkers"
                  :key="marker.key"
                  type="button"
                  class="zero-marker"
                  :class="marker.markerType"
                  :style="zeroMarkerStyle(marker)"
                  @click.stop="placeMarkerBet(marker)"
                >
                  <span class="marker-dot" />
                  <div v-if="selectedBets[marker.key]" class="chip marker-chip bg-warning">
                    <span class="chipSpan">{{ selectedBets[marker.key][0] }}</span>
                  </div>
                </button>
              </div>

              <div class="grid-wrap">
                <div class="number-grid">
                  <template v-for="(row, rowIndex) in numberRows" :key="`row-${rowIndex}`">
                    <button
                      v-for="number in row"
                      :key="`num-${number}`"
                      type="button"
                      class="number-cell"
                      :class="`number-${getColor(number)}`"
                      @click="placeDirectNumberBet(number)"
                    >
                      <span>{{ number }}</span>
                      <div v-if="selectedBets[`num-${number}`]" class="chip number-chip bg-warning">
                        <span class="chipSpan">{{ selectedBets[`num-${number}`][0] }}</span>
                      </div>
                    </button>
                  </template>
                </div>

                <div class="marker-layer">
                  <button
                    v-for="marker in insideMarkers"
                    :key="marker.key"
                    type="button"
                    class="board-marker"
                    :class="`marker-${marker.markerType}`"
                    :style="markerStyle(marker)"
                    @click="placeMarkerBet(marker)"
                  >
                    <span class="marker-dot" />
                    <div v-if="selectedBets[marker.key]" class="chip marker-chip bg-warning">
                      <span class="chipSpan">{{ selectedBets[marker.key][0] }}</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>

            <div class="line-column">
              <button
                v-for="row in [1, 2, 3]"
                :key="`line-${row}`"
                type="button"
                class="line-cell"
                @click="twoToOne(row)"
              >
                <span>2:1</span>
                <div v-if="selectedBets[`line${row}`]" class="chip number-chip bg-warning">
                  <span class="chipSpan">{{ selectedBets[`line${row}`][0] }}</span>
                </div>
              </button>
            </div>
          </div>

          <div class="outside-bets">
            <div class="outside-row outside-row-three">
              <button
                v-for="(dozen, index) in bet_dozens"
                :key="dozen"
                type="button"
                class="outside-cell"
                @click="genDozens(index, dozen)"
              >
                <span>{{ outsideBetLabel(dozen) }}</span>
                <div v-if="selectedBets[dozen]" class="chip number-chip bg-warning">
                  <span class="chipSpan">{{ selectedBets[dozen][0] }}</span>
                </div>
              </button>
            </div>

            <div class="outside-row outside-row-six">
              <button
                v-for="bet in bets"
                :key="bet"
                type="button"
                class="outside-cell"
                @click="generalBets(bet)"
              >
                <span>{{ outsideBetLabel(bet) }}</span>
                <div v-if="selectedBets[bet]" class="chip number-chip bg-warning">
                  <span class="chipSpan">{{ selectedBets[bet][0] }}</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="alerts" v-if="feedbackError || feedbackSuccess">
      <p v-if="feedbackError" class="text-danger fw-semibold mb-1">{{ feedbackError }}</p>
      <p v-if="feedbackSuccess" class="text-success fw-semibold mb-1">{{ feedbackSuccess }}</p>
    </section>

    <section v-if="resolvedSpinData" class="result-box mb-3">
      <h4 class="mb-2">{{ $t("roulette.result.title") }}</h4>
      <div class="result-grid">
        <p><strong>{{ $t("roulette.result.drawnNumber") }}:</strong> {{ resolvedSpinData.drawn_number }}</p>
        <p><strong>{{ $t("roulette.result.totalBet") }}:</strong> {{ resolvedSpinData.total_bet }}</p>
        <p><strong>{{ $t("roulette.result.winningProfit") }}:</strong> {{ resolvedSpinData.total_winnings }}</p>
        <p><strong>{{ $t("roulette.result.losingStake") }}:</strong> {{ spinLosses(resolvedSpinData).toFixed(2) }}</p>
        <p><strong>{{ $t("roulette.result.totalReturn") }}:</strong> {{ spinPayout(resolvedSpinData).toFixed(2) }}</p>
        <p><strong>{{ $t("roulette.result.netResult") }}:</strong> {{ resolvedSpinData.net_result }}</p>
      </div>
    </section>

    <section v-if="selectedBetList.length" class="selection-box mb-3">
      <h4 class="mb-2">{{ $t("roulette.selectedBets.title") }}</h4>
      <div class="selection-list">
        <div class="selection-item" v-for="bet in selectedBetList" :key="bet.key">
          <div>
            <strong>{{ bet.type }}</strong>
            <p class="mb-0 text-muted small">{{ $t("common.numbers") }}: {{ bet.numbers.join(", ") }}</p>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="fw-semibold">{{ Number(bet.value).toFixed(2) }}</span>
            <button type="button" class="btn btn-sm btn-outline-secondary" @click="removeBet(bet.key)">
              {{ $t("common.remove") }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="tx-box">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-2">
        <h4 class="mb-0">{{ $t("roulette.transactions.title") }}</h4>
        <span class="pill-label">{{ $t("common.total") }}: {{ transactionTotal }}</span>
      </div>

      <div class="tx-toolbar mb-2">
        <input
          v-model.trim="transactionQuery"
          type="text"
          class="form-control tx-search"
          :placeholder="$t('roulette.transactions.searchPlaceholder')"
          :disabled="loadingTransactions"
          @input="onTransactionSearchInput"
        />
        <button
          type="button"
          class="btn btn-sm btn-brand-outline"
          :disabled="loadingTransactions"
          @click="refreshTransactions"
        >
          {{ loadingTransactions ? $t("roulette.transactions.updating") : $t("common.refresh") }}
        </button>
      </div>

      <div v-if="loadingWallet && !transactions.length" class="text-muted">{{ $t("roulette.transactions.loadingWallet") }}</div>
      <div v-else-if="loadingTransactions && !transactions.length" class="text-muted">{{ $t("roulette.transactions.loadingTransactions") }}</div>
      <div v-else-if="!transactions.length" class="text-muted">{{ $t("roulette.transactions.empty") }}</div>

      <div v-else class="tx-list" @scroll.passive="handleTxScroll">
        <div class="tx-item" v-for="item in transactions" :key="item.id">
          <div>
            <strong :class="Number(item.amount) >= 0 ? 'text-success' : 'text-danger'">
              {{ Number(item.amount) >= 0 ? "+" : "" }}{{ Number(item.amount).toFixed(2) }}
            </strong>
            <p class="mb-0 small text-muted">{{ transactionDescription(item) }}</p>
          </div>
          <small class="text-muted">{{ formatDate(item.timestamp) }}</small>
        </div>
      </div>

      <div class="tx-actions mt-2" v-if="hasMoreTransactions || loadingTransactions">
        <button
          v-if="hasMoreTransactions"
          type="button"
          class="btn btn-sm btn-outline-secondary"
          :disabled="loadingTransactions"
          @click="loadTransactions()"
        >
          {{ loadingTransactions ? $t("common.loading") : $t("roulette.transactions.loadMore") }}
        </button>
        <small v-else-if="loadingTransactions" class="text-muted">{{ $t("common.loading") }}</small>
      </div>
    </section>
  </div>
</template>

<script>
import { depositCoins, fetchTransactions, fetchWallet, sendBets } from "@/services/apiService";
import { isAuthError } from "@/services/errorService";
import { translateBetType } from "@/utils/betType";
import { formatTransactionDescription } from "@/utils/transactionDescription";

export default {
  name: "RouletteComponent",
  props: {
    isSpinning: {
      type: Boolean,
      default: false,
    },
    resolvedSpinData: {
      type: Object,
      default: null,
    },
  },
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
      bets: ["1-18", "even", "red", "black", "odd", "19-36"],
      insideMarkers: [],
      zeroMarkers: [
        { key: "zero-0-3", type: "zero_bets", numbers: [0, 3], x: 0.96, y: 0.5, markerType: "zero-single" },
        { key: "zero-0-2-3", type: "zero_bets", numbers: [0, 2, 3], x: 0.96, y: 1.0, markerType: "zero-combo" },
        { key: "zero-0-2", type: "zero_bets", numbers: [0, 2], x: 0.96, y: 1.5, markerType: "zero-single" },
        { key: "zero-0-1-2", type: "zero_bets", numbers: [0, 1, 2], x: 0.96, y: 2.0, markerType: "zero-combo" },
        { key: "zero-0-1", type: "zero_bets", numbers: [0, 1], x: 0.96, y: 2.5, markerType: "zero-single" },
      ],
      selectedBets: {},
      betOrder: {},
      betOrderCounter: 0,
      chipValue: 5,
      chipOptions: [5, 10, 25, 50, 100],
      quickDeposits: [100, 500, 1000],
      isSubmitting: false,
      loadingWallet: false,
      wallet: { balance: 0 },
      transactions: [],
      transactionTotal: 0,
      transactionOffset: 0,
      transactionLimit: 20,
      hasMoreTransactions: false,
      loadingTransactions: false,
      transactionQuery: "",
      transactionSearchDebounce: null,
      feedbackError: "",
      feedbackSuccess: "",
    };
  },
  watch: {
    async resolvedSpinData(newSpinData) {
      if (!newSpinData) {
        return;
      }

      this.wallet.balance = newSpinData.new_balance;
      this.feedbackError = "";
      this.feedbackSuccess = this.$t("roulette.feedback.spinStopped", { number: newSpinData.drawn_number });
      await this.loadWallet({ refreshTransactions: true });
    },
  },
  computed: {
    numberRows() {
      return Array.from({ length: 3 }, (_, row) =>
        Array.from({ length: 12 }, (_, col) => this.numberAt(row, col)),
      );
    },
    selectedBetList() {
      return Object.entries(this.selectedBets)
        .map(([key, bet]) => ({
          key,
          value: Number(bet[0]),
          type: this.formatBetType(bet[1]),
          numbers: bet[2],
          order: this.betOrder[key] || 0,
        }))
        .sort((a, b) => b.order - a.order);
    },
    totalSelectedAmount() {
      return this.selectedBetList.reduce((acc, current) => acc + Number(current.value), 0);
    },
  },
  mounted() {
    this.buildInsideMarkers();
    this.loadWallet({ refreshTransactions: true });
  },
  beforeUnmount() {
    if (this.transactionSearchDebounce) {
      clearTimeout(this.transactionSearchDebounce);
    }
  },
  methods: {
    translateBet(type) {
      return translateBetType((key, params) => this.$t(key, params), type);
    },

    outsideBetLabel(type) {
      return this.translateBet(type);
    },

    transactionDescription(item) {
      return formatTransactionDescription(
        (key, params) => this.$t(key, params),
        item,
        this.$t("roulette.transactions.defaultMovement"),
      );
    },

    async handleError(error, fallbackKey) {
      if (isAuthError(error)) {
        this.feedbackSuccess = "";
        this.feedbackError = this.$t("roulette.errors.sessionExpiredRedirect");
        try {
          await this.$store.dispatch("logout");
        } catch (_) {
          this.$store.commit("SET_AUTHENTICATED", false);
        }

        setTimeout(() => {
          this.$router.push({ name: "Login", query: { reason: "session_expired" } });
        }, 900);
        return;
      }

      this.feedbackError = error?.userMessage || this.$t(fallbackKey);
    },

    numberAt(row, col) {
      const rowOffset = [3, 2, 1];
      return col * 3 + rowOffset[row];
    },

    buildInsideMarkers() {
      const markers = [];

      for (let row = 0; row < 3; row += 1) {
        for (let col = 0; col < 11; col += 1) {
          markers.push({
            key: `split-h-${row}-${col}`,
            type: "split",
            numbers: [this.numberAt(row, col), this.numberAt(row, col + 1)],
            x: col + 1,
            y: row + 0.5,
            markerType: "split-h",
          });
        }
      }

      for (let col = 0; col < 12; col += 1) {
        for (let row = 0; row < 2; row += 1) {
          markers.push({
            key: `split-v-${row}-${col}`,
            type: "split",
            numbers: [this.numberAt(row, col), this.numberAt(row + 1, col)],
            x: col + 0.5,
            y: row + 1,
            markerType: "split-v",
          });
        }
      }

      for (let row = 0; row < 2; row += 1) {
        for (let col = 0; col < 11; col += 1) {
          markers.push({
            key: `corner-${row}-${col}`,
            type: "corner",
            numbers: [
              this.numberAt(row, col),
              this.numberAt(row + 1, col),
              this.numberAt(row, col + 1),
              this.numberAt(row + 1, col + 1),
            ],
            x: col + 1,
            y: row + 1,
            markerType: "corner",
          });
        }
      }

      for (let col = 0; col < 12; col += 1) {
        markers.push({
          key: `street-${col}`,
          type: "street",
          numbers: [this.numberAt(0, col), this.numberAt(1, col), this.numberAt(2, col)].sort(
            (a, b) => a - b,
          ),
          x: col + 0.5,
          y: 3.08,
          markerType: "street",
        });
      }

      for (let col = 0; col < 11; col += 1) {
        const leftStreet = [this.numberAt(0, col), this.numberAt(1, col), this.numberAt(2, col)];
        const rightStreet = [
          this.numberAt(0, col + 1),
          this.numberAt(1, col + 1),
          this.numberAt(2, col + 1),
        ];
        markers.push({
          key: `two-street-${col}`,
          type: "two street",
          numbers: [...leftStreet, ...rightStreet].sort((a, b) => a - b),
          x: col + 1,
          y: -0.08,
          markerType: "two-street",
        });
      }

      this.insideMarkers = markers;
    },

    markerStyle(marker) {
      return {
        left: `${(marker.x / 12) * 100}%`,
        top: `${(marker.y / 3) * 100}%`,
      };
    },

    zeroMarkerStyle(marker) {
      return {
        left: `${marker.x * 100}%`,
        top: `${(marker.y / 3) * 100}%`,
      };
    },

    formatBetType(type) {
      return this.translateBet(type);
    },

    touchBet(key) {
      this.betOrderCounter += 1;
      this.betOrder = {
        ...this.betOrder,
        [key]: this.betOrderCounter,
      };
    },

    upsertBet(key, betType, numbers) {
      const parsedNumbers = numbers.map((value) => Number(value));
      if (this.selectedBets[key]) {
        this.selectedBets[key][0] = Number(this.selectedBets[key][0]) + Number(this.chipValue);
      } else {
        this.selectedBets[key] = [Number(this.chipValue), betType, parsedNumbers];
      }
      this.touchBet(key);
    },

    placeMarkerBet(marker) {
      this.upsertBet(marker.key, marker.type, marker.numbers);
    },

    placeDirectNumberBet(number) {
      this.upsertBet(`num-${number}`, "straight-up", [number]);
    },

    placeOutsideBet(key, type, numbers) {
      this.upsertBet(key, type, numbers);
    },

    twoToOne(row) {
      const start = 4 - row;
      const resultRange = Array.from({ length: 12 }, (_, i) => start + i * 3);
      this.placeOutsideBet(`line${row}`, `line${row}`, resultRange);
    },

    genDozens(index, betType) {
      const start = index * 12;
      const resultRange = Array.from({ length: 12 }, (_, i) => start + i + 1);
      this.placeOutsideBet(betType, betType, resultRange);
    },

    generalBets(bet) {
      const cleanBet = bet.trim().toLowerCase();
      const bets = {
        "1-18": Array.from({ length: 18 }, (_, i) => i + 1),
        "19-36": Array.from({ length: 18 }, (_, i) => i + 19),
        black: Object.keys(this.roulette)
          .filter((key) => this.roulette[key] === "black")
          .map((value) => Number(value)),
        red: Object.keys(this.roulette)
          .filter((key) => this.roulette[key] === "red")
          .map((value) => Number(value)),
        even: Array.from({ length: 36 }, (_, i) => i + 1).filter((num) => num % 2 === 0),
        odd: Array.from({ length: 36 }, (_, i) => i + 1).filter((num) => num % 2 === 1),
      };
      const resultBet = bets[cleanBet];
      this.placeOutsideBet(bet, cleanBet, resultBet);
    },

    clearBets() {
      this.selectedBets = {};
      this.betOrder = {};
      this.betOrderCounter = 0;
    },

    removeBet(key) {
      delete this.selectedBets[key];
      this.selectedBets = { ...this.selectedBets };
      delete this.betOrder[key];
      this.betOrder = { ...this.betOrder };
    },

    formatDate(value) {
      if (!value) {
        return "";
      }
      return new Date(value).toLocaleString(this.$i18n.locale);
    },

    getColor(number) {
      return this.roulette[number];
    },

    onTransactionSearchInput() {
      if (this.transactionSearchDebounce) {
        clearTimeout(this.transactionSearchDebounce);
      }

      this.transactionSearchDebounce = setTimeout(() => {
        this.loadTransactions({ reset: true });
      }, 320);
    },

    async refreshTransactions() {
      await this.loadTransactions({ reset: true });
    },

    async loadTransactions({ reset = false } = {}) {
      if (this.loadingTransactions) {
        return;
      }

      if (!reset && !this.hasMoreTransactions && this.transactions.length > 0) {
        return;
      }

      const offset = reset ? 0 : this.transactionOffset;
      if (reset) {
        this.transactions = [];
        this.transactionOffset = 0;
        this.hasMoreTransactions = false;
      }

      this.loadingTransactions = true;
      try {
        const data = await fetchTransactions({
          offset,
          limit: this.transactionLimit,
          q: this.transactionQuery,
        });

        const incoming = Array.isArray(data?.results) ? data.results : [];
        if (reset) {
          this.transactions = incoming;
        } else {
          const existingIds = new Set(this.transactions.map((item) => item.id));
          const uniqueIncoming = incoming.filter((item) => !existingIds.has(item.id));
          this.transactions = [...this.transactions, ...uniqueIncoming];
        }

        const pagination = data?.pagination || {};
        const nextOffset = Number(pagination.next_offset);
        const total = Number(pagination.total);

        this.transactionOffset = Number.isFinite(nextOffset)
          ? nextOffset
          : offset + incoming.length;
        this.hasMoreTransactions = Boolean(pagination.has_next);
        this.transactionTotal = Number.isFinite(total) ? total : this.transactions.length;
      } catch (error) {
        await this.handleError(error, "roulette.errors.loadTransactions");
      } finally {
        this.loadingTransactions = false;
      }
    },

    handleTxScroll(event) {
      if (this.loadingTransactions || !this.hasMoreTransactions) {
        return;
      }

      const element = event.target;
      const nearBottom = element.scrollTop + element.clientHeight >= element.scrollHeight - 44;
      if (nearBottom) {
        this.loadTransactions();
      }
    },

    async loadWallet({ refreshTransactions = false } = {}) {
      this.loadingWallet = true;
      try {
        const data = await fetchWallet(1);
        this.wallet = data.wallet || { balance: 0 };

        if (refreshTransactions || (!this.transactions.length && this.transactionOffset === 0)) {
          await this.loadTransactions({ reset: true });
        }
      } catch (error) {
        await this.handleError(error, "roulette.errors.loadWallet");
      } finally {
        this.loadingWallet = false;
      }
    },

    async deposit(amount) {
      try {
        const response = await depositCoins(amount);
        this.feedbackError = "";
        this.feedbackSuccess = this.$t("roulette.feedback.depositSuccess", { amount: response.amount });
        await this.loadWallet({ refreshTransactions: true });
      } catch (error) {
        this.feedbackSuccess = "";
        await this.handleError(error, "roulette.errors.deposit");
      }
    },

    async sendAllBets() {
      if (this.isSpinning) {
        this.feedbackSuccess = "";
        this.feedbackError = this.$t("roulette.validation.waitSpin");
        return;
      }

      if (Object.keys(this.selectedBets).length === 0) {
        this.feedbackSuccess = "";
        this.feedbackError = this.$t("roulette.validation.pickBet");
        return;
      }

      if (Number(this.wallet.balance) < this.totalSelectedAmount) {
        this.feedbackSuccess = "";
        this.feedbackError = this.$t("roulette.validation.insufficientForStake");
        return;
      }

      this.isSubmitting = true;
      this.feedbackError = "";

      try {
        const data = await sendBets(this.selectedBets);
        this.feedbackSuccess = this.$t("roulette.feedback.betConfirmed");
        this.$emit("spin", data);
        this.clearBets();
      } catch (error) {
        this.feedbackSuccess = "";
        await this.handleError(error, "roulette.errors.sendBets");
      } finally {
        this.isSubmitting = false;
      }
    },

    spinLosses(spinData) {
      const bets = spinData?.resolved_bets || [];
      return bets.reduce((acc, bet) => {
        const net = Number(bet.net_change || 0);
        return net < 0 ? acc + Math.abs(net) : acc;
      }, 0);
    },

    spinPayout(spinData) {
      const totalBet = Number(spinData?.total_bet || 0);
      const netResult = Number(spinData?.net_result || 0);
      return totalBet + netResult;
    },
  },
};
</script>
<style scoped>
.roulette-border {
  width: 100%;
}

.info-grid {
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.wallet-box,
.bet-box,
.table-card,
.result-box,
.selection-box,
.tx-box {
  border: 1px solid rgba(174, 138, 64, 0.28);
  border-radius: 18px;
  background: #fff8e8;
  padding: 0.9rem;
}

.wallet-value {
  font-family: "Racing Sans One", sans-serif;
  font-size: 2rem;
  line-height: 1;
  color: #17452f;
}

.wallet-note {
  color: #536b5e;
  font-size: 0.9rem;
}

.chip-label {
  font-size: 0.84rem;
  font-weight: 600;
  color: #41594c;
}

.chip-select {
  max-width: 220px;
}

.table-card {
  padding: 0.7rem;
}

.table-scroll {
  overflow-x: auto;
  padding-bottom: 0.35rem;
}

.roulette-table {
  --cell: clamp(2rem, 3.8vw, 2.6rem);
  --zero-width: calc(var(--cell) * 1.18);
  --zero-gap: clamp(0.08rem, 0.35vw, 0.16rem);
  --board-gap: clamp(0.3rem, 0.9vw, 0.55rem);
  width: max-content;
  min-width: max-content;
  background: linear-gradient(180deg, #0f6a40 0%, #0c5533 100%);
  border: 2px solid #d7bf80;
  border-radius: 18px;
  padding: 0.75rem;
}

.board-row {
  display: flex;
  align-items: stretch;
  gap: var(--board-gap);
}

.board-core {
  display: flex;
  gap: var(--zero-gap);
}

.board-zone,
.number-cell,
.line-cell,
.outside-cell {
  border: 1px solid rgba(255, 255, 255, 0.72);
  color: #fff;
  font-weight: 700;
  position: relative;
}

.zero-cell {
  width: var(--zero-width);
  height: calc(var(--cell) * 3);
  border-radius: calc(var(--cell) * 0.75) 0 0 calc(var(--cell) * 0.75);
  background: #10804d;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.zero-label {
  font-size: clamp(1.1rem, 1.8vw, 1.5rem);
}

.grid-wrap {
  position: relative;
}

.number-grid {
  display: grid;
  grid-template-columns: repeat(12, var(--cell));
  grid-template-rows: repeat(3, var(--cell));
}

.number-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(0.75rem, 1vw, 0.95rem);
  cursor: pointer;
}

.number-red {
  background: #be2d33;
}

.number-black {
  background: #191e24;
}

.marker-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: visible;
}

.board-marker,
.zero-marker {
  position: absolute;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(255, 255, 255, 0.32);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  cursor: pointer;
  pointer-events: auto;
  padding: 0;
}

.board-marker {
  width: 0.68rem;
  height: 0.68rem;
}

.marker-split-h,
.marker-split-v {
  width: 0.62rem;
  height: 0.62rem;
}

.marker-corner {
  width: 0.52rem;
  height: 0.52rem;
}

.marker-street {
  width: 0.92rem;
  height: 0.54rem;
  border-radius: 999px;
}

.marker-two-street {
  width: 0.64rem;
  height: 0.64rem;
}

.zero-marker {
  width: 1rem;
  height: 1rem;
  border: 0;
  background: transparent;
}

.zero-marker.zero-single {
  width: 1rem;
  height: 1rem;
}

.zero-marker.zero-combo {
  width: 1rem;
  height: 1rem;
}

.zero-marker .marker-dot {
  width: 0.42rem;
  height: 0.42rem;
  margin: auto;
  border-radius: 999px;
  background: #111922;
  border: 1px solid rgba(255, 255, 255, 0.72);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.35);
  transition: transform 0.16s ease, background-color 0.16s ease;
}

.zero-marker:hover .marker-dot {
  transform: scale(1.12);
  background: #1d2731;
}

.marker-dot {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 999px;
}

.line-column {
  display: grid;
  grid-template-rows: repeat(3, var(--cell));
}

.line-cell {
  width: calc(var(--cell) * 1.3);
  background: rgba(255, 255, 255, 0.1);
  font-size: 0.84rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.outside-bets {
  margin-left: calc(var(--zero-width) + var(--zero-gap));
  margin-top: var(--board-gap);
  width: calc(var(--cell) * 12);
}

.outside-row {
  display: grid;
}

.outside-row-three {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.outside-row-six {
  grid-template-columns: repeat(6, minmax(0, 1fr));
}

.outside-cell {
  min-height: calc(var(--cell) * 0.9);
  background: rgba(255, 255, 255, 0.08);
  font-size: clamp(0.68rem, 0.85vw, 0.8rem);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.number-cell:hover,
.line-cell:hover,
.outside-cell:hover,
.zero-cell:hover,
.board-marker:hover,
.zero-marker:hover {
  filter: brightness(1.12);
}

.disable-select {
  user-select: none;
}

.chip {
  width: 20px;
  height: 20px;
  border: 1px solid #fff;
  border-radius: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.25);
}

.number-chip,
.marker-chip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.chipSpan {
  color: #1b1b1b;
  font-weight: 700;
  font-size: 10px;
  text-align: center;
  line-height: 1;
}

.result-box h4,
.selection-box h4,
.tx-box h4 {
  font-family: "Racing Sans One", sans-serif;
  color: #1a472f;
}

.result-grid {
  display: grid;
  gap: 0.4rem;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.result-grid p {
  margin: 0;
}

.selection-list,
.tx-list {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.selection-list {
  max-height: 320px;
  overflow-y: auto;
  padding-right: 0.2rem;
}

.tx-list {
  max-height: 360px;
  overflow-y: auto;
  padding-right: 0.2rem;
}

.tx-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  align-items: center;
}

.tx-search {
  flex: 1 1 260px;
  min-width: 220px;
}

.tx-actions {
  display: flex;
  justify-content: center;
}

.selection-item,
.tx-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border: 1px solid #e5d6b6;
  border-radius: 10px;
  padding: 0.6rem;
  background: #fffdf8;
}

@media (max-width: 900px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .result-grid {
    grid-template-columns: 1fr;
  }

  .selection-item,
  .tx-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .roulette-table {
    --cell: clamp(1.7rem, 7.8vw, 2.2rem);
  }
}
</style>
