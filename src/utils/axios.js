import axios from "axios";

// 创建 axios 实例
const instance = axios.create({
  baseURL: "http://127.0.0.1:5000",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token（如果后端实现了 token 机制）
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除用户信息并跳转到登录页
          localStorage.removeItem("user");
          localStorage.removeItem("token");
          window.location.href = "/login";
          break;
        case 403:
          // 权限不足
          console.error("权限不足");
          break;
        case 404:
          // 请求的资源不存在
          console.error("请求的资源不存在");
          break;
        case 500:
          // 服务器错误
          console.error("服务器错误");
          break;
        default:
          console.error("发生错误:", error.response.data.message);
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      console.error("服务器无响应");
    } else {
      // 请求配置出错
      console.error("请求配置出错:", error.message);
    }
    return Promise.reject(error);
  }
);

export default instance;
