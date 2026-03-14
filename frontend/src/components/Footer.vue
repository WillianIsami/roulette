<template>
  <footer class="footer-shell d-flex flex-wrap align-items-center justify-content-between gap-3 px-3 px-md-4 py-3">
    <div class="d-flex align-items-center gap-2">
      <img src="@/assets/branding/brand-mark.svg" :alt="$t('common.appName')" class="footer-logo" />
      <div>
        <p class="mb-0 footer-title">{{ $t("common.appName") }}</p>
        <small class="footer-copy">© {{ currentYear }} - {{ $t("footer.caption") }}</small>
      </div>
    </div>

    <div class="d-flex gap-2 align-items-center">
      <span class="pill-label">Vue 3</span>
      <span class="pill-label">{{ $t("footer.djangoApi") }}</span>
      <span class="pill-label">{{ $t("common.walletCoins") }}</span>
    </div>
  </footer>
</template>

<script>
export default {
  name: "FooterComponent",
  computed: {
    currentYear() {
      return new Date().getFullYear();
    },
  },
};
</script>

<style scoped>
.footer-shell {
  border-radius: 18px 18px 0 0;
  border: 1px solid rgba(178, 136, 35, 0.24);
  border-bottom: none;
  background: rgba(255, 248, 230, 0.88);
}

.footer-logo {
  width: 34px;
  height: 34px;
}

.footer-title {
  font-weight: 700;
  color: #224532;
}

.footer-copy {
  color: #4f6558;
}
</style>
