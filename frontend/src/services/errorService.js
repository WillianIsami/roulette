import { translate } from "@/i18n";

export class AppError extends Error {
  constructor({ userMessage, technicalMessage = "", status = null, code = "UNKNOWN", details = null }) {
    const fallbackMessage = translate("errors.operationFailed");
    super(userMessage || fallbackMessage);
    this.name = "AppError";
    this.userMessage = userMessage || fallbackMessage;
    this.technicalMessage = technicalMessage;
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function extractBackendMessage(payload) {
  if (!payload) {
    return "";
  }

  if (typeof payload === "string") {
    return payload;
  }

  if (typeof payload === "object") {
    if (typeof payload.error === "string") return payload.error;
    if (typeof payload.message === "string") return payload.message;
    if (typeof payload.detail === "string") return payload.detail;

    for (const value of Object.values(payload)) {
      if (Array.isArray(value) && value.length > 0) {
        const first = value[0];
        if (typeof first === "string") return first;
      }
      if (typeof value === "string") {
        return value;
      }
    }
  }

  return "";
}

function normalizeText(value) {
  if (!value) {
    return "";
  }
  return String(value).trim().toLowerCase();
}

function buildMappedError(code, key) {
  return {
    code,
    userMessage: translate(key),
  };
}

function mapMessage({ status, payload, technicalMessage = "" }) {
  const raw = extractBackendMessage(payload).trim();
  const normalized = normalizeText(raw);
  const normalizedTechnical = normalizeText(technicalMessage);

  if (
    status === 401 ||
    normalized.includes("invalid token") ||
    normalized.includes("token not provided") ||
    normalized.includes("not authenticated")
  ) {
    return buildMappedError("AUTH_REQUIRED", "errors.authRequired");
  }

  if (
    normalized.includes("invalid credentials") ||
    normalized.includes("no active account found") ||
    normalized.includes("unable to log in")
  ) {
    return buildMappedError("INVALID_CREDENTIALS", "errors.invalidCredentials");
  }

  if (normalized.includes("insufficient balance")) {
    return buildMappedError("INSUFFICIENT_BALANCE", "errors.insufficientBalance");
  }

  if (
    normalized.includes("bet not found") ||
    normalized.includes("unknown bet type") ||
    normalized.includes("at least one bet is required")
  ) {
    return buildMappedError("INVALID_BET", "errors.invalidBet");
  }

  if (normalized.includes("invalid amount") || normalized.includes("positive number")) {
    return buildMappedError("INVALID_AMOUNT", "errors.invalidAmount");
  }

  if (normalized.includes("already exists") || normalized.includes("unique")) {
    return buildMappedError("DUPLICATED_USER", "errors.duplicatedUser");
  }

  if (normalized.includes("username must contain at least")) {
    return buildMappedError("INVALID_USERNAME", "errors.invalidUsername");
  }

  if (
    normalized.includes("password") &&
    (normalized.includes("minimum") ||
      normalized.includes("too short") ||
      normalized.includes("must contain at least") ||
      normalized.includes("too common") ||
      normalized.includes("entirely numeric") ||
      normalized.includes("too similar"))
  ) {
    return buildMappedError("WEAK_PASSWORD", "errors.weakPassword");
  }

  if (status === 403 || normalized.includes("permission denied")) {
    return buildMappedError("FORBIDDEN", "errors.forbidden");
  }

  if (
    normalized.includes("field may not be blank") ||
    normalized.includes("this field is required") ||
    normalized.includes("is required")
  ) {
    return buildMappedError("MISSING_FIELDS", "errors.missingFields");
  }

  if (
    status === 0 ||
    normalizedTechnical.includes("failed to fetch") ||
    normalizedTechnical.includes("network") ||
    normalizedTechnical.includes("load failed")
  ) {
    return buildMappedError("NETWORK_ERROR", "errors.networkError");
  }

  if (status >= 500) {
    return buildMappedError("SERVER_ERROR", "errors.serverError");
  }

  if (status === 404 || normalized.includes("not found")) {
    return buildMappedError("NOT_FOUND", "errors.notFound");
  }

  if (status === 400) {
    return buildMappedError("BAD_REQUEST", "errors.badRequest");
  }

  if (raw) {
    return {
      code: "UNKNOWN",
      userMessage: raw,
    };
  }

  return buildMappedError("UNKNOWN", "errors.operationFailed");
}

export function buildAppErrorFromHttpResponse(status, payload, technicalMessage = "") {
  const mapped = mapMessage({ status, payload, technicalMessage });
  return new AppError({
    userMessage: mapped.userMessage,
    technicalMessage,
    status,
    code: mapped.code,
    details: payload,
  });
}

export function buildAppErrorFromNetworkError(error) {
  const technicalMessage = error?.message || "network error";
  const mapped = mapMessage({ status: 0, payload: null, technicalMessage });
  return new AppError({
    userMessage: mapped.userMessage,
    technicalMessage,
    status: 0,
    code: mapped.code,
  });
}

export function isAuthError(error) {
  return Boolean(error?.code === "AUTH_REQUIRED" || error?.status === 401);
}
