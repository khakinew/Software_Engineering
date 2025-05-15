<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录</h2>
      <div class="user-type-selector">
        <button
          :class="['type-btn', { active: loginType === 'user' }]"
          @click="loginType = 'user'"
        >
          普通用户
        </button>
        <button
          :class="['type-btn', { active: loginType === 'admin' }]"
          @click="loginType = 'admin'"
        >
          管理员
        </button>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            :placeholder="loginType === 'admin' ? 'admin' : 'user'"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            :placeholder="loginType === 'admin' ? 'admin123' : 'user123'"
          />
        </div>
        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住登录状态</span>
          </label>
        </div>
        <div class="login-tips">
          提示：{{
            loginType === "admin"
              ? "管理员账号：admin / admin123"
              : "用户账号：user / user123"
          }}
        </div>
        <button type="submit" class="login-btn">登录</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  name: "Login",
  setup() {
    const router = useRouter();
    const store = useStore();
    const username = ref("");
    const password = ref("");
    const rememberMe = ref(false);
    const loginType = ref("user");

    const handleLogin = async () => {
      try {
        await store.dispatch("login", {
          username: username.value,
          password: password.value,
          rememberMe: rememberMe.value,
        });
        router.push("/");
      } catch (error) {
        alert("登录失败：" + error.message);
      }
    };

    return {
      username,
      password,
      rememberMe,
      loginType,
      handleLogin,
    };
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.login-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.user-type-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.type-btn {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  background-color: white;
  color: #666;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.type-btn.active {
  background-color: #42b983;
  color: white;
  border-color: #42b983;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.checkbox-group {
  margin: 1rem 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
}

.login-tips {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
  text-align: center;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

.login-btn:hover {
  background-color: #45a049;
}
</style>
