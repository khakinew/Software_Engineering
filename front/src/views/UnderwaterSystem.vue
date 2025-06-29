<template>
  <div class="underwater-system">



    <div class="main-content">
      <!-- 左侧面板 -->
      <div class="left-panel">
        <div class="panel-section">
          <div class="section-header">
            <h2>各省站点数量</h2>
          </div>
          <div class="bar-chart" ref="barChart"></div> <!-- 替换为柱状图容器 -->
        </div>
      </div>
        <!-- 中间面板 -->
        <div class="center-panel">      
        <div class="station-selector panel-section">

<!-- 折线图容器 -->
<div v-if="mergedData.length" ref="lineChartRef" class="line-chart"></div>
<div class="action-buttons">
  <el-button 
    type="primary" 
    size="small" 
    icon="el-icon-download"
    @click="exportMonitorData"
    class="export-button"
  >
    导出监测数据
  </el-button>
  
  <el-button 
    type="primary" 
    size="small" 
    icon="el-icon-download"
    @click="exportSites"
    class="export-button"
  >
    导出站点数据
  </el-button>
</div>
<div class="import-section">
  <!-- 隐藏的文件输入 -->
  <input 
    type="file" 
    accept=".csv" 
    @change="handleFileUpload"
    ref="fileInput"
    style="display: none"
  />

  <!-- 可见的操作按钮 -->
  <el-button 
    type="primary" 
    size="small" 
    icon="el-icon-folder-opened"
    @click="triggerFileInput"
    class="file-select-button"
  >
    选择CSV文件
  </el-button>

  <!-- 显示选中的文件名 -->
  <span v-if="selectedFile" class="file-name">
    {{ selectedFile.name }} 
    <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
  </span>

  <!-- 上传按钮带加载状态 -->
  <el-button 
    type="success" 
    size="small" 
    icon="el-icon-upload"
    @click="importData" 
    :disabled="!selectedFile || isUploading"
    :class="{
      'enabled': selectedFile && !isUploading,
      'disabled': !selectedFile || isUploading
    }"
    :loading="isUploading"
    class="upload-button"
  >
    {{ isUploading ? '上传中...' : '上传水质数据' }}
  </el-button>
</div>


     
          <!-- 选择器 -->
          <div class="selector-group">
            <label for="siteSelect" class="selector-label">选择监测点：</label>
            <select id="siteSelect" v-model="selectedSiteId" @change="onSiteChange" class="selector-dropdown">

              <option
                  v-for="site in siteList"
                  :key="site.site_id"
                  :value="site.site_id"
                  :style="{ color: site.status === '正常' ? 'green' : 'red' }"
              >
                {{ site.site_name }}（{{ site.status }}）
              </option>
            </select>
          </div>

          <!-- 数据表格 -->
          <table class="data-table">
            <thead>
            <tr>
              <th>时间</th>
              <th>pH</th>
              <th>溶解氧</th>
              <th>温度</th>
              <th>浊度</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(row, index) in tableData" :key="index">
              <td>{{ row.date }} {{ row.time }}</td>
              <td>{{ row.ph }}</td>
              <td>{{ row.dissolved_oxygen }}</td>
              <td>{{ row.temperature }}</td>
              <td>{{ row.turbidity }}</td>
            </tr>
            </tbody>
          </table>
        </div>

      </div>

      <!-- 右侧面板 -->
    
      
      <div class="right-panel">

    <div class="info-cards">
    <div class="info-card">
      <div class="card-header">鱼种</div>
      <div class="card-value">{{ stats.species_count }}<span class="unit">+</span></div>
    </div>
    <div class="info-card">
      <div class="card-header">鱼苗</div>
      <div class="card-value">{{ stats.total_fish }}<span class="unit">尾</span></div>
    </div>
    <div class="info-card">
      <div class="card-header">平均重量</div>
      <div class="card-value">{{ stats.avg_weight }}<span class="unit">g</span></div>
    </div>
  </div>  

  <div class="panel-section">
    <div class="section-header">
      <h2>鱼群种类统计</h2>
      <!-- 添加导出按钮 -->
      <el-button 
        type="primary" 
        size="small" 
        icon="el-icon-download"
        @click="exportFishData"
        class="export-button"
      >
        导出数据
      </el-button>
    </div>
    <div class="pie-chart" ref="speciesChart"></div>
  </div>
  <div class="panel-section">
    <div class="section-header">
      <h2>鱼群数据对比</h2>
    </div>
    <div class="line-chart" ref="populationChart"></div>
  </div>
