<template>
  <div class="intelligent-center">
    <!-- 左侧环境得分面板 -->
    <div class="left-panel">
      <div class="score-panel">
        <h3 class="panel-title">海洋牧场环境总得分</h3>
        <div class="depth-scores">
          <div
            class="depth-item"
            v-for="(score, index) in depthScores"
            :key="index"
          >
            {{ score.depth }}深水层
          </div>
        </div>
        <div class="gauge-chart">
          <div class="gauge" ref="gaugeChart"></div>
          <div class="warning-text">
            <div class="warning-icon">
              <i class="fas fa-thermometer-half"></i>
            </div>
            <div class="warning-content">
              <div>预警</div>
              <div>水温过高</div>
            </div>
          </div>
        </div>
      </div>
      <div class="network-panel">
        <h3 class="panel-title">网衰监测</h3>
        <div
          class="province-chart"
          ref="networkChart"
          @dblclick="handleNetloadChart"
        ></div>
        <div class="network-info">
          <div class="info-date">网衰破损（2024-02-01）</div>
        </div>
      </div>
    </div>

    <!-- 中间视频识别面板 -->
    <div class="center-panel">
      <div class="video-section">
        <h3 class="panel-title">图像识别</h3>
        <div class="video-container">
          <div class="main-video">
            <video ref="mainVideo" autoplay loop muted :key="currentVideo">
              <source :src="currentVideoSrc" type="video/mp4" />
            </video>
            <div class="video-info">
              <span>2024年01月31日 星期三 21:00:00</span>
            </div>
          </div>
          <div class="video-controls">
            <button
              v-for="n in 4"
              :key="n"
              :class="{ active: currentVideo === n }"
              @click="switchVideo(n)"
            >
              视频{{ n }}
            </button>
          </div>
        </div>

        <div class="bottom-cameras">
          <div class="camera-view">
            <h4 class="panel-title">左目镜头</h4>
            <video :key="leftEyeSrc" autoplay muted loop playsinline>
              <source :src="leftEyeSrc" type="video/mp4" />
            </video>
          </div>
          <div class="camera-view">
            <h4 class="panel-title">右目镜头</h4>
            <video :key="rightEyeSrc" autoplay muted loop playsinline>
              <source :src="rightEyeSrc" type="video/mp4" />
            </video>
          </div>
        </div>

        <div class="fish-info">
          <h3 class="section-title">识别出的鱼的信息</h3>
          <div class="info-grid">
            <div class="info-card">
              <div class="card-icon">T</div>
              <div class="card-content">
                <div class="card-label">编号</div>
                <div class="card-value">fish-9527</div>
              </div>
            </div>
            <div class="info-card">
              <div class="card-icon">🐟</div>
              <div class="card-content">
                <div class="card-label">鱼种</div>
                <div class="card-value">moonfish</div>
              </div>
            </div>
            <div class="info-card">
              <div class="card-icon">📏</div>
              <div class="card-content">
                <div class="card-label">体长</div>
                <div class="card-value">10寸</div>
              </div>
            </div>
            <div class="info-card">
              <div class="card-icon">⚖️</div>
              <div class="card-content">
                <div class="card-label">体重</div>
                <div class="card-value">5kg</div>
              </div>
            </div>
          </div>
          <div class="action-buttons">
            <button class="action-btn danger">
              <i class="fas fa-exclamation-triangle"></i>
              疾病预警【黄】
            </button>
            <button class="action-btn warning">
              <i class="fas fa-fish"></i>
              鱼群异常（聚群）
            </button>
            <button class="action-btn primary">
              <i class="fas fa-chart-line"></i>
              轨迹追踪
            </button>
            <button class="action-btn primary">
              <i class="fas fa-chart-bar"></i>
              轨迹分析
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧监控面板 -->
    <div class="right-panel">
      <div class="ai-stats">
        <div class="ai-logo">
          <h3 class="panel-title">AI决策</h3>
          <a
            href="https://chat.openai.com/"
            target="_blank"
            title="点击和GPT对话"
          >
            <img src="/images/AI.png" alt="AI决策" />
          </a>
        </div>
        <div class="stats-list">
          <div class="stat-item">
            <span class="stat-label">温度：</span>
            <span class="stat-value">10 ~ 20</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">光照：</span>
            <span class="stat-value">20 ~ 100</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">溶解氧：</span>
            <span class="stat-value">0.2 ~ 0.5</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">pH：</span>
            <span class="stat-value">8 ~ 8.7</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">盐度：</span>
            <span class="stat-value">0.01 ~ 0.03</span>
          </div>
        </div>
        <div class="ai-suggestion">
          <h4>提示：</h4>
          <p>未来几天可能降雨</p>
          <p>请确保温度、风度正常</p>
        </div>
      </div>
      <div class="weather-info">
        <!-- 只有在 weather 有值后才渲染下面内容 -->
        <div class="weather-grid" v-if="weather">
          <div class="weather-item">
            <i class="fas fa-temperature-low"></i>
            <span>{{ weather.temperature }}</span>
          </div>
          <div class="weather-item">
            <i class="fas fa-wind"></i>
            <span>{{ weather.wind }}</span>
          </div>
          <div class="weather-item">
            <i class="fas fa-tint"></i>
            <span>{{ weather.humidity }}</span>
          </div>
        </div>

        <div class="weather-alert" v-if="weather">
          <div class="alert-time">{{ weather.reporttime }}</div>
          <div class="alert-source">{{ weather.source }}</div>
        </div>
      </div>
    </div>
    <a href="localhost:2222" target="_blank" class="floating-button">
      和智能助手聊天吧！
    </a>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import * as echarts from "echarts";
