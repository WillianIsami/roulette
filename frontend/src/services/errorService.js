export class AppError extends Error {
  constructor({ userMessage, technicalMessage = "", status = null, code = "UNKNOWN", details = null }) {
    super(userMessage || "Não foi possível concluir a operação.");
    this.name = "AppError";
    this.userMessage = userMessage || "Não foi possível concluir a operação.";
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
    return {
      code: "AUTH_REQUIRED",
      userMessage: "Sua sessão expirou. Faça login novamente.",
    };
  }

  if (
    normalized.includes("invalid credentials") ||
    normalized.includes("no active account found") ||
    normalized.includes("unable to log in")
  ) {
    return {
      code: "INVALID_CREDENTIALS",
      userMessage: "Usuário ou senha inválidos. Verifique e tente novamente.",
    };
  }

  if (normalized.includes("insufficient balance")) {
    return {
      code: "INSUFFICIENT_BALANCE",
      userMessage: "Saldo insuficiente para essa aposta.",
    };
  }

  if (normalized.includes("bet not found") || normalized.includes("unknown bet type")) {
    return {
      code: "INVALID_BET",
      userMessage: "Aposta inválida. Revise os números selecionados e tente novamente.",
    };
  }

  if (normalized.includes("invalid amount")) {
    return {
      code: "INVALID_AMOUNT",
      userMessage: "Valor inválido. Digite um valor maior que zero.",
    };
  }

  if (normalized.includes("already exists") || normalized.includes("unique")) {
    return {
      code: "DUPLICATED_USER",
      userMessage: "Este nome de usuário já está em uso. Escolha outro.",
    };
  }

  if (normalized.includes("username must contain at least")) {
    return {
      code: "INVALID_USERNAME",
      userMessage: "Escolha um usuário com pelo menos 3 caracteres.",
    };
  }

  if (
    normalized.includes("password") &&
    (
      normalized.includes("minimum") ||
      normalized.includes("too short") ||
      normalized.includes("must contain at least") ||
      normalized.includes("too common") ||
      normalized.includes("entirely numeric")
    )
  ) {
    return {
      code: "WEAK_PASSWORD",
      userMessage: "A senha está fraca. Use pelo menos 8 caracteres.",
    };
  }

  if (status === 403 || normalized.includes("permission denied")) {
    return {
      code: "FORBIDDEN",
      userMessage: "Você não tem permissão para executar essa ação.",
    };
  }

  if (
    normalized.includes("field may not be blank") ||
    normalized.includes("this field is required") ||
    normalized.includes("is required")
  ) {
    return {
      code: "MISSING_FIELDS",
      userMessage: "Preencha os campos obrigatórios para continuar.",
    };
  }

  if (
    status === 0 ||
    normalizedTechnical.includes("failed to fetch") ||
    normalizedTechnical.includes("network") ||
    normalizedTechnical.includes("load failed")
  ) {
    return {
      code: "NETWORK_ERROR",
      userMessage: "Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.",
    };
  }

  if (status >= 500) {
    return {
      code: "SERVER_ERROR",
      userMessage: "O servidor está indisponível no momento. Tente novamente em instantes.",
    };
  }

  if (status === 404) {
    return {
      code: "NOT_FOUND",
      userMessage: "Recurso não encontrado. Atualize a página e tente novamente.",
    };
  }

  if (status === 400 && raw) {
    return {
      code: "BAD_REQUEST",
      userMessage: raw,
    };
  }

  return {
    code: "UNKNOWN",
    userMessage: raw || "Não foi possível concluir a operação. Tente novamente.",
  };
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
