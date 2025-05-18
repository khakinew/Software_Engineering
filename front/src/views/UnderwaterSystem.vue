<template>
  <div class="underwater-system">
    <!-- 顶部计数器 -->
    <div class="counter-section">
      <div class="fish-counter">
        <div class="digit-group">
          <div class="digit">0</div>
          <div class="digit">1</div>
          <div class="digit">0</div>
          <div class="digit">3</div>
          <div class="digit">8</div>
        </div>
        <div class="counter-labels">
          <div>今日新增</div>
          <div>今日死亡</div>
        </div>
      </div>
    </div>

    <div class="main-content">
      <!-- 左侧面板 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h2>环境得分计算</h2>
          </div>
          <div class="environment-scores">
            <div class="score-item">
              <div class="score-label">0.25M深水层</div>
              <div class="score-value">85</div>
            </div>
            <div class="score-item">
              <div class="score-label">0.5M深水层</div>
              <div class="score-value">92</div>
            </div>
            <div class="score-item">
              <div class="score-label">0.75M深水层</div>
              <div class="score-value">88</div>
            </div>
            <div class="score-item">
              <div class="score-label">1.0M深水层</div>
              <div class="score-value">90</div>
            </div>
          </div>
          <div class="gauge-chart" ref="gaugeChart"></div>
        </div>
      </div>

      <!-- 中间面板 -->
      <div class="center-panel">
        <div class="info-cards">
          <div class="info-card">
            <div class="card-header">鱼种</div>
            <div class="card-value">50<span class="unit">+</span></div>
          </div>
          <div class="info-card">
            <div class="card-header">鱼苗</div>
            <div class="card-value">500<span class="unit">尾</span></div>
          </div>
          <div class="info-card">
            <div class="card-header">生长</div>
            <div class="card-value">600<span class="unit">尾</span></div>
          </div>
        </div>

        <div class="circle-progress">
          <div class="progress-title">总信息统计展示</div>
          <div class="progress-chart" ref="circleProgressChart"></div>
          <div class="digital-display">
            <div class="display-title">已保障养殖鱼群</div>
            <div class="digital-number">
              <span
                v-for="(digit, index) in '000000000'"
                :key="index"
                class="digit-box"
                >{{ digit }}</span
              >
              <span class="unit">尾</span>
            </div>
          </div>
        </div>

        <div class="device-info">
          <div class="device-card">
            <div class="card-header">镜头</div>
            <div class="card-value">5<span class="unit">+</span></div>
          </div>
          <div class="device-card">
            <div class="card-header">云台</div>
            <div class="card-value">2</div>
          </div>
          <div class="device-card">
            <div class="card-header">声呐</div>
            <div class="card-value">1</div>
          </div>
        </div>
      </div>

      <!-- 右侧面板 -->
      <div class="right-panel">
        <div class="panel-section">
          <div class="section-header">
            <h2>鱼群种类统计</h2>
          </div>
          <div class="pie-chart" ref="speciesChart"></div>
        </div>
        <div class="panel-section">
          <div class="section-header">
            <h2>鱼群数量变化</h2>
          </div>
          <div class="line-chart" ref="populationChart"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import * as echarts from "echarts";

