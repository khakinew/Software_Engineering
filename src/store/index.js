import { createStore } from "vuex";
import { authApi } from "../api/auth";

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
      try {
        const response = await authApi.login(username, password);
        if (response.success) {
          const userData = response.user;

          if (rememberMe) {
            localStorage.setItem("user", JSON.stringify(userData));
            localStorage.setItem("isAuthenticated", "true");
          } else {
            sessionStorage.setItem("user", JSON.stringify(userData));
            sessionStorage.setItem("isAuthenticated", "true");
          }

          commit("SET_USER", userData);
          commit("SET_AUTH", true);
          return response;
        }
        throw new Error(response.message || "登录失败");
      } catch (error) {
        throw error;
      }
    },

    async register({ commit }, { username, password, repassword }) {
      try {
        const response = await authApi.register(username, password, repassword);
        if (response.success) {
          return response;
        }
        throw new Error(response.message || "注册失败");
      } catch (error) {
        throw error;
      }
    },

    async logout({ commit }) {
      try {
        await authApi.logout();
      } catch (error) {
        console.error("退出登录失败:", error);
      } finally {
        // 无论退出是否成功，都清除本地状态
        localStorage.removeItem("user");
        localStorage.removeItem("isAuthenticated");
        sessionStorage.removeItem("user");
        sessionStorage.removeItem("isAuthenticated");
        commit("CLEAR_AUTH");
      }
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
