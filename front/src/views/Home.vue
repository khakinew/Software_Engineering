<template>
  <div class="home">
    <!-- 左侧视频区域 -->
    <div class="section video-section">
      <div class="section-header">
        <span class="icon">监控视频</span>
        <h2>视频展示</h2>
      </div>
      <div class="video-container">
        <div class="video-tabs">
          <button
            v-for="n in 4"
            :key="n"
            :class="['tab-btn', { active: currentVideo === n }]"
            @click="currentVideo = n"
          >
            视频{{ n }}
          </button>
        </div>
        <div class="video-player">
          <video
              class="video-stream"
              :src="currentVideoSrc"
              type="video/mp4"
              controls
              autoplay
              muted
              loop
          ></video>
          <div class="video-info">{{ currentDate }} {{ currentTime }}</div>
        </div>
        <div class="video-controls">
          <div class="control-group">
            <h3>附加功能</h3>
            <div class="control-buttons">
              <button class="control-btn" :class="{ active: controls.camera }">
                <i class="icon-camera">📷</i>
                摄像机
              </button>
              <button class="control-btn" :class="{ active: controls.light }">
                <i class="icon-light">💡</i>
                灯光
              </button>
              <button class="control-btn" :class="{ active: controls.cleaner }">
                <i class="icon-cleaner">🧹</i>
                清洁刷
              </button>
            </div>
            <div class="control-buttons">
              <button class="control-btn">
                <i class="icon-playback">🔵</i>
                视频回放
              </button>
              <button class="control-btn">
                <i class="icon-split">💟</i>
                视频同时播放
              </button>
              <button class="control-btn">
                <i class="icon-cloud">📹️</i>
                云台摄像机
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧数据区域 -->
    <div class="right-panel">
      <!-- 水文气象数据 -->
      <div class="section data-section">
        <div class="section-header">
          <span class="icon">水文气象</span>
          <h2>水文数据展示</h2>
        </div>
        <div class="data-grid">
          <div class="data-item" v-for="item in waterData" :key="item.label">
            <div class="data-label">{{ item.label }}</div>
            <div class="data-value" :style="{ color: item.color }">
              {{ item.value }}
            </div>
            <div class="data-progress">
              <div
                class="progress-bar"
                :style="{
                  width: item.percentage + '%',
                  backgroundColor: item.color,
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 位置信息 -->
      <div class="section map-section">
        <div class="section-header">
          <span class="icon">定位</span>
          <h2>海洋牧场位置展示</h2>
        </div>
        <div class="map-container">
          <div id="amap" class="map-image"></div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div class="section history-section">
        <div class="section-header">
          <span class="icon">历史记录</span>
          <h2>历史水文数据展示</h2>
        </div>
        <div class="history-container">
          <div class="history-controls">
            <button
            v-for="period in ['近一天', '近一周', '近一月', '近一年']"
  :key="period"
  :class="['period-btn', { active: currentPeriod === period }]"
  @click="onPeriodClick(period)"
            >
              {{ period }}
            </button>
            <select v-model="selectedMetric">
              <option value="电导率">电导率</option>
              <option value="水温">水温</option>
              <option value="ph">ph值</option>
            </select>
          </div>
          <div class="chart-container" ref="chartContainer" @dblclick="handleDownloadChart">
            <div class="chart-hint">点击图表下载</div>
          </div>
        </div>
      </div>

      <!-- 设备状态 -->
      <div class="section device-section">
        <div class="section-header">
          <span class="icon">设备状态</span>
        </div>
        <div class="device-info">
          <div class="info-row">
            <span class="label">设备ID</span>
            <span class="value">8D19C331-4F08-47A1</span>
          </div>
          <div class="info-row">
            <span class="label">主控状态</span>
            <div class="status-group">
              <div class="status-item">
                <span class="label">版本：</span>
                <span class="value">V0.1.1</span>
              </div>
              <div class="status-item">
                <span class="label">温度：</span>
                <span class="value warning">39.64°C</span>
              </div>
            </div>
          </div>
          <div class="info-row">
            <span class="label">次控状态</span>
            <div class="status-group">
              <div class="status-item">
                <span class="label">连接：</span>
                <span class="value error">断开</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from "vue";