import axios from "axios";
import { downloadEChart } from "@/utils/echart";

export default {
  data() {
    return {
      currentVideo: 1,
    };
  },
  computed: {
    currentVideoSrc() {
      return `/videos/zhineng_${this.currentVideo}.mp4`;
    },
    leftEyeSrc() {
      return `/videos/left_eye_${this.currentVideo}.mp4`;
    },
    rightEyeSrc() {
      return `/videos/shiping_${this.currentVideo}.mp4`;
    },
  },
  methods: {
    switchVideo(n) {
      this.currentVideo = n;
      const videoEl = this.$refs.mainVideo;
      if (videoE1) {
        videoE1.load();
      }
    },
  },
  name: "IntelligentCenter",
  setup() {
    const gaugeChart = ref(null);
    const networkChart = ref(null);
    const currentVideo = ref(1);
    const analysisData = ref({
      temperature: { current: 15, trend: "up", warning: true },
      oxygen: { current: 0.35, trend: "stable", warning: false },
      ph: { current: 8.3, trend: "down", warning: false },
      salinity: { current: 0.02, trend: "stable", warning: false },
    });

    const depthScores = ref([
      { depth: "0.25M", score: 85 },
      { depth: "0.5M", score: 92 },
      { depth: "0.75M", score: 88 },
      { depth: "1.0M", score: 90 },
    ]);

    // 智能分析函数
    const analyzeEnvironment = () => {
      // 模拟智能分析逻辑
      const analysis = [];
      if (analysisData.value.temperature.warning) {
        analysis.push({
          type: "warning",
          message: "水温异常，建议开启降温系统",
          action: "启动降温",
        });
      }
      return analysis;
    };

    // 实时数据更新
    const updateEnvironmentData = () => {
      // 模拟数据更新
      const interval = setInterval(() => {
        analysisData.value.temperature.current += (Math.random() - 0.5) * 0.1;
        analysisData.value.oxygen.current += (Math.random() - 0.5) * 0.01;
        analysisData.value.ph.current += (Math.random() - 0.5) * 0.05;
        analysisData.value.salinity.current += (Math.random() - 0.5) * 0.001;

        // 更新趋势
        analysisData.value.temperature.trend =
          analysisData.value.temperature.current > 20 ? "up" : "stable";

        // 更新警告状态
        analysisData.value.temperature.warning =
          analysisData.value.temperature.current > 25;
      }, 5000);

      onUnmounted(() => {
        clearInterval(interval);
      });
    };
    const weather = ref({
      temperature: "--",
      wind: "--",
      humidity: "--",
      reporttime: "--",
      city: "--",
      source: "高德地图气象中心",
    });

    const getWeather = async () => {
      try {
        const key = "cf66b80cc13dbeae7fcbbcc2c001af66";
        const cityCode = "120000";
        const res = await axios.get(
          "https://restapi.amap.com/v3/weather/weatherInfo",
          {
            params: {
              key,
              city: cityCode,
              extensions: "base",
            },
          }
        );

        console.log("天气数据返回：", res.data);

        if (res.data.status === "1") {
          const data = res.data.lives[0];
          weather.value = {
            temperature: data.temperature + "°C",
            wind: data.winddirection + "风" + data.windpower + "级",
            humidity: data.humidity + "%",
            reporttime: data.reporttime,
            city: data.city,
            source: "高德地图气象中心",
          };
        }
      } catch (err) {
        console.error("天气获取失败：", err);
      }
    };

    // 初始化图表
    const initGaugeChart = () => {
      if (!gaugeChart.value) return;

      const chart = echarts.init(gaugeChart.value);
      const option = {
        series: [
          {
            type: "gauge",
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 100,
            splitNumber: 10,
            itemStyle: {
              color: "#58D9F9",
              shadowColor: "rgba(0,138,255,0.45)",
              shadowBlur: 10,
              shadowOffsetX: 2,
              shadowOffsetY: 2,
            },
            progress: {
              show: true,
              roundCap: true,
              width: 18,
            },
            pointer: {
              icon: "path://M2090.36389,615.30999 L2090.36389,615.30999 C2091.48372,615.30999 2092.40383,616.194028 2092.44859,617.312956 L2096.90698,728.755929 C2097.05155,732.369577 2094.2393,735.416212 2090.62566,735.56078 C2090.53845,735.564269 2090.45117,735.566014 2090.36389,735.566014 L2090.36389,735.566014 C2086.74736,735.566014 2083.81557,732.63423 2083.81557,729.017692 C2083.81557,728.930412 2083.81732,728.84314 2083.82081,728.755929 L2088.2792,617.312956 C2088.32396,616.194028 2089.24407,615.30999 2090.36389,615.30999 Z",
              length: "75%",
              width: 16,
              offsetCenter: [0, "5%"],
            },
            axisLine: {
              roundCap: true,
              lineStyle: {
                width: 18,
              },
            },
            axisTick: {
              splitNumber: 2,
              lineStyle: {
                width: 2,
                color: "#999",
              },
            },
            splitLine: {
              length: 12,
              lineStyle: {
                width: 3,
                color: "#999",
              },
            },
            axisLabel: {
              distance: 30,
              color: "#999",
              fontSize: 14,
            },
            title: {
              show: false,
            },
            detail: {
              backgroundColor: "#fff",
              borderColor: "#999",
              borderWidth: 2,
              width: "60%",
              lineHeight: 40,
              height: 40,
              borderRadius: 8,
              offsetCenter: [0, "35%"],
              valueAnimation: true,
              formatter: function (value) {
                return "{value|" + value.toFixed(0) + "}{unit|分}";
              },
              rich: {
                value: {
                  fontSize: 30,
                  fontWeight: "bolder",
                  color: "#777",
                },
                unit: {
                  fontSize: 14,
                  color: "#999",
                  padding: [0, 0, -20, 10],
                },
              },
            },
            data: [
              {
                value: 85,
              },
            ],
          },
        ],
      };

      chart.setOption(option);
    };

    const initNetworkChart = () => {
      const chart = echarts.init(document.querySelector(".province-chart"));
      const option = {
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        tooltip: { trigger: "axis" },
        xAxis: {
          type: "category",
          data: [
            "1月",
            "2月",
            "3月",
            "4月",
            "5月",
            "6月",
            "7月",
            "8月",
            "9月",
            "10月",
            "11月",
            "12月",
          ],
          axisLabel: {
            color: "#fff",
          },
        },
        yAxis: {
          type: "value",
          axisLabel: {
            color: "#fff",
          },
        },
        series: [
          {
            data: [12, 15, 8, 23, 19, 27, 31, 24, 28, 21, 17, 22],
            type: "bar",
            itemStyle: {
              color: "#58D9F9",
            },
          },
        ],
      };
      chart.setOption(option);
      networkChart.value = chart;
    };
    const handleNetloadChart = () => {
      if (networkChart.value) {
        downloadEChart(networkChart.value, "network_chart.png");
      } else {
        console.warn("networkChart 未初始化");
      }
    };

    const switchVideo = (n) => {
      currentVideo.value = n;
    };

    onMounted(() => {
      getWeather();
      initGaugeChart();
      initNetworkChart();
      updateEnvironmentData();

      window.addEventListener("resize", () => {
        gaugeChart.value?.resize();
        networkChart.value?.resize();
      });
    });

    onUnmounted(() => {
      window.removeEventListener("resize", () => {
        gaugeChart.value?.resize();
        networkChart.value?.resize();
      });
    });

    return {
      handleNetloadChart,
      weather,
      currentVideo,
      depthScores,
      switchVideo,
    };
  },
};
</script>

