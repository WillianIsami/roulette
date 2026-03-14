import authService from "@/services/authService";

const state = () => ({
  isAuthenticated: false,
  authChecked: false,
});

const mutations = {
  SET_AUTHENTICATED(currentState, isAuthenticated) {
    currentState.isAuthenticated = isAuthenticated;
    currentState.authChecked = true;
  },
  SET_AUTH_CHECKED(currentState, authChecked) {
    currentState.authChecked = authChecked;
  },
};

const actions = {
  async login({ commit }, credentials) {
    const response = await authService.login(credentials);
    commit("SET_AUTHENTICATED", true);
    return response;
  },
  async logout({ commit }) {
    try {
      await authService.logout();
    } catch (_) {
      // Local logout should still happen even if API logout fails.
    } finally {
      commit("SET_AUTHENTICATED", false);
    }
  },
  async checkAuth({ commit }) {
    try {
      const response = await authService.isAuthenticated();
      commit("SET_AUTHENTICATED", Boolean(response.data.isAuthenticated));
    } catch (error) {
      commit("SET_AUTHENTICATED", false);
    }
  },
};

const getters = {
  isAuthenticated: (currentState) => currentState.isAuthenticated,
  authChecked: (currentState) => currentState.authChecked,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
