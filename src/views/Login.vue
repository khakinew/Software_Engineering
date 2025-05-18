<template>
  <div class="login-container">
    <div class="login-box">
      <h2>{{ isRegister ? "注册" : "登录" }}</h2>

      <!-- 用户类型选择 -->
      <div class="user-type-selector">
        <button
          :class="['type-btn', { active: userType === 'user' }]"
          @click="switchToUser"
        >
          普通用户
        </button>
        <button
          :class="['type-btn', { active: userType === 'admin' }]"
          @click="switchToAdmin"
        >
          管理员
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            required
            :placeholder="userType === 'admin' ? 'admin' : '请输入用户名'"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            required
            :placeholder="userType === 'admin' ? 'admin123' : '请输入密码'"
          />
        </div>
        <div class="form-group" v-if="isRegister && userType === 'user'">
          <label for="repassword">确认密码</label>
          <input
            type="password"
            id="repassword"
            v-model="form.repassword"
            required
            placeholder="请再次输入密码"
          />
        </div>
        <div v-if="!isRegister" class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="form.rememberMe" />
            <span>记住登录状态</span>
          </label>
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <div class="login-tips" v-if="userType === 'admin'">
          提示：管理员账号：admin / admin123
        </div>
        <button type="submit" class="submit-btn">
          {{ isRegister ? "注册" : "登录" }}
        </button>
      </form>
      <div class="switch-mode" v-if="userType === 'user'">
        <a href="#" @click.prevent="toggleMode">
          {{ isRegister ? "已有账号？去登录" : "没有账号？去注册" }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  name: "Login",
  setup() {
    const router = useRouter();
    const store = useStore();
    const isRegister = ref(false);
    const errorMessage = ref("");
    const userType = ref("user");

    const form = reactive({
      username: "",
      password: "",
      repassword: "",
      rememberMe: false,
    });

    const handleSubmit = async () => {
      try {
        errorMessage.value = "";

        if (isRegister.value && userType.value === "user") {
          // 注册流程
          await store.dispatch("register", {
            username: form.username,
            password: form.password,
            repassword: form.repassword,
            role: "user",
          });

          // 注册成功后自动登录
          await store.dispatch("login", {
            username: form.username,
            password: form.password,
            rememberMe: true,
          });
        } else {
          // 登录流程
          await store.dispatch("login", {
            username: form.username,
            password: form.password,
            rememberMe: form.rememberMe,
          });
        }

        router.push("/");
      } catch (error) {
        errorMessage.value = error.message;
      }
    };

    const switchToAdmin = () => {
      userType.value = "admin";
      isRegister.value = false;
      form.username = "admin";
      form.password = "admin123";
      errorMessage.value = "";
    };

    const switchToUser = () => {
      userType.value = "user";
      form.username = "";
      form.password = "";
      form.repassword = "";
      errorMessage.value = "";
    };

    const toggleMode = () => {
      if (userType.value === "user") {
        isRegister.value = !isRegister.value;
        form.username = "";
        form.password = "";
        form.repassword = "";
        form.rememberMe = false;
        errorMessage.value = "";
      }
    };

    return {
      form,
      isRegister,
      errorMessage,
      userType,
      handleSubmit,
      toggleMode,
      switchToAdmin,
      switchToUser,
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
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  border-color: #42b983;
  outline: none;
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

.error-message {
  color: #e74c3c;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.login-tips {
  color: #666;
  margin: 1rem 0;
  font-size: 0.9rem;
  text-align: center;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #3aa876;
}

.switch-mode {
  text-align: center;
  margin-top: 1rem;
}

.switch-mode a {
  color: #42b983;
  text-decoration: none;
}

.switch-mode a:hover {
  text-decoration: underline;
}
</style>