<style scoped>
.intelligent-center {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
  padding: 20px;
  background-color: #0a1929;
  min-height: 100vh;
  color: white;
}

.panel-title {
  color: #ff4081;
  font-size: 16px;
  margin-bottom: 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.left-panel,
.center-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: min-content;
}

.bottom-cameras {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  gap: 20px;
}

.bottom-cameras .camera-view {
  flex: 1;
  background: #111;
  border-radius: 10px;
  overflow: hidden;
  background-color: rgba(0, 30, 60, 0.5);
}

.bottom-cameras .camera-view video {
  width: 100%;
  height: auto;
  object-fit: contain;
}

.score-panel,
.network-panel,
.video-section,
.camera-feeds,
.ai-stats,
.weather-info {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
}

.depth-scores {
  margin-bottom: 20px;
}

.depth-item {
  padding: 8px;
  background-color: rgba(0, 0, 0, 0.2);
  margin-bottom: 8px;
  border-radius: 4px;
  color: #90caf9;
}

.gauge-chart {
  height: 300px;
  position: relative;
}

.gauge {
  height: 100%;
}

.warning-text {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 10px;
}

.warning-icon {
  color: #ff4081;
  font-size: 24px;
}

.province-chart {
  height: 200px;
}

.network-info {
  text-align: center;
  margin-top: 10px;
  color: #ff4081;
}