import * as echarts from "echarts";
import AMapLoader from '@amap/amap-jsapi-loader'
import { downloadEChart } from "@/utils/echart";
import {getEchartData} from "@/api/auth"
import { debounce } from 'lodash';

export default {
  computed: {
    currentVideoSrc() {
      return `/videos/shiping_${this.currentVideo}.mp4`;
    },
  },
  name: "Home",
  setup() {
    const currentVideo = ref(1);
    const currentPeriod = ref("近一天");
    const selectedMetric = ref("电导率");
    const chartContainerMap = ref(null);
    const controls = ref({
      camera: true,
      light: true,
      cleaner: false,
    });

    const currentDate = computed(() => {
      const date = new Date();
      return `${date.getFullYear()}年${
        date.getMonth() + 1
      }月${date.getDate()}日`;
    });

    const currentTime = computed(() => {
      const date = new Date();
      return `${date.getHours().toString().padStart(2, "0")}:${date
        .getMinutes()
        .toString()
        .padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")}`;
    });

    const waterData = ref([
      {
        label: "电池电压 (V)",
        value: "25.90",
        color: "#FFB74D",
        percentage: 80,
      },
      { label: "盐度 (‰)", value: "34.16", color: "#4CAF50", percentage: 65 },
      {
        label: "溶解氧 (mg/L)",
        value: "0.00",
        color: "#F44336",
        percentage: 0,
      },
      { label: "浊度 (NTU)", value: "2.05", color: "#2196F3", percentage: 20 },
      { label: "pH", value: "8.37", color: "#9C27B0", percentage: 75 },
      { label: "水温 (°C)", value: "15", color: "#00BCD4", percentage: 45 },
    ]);

    // 模拟视频源
    const videoSource = ref(
      "https://via.placeholder.com/800x450/1a237e/ffffff?text=Video+Stream"
    );
    // 模拟地图源
    const mapSource = ref(
      "https://via.placeholder.com/400x300/1a237e/ffffff?text=Location+Map"
    );

    let chart = null;

    onMounted(() => {
      AMapLoader.load({
        key:"035feed40c80a0a3a028dc37b5166910",
        version:"2.0",
        plugins:["Amap.Geolocation"],
      })
          .then((AMap)=>{
            const map = new AMap.Map("amap", {
              resizeEnable: true,
              zoom: 11,
              center: [117.77475, 39.064596], // 默认中心点，北京
            });
            new AMap.Marker({
              position: [117.77475, 39.064596],
              map: map,
            });
          })
          .catch((e)=>{
            console.error("高德地图加载失败：",e);
          });
      initChart("day").then(() => {});
      // 更新当前时间
      setInterval(() => {
        currentTime.value = new Date().toLocaleTimeString();
      }, 1000);
    });

    watch(selectedMetric, () => {
      const periodType = periodMap[currentPeriod.value];
      initChart(periodType);
    });

    const initChart =async (timeStr) => {
      const metricMap = {
        "电导率": "conductivity",
        "水温": "temperature",
        "ph值": "ph"
      };
      const metricKey = metricMap[selectedMetric.value];
      const res = await getEchartData(timeStr, "", metricKey); // "" 为 site 名占位符，如有需要后续可加

      const resData=res.data

      const chartDom = document.querySelector(".chart-container");

      chart = echarts.init(chartDom);
      chartContainerMap.value = chart;
      const option = {
        grid: {
          top: 40,
          right: 20,
          bottom: 40,
          left: 60,
        },
        tooltip: { trigger: "axis" },
        title: {
          text: selectedMetric.value + '变化趋势',
          textStyle: {
            color: '#ffffff'
          }
        },
        xAxis: {
          type: "category",
          data: resData.x,
          axisLine: {
            lineStyle: {
              color: "#ffffff",
              show: true, // 确保显示标签
              fontSize: 12
            },
          },
          axisLabel: {
            color: "#ffffff",
            show: true // 确保显示轴线
          },
        },
        yAxis: {
          type: "value",
          axisLine: {
            lineStyle: {
              color: "#ffffff",
              show: true, // 确保显示标签
              fontSize: 12
            },
          },
          axisLabel: {
            color: "#ffffff",
            show: true // 确保显示轴线
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255,255,255,0.1)",
            },
          },
        },
        series: [
          {
            data:resData.y,
            type: "line",
            smooth: true,
            lineStyle: {
              color: "#4CAF50",
            },
            areaStyle: {
              color: {
                type: "linear",
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: "rgba(76,175,80,0.3)",
                  },
                  {
                    offset: 1,
                    color: "rgba(76,175,80,0)",
                  },
                ],
              },
            },
          },
        ],
      };

      chart.setOption(option);
    };
    const handleDownloadChart = () => {
      downloadEChart(chartContainerMap.value, "chart.png");
    };


