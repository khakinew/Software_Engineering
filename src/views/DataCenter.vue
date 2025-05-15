<template>
  <div class="data-center">
    <!-- 顶部统计卡片 -->
    <div class="statistics-row">
      <div v-for="stat in statistics" :key="stat.title" class="stat-card">
        <div class="stat-icon" :style="{ backgroundColor: stat.color }">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-title">{{ stat.title }}</div>
        </div>
      </div>
    </div>

    <!-- 数据图表区域 -->
    <div class="charts-container">
      <!-- 左侧图表 -->
      <div class="chart-section">
        <div class="section-header">
          <h2>水质参数趋势</h2>
          <div class="time-selector">
            <button
              v-for="period in timePeriods"
              :key="period"
              :class="['time-btn', { active: currentPeriod === period }]"
              @click="currentPeriod = period"
            >
              {{ period }}
            </button>
          </div>
        </div>
        <div class="chart-wrapper" ref="waterQualityChart"></div>
      </div>

      <!-- 右侧图表 -->
      <div class="chart-section">
        <div class="section-header">
          <h2>设备运行状态</h2>
          <div class="type-selector">
            <select v-model="selectedDeviceType">
              <option value="all">所有设备</option>
              <option value="camera">摄像设备</option>
              <option value="sensor">传感器</option>
            </select>
          </div>
        </div>
        <div class="chart-wrapper" ref="deviceStatusChart"></div>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="data-table-section">
      <div class="section-header">
        <h2>实时数据记录</h2>
        <div class="table-controls">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索..."
            class="search-input"
          />
          <button class="export-btn">导出数据</button>
        </div>
      </div>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th v-for="header in tableHeaders" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in tableData" :key="index">
              <td>{{ row.timestamp }}</td>
              <td>{{ row.deviceId }}</td>
              <td>{{ row.temperature }}</td>
              <td>{{ row.ph }}</td>
              <td>{{ row.oxygen }}</td>
              <td>{{ row.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">
          上一页
        </button>
        <span>第 {{ currentPage }} 页</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import * as echarts from "echarts";

export default {
  name: "DataCenter",
  setup() {
    const currentPeriod = ref("24小时");
    const selectedDeviceType = ref("all");
    const searchQuery = ref("");
    const currentPage = ref(1);
    const totalPages = ref(10);

    const statistics = ref([
      { title: "在线设备", value: "42", color: "#4CAF50", icon: "icon-device" },
      { title: "报警次数", value: "3", color: "#F44336", icon: "icon-alert" },
      {
        title: "数据采集量",
        value: "1,234",
        color: "#2196F3",
        icon: "icon-data",
      },
      { title: "运行天数", value: "365", color: "#FF9800", icon: "icon-time" },
    ]);

    const timePeriods = ["24小时", "7天", "30天", "自定义"];
    const tableHeaders = [
      "时间",
      "设备ID",
      "温度(°C)",
      "pH值",
      "溶解氧(mg/L)",
      "状态",
    ];

    const tableData = ref([
      {
        timestamp: "2024-01-31 14:30:00",
        deviceId: "DEV001",
        temperature: "25.6",
        ph: "7.8",
        oxygen: "6.5",
        status: "正常",
      },
      // ... 更多数据
    ]);

    let waterQualityChart = null;
    let deviceStatusChart = null;

    onMounted(() => {
      initWaterQualityChart();
      initDeviceStatusChart();
    });

    const initWaterQualityChart = () => {
      const chartDom = document.querySelector(".chart-wrapper");
      waterQualityChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: ["温度", "pH值", "溶解氧"],
          textStyle: { color: "#fff" },
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: ["00:00", "06:00", "12:00", "18:00", "24:00"],
          axisLabel: { color: "#fff" },
        },
        yAxis: {
          type: "value",
          axisLabel: { color: "#fff" },
        },
        series: [
          {
            name: "温度",
            type: "line",
            data: [23, 24, 25, 26, 25],
            smooth: true,
          },
          {
            name: "pH值",
            type: "line",
            data: [7.5, 7.6, 7.8, 7.7, 7.6],
            smooth: true,
          },
          {
            name: "溶解氧",
            type: "line",
            data: [6.2, 6.5, 6.8, 6.6, 6.4],
            smooth: true,
          },
        ],
      };

      waterQualityChart.setOption(option);
    };

    const initDeviceStatusChart = () => {
      const chartDom = document.querySelectorAll(".chart-wrapper")[1];
      deviceStatusChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
          textStyle: { color: "#fff" },
        },
        series: [
          {
            name: "设备状态",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "20",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: 35, name: "正常运行" },
              { value: 5, name: "离线" },
              { value: 2, name: "故障" },
            ],
          },
        ],
      };

      deviceStatusChart.setOption(option);
    };

    return {
      currentPeriod,
      selectedDeviceType,
      searchQuery,
      currentPage,
      totalPages,
      statistics,
      timePeriods,
      tableHeaders,
      tableData,
    };
  },
};
</script>

<style scoped>
.data-center {
  padding: 20px;
  background-color: #0a1929;
  min-height: calc(100vh - 60px);
  color: white;
}

.statistics-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-title {
  color: #90caf9;
  font-size: 14px;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-section {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  font-size: 18px;
  color: #90caf9;
}

.time-selector {
  display: flex;
  gap: 10px;
}

.time-btn {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.time-btn.active {
  background-color: #1976d2;
  border-color: #1976d2;
}

.chart-wrapper {
  height: 300px;
}

.data-table-section {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
}

.table-controls {
  display: flex;
  gap: 10px;
}

.search-input {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background-color: rgba(0, 0, 0, 0.2);
  color: white;
}

.export-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.table-wrapper {
  margin: 20px 0;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  background-color: rgba(0, 0, 0, 0.2);
  color: #90caf9;
}

tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 20px;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: rgba(25, 118, 210, 0.5);
  cursor: not-allowed;
}

select {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
}
</style>
