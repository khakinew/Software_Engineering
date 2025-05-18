<template>
  <div id="app">
    <nav v-if="!isLoginPage" class="navbar">
      <router-link to="/" class="nav-item">主要信息</router-link>
      <router-link to="/underwater" class="nav-item">水下系统</router-link>
      <router-link to="/datacenter" class="nav-item">数据中心</router-link>
      <router-link to="/intelligent" class="nav-item">智能中心</router-link>
      <router-link v-if="isAdmin" to="/admin" class="nav-item"
        >管理员管理</router-link
      >
      <div class="auth-section">
        <template v-if="isLoggedIn">
          <span class="username">{{ user ? user.username : "" }}</span>
          <button @click="handleLogout" class="logout-btn">退出</button>
        </template>
        <template v-else>
          <button @click="goToLogin" class="login-btn">登录</button>
        </template>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "App",
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();

    const user = computed(() => store.state.user);
    const isAdmin = computed(() => store.getters.isAdmin);
    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const isLoginPage = computed(() => route.path === "/login");

    const handleLogout = async () => {
      try {
        await store.dispatch("logout");
        router.push("/login");
      } catch (error) {
        console.error("退出登录失败:", error);
        router.push("/login");
      }
    };

    const goToLogin = () => {
      router.push("/login");
    };

    return {
      user,
      isAdmin,
      isLoggedIn,
      isLoginPage,
      handleLogout,
      goToLogin,
    };
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
}

.navbar {
  background-color: #2c3e50;
  padding: 1rem;
  display: flex;
  align-items: center;
  color: white;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  margin-right: 1rem;
}

.nav-item:hover {
  background-color: #34495e;
  border-radius: 4px;
}

.auth-section {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: white;
  font-weight: 500;
}

.logout-btn {
  background-color: #e74c3c !important;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c0392b !important;
}

.login-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #3aa876;
}
</style>
