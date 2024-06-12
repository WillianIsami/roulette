import authService from '@/services/authService';

const state = {
  isAuthenticated: false
};

const mutations = {
  SET_AUTHENTICATED(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  }
};

const actions = {
  async login(credentials) {
    await authService.login(credentials);
    mutations.SET_AUTHENTICATED(state, true);
  },
  async logout() {
    await authService.logout();
    mutations.SET_AUTHENTICATED(state, false);
  },
  async checkAuth() {
    try {
      const response = await authService.isAuthenticated();
      mutations.SET_AUTHENTICATED(state, response.data.isAuthenticated);
    } catch (error) {
      mutations.SET_AUTHENTICATED(state, false);
    }
  }
};

const getters = {
  isAuthenticated: _ => state.isAuthenticated
};

export default {
  state,
  mutations,
  actions,
  getters
};
