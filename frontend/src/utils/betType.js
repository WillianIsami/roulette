const BET_TYPE_KEY_MAP = {
  "straight-up": "betTypes.straightUp",
  "straight up": "betTypes.straightUp",
  split: "betTypes.split",
  street: "betTypes.street",
  "two street": "betTypes.twoStreet",
  two_street: "betTypes.twoStreet",
  corner: "betTypes.corner",
  line: "betTypes.line",
  line1: "betTypes.line1",
  "line 1": "betTypes.line1",
  line2: "betTypes.line2",
  "line 2": "betTypes.line2",
  line3: "betTypes.line3",
  "line 3": "betTypes.line3",
  "1st 12": "betTypes.first12",
  "1st12": "betTypes.first12",
  "2nd 12": "betTypes.second12",
  "2nd12": "betTypes.second12",
  "3rd 12": "betTypes.third12",
  "3rd12": "betTypes.third12",
  "1-18": "betTypes.low",
  "19-36": "betTypes.high",
  even: "betTypes.even",
  red: "betTypes.red",
  black: "betTypes.black",
  odd: "betTypes.odd",
  zero_bets: "betTypes.zeroBets",
  "zero bets": "betTypes.zeroBets",
};

export function normalizeBetType(rawType) {
  if (!rawType) {
    return "";
  }
  return String(rawType).trim().toLowerCase().replace(/_/g, " ").replace(/\s+/g, " ");
}

export function getBetTypeTranslationKey(rawType) {
  const normalized = normalizeBetType(rawType);
  return BET_TYPE_KEY_MAP[normalized] || null;
}

export function translateBetType(t, rawType) {
  const key = getBetTypeTranslationKey(rawType);
  if (!key) {
    return t("betTypes.unknown");
  }
  return t(key);
}
