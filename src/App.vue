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
          <button @click="showLoginModal = true">登录</button>
        </template>
      </div>
    </nav>

    <!-- 登录模态框 -->
    <div v-if="showLoginModal" class="modal">
      <div class="modal-content">
        <h2>登录</h2>
        <input v-model="loginForm.username" placeholder="用户名" />
        <input
          v-model="loginForm.password"
          type="password"
          placeholder="密码"
        />
        <button @click="handleLogin">登录</button>
        <button @click="showLoginModal = false">取消</button>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "App",
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const showLoginModal = ref(false);
    const loginForm = reactive({
      username: "",
      password: "",
    });

    const user = computed(() => store.state.user);
    const isAdmin = computed(() => store.getters.isAdmin);
    const isLoggedIn = computed(() => store.getters.isLoggedIn);
    const isLoginPage = computed(() => route.path === "/login");

    const handleLogin = async () => {
      try {
        await store.dispatch("login", loginForm);
        showLoginModal.value = false;
        loginForm.username = "";
        loginForm.password = "";
      } catch (error) {
        console.error("登录失败:", error);
      }
    };

    const handleLogout = () => {
      store.dispatch("logout");
      router.push("/login");
    };

    return {
      showLoginModal,
      loginForm,
      user,
      isAdmin,
      isLoggedIn,
      isLoginPage,
      handleLogin,
      handleLogout,
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

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3aa876;
}
</style>
