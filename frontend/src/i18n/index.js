import { createI18n } from "vue-i18n";
import messages from "@/i18n/messages";

export const SUPPORTED_LOCALES = ["en", "pt-BR", "es"];
export const DEFAULT_LOCALE = "en";
const STORAGE_KEY = "roulette.locale";

function normalizeLocale(rawLocale) {
  if (!rawLocale) {
    return null;
  }

  const normalized = String(rawLocale).trim().toLowerCase();
  if (normalized === "en" || normalized.startsWith("en-")) {
    return "en";
  }
  if (normalized === "pt" || normalized === "pt-br" || normalized.startsWith("pt-")) {
    return "pt-BR";
  }
  if (normalized === "es" || normalized.startsWith("es-")) {
    return "es";
  }
  return null;
}

function getStoredLocale() {
  try {
    if (typeof localStorage === "undefined") {
      return null;
    }
    return localStorage.getItem(STORAGE_KEY);
  } catch (_) {
    return null;
  }
}

function detectLocale() {
  const storedLocale = normalizeLocale(getStoredLocale());
  if (storedLocale) {
    return storedLocale;
  }
  return DEFAULT_LOCALE;
}

function syncDocumentLanguage(locale) {
  if (typeof document !== "undefined") {
    document.documentElement.lang = locale;
  }
}

const initialLocale = detectLocale();

export const i18n = createI18n({
  legacy: true,
  globalInjection: true,
  locale: initialLocale,
  fallbackLocale: DEFAULT_LOCALE,
  messages,
});

syncDocumentLanguage(initialLocale);

export function setLocale(locale) {
  const normalizedLocale = normalizeLocale(locale) || DEFAULT_LOCALE;
  i18n.global.locale = normalizedLocale;

  try {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(STORAGE_KEY, normalizedLocale);
    }
  } catch (_) {
    // Ignore localStorage failures and keep runtime locale only.
  }

  syncDocumentLanguage(normalizedLocale);
  return normalizedLocale;
}

export function getCurrentLocale() {
  return i18n.global.locale;
}

export function translate(messageKey, params = {}) {
  return i18n.global.t(messageKey, params);
}
