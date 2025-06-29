<template>
  <div v-if="alerts.length" class="alert-banner">
    <div v-for="alert in alerts" :key="alert.field" class="alert-item">
      <strong>{{ alert.field }} 异常：</strong>
      <span>{{ alert.message }}</span>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  data() {
    return {
      alerts: []
    };
  },
  methods: {
    fetchAlerts() {
      axios.get("/api/alerts/latest")
        .then(response => {
          if (response.data.code === 200) {
            this.alerts = response.data.alerts;
          }
        })
        .catch(error => {
          console.error("获取报警信息失败", error);
        });
    }
  },
  mounted() {
    this.fetchAlerts();
    setInterval(this.fetchAlerts, 30000);  // 每30秒检查一次
  }
};
</script>

<style scoped>
.alert-banner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: red;
  color: white;
  padding: 10px;
  text-align: center;
  font-size: 16px;
  z-index: 9999;
}
.alert-item {
  margin-bottom: 5px;
}
</style>
