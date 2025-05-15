import { createStore } from "vuex";

const users = {
  admin: { username: "admin", password: "admin123", role: "admin" },
  user: { username: "user", password: "user123", role: "user" },
};

export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
    userRole: null,
  },
  mutations: {
    SET_AUTH(state, auth) {
      state.isAuthenticated = auth;
    },
    SET_USER(state, user) {
      state.user = user;
      if (user) {
        state.userRole = user.role;
      } else {
        state.userRole = null;
      }
    },
    CLEAR_AUTH(state) {
      state.isAuthenticated = false;
      state.user = null;
      state.userRole = null;
    },
  },
  actions: {
    async login({ commit }, { username, password, rememberMe }) {
      // 验证用户
      const user = Object.values(users).find(
        (u) => u.username === username && u.password === password
      );

      if (user) {
        const userData = {
          username: user.username,
          role: user.role,
        };

        if (rememberMe) {
          localStorage.setItem("user", JSON.stringify(userData));
          localStorage.setItem("isAuthenticated", "true");
        } else {
          sessionStorage.setItem("user", JSON.stringify(userData));
          sessionStorage.setItem("isAuthenticated", "true");
        }

        commit("SET_USER", userData);
        commit("SET_AUTH", true);
      } else {
        throw new Error("用户名或密码错误");
      }
    },
    logout({ commit }) {
      // 清除所有存储
      localStorage.removeItem("user");
      localStorage.removeItem("isAuthenticated");
      sessionStorage.removeItem("user");
      sessionStorage.removeItem("isAuthenticated");
      commit("CLEAR_AUTH");
    },
    checkAuth({ commit }) {
      // 先检查 sessionStorage（当前会话）
      let isAuthenticated =
        sessionStorage.getItem("isAuthenticated") === "true";
      let user = JSON.parse(sessionStorage.getItem("user"));

      // 如果在 sessionStorage 中没有找到，再检查 localStorage（持久存储）
      if (!isAuthenticated) {
        isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
        user = JSON.parse(localStorage.getItem("user"));
      }

      if (isAuthenticated && user) {
        commit("SET_USER", user);
        commit("SET_AUTH", true);
      } else {
        commit("CLEAR_AUTH");
      }
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    user: (state) => state.user,
    isAdmin: (state) => state.userRole === "admin",
    isLoggedIn: (state) => !!state.user,
  },
});
