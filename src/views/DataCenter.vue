<template>
  <div class="data-center">
    <!-- 数据总量区域 -->
    <div class="data-total-section">
      <div class="counter-display">
        <div class="digit-group">
          <div class="digit" v-for="(digit, index) in '01038'" :key="index">
            {{ digit }}
          </div>
        </div>
        <div class="unit">T</div>
      </div>

      <div class="storage-info">
        <div class="storage-container">
          <div class="storage-level" :style="{ height: '65%' }"></div>
          <div class="storage-text">
            <div>磁盘：</div>
            <div>已使用1000T</div>
            <div>剩余1500T</div>
          </div>
        </div>

        <div class="system-status">
          <div class="status-item">
            <div class="status-label">CPU运行状态</div>
            <div class="status-bar">
              <div class="bar-fill" style="width: 70%"></div>
            </div>
          </div>
          <div class="status-item">
            <div class="status-label">内存运行状态</div>
            <div class="status-bar">
              <div class="bar-fill" style="width: 85%"></div>
            </div>
          </div>
          <div class="status-item">
            <div class="status-label">GPU运行状态</div>
            <div class="status-bar">
              <div class="bar-fill" style="width: 60%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 数据中心分布地图 -->
      <div class="map-section">
        <div class="section-title">数据中心分布</div>
        <div class="map-container" ref="mapContainer"></div>
        <div class="location-list">
          <div
            v-for="loc in locations"
            :key="loc.city"
            class="location-item"
            :class="{ active: selectedLocation.city === loc.city }"
            @click="selectLocation(loc)"
          >
            <div class="location-dot"></div>
            <div class="location-info">
              <div class="location-name">{{ loc.city }}</div>
              <div class="location-detail">{{ loc.provider }}</div>
            </div>
          </div>
        </div>
        <div class="data-center-info">
          <div class="info-box">
            <div class="info-label">地点：</div>
            <div class="info-value">{{ selectedLocation.city }}</div>
          </div>
          <div class="info-box">
            <div class="info-label">服务商：</div>
            <div class="info-value">{{ selectedLocation.provider }}</div>
          </div>
          <div class="info-box">
            <div class="info-label">连接：</div>
            <div class="info-value">{{ selectedLocation.latency }}</div>
          </div>
        </div>
      </div>

      <!-- 传感器信息表格 -->
      <div class="sensor-section">
        <div class="section-title">传感器信息</div>
        <div class="time-info">
          <div class="time-item">
            <div class="time-label">平均传输时长</div>
            <div class="time-value">02:45</div>
          </div>
          <div class="time-item">
            <div class="time-label">平均处理时长</div>
            <div class="time-value">00:02</div>
          </div>
        </div>
        <div class="sensor-table">
          <table>
            <thead>
              <tr>
                <th>设备</th>
                <th>编号</th>
                <th>类型</th>
                <th>大小</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in sensorData" :key="index">
                <td>{{ item.device }}</td>
                <td>{{ item.code }}</td>
                <td>{{ item.type }}</td>
                <td>{{ item.size }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 数据统计图表 -->
      <div class="stats-section">
        <div class="data-type-stats">
          <div class="section-title">数据类型统计</div>
          <div class="pyramid-chart" ref="pyramidChart"></div>
        </div>
        <div class="data-distribution">
          <div class="section-title">数据类型占比</div>
          <div class="radar-chart" ref="radarChart"></div>
        </div>
        <div class="data-flow">
          <div class="section-title">结构化数据</div>
          <div class="sankey-chart" ref="sankeyChart"></div>
        </div>
      </div>

      <!-- 数据库交互统计 -->
      <div class="database-section">
        <div class="section-title">数据库交互统计</div>
        <div class="db-stats">
          <div class="db-info">
            <div>数据库：MySQL, HBase</div>
            <div>查询次数：567890</div>
            <div>成功次数：567890</div>
            <div>查询时间：0.1s</div>
          </div>
          <div class="db-system-btn">访问数据服务系统</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import * as echarts from "echarts";

export default {
  name: "DataCenter",
  setup() {
    const mapContainer = ref(null);
    const pyramidChart = ref(null);
    const radarChart = ref(null);
    const sankeyChart = ref(null);
    const mapLoaded = ref(false);

    const locations = [
      {
        city: "杭州",
        provider: "阿里云",
        latency: "30ms",
        region: "华东",
      },
      {
        city: "北京",
        provider: "腾讯云",
        latency: "45ms",
        region: "华北",
      },
      {
        city: "上海",
        provider: "华为云",
        latency: "35ms",
        region: "华东",
      },
      {
        city: "广州",
        provider: "阿里云",
        latency: "40ms",
        region: "华南",
      },
    ];

    const selectedLocation = ref(locations[0]);

    const sensorData = ref([
      { device: "水底摄像头", code: "video-1", type: "H.264", size: "4Mb" },
      { device: "水底摄像头", code: "video-2", type: "4CIF", size: "128kb" },
      { device: "水底摄像头", code: "video-3", type: "H.264", size: "100b" },
      { device: "云台", code: "holder-1", type: "H.264", size: "1kb" },
      { device: "声呐", code: "sonar-1", type: "CSV", size: "10kb" },
      { device: "传感器", code: "sensor-1", type: "TXT", size: "2kb" },
      { device: "气象站", code: "meteor-1", type: "TXT", size: "500b" },
    ]);

    const selectLocation = (location) => {
      selectedLocation.value = location;
    };

    // 使用简单的图表代替地图
    const initLocationChart = () => {
      if (!mapContainer.value) return;

      try {
        const chart = echarts.init(mapContainer.value);
        const option = {
          backgroundColor: "transparent",
          tooltip: {
            trigger: "item",
          },
          legend: {
            top: "5%",
            left: "center",
            textStyle: {
              color: "#fff",
            },
          },
          series: [
            {
              name: "数据中心分布",
              type: "pie",
              radius: ["40%", "70%"],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: "#fff",
                borderWidth: 2,
              },
              label: {
                show: true,
                color: "#fff",
                formatter: "{b}\n{c}个",
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: "20",
                  fontWeight: "bold",
                },
              },
              labelLine: {
                show: true,
              },
              data: [
                { value: 2, name: "华东" },
                { value: 1, name: "华北" },
                { value: 1, name: "华南" },
              ],
            },
          ],
        };

        chart.setOption(option);

        // 添加点击事件
        chart.on("click", (params) => {
          const location = locations.find((loc) => loc.region === params.name);
          if (location) {
            selectLocation(location);
          }
        });
      } catch (error) {
        console.error("图表加载失败:", error);
      }
    };

    onMounted(() => {
      initLocationChart();
      initPyramidChart();
      initRadarChart();
      initSankeyChart();

      window.addEventListener("resize", () => {
        pyramidChart.value?.resize();
        radarChart.value?.resize();
        sankeyChart.value?.resize();
      });
    });

    const initPyramidChart = () => {
      const chart = echarts.init(document.querySelector(".pyramid-chart"));
      pyramidChart.value = chart;

      const option = {
        tooltip: {
          trigger: "item",
          formatter: "{b} : {c}",
        },
        series: [
          {
            type: "funnel",
            width: "80%",
            height: "80%",
            min: 0,
            max: 100,
            sort: "descending",
            gap: 2,
            label: {
              show: true,
              position: "inside",
            },
            itemStyle: {
              borderColor: "#fff",
              borderWidth: 1,
            },
            emphasis: {
              label: {
                fontSize: 20,
              },
            },
            data: [
              { value: 100, name: "采集" },
              { value: 80, name: "清洗" },
              { value: 60, name: "分析" },
              { value: 40, name: "存储" },
              { value: 20, name: "应用" },
            ],
          },
        ],
      };

      chart.setOption(option);
    };

    const initRadarChart = () => {
      const chart = echarts.init(document.querySelector(".radar-chart"));
      radarChart.value = chart;

      const option = {
        radar: {
          indicator: [
            { name: "视频数据", max: 100 },
            { name: "图像数据", max: 100 },
            { name: "文本数据", max: 100 },
            { name: "传感器数据", max: 100 },
            { name: "其他数据", max: 100 },
          ],
          shape: "pentagon",
          splitNumber: 5,
          axisName: {
            color: "#fff",
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255, 255, 255, 0.2)",
            },
          },
          splitArea: {
            show: false,
          },
          axisLine: {
            lineStyle: {
              color: "rgba(255, 255, 255, 0.2)",
            },
          },
        },
        series: [
          {
            type: "radar",
            data: [
              {
                value: [90, 85, 70, 95, 60],
                name: "数据分布",
                itemStyle: {
                  color: "#58D9F9",
                },
                areaStyle: {
                  color: "rgba(88, 217, 249, 0.3)",
                },
              },
            ],
          },
        ],
      };

      chart.setOption(option);
    };

    const initSankeyChart = () => {
      const chart = echarts.init(document.querySelector(".sankey-chart"));
      sankeyChart.value = chart;

      const option = {
        series: {
          type: "sankey",
          layout: "none",
          emphasis: {
            focus: "adjacency",
          },
          data: [
            { name: "原始数据" },
            { name: "预处理" },
            { name: "特征提取" },
            { name: "分类存储" },
            { name: "应用层" },
          ],
          links: [
            { source: "原始数据", target: "预处理", value: 5 },
            { source: "预处理", target: "特征提取", value: 3 },
            { source: "特征提取", target: "分类存储", value: 2 },
            { source: "分类存储", target: "应用层", value: 1 },
          ],
        },
      };

      chart.setOption(option);
    };

    return {
      sensorData,
      selectedLocation,
      locations,
      selectLocation,
      mapContainer,
      mapLoaded,
    };
  },
};
</script>

