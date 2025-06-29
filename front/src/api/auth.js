import axios from "../utils/axios";

export const authApi = {
  async login(username, password) {
    try {
      const response = await axios.post("/login", {
        username,
        password,
      });
      console.log(response);
      const data = response.data;
      console.log(data);
      
      if (data.code = 200) {
        window.localStorage.setItem("token", data.token);
      }
      return data;
    } catch (error) {
      return {
        data: null,
        success: false,
        message: error.response.data.message,
        code: 400,
      };
    }
  },

  async register(username, password, repassword, role = "user") {
    try {
      const response = await axios.post("/register", {
        username,
        password,
        repassword,
        role,
      });
      return response.data;
    } catch (error) {
      if (error.response?.data) {
        throw new Error(error.response.data.message || "注册失败");
      }
      throw new Error("网络错误，请稍后重试");
    }
  },

  async logout() {
    try {
      const response = await axios.post("/logout");
      return response.data;
    } catch (error) {
      if (error.response?.data) {
        throw new Error(error.response.data.message || "退出登录失败");
      }
      throw new Error("网络错误，请稍后重试");
    }
  },

  async importMonitorData(file) {
    try {
      const formData = new FormData();
      formData.append('file', file); // 'file' 对应后端接收的文件字段名

      const response = await axios.post('/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data' // 必须设置表单类型
        },
        withCredentials: true
      });

      return response.data;
    } catch (error) {
      if (error.response) {
        // 提取后端返回的错误消息
        const errorMsg = error.response.data?.message || "导入失败";
        throw new Error(errorMsg);
      } else if (error.request) {
        throw new Error("请求未发送到服务器");
      } else {
        throw new Error("请求配置错误: " + error.message);
      }
    }
  },
};


export const auth = async () => {
  try {
    return await axios.get("/auth");
  } catch (e) {
    return { code: 401 };
  }
};

//用户管理模块
const user = "/api/admin/user";
export const get_users = async () => {
  try {
    return axios.get(user + "/get_user_list");
  } catch (e) {
    return { code: 200, data: [] };
  }
};

export const deleteUserApi = (id) => {
  try {
    return axios.delete(user + "/delete?id=" + id);
  } catch (e) {
    return { code: 200, data: [] };
  }
};

export const addUserApi = (data) => {
  try {
    return axios.post(user + "/add", data);
  } catch (e) {
    return { code: 400, message: "network error" };
  }
};


export const updateUserApi = (data) => {
  try {
    return axios.put(user + "/edit", data);
  } catch (e) {
    return { code: 400, message: "network error" };
  }
};

// 鱼类信息模块
export const getFishList = async () => {
  try {
    const response = await axios.get('/fish',{withCredentials:true});

    return response.data; // 假设后端返回的是数组格式的鱼类数据
  } catch (e) {
    console.error('获取鱼类信息失败:', e);
    return;
  }
};

// 水质信息
export const getMergedData = async () =>{
  try {
    const response = await axios.get('/merged_data', { withCredentials: true });
    return response.data;  // 假设后端返回的是已经合并的数据
  } catch (e) {
    console.error('获取合并数据失败:', e);
    return [];
  }
}

export const exportMonitorData = async () => {
  try {
    const response = await axios.get('/monitor_data', {
      responseType: 'blob',
      withCredentials: true
    });
    
    if (response.status >= 200 && response.status < 300) {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'monitor_data.csv');
      document.body.appendChild(link);
      link.click();
      return { success: true, message: "下载成功" };
    } else {
      return { 
        success: false, 
        message: `导出失败: 服务器返回状态 ${response.status}` 
      };
    }
  } catch (error) {
    console.error('水质数据导出失败:', error);
    
    let errorMessage = "水质数据导出失败";
    
    if (error.response) {
      errorMessage = error.response.data?.message || 
                    `服务器错误: ${error.response.status}`;
    } else if (error.request) {
      errorMessage = "网络错误: 服务器无响应";
    } else {
      errorMessage = `请求错误: ${error.message}`;
    }
    
    return { success: false, message: errorMessage };
  }
};


export const exportSites = async () => {
  try {
    const response = await axios.get('/sites', {
      responseType: 'blob',
      withCredentials: true
    });
    
    if (response.status >= 200 && response.status < 300) {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'sites.csv');
      document.body.appendChild(link);
      link.click();
      return { success: true, message: "下载成功" };
    } else {
      return { 
        success: false, 
        message: `导出失败: 服务器返回状态 ${response.status}` 
      };
    }
  } catch (error) {
    console.error('水质数据导出失败:', error);
    
    let errorMessage = "水质数据导出失败";
    
    if (error.response) {
      errorMessage = error.response.data?.message || 
                    `服务器错误: ${error.response.status}`;
    } else if (error.request) {
      errorMessage = "网络错误: 服务器无响应";
    } else {
      errorMessage = `请求错误: ${error.message}`;
    }
    
    return { success: false, message: errorMessage };
  }
};


// 在API文件中添加鱼类数据导出接口
export const exportFishData = async () => {
  try {
    const response = await axios.get('/fish_export', {
      responseType: 'blob',
      withCredentials: true
    });
    
    if (response.status >= 200 && response.status < 300) {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'fish_data.csv');
      document.body.appendChild(link);
      link.click();
      return { success: true, message: "下载成功" };
    } else {
      return { 
        success: false, 
        message: `导出失败: 服务器返回状态 ${response.status}` 
      };
    }
  } catch (error) {
    console.error('鱼类数据导出失败:', error);
    
    let errorMessage = "鱼类数据导出失败";
    
    if (error.response) {
      errorMessage = error.response.data?.message || 
                    `服务器错误: ${error.response.status}`;
    } else if (error.request) {
      errorMessage = "网络错误: 服务器无响应";
    } else {
      errorMessage = `请求错误: ${error.message}`;
    }
    
    return { success: false, message: errorMessage };
  }
};

export const getFishStats = async () => {
  try {
    const response = await axios.get('/fish_stats', { withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('获取鱼类统计数据失败:', error);
    return {
      success: false,
      message: error.response?.data?.message || "网络错误，请稍后重试",
      species_count: 0,
      total_fish: 0,
      avg_weight: 0
    };
  }
};

export const getFishMetrics = async () => {
  try {
    const response = await axios.get('/fish_metrics', { withCredentials: true });
    return response.data;
  } catch (error) {
    console.error('获取鱼类指标失败:', error);
    return {
      success: false,
      message: error.response?.data?.message || "网络错误，请稍后重试",
      species_count: 0,
      total_fish: 0,
      avg_weight: 0,
      avg_length: 0,
      today_added: 0
    };
  }
};

export const getFishAnalysis = async () => {
  try {
      const response = await axios.get('/fish_analysis', { withCredentials: true });
      return response.data;
  } catch (error) {
      console.error('获取鱼类分析数据失败:', error);
      return {
          success: false,
          message: error.response?.data?.message || "网络错误，请稍后重试",
          data: []
      };
  }
};

export const getProvinceSiteCount = () => {
  return axios.get('/province_site_count', { withCredentials: true });
};