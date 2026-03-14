import { normalizeBetType, translateBetType } from "@/utils/betType";

function normalizeNumbers(numbers) {
  if (Array.isArray(numbers)) {
    return numbers.join(", ");
  }
  if (typeof numbers === "string") {
    return numbers
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
      .join(", ");
  }
  return "";
}

function formatKnownDescription(t, descriptionKey, context = {}) {
  if (!descriptionKey) {
    return "";
  }

  const betTypeLabel = context.bet_type
    ? translateBetType(t, context.bet_type)
    : translateBetType(t, context.betType || "");

  const params = {
    amount: context.amount ?? "",
    betType: betTypeLabel,
    numbers: normalizeNumbers(context.numbers),
    drawnNumber: context.drawn_number ?? context.drawnNumber ?? "",
    profit: context.profit ?? "",
    stake: context.stake ?? "",
  };

  if (descriptionKey === "transaction.wallet_deposit") {
    return t("transactionDescriptions.deposit", params);
  }
  if (descriptionKey === "transaction.bet_win") {
    return t("transactionDescriptions.win", params);
  }
  if (descriptionKey === "transaction.bet_loss") {
    return t("transactionDescriptions.loss", params);
  }

  return "";
}

function parseLegacyDescription(t, description) {
  if (!description || typeof description !== "string") {
    return "";
  }

  const depositMatch = description.match(/^Deposit of\s+([\d.]+)\s+coins$/i);
  if (depositMatch) {
    return t("transactionDescriptions.deposit", { amount: depositMatch[1] });
  }

  const winMatch = description.match(
    /^Win on\s+(.+?):\s+numbers\s+\[(.*?)\],\s+drawn\s+(\d+),\s+profit\s+([\d.]+)$/i,
  );
  if (winMatch) {
    return t("transactionDescriptions.win", {
      betType: translateBetType(t, normalizeBetType(winMatch[1])),
      numbers: normalizeNumbers(winMatch[2]),
      drawnNumber: winMatch[3],
      profit: winMatch[4],
    });
  }

  const lossMatch = description.match(
    /^Loss on\s+(.+?):\s+numbers\s+\[(.*?)\],\s+drawn\s+(\d+),\s+stake\s+([\d.]+)$/i,
  );
  if (lossMatch) {
    return t("transactionDescriptions.loss", {
      betType: translateBetType(t, normalizeBetType(lossMatch[1])),
      numbers: normalizeNumbers(lossMatch[2]),
      drawnNumber: lossMatch[3],
      stake: lossMatch[4],
    });
  }

  return "";
}

export function formatTransactionDescription(t, transaction, fallbackText) {
  const formattedKnown = formatKnownDescription(
    t,
    transaction?.description_key,
    transaction?.description_context || {},
  );
  if (formattedKnown) {
    return formattedKnown;
  }

  const formattedLegacy = parseLegacyDescription(t, transaction?.description);
  if (formattedLegacy) {
    return formattedLegacy;
  }

  if (transaction?.description) {
    return transaction.description;
  }

  return fallbackText;
}
