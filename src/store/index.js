import { createStore } from "vuex";

export default createStore({
  state: {
    user: null,
    userRole: localStorage.getItem("userRole") || "guest",
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setUserRole(state, role) {
      state.userRole = role;
      localStorage.setItem("userRole", role);
    },
    logout(state) {
      state.user = null;
      state.userRole = "guest";
      localStorage.removeItem("userRole");
    },
  },
  actions: {
    login({ commit }, { username, password }) {
      // 这里应该是实际的登录逻辑，现在用模拟数据
      return new Promise((resolve) => {
        setTimeout(() => {
          const isAdmin = username === "admin" && password === "admin";
          const role = isAdmin ? "admin" : "user";
          commit("setUser", { username });
          commit("setUserRole", role);
          resolve({ role });
        }, 1000);
      });
    },
  },
  getters: {
    isAdmin: (state) => state.userRole === "admin",
    isLoggedIn: (state) => !!state.user,
  },
});
