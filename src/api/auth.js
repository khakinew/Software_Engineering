import axios from "../utils/axios";

export const authApi = {
  async login(username, password) {
    try {
      const response = await axios.post("/login", {
        username,
        password,
      });
      return response.data;
    } catch (error) {
      if (error.response?.data) {
        throw new Error(error.response.data.message || "登录失败");
      }
      throw new Error("网络错误，请稍后重试");
    }
  },

  async register(username, password, repassword, role = "user") {
    try {
      const response = await axios.post("/register", {
        username,
        password,
        repassword,
        role,
      });
      return response.data;
    } catch (error) {
      if (error.response?.data) {
        throw new Error(error.response.data.message || "注册失败");
      }
      throw new Error("网络错误，请稍后重试");
    }
  },

  async logout() {
    try {
      const response = await axios.post("/logout");
      return response.data;
    } catch (error) {
      if (error.response?.data) {
        throw new Error(error.response.data.message || "退出登录失败");
      }
      throw new Error("网络错误，请稍后重试");
    }
  },
};