export default {
  name: "UnderwaterSystem",
  setup() {
    let gaugeChart = null;
    let circleProgressChart = null;
    let speciesChart = null;
    let populationChart = null;

    onMounted(() => {
      initGaugeChart();
      initCircleProgressChart();
      initSpeciesChart();
      initPopulationChart();

      // 响应式调整
      window.addEventListener("resize", () => {
        gaugeChart?.resize();
        circleProgressChart?.resize();
        speciesChart?.resize();
        populationChart?.resize();
      });
    });

    const initGaugeChart = () => {
      const chartDom = document.querySelector(".gauge-chart");
      gaugeChart = echarts.init(chartDom);

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
              fontSize: 12,
            },
            title: {
              offsetCenter: [0, "30%"],
              fontSize: 20,
              color: "#fff",
            },
            detail: {
              backgroundColor: "#fff",
              borderColor: "#999",
              borderWidth: 2,
              width: 60,
              height: 40,
              offsetCenter: [0, "70%"],
              valueAnimation: true,
              formatter: "{value}",
              color: "#58D9F9",
            },
            data: [
              {
                value: 70,
                name: "环境评分",
              },
            ],
          },
        ],
      };

      gaugeChart.setOption(option);
    };

    const initCircleProgressChart = () => {
      const chartDom = document.querySelector(".progress-chart");
      circleProgressChart = echarts.init(chartDom);

      const option = {
        series: [
          {
            type: "pie",
            radius: ["75%", "90%"],
            avoidLabelOverlap: false,
            label: {
              show: false,
            },
            emphasis: {
              label: {
                show: false,
              },
            },
            data: [
              { value: 75, name: "已完成", itemStyle: { color: "#58D9F9" } },
              {
                value: 25,
                name: "未完成",
                itemStyle: { color: "rgba(255, 255, 255, 0.2)" },
              },
            ],
          },
        ],
      };

      circleProgressChart.setOption(option);
    };

    const initSpeciesChart = () => {
      const chartDom = document.querySelector(".pie-chart");
      speciesChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: "item",
        },
        series: [
          {
            type: "pie",
            radius: "70%",
            data: [
              { value: 30, name: "鲈鱼", itemStyle: { color: "#FF6B6B" } },
              { value: 25, name: "鲤鱼", itemStyle: { color: "#4ECDC4" } },
              { value: 20, name: "草鱼", itemStyle: { color: "#45B7D1" } },
              { value: 15, name: "鲫鱼", itemStyle: { color: "#96CEB4" } },
              { value: 10, name: "其他", itemStyle: { color: "#FFEEAD" } },
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };

      speciesChart.setOption(option);
    };

    const initPopulationChart = () => {
      const chartDom = document.querySelector(".line-chart");
      populationChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: "axis",
        },
        grid: {
          top: "10%",
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: ["2018", "2019", "2020", "2021", "2022", "2023"],
          axisLine: {
            lineStyle: {
              color: "#fff",
            },
          },
        },
        yAxis: {
          type: "value",
          axisLine: {
            lineStyle: {
              color: "#fff",
            },
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255, 255, 255, 0.1)",
            },
          },
        },
        series: [
          {
            data: [120, 200, 150, 280, 170, 220],
            type: "line",
            smooth: true,
            lineStyle: {
              color: "#58D9F9",
              width: 4,
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
                    color: "rgba(88,217,249,0.3)",
                  },
                  {
                    offset: 1,
                    color: "rgba(88,217,249,0.1)",
                  },
                ],
              },
            },
            symbol: "circle",
            symbolSize: 8,
          },
        ],
      };

      populationChart.setOption(option);
    };

    return {};
  },
};
</script>

<style scoped>
.underwater-system {
  padding: 20px;
  background-color: #0a1929;
  min-height: calc(100vh - 60px);
  color: white;
}

.counter-section {
  margin-bottom: 20px;
}

.fish-counter {
  background-color: rgba(0, 30, 60, 0.5);
  padding: 15px;
  border-radius: 8px;
}

.digit-group {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.digit {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 10px 15px;
  border-radius: 4px;
  font-size: 24px;
  font-weight: bold;
  color: #58d9f9;
}

.counter-labels {
  display: flex;
  gap: 20px;
  color: #90caf9;
  font-size: 14px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
}

.panel-section {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.section-header {
  margin-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
}

.section-header h2 {
  margin: 0;
  font-size: 16px;
  color: #ff4081;
}

.environment-scores {
  margin-bottom: 20px;
}

.score-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 8px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.score-label {
  color: #90caf9;
}

.score-value {
  color: #58d9f9;
  font-weight: bold;
}

.gauge-chart {
  height: 300px;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.info-card,
.device-card {
  background-color: rgba(0, 30, 60, 0.5);
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.card-header {
  color: #90caf9;
  margin-bottom: 10px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #58d9f9;
}

.unit {
  font-size: 14px;
  margin-left: 2px;
}

.circle-progress {
  background-color: rgba(0, 30, 60, 0.5);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.progress-title {
  color: #90caf9;
  margin-bottom: 15px;
}

.progress-chart {
  height: 300px;
}

.digital-display {
  margin-top: 20px;
}

.display-title {
  color: #90caf9;
  margin-bottom: 10px;
}

.digital-number {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-top: 10px;
}

.digit-box {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 5px 10px;
  border-radius: 4px;
  color: #58d9f9;
  font-weight: bold;
}

.device-info {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.pie-chart,
.line-chart {
  height: 300px;
}
</style>
