import axios from 'axios';

const API_URL = process.env.VUE_APP_BASE_URL

export default {
  login(credentials) {
    return axios.post(`${API_URL}/api/token/`, credentials, { withCredentials: true });
  },
  logout() {
    return axios.post(`${API_URL}/api/logout/`, {}, { withCredentials: true });
  },
  isAuthenticated() {
    return axios.get(`${API_URL}/api/is-authenticated/`, { withCredentials: true });
  }
};