</div>
    </div>
  </div>
</template>

<script>
import { nextTick, ref, onMounted } from "vue";
import * as echarts from "echarts";
import { getMergedData,getFishList } from "@/api/auth";
import { exportMonitorData ,exportSites } from '@/api/auth' 
import { authApi } from "@/api/auth";
import { exportFishData } from '@/api/auth' 
import { getFishStats } from '@/api/auth';
import { getFishAnalysis } from "@/api/auth";
import { getProvinceSiteCount } from "@/api/auth"; // 引入新接口


export default {
  data() {
    return {
      // 添加响应式变量
      selectedFile: null,
      isUploading: false,
      stats: {
        species_count: 0,
        total_fish: 0,
        avg_weight: 0
      },
      fishAnalysisData: [],
      timer: null
    };
  },
  mounted() {
    this.fetchFishStats();
    // 每5分钟刷新一次数据
    this.timer = setInterval(this.fetchFishStats, 5 * 60 * 1000);
    this.fetchFishAnalysis(); // 新增：获取鱼类分析数据
},
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    // 导出监测数据
    async exportMonitorData() {
      const result = await exportMonitorData();
      if (result.success) {
        alert("水质数据导出成功");
      } else {
        alert(result.message);
        console.error("水质数据导出失败详情:", result.message);
    
        // 特定错误处理
        if (result.message.includes("401")) {
          alert("请重新登录");
        } else if (result.message.includes("403")) {
          alert("您没有导出权限");
        }
      }
    },

    async exportSites() {
      const result = await exportSites();
      if (result.success) {
        alert("站点数据导出成功");
      } else {
        alert(result.message);
        console.error("站点数据导出失败详情:", result.message);
    
        // 特定错误处理
        if (result.message.includes("401")) {
          alert("请重新登录");
        } else if (result.message.includes("403")) {
          alert("您没有导出权限");
        }
      }
    },

    // 导出鱼类数据
    async exportFishData() {
      const result = await exportFishData();
      if (result.success) {
        alert("鱼类数据导出成功");
      } else {
        alert(result.message);
        console.error("鱼类数据导出失败详情:", result.message);
    
        // 特定错误处理
        if (result.message.includes("401")) {
          alert("请重新登录");
        } else if (result.message.includes("403")) {
          alert("您没有导出权限");
        }
      }
    },
    async fetchFishStats() {
      try {
        const response = await getFishStats();
        if (response.success) {
          this.stats = {
            species_count: response.species_count,
            total_fish: response.total_fish,
            avg_weight: response.avg_weight
          };
        }
      } catch (error) {
        console.error('获取鱼类统计数据失败:', error);
      }
    },

    async fetchFishAnalysis() {
        const result = await getFishAnalysis();
        if (result.success) {
            this.fishAnalysisData = result.data;
            this.initFishAnalysisChart();
        } else {
            console.error('获取鱼类分析数据失败:', result.message);
        }
    },

    initFishAnalysisChart() {
        const chartDom = document.querySelector(".line-chart");
        const populationChart = echarts.init(chartDom);

        const xData = this.fishAnalysisData.map(item => item.species);
        const avgWeight = this.fishAnalysisData.map(item => item.avg_weight);
        const avgHeight = this.fishAnalysisData.map(item => item.avg_height);
        const avgLength = this.fishAnalysisData.map(item => item.avg_length);
        const avgWidth = this.fishAnalysisData.map(item => item.avg_width);

        const option = {
            tooltip: {
                trigger: "axis"
            },
            legend: {
                data: ["平均重量", "平均高度", "平均长度", "平均宽度"],
                textStyle: {
                    color: '#ff4081'
                }
            },
            xAxis: {
                type: "category",
                data: xData,
                axisLine: {
                    lineStyle: {
                        color: "#fff"
                    }
                }
            },
            yAxis: {
                type: "value",
                axisLine: {
                    lineStyle: {
                        color: "#fff"
                    }
                },
                splitLine: {
                    lineStyle: {
                        color: "rgba(255, 255, 255, 0.1)"
                    }
                }
            },
            series: [
                {
                    name: "平均重量",
                    type: "line",
                    data: avgWeight,
                    lineStyle: {
                        color: "#58D9F9"
                    }
                },
                {
                    name: "平均高度",
                    type: "line",
                    data: avgHeight,
                    lineStyle: {
                        color: "#FFA500"
                    }
                },
                {
                    name: "平均长度",
                    type: "line",
                    data: avgLength,
                    lineStyle: {
                        color: "#FF6347"
                    }
                },
                {
                    name: "平均宽度",
                    type: "line",
                    data: avgWidth,
                    lineStyle: {
                        color: "#9370DB"
                    }
                }
            ]
        };

        populationChart.setOption(option);
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    // 触发文件选择对话框
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    // 处理文件选择
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },

    // 新增：执行数据导入
    async importData() {
  if (!this.selectedFile) {
    alert("请先选择CSV文件"); // 替换为 alert
    return;
  }

  this.isUploading = true;
  
  try {
    const result = await authApi.importMonitorData(this.selectedFile);
    
    if (result.success) {
      alert("数据导入成功"); // 替换为 alert
      this.selectedFile = null;
      this.$refs.fileInput.value = "";
    } else {
      alert(result.message || "导入失败"); // 替换为 alert
    }
  } catch (error) {
    console.error("导入失败:", error);
    alert(`导入失败: ${error.message}`); // 替换为 alert
  } finally {
    this.isUploading = false;
  }
}
  },

  name: "UnderwaterSystem",
  setup() {
    let speciesChart = null;
    let populationChart = null;
    let lineChart = null;

    const fishChart = ref(null)

    const lineChartRef = ref(null);
    const tableData = ref([]);

    const mergedData = ref([]);
    const selectedSiteId = ref(null);
    const siteList = ref([]);
    const barChart = ref(null); // 柱状图引用

    const initDataTable = (siteData) => {
      tableData.value = siteData;
    };

    onMounted(() => {
      fetchFishData();
      initSpeciesChart();
      initPopulationChart();
      fetchMergedData();
      fetchProvinceSiteCount(); // 获取数据并初始化图表

      // 响应式调整
      window.addEventListener("resize", () => {
        speciesChart?.resize();
        populationChart?.resize();
        lineChart?.resize();
      });
    });

      
    // 初始化柱状图
    const initBarChart = (data) => {
      if (!barChart.value) return;
      const chart = echarts.init(barChart.value);
      const provinces = data.map(item => item.province);
      const siteCounts = data.map(item => item.site_count);
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        },
        yAxis: {
          type: 'category',
          data: provinces,
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        series: [
          {
            type: 'bar',
            data: siteCounts,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            }
          }
        ]
      };
      
      chart.setOption(option);
      return chart;
    };