<style scoped>
.data-center {
  padding: 20px;
  background-color: #0a1929;
  min-height: 100vh;
  color: white;
}

.data-total-section {
  background-color: rgba(0, 30, 60, 0.5);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
}

.counter-display {
  display: flex;
  align-items: center;
}

.digit-group {
  display: flex;
  gap: 5px;
}

.digit {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 10px 15px;
  border-radius: 4px;
  font-size: 24px;
  font-weight: bold;
  color: #58d9f9;
}

.unit {
  margin-left: 10px;
  color: #90caf9;
  font-size: 20px;
}

.storage-info {
  display: flex;
  gap: 40px;
  flex-grow: 1;
}

.storage-container {
  width: 100px;
  height: 150px;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.storage-level {
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: #58d9f9;
  transition: height 0.3s ease;
}

.storage-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  font-size: 12px;
  width: 100%;
}

.system-status {
  flex-grow: 1;
}

.status-item {
  margin-bottom: 15px;
}

.status-label {
  color: #90caf9;
  margin-bottom: 5px;
}

.status-bar {
  height: 8px;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background-color: #58d9f9;
  transition: width 0.3s ease;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.section-title {
  color: #ff4081;
  font-size: 16px;
  margin-bottom: 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.map-section,
.sensor-section,
.stats-section,
.database-section {
  background-color: rgba(0, 30, 60, 0.5);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.map-container {
  height: 400px;
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
}

.data-center-info {
  margin-top: 15px;
  display: flex;
  gap: 20px;
}

.info-box {
  display: flex;
  gap: 10px;
}

.info-label {
  color: #90caf9;
}

.info-value {
  color: #58d9f9;
}

.time-info {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.time-item {
  text-align: center;
}

.time-label {
  color: #90caf9;
  margin-bottom: 5px;
}

.time-value {
  color: #58d9f9;
  font-size: 24px;
  font-weight: bold;
}

.sensor-table {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

th {
  color: #90caf9;
  font-weight: normal;
}

td {
  color: #fff;
}

.pyramid-chart,
.radar-chart,
.sankey-chart {
  height: 300px;
}

.db-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.db-info {
  color: #90caf9;
  line-height: 1.6;
}

.db-system-btn {
  background-color: #004bcc;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.db-system-btn:hover {
  background-color: #0056e9;
}

.map-fallback {
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.location-list {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.location-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.location-item:hover {
  background-color: rgba(0, 30, 60, 0.8);
}

.location-item.active {
  background-color: #004bcc;
}

.location-dot {
  width: 12px;
  height: 12px;
  background-color: #58d9f9;
  border-radius: 50%;
}

.location-info {
  flex: 1;
}

.location-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 5px;
}

.location-detail {
  color: #90caf9;
  font-size: 0.9em;
}
</style>
