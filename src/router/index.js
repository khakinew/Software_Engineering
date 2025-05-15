import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import UnderwaterSystem from "../views/UnderwaterSystem.vue";
import IntelligentCenter from "../views/IntelligentCenter.vue";
import Admin from "../views/Admin.vue";
import Login from "../views/Login.vue";
import DataCenter from "../views/DataCenter.vue";
import store from "../store";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: "/underwater",
    name: "UnderwaterSystem",
    component: UnderwaterSystem,
    meta: { requiresAuth: true },
  },
  {
    path: "/intelligent",
    name: "IntelligentCenter",
    component: IntelligentCenter,
    meta: { requiresAuth: true },
  },
  {
    path: "/datacenter",
    name: "DataCenter",
    component: DataCenter,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  // 检查认证状态
  await store.dispatch("checkAuth");
  const isAuthenticated = store.getters.isAuthenticated;
  const user = store.getters.user;

  // 如果需要认证但未登录，重定向到登录页
  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");
    return;
  }

  // 如果需要管理员权限
  if (to.meta.requiresAdmin && (!user || user.role !== "admin")) {
    next("/");
    return;
  }

  // 如果已登录且访问登录页，重定向到首页
  if (to.path === "/login" && isAuthenticated) {
    next("/");
    return;
  }

  next();
});

export default router;
