import { ElMessage } from "element-plus"


export function downloadEChart(chartInstance, filename = 'chart.png') {
    console.log(ElMessage)
    if (!chartInstance || typeof chartInstance.getDataURL !== 'function') {
      console.warn('图表实例无效或未初始化')
      return
    }

    // 添加延迟确保图表渲染完成
    setTimeout(() => {
        const imgData = chartInstance.getDataURL({
            type: 'png',
            pixelRatio: 3, // 提高分辨率
            backgroundColor: "#0a1929",
            excludeComponents: [] // 确保不排除任何组件
             })


    const a = document.createElement('a')
    a.href = imgData
    a.download = filename
    document.body.appendChild(a)
    a.click()
    ElMessage.success('下载成功')
    document.body.removeChild(a)
    }, 300)
}