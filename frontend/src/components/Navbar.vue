<template>
  <header class="glass-card nav-shell px-3 px-md-4 py-3">
    <RouterLink to="/" class="brand d-flex align-items-center text-decoration-none">
      <img src="@/assets/branding/brand-mark.svg" :alt="$t('common.appName')" class="brand-logo" />
      <div>
        <p class="brand-title mb-0">{{ $t("common.appName") }}</p>
        <small class="brand-sub">{{ $t("nav.tagline") }}</small>
      </div>
    </RouterLink>

    <nav class="nav-links d-flex align-items-center justify-content-center">
      <RouterLink to="/" class="link-item" :class="{ active: $route.path === '/' }">{{ $t("nav.home") }}</RouterLink>
      <RouterLink to="/about" class="link-item" :class="{ active: $route.path === '/about' }">{{ $t("nav.about") }}</RouterLink>
      <RouterLink to="/bets" class="link-item" :class="{ active: $route.path === '/bets' }">{{ $t("nav.bets") }}</RouterLink>
      <RouterLink to="/faq" class="link-item" :class="{ active: $route.path === '/faq' }">{{ $t("nav.howToPlay") }}</RouterLink>
    </nav>

    <div class="nav-actions d-flex align-items-center justify-content-end gap-2">
      <label class="visually-hidden" for="language-switch">{{ $t("locale.label") }}</label>
      <select id="language-switch" v-model="selectedLocale" class="form-select form-select-sm locale-select" @change="onLocaleChange">
        <option v-for="locale in locales" :key="locale" :value="locale">
          {{ localeLabel(locale) }}
        </option>
      </select>

      <template v-if="isAuthenticated">
        <button class="btn btn-brand-outline" type="button" @click="logout">{{ $t("nav.logout") }}</button>
      </template>
      <template v-else>
        <RouterLink to="/login" class="btn btn-brand-outline">{{ $t("nav.login") }}</RouterLink>
        <RouterLink to="/register" class="btn btn-brand">{{ $t("nav.register") }}</RouterLink>
      </template>
    </div>
  </header>
</template>

<script>
import { getCurrentLocale, setLocale, SUPPORTED_LOCALES } from "@/i18n";

export default {
  name: "NavbarComponent",
  data() {
    return {
      locales: SUPPORTED_LOCALES,
      selectedLocale: getCurrentLocale(),
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  watch: {
    "$i18n.locale"(newLocale) {
      this.selectedLocale = newLocale;
    },
  },
  methods: {
    localeLabel(locale) {
      const map = {
        en: "locale.en",
        "pt-BR": "locale.ptBR",
        es: "locale.es",
      };
      return this.$t(map[locale] || "locale.en");
    },
    onLocaleChange() {
      const appliedLocale = setLocale(this.selectedLocale);
      this.selectedLocale = appliedLocale;
    },
    async logout() {
      try {
        await this.$store.dispatch("logout");
      } finally {
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style scoped>
.nav-shell {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
  margin-top: 1rem;
}

.brand {
  gap: 0.75rem;
}

.brand-logo {
  width: 52px;
  height: 52px;
}

.brand-title {
  font-family: "Racing Sans One", sans-serif;
  font-size: 1.2rem;
  color: #153c2a;
  line-height: 1.1;
}

.brand-sub {
  color: #4d6658;
  font-size: 0.76rem;
}

.nav-links {
  gap: 0.25rem;
  padding: 0.35rem;
  border-radius: 999px;
  border: 1px solid #d7c6a2;
  background: #f5ebd4;
  justify-self: center;
}

.link-item {
  color: #335341;
  font-size: 0.92rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 999px;
  padding: 0.4rem 0.85rem;
}

.link-item:hover {
  color: #19392b;
}

.link-item.active {
  color: #0f2a1f;
  background: #e8d9b7;
  border: 1px solid #c89a3b;
}

.locale-select {
  width: 150px;
  border-color: #d7c6a2;
  background-color: #f8f1dd;
  color: #204533;
  font-weight: 600;
}

@media (max-width: 980px) {
  .nav-shell {
    grid-template-columns: 1fr;
  }

  .brand,
  .nav-actions {
    justify-content: center;
  }

  .nav-links {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
  }
}
</style>
