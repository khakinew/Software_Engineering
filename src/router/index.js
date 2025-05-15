import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import UnderwaterSystem from "../views/UnderwaterSystem.vue";
import IntelligentCenter from "../views/IntelligentCenter.vue";
import Admin from "../views/Admin.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/underwater",
    name: "UnderwaterSystem",
    component: UnderwaterSystem,
  },
  {
    path: "/intelligent",
    name: "IntelligentCenter",
    component: IntelligentCenter,
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAdmin)) {
    if (localStorage.getItem("userRole") !== "admin") {
      next("/");
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
