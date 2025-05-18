<template>
  <div class="register-container">
    <h1>注册</h1>

    <div class="form-container">
      <!-- 注册表单 -->
      <div class="form-group">
        <input
          v-model="form.username"
          type="text"
          placeholder="用户名"
          class="form-input"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.password"
          type="password"
          placeholder="密码"
          class="form-input"
        />
      </div>

      <div class="form-group">
        <input
          v-model="form.repassword"
          type="password"
          placeholder="确认密码"
          class="form-input"
        />
      </div>

      <div class="error-message" v-if="errorMessage">
        {{ errorMessage }}
      </div>

      <button class="submit-btn" @click="handleSubmit">注册</button>

      <div class="login-link">
        <a href="#" @click.prevent="goToLogin"> 已有账号？去登录 </a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "Register",
  setup() {
    const store = useStore();
    const router = useRouter();
    const errorMessage = ref("");

    const form = reactive({
      username: "",
      password: "",
      repassword: "",
    });

    const handleSubmit = async () => {
      try {
        errorMessage.value = "";

        if (!form.username || !form.password || !form.repassword) {
          errorMessage.value = "请填写所有必填项";
          return;
        }

        if (form.password !== form.repassword) {
          errorMessage.value = "两次输入的密码不一致";
          return;
        }

        // 先注册
        const registerResponse = await store.dispatch("register", form);

        if (registerResponse.success) {
          // 注册成功后自动登录
          await store.dispatch("login", {
            username: form.username,
            password: form.password,
            rememberMe: true, // 注册后自动登录默认记住登录状态
          });
          router.push("/");
        }
      } catch (error) {
        errorMessage.value = error.message;
      }
    };

    const goToLogin = () => {
      router.push("/login");
    };

    return {
      form,
      errorMessage,
      handleSubmit,
      goToLogin,
    };
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 50px 20px;
  background-color: #f5f5f5;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 28px;
}

.form-container {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #42b983;
  outline: none;
}

.error-message {
  color: #e74c3c;
  margin: 10px 0;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 10px;
}

.submit-btn:hover {
  background: #3aa876;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link a {
  color: #3498db;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