const fetchProvinceSiteCount = async () => {
  try {
    const res = await getProvinceSiteCount();
    
    // 检查响应结构
    if (res.data?.success && res.data.data) {
      await nextTick(); // 等待 DOM 渲染完成
      initBarChart(res.data.data);
    }
  } catch (error) {
    console.error('请求失败:', error);
    
    // 检查错误响应
    if (error.response) {
      console.error('错误详情:', error.response.data);
      if (error.response.status === 401) {
        alert("认证失败，请重新登录");
      }
    }
  }
};
    
    const initLineChart = (siteData) => {
      if (!lineChartRef.value) {
        console.warn("⚠️ 图表容器还没挂载！");
        return;
      }

      if (!lineChart) {
        lineChart = echarts.init(lineChartRef.value);
      } else {
        lineChart.clear();
      }

      const xData = siteData.map(d => d.time || d.date);
      const ph = siteData.map(d => d.ph);
      const oxygen = siteData.map(d => d.dissolved_oxygen);
      const temperature = siteData.map(d => d.temperature);

      const option = {
        title: {
          text: "水质变化折线图",
          textStyle: {
            color: '#ff4081'
          },
        },
        tooltip: { trigger: "axis" },
        legend: { data: ["pH", "溶解氧", "温度"] ,
          textStyle: {
            color: '#ff4081'
          },
        },
        xAxis: { type: "category", data: xData },
        yAxis: { type: "value" },
        series: [
          { name: "pH", type: "line", data: ph },
          { name: "溶解氧", type: "line", data: oxygen },
          { name: "温度", type: "line", data: temperature },
        ],
      };

      lineChart.setOption(option);
    };

    const fetchMergedData = async () => {
      const res = await getMergedData()
      console.log("🐟 来自后端的位置数据：", res)

      if (!Array.isArray(res)) {
        console.error("🐟 位置数据格式错误，期待的是数组格式！");
        return;
      }

      mergedData.value = res || [];

      siteList.value = [
        ...new Map(mergedData.value.map(item => [item.site_id, item])).values()
      ];

      selectedSiteId.value = siteList.value[0]?.site_id;

      await nextTick();
      updateChartsAndTables();
    };

    const updateChartsAndTables = () => {
      const siteData = mergedData.value.filter(item => item.site_id === selectedSiteId.value);
      tableData.value = siteData;

      initLineChart(siteData);
    };



    const fetchFishData = async () =>{
      const res = await getFishList()
      console.log("🐟 来自后端的鱼类数据：", res)

      if (!Array.isArray(res)) {
        console.error("🐟 鱼类数据格式错误，期待的是数组格式！");
        return;
      }


      const speciesCount = {}
      res.forEach(fish =>{
        speciesCount[fish.species] = (speciesCount[fish.species]||0)+1
      });

      const chartData = Object.entries(speciesCount).map(([species,count]) =>({
        name:species,
        value:count
      }));
      await nextTick();
      initSpeciesChart(chartData);
    };

    const onSiteChange = () => {
      updateChartsAndTables();
    };

    const initSpeciesChart = (chartData) => {
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
            data: chartData,
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

    return {
      lineChartRef,
      mergedData,
      tableData,
      siteList,
      selectedSiteId,
      onSiteChange,
      barChart,
    };
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
.station-selector {
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.selector-group {
  margin: 15px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.selector-label {
  color: #90caf9;
  font-size: 14px;
}

.selector-dropdown {
  background-color: #0a1929;
  color: #58d9f9;
  border: 1px solid #58d9f9;
  border-radius: 4px;
  padding: 5px 10px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background-color: rgba(0, 0, 0, 0.1);
  color: #ffffff;
}

.data-table th,
.data-table td {
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 10px;
  text-align: center;
  font-size: 14px;
}

.data-table th {
  background-color: rgba(255, 255, 255, 0.05);
  color: #90caf9;
}

.data-table tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.02);
}

.data-table tr:hover {
  background-color: rgba(88, 217, 249, 0.1);
}


.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.export-button {
  background-color: #409EFF;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
}

.export-button:hover {
  background-color: #66b1ff;
}

.export-button i {
  margin-right: 5px;
}

/* 按钮容器 */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.import-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}

