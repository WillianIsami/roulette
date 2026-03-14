import {
  AppError,
  buildAppErrorFromHttpResponse,
  buildAppErrorFromNetworkError,
} from "@/services/errorService";

const API_URL = process.env.VUE_APP_BASE_URL;

async function readResponsePayload(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json().catch(() => ({}));
  }

  const text = await response.text().catch(() => "");
  if (!text) {
    return {};
  }

  return { message: text };
}

async function parseResponse(response) {
  const payload = await readResponsePayload(response);
  if (!response.ok) {
    throw buildAppErrorFromHttpResponse(response.status, payload, `HTTP ${response.status}`);
  }
  return payload;
}

async function request(url, options = {}) {
  try {
    const response = await fetch(url, options);
    return await parseResponse(response);
  } catch (error) {
    if (error instanceof AppError) {
      throw error;
    }
    throw buildAppErrorFromNetworkError(error);
  }
}

export const register = async (payload) =>
  request(`${API_URL}/api/create/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

export const sendBets = async (bets) =>
  request(`${API_URL}/api/spin/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(bets),
  });

export const fetchWallet = async (limit = 20) =>
  request(`${API_URL}/api/wallet/?limit=${limit}`, {
    method: "GET",
    credentials: "include",
  });

export const fetchTransactions = async ({ offset = 0, limit = 30, q = "" } = {}) => {
  const params = new URLSearchParams({
    offset: String(Math.max(0, Number(offset) || 0)),
    limit: String(Math.max(1, Number(limit) || 30)),
  });

  const trimmedQuery = String(q || "").trim();
  if (trimmedQuery) {
    params.set("q", trimmedQuery);
  }

  return request(`${API_URL}/api/transactions/?${params.toString()}`, {
    method: "GET",
    credentials: "include",
  });
};

export const depositCoins = async (amount) =>
  request(`${API_URL}/api/wallet/deposit/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ amount }),
  });

export const fetchBets = async () =>
  request(`${API_URL}/api/`, {
    method: "GET",
    credentials: "include",
  });
