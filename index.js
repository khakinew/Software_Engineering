import { createStore } from "vuex";
import { authApi,auth } from "../api/auth";
// 默认管理员账号
const ADMIN_CREDENTIALS = {
  username: "admin",
  password: "admin123",
  role: "admin",
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
        // 检查是否是管理员默认账号
        if (
          username === ADMIN_CREDENTIALS.username &&
          password === ADMIN_CREDENTIALS.password
        ) {
          const adminData = {
            username: ADMIN_CREDENTIALS.username,
            role: ADMIN_CREDENTIALS.role,
          };

          if (rememberMe) {
            localStorage.setItem("user", JSON.stringify(adminData));
            localStorage.setItem("isAuthenticated", "true");
          } else {
            sessionStorage.setItem("user", JSON.stringify(adminData));
            sessionStorage.setItem("isAuthenticated", "true");
          }

          commit("SET_USER", adminData);
          commit("SET_AUTH", true);
          return { success: true, user: adminData };
        }

        // 非管理员账号，使用后端 API
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
        // 禁止注册管理员账号
        if (username === ADMIN_CREDENTIALS.username) {
          throw new Error("不能使用保留的用户名");
        }

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
    
       auth().then(res=>{
        console.log(res);
        
       })
      let isAuthenticated =
        sessionStorage.getItem("isAuthenticated") === "true";
      let user = JSON.parse(sessionStorage.getItem("user"));
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