/* 按钮通用样式 */
.export-button,
.file-select-button,
.upload-button {
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 13px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

/* 导出按钮样式 */
.export-button {
  background-color: #409EFF;
  color: white;
  border: none;
}

.export-button:hover {
  background-color: #66b1ff;
}

/* 文件选择按钮样式 */
.file-select-button {
  background-color: #67C23A;
  color: white;
  border: none;
}

.file-select-button:hover {
  background-color: #85ce61;
}

/* 上传按钮 - 启用状态 */
.upload-button.enabled {
  background-color: #67C23A; /* 绿色 */
  color: white;
  border: none;
  cursor: pointer;
  opacity: 1;
}

/* 上传按钮 - 禁用状态 */
.upload-button.disabled {
  background-color: #f0f9eb;
  color: #c2c7cc;
  border: 1px solid #ebeef5;
  cursor: not-allowed;
  opacity: 0.7;
}

/* 悬停效果 */
.upload-button.enabled:hover {
  background-color: #85ce61;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(103, 194, 58, 0.3);
}

/* 加载动画 */
.el-button.is-loading:before {
  background-color: rgba(103, 194, 58, 0.3);
}


/* 文件名样式 */
.file-name {
  margin: 0 10px;
  font-size: 13px;
  color: #606266;
}

.file-size {
  color: #909399;
  font-size: 12px;
}

.digital-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #00aaff;
  text-align: center;
  margin: 15px 0;
}

.unit {
  font-size: 1rem;
  font-weight: normal;
  margin-left: 5px;
  color: #666;
}

.bar-chart {
  height: 800px;
  width: 100%;
}

/* 移除不再需要的样式 */
.environment-scores {
  display: none;
}

/* 调整面板高度 */
.left-panel .panel-section {
  height: 500px; /* 根据实际需要调整 */
}

</style>