.video-container {
  margin-bottom: 20px;
}

.main-video {
  position: relative;
  width: 100%;
  height: 400px;
  background-color: #000;
  margin-bottom: 10px;
}

.main-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 5px 10px;
  border-radius: 4px;
}

.video-controls {
  display: flex;
  gap: 10px;
}

.video-controls button {
  background-color: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.video-controls button.active {
  background-color: #004bcc;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.info-card {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-icon {
  width: 40px;
  height: 40px;
  background-color: #004bcc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.card-content {
  flex: 1;
}

.card-label {
  color: #90caf9;
  font-size: 12px;
  margin-bottom: 5px;
}

.card-value {
  color: #fff;
  font-weight: bold;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.action-btn {
  padding: 10px;
  border-radius: 4px;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.action-btn.danger {
  background-color: #ff4081;
}

.action-btn.warning {
  background-color: #ffa726;
}

.action-btn.primary {
  background-color: #004bcc;
}

.camera-view {
  width: 100%;
  height: 200px;
  background-color: #000;
  margin-bottom: 20px;
  border-radius: 4px;
  overflow: hidden;
  object-fit: contain;
}

.camera-view img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ai-stats {
  text-align: center;
}

.ai-logo {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
}

.ai-logo img {
  width: 70%;
  height: 70%;
}

.stats-list {
  text-align: left;
  margin-bottom: 20px;
}

.stat-item {
  margin-bottom: 10px;
}

.stat-label {
  color: #90caf9;
}

.ai-suggestion {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 4px;
  text-align: left;
}

.ai-suggestion h4 {
  color: #ff4081;
  margin-bottom: 10px;
}

.weather-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 15px;
}

.weather-item {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.weather-item i {
  color: #58d9f9;
  font-size: 20px;
}

.weather-alert {
  background-color: rgba(255, 0, 0, 0.1);
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.alert-time {
  color: #ff4081;
  margin-bottom: 5px;
}

.alert-source {
  font-size: 12px;
  color: #90caf9;
}

.floating-button {
  position: fixed;
  right: 30px;
  bottom: 30px;
  width: 60px;
  height: 60px;
  background-color: #4caf50;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 60px;
  font-size: 24px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  text-decoration: none;
  transition: all 0.3s;
}

.floating-button:hover {
  background-color: #45a049;
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}
</style>