// 后端映射（比如你接口需要 day/week/month/year）
const periodMap = {
  '近一天': 'day',
  '近一周': 'week',
  '近一月': 'month',
  '近一年': 'year',
};

const onPeriodClick = debounce((period) => {
  currentPeriod.value = period;
  const periodType = periodMap[period];
  initChart(periodType); // 比如调用接口或更新图表
}, 500); // 500 毫秒内只触发一次
    return {
      currentVideo,
      currentPeriod,
      selectedMetric,
      getEchartData,
      controls,
      waterData,
      videoSource,
      mapSource,
      currentDate,
      currentTime,
      chartContainerMap,
      downloadEChart,
      handleDownloadChart,
      onPeriodClick
    };
  },
};
</script>

<style scoped>
.home {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #0a1929;
  min-height: calc(100vh - 60px);
  color: white;
}

.section {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

.section-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #ff4081;
}

.video-section {
  flex: 1;
  min-width: 800px;
}

.right-panel {
  width: 400px;
}

.video-container {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.video-tabs {
  display: flex;
  gap: 10px;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.2);
}

.tab-btn {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.tab-btn.active {
  background-color: #1976d2;
  border-color: #1976d2;
}

.video-player {
  position: relative;
}

.video-stream {
  width: 100%;
  height: auto;
  display: block;
}

.video-info {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 5px 10px;
  border-radius: 4px;
}

.control-group {
  padding: 15px;
}

.control-group h3 {
  margin: 0 0 15px 0;
  font-size: 1rem;
  color: #90caf9;
}

.control-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}

.control-btn {
  background-color: rgba(25, 118, 210, 0.1);
  border: 1px solid rgba(25, 118, 210, 0.2);
  color: white;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.control-btn.active {
  background-color: rgba(25, 118, 210, 0.3);
  border-color: #1976d2;
}

.data-grid {
  display: grid;
  gap: 15px;
}

.data-item {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 10px;
  border-radius: 4px;
}

.data-label {
  font-size: 0.9rem;
  color: #90caf9;
  margin-bottom: 5px;
}

.data-value {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.data-progress {
  height: 4px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.progress-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.map-container {
  height: 300px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.history-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.period-btn {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.period-btn.active {
  background-color: #1976d2;
  border-color: #1976d2;
}

.chart-container {
  height: 300px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}



.device-info {
  display: grid;
  gap: 15px;
}

.info-row {
  display: grid;
  gap: 10px;
}

.info-row .label {
  color: #90caf9;
}

.status-group {
  display: flex;
  gap: 20px;
}

.status-item {
  display: flex;
  gap: 5px;
}

.warning {
  color: #ffc107;
}

.error {
  color: #f44336;
}

select {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
}

/* 图标样式 */
[class^="icon-"] {
  width: 24px;
  height: 24px;
  display: inline-block;
  background-color: currentColor;
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
}
</style>
