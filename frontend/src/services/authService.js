import axios from "axios";
import {
  AppError,
  buildAppErrorFromHttpResponse,
  buildAppErrorFromNetworkError,
} from "@/services/errorService";

const API_URL = process.env.VUE_APP_BASE_URL;

function convertAxiosError(error) {
  if (error instanceof AppError) {
    return error;
  }

  if (error?.response) {
    return buildAppErrorFromHttpResponse(error.response.status, error.response.data, error.message);
  }

  return buildAppErrorFromNetworkError(error);
}

async function safeRequest(fn) {
  try {
    return await fn();
  } catch (error) {
    throw convertAxiosError(error);
  }
}

export default {
  login(credentials) {
    return safeRequest(() => axios.post(`${API_URL}/api/token/`, credentials, { withCredentials: true }));
  },
  logout() {
    return safeRequest(() => axios.post(`${API_URL}/api/logout/`, {}, { withCredentials: true }));
  },
  isAuthenticated() {
    return safeRequest(() => axios.get(`${API_URL}/api/is-authenticated/`, { withCredentials: true }));
  },
};
