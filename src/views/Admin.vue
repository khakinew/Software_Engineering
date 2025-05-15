<template>
  <div class="admin">
    <h1>管理员管理界面</h1>
    <div class="content">
      <p>系统管理与用户管理</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Admin",
  beforeRouteEnter(to, from, next) {
    // 检查用户是否是管理员
    if (localStorage.getItem("userRole") === "admin") {
      next();
    } else {
      next("/");
    }
  },
};
</script>

<style scoped>
.admin {
  padding: 20px;
}
</style>
