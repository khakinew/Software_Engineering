<template>
  <div class="admin">
    <div class="admin-header">
      <h2>系统管理控制台</h2>
      <div class="admin-info">
        <span class="admin-name">管理员：{{ adminName }}</span>
        <span class="admin-time">{{ currentTime }}</span>
      </div>
    </div>

    <div class="admin-content">
      <!-- 左侧导航 -->
      <div class="admin-nav">
        <div
          v-for="(item, index) in menuItems"
          :key="index"
          class="nav-item"
          :class="{ active: currentMenu === item.key }"
          @click="switchMenu(item.key)"
        >
          <i :class="item.icon"></i>
          <span>{{ item.label }}</span>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="admin-main">
        <!-- 用户管理 -->
        <div v-if="currentMenu === 'users'" class="content-section">
          <div class="section-header">
            <h3>用户管理</h3>
            <button class="add-btn" @click="showAddUserModal = true">
              <i class="fas fa-plus"></i> 添加用户
            </button>
          </div>
          <div class="user-table">
            <table>
              <thead>
                <tr>
                  <th>用户ID</th>
                  <th>用户名</th>
                  <th>角色</th>
                  <th>状态</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.role }}</td>
                  <td>
                    <span :class="['status-badge', user.status]">
                      {{ user.status=='active' ? "正常" : "禁用" }}
                    </span>
                  </td>
                  <td>{{ user.createTime }}</td>
                  <td>
                    <button class="action-btn edit" @click="editUser(user)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" @click="deleteUser(user)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 系统设置 -->
        <div v-if="currentMenu === 'settings'" class="content-section">
          <div class="section-header">
            <h3>系统设置</h3>
          </div>
          <div class="settings-form">
            <div class="form-group">
              <label>系统名称</label>
              <input type="text" v-model="settings.systemName" />
            </div>
            <div class="form-group">
              <label>数据备份周期</label>
              <select v-model="settings.backupCycle">
                <option value="daily">每天</option>
                <option value="weekly">每周</option>
                <option value="monthly">每月</option>
              </select>
            </div>
            <div class="form-group">
              <label>日志保留时间</label>
              <select v-model="settings.logRetention">
                <option value="30">30天</option>
                <option value="60">60天</option>
                <option value="90">90天</option>
              </select>
            </div>
            <div class="form-group">
              <label>系统维护时间</label>
              <input type="time" v-model="settings.maintenanceTime" />
            </div>
            <div class="form-actions">
              <button class="save-btn" @click="saveSettings">保存设置</button>
            </div>
          </div>
        </div>

        <!-- 日志查看 -->
        <div v-if="currentMenu === 'logs'" class="content-section">
          <div class="section-header">
            <h3>系统日志</h3>
            <div class="log-actions">
              <button class="action-btn export" @click="exportLogs">
                <i class="fas fa-download"></i> 导出日志
              </button>
              <button class="action-btn clear" @click="clearLogs">
                <i class="fas fa-trash"></i> 清除日志
              </button>
            </div>
            <div class="log-filters">
              <select v-model="logFilter.type">
                <option value="all">所有类型</option>
                <option value="error">错误</option>
                <option value="warning">警告</option>
                <option value="info">信息</option>
              </select>
              <input type="date" v-model="logFilter.date" class="date-picker" />
            </div>
          </div>
          <div class="log-list">
            <div v-if="filteredLogs.length === 0" class="no-logs">
              暂无日志记录
            </div>
            <div
              v-else
              v-for="log in filteredLogs"
              :key="log.id"
              class="log-item"
              :class="log.type"
            >
              <div class="log-time">{{ log.time }}</div>
              <div class="log-content">{{ log.content }}</div>
              <div class="log-type">{{ log.type }}</div>
            </div>
          </div>
        </div>

        <!-- 系统监控 -->
        <div v-if="currentMenu === 'monitor'" class="content-section">
          <div class="section-header">
            <h3>系统监控</h3>
          </div>
          <div class="system-status">
            <div class="status-item">
              <span class="label">CPU使用率</span>
              <span class="value">{{ systemStatus.cpu.usage }}%</span>
              <span class="warning" v-if="systemStatus.cpu.warning">警告</span>
            </div>
            <div class="status-item">
              <span class="label">内存使用率</span>
              <span class="value">{{ systemStatus.memory.usage }}%</span>
              <span class="warning" v-if="systemStatus.memory.warning"
                >警告</span
              >
            </div>
            <div class="status-item">
              <span class="label">磁盘使用率</span>
              <span class="value">{{ systemStatus.disk.usage }}%</span>
              <span class="warning" v-if="systemStatus.disk.warning">警告</span>
            </div>
            <div class="status-item">
              <span class="label">网络状态</span>
              <span class="value">{{ systemStatus.network.status }}</span>
            </div>
            <div class="status-item">
              <span class="label">网络带宽</span>
              <span class="value">{{ systemStatus.network.bandwidth }}</span>
            </div>
          </div>
        </div>

        <!-- 数据备份 -->
        <div v-if="currentMenu === 'backup'" class="content-section">
          <div class="section-header">
            <h3>数据备份</h3>
          </div>
          <div class="backup-config">
            <div class="form-group">
              <label>自动备份</label>
              <input type="checkbox" v-model="backupConfig.autoBackup" />
            </div>
            <div class="form-group">
              <label>备份时间</label>
              <input type="time" v-model="backupConfig.backupTime" />
            </div>
            <div class="form-group">
              <label>备份路径</label>
              <input type="text" v-model="backupConfig.backupPath" />
            </div>
            <div class="form-group">
              <label>备份保留时间</label>
              <input type="number" v-model="backupConfig.retention" />
            </div>
            <div class="form-group">
              <label>上次备份时间</label>
              <span>{{ backupConfig.lastBackup }}</span>
            </div>
            <div class="form-actions">
              <button class="backup-btn" @click="performBackup">
                执行备份
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加用户弹窗 -->
    <div v-if="showAddUserModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>添加用户</h3>
          <button class="close-btn" @click="showAddUserModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="newUser.username" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="newUser.password" />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="newUser.role">
              <option value="user">普通用户</option>
              <option value="admin">管理员</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddUserModal = false">
            取消
          </button>
          <button class="confirm-btn" @click="addUser">确认</button>
        </div>
      </div>
    </div>

    <!-- 编辑 -->
    <div v-if="showUpdateUserModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>编辑用户</h3>
          <button class="close-btn" @click="showUpdateUserModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="updateUser.username" />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="updateUser.password" />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="updateUser.role">
              <option value="user">普通用户</option>
              <option value="admin">管理员</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showUpdateUserModal = false">
            取消
          </button>
          <button class="confirm-btn" @click="updateUserHa">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get_users,deleteUserApi,addUserApi ,updateUserApi } from "@/api/auth";
import { ref, onMounted, computed, onUnmounted,reactive } from "vue";

export default {
  name: "Admin",
  setup() {
    const adminName = ref("超级管理员");
    const currentTime = ref("");
    const currentMenu = ref("users");
    const showAddUserModal = ref(false);
    const showUpdateUserModal=ref(false)
    const editUser=(user)=>{
      updateUser.role=user.role
      updateUser.username=user.username
      showUpdateUserModal.value=true
    }
    const updateUser=reactive({
      username:"",
      password:"",
      role:''
    })

    // 系统设置数据
    const settings = ref({
      systemName: "岸基数据中心海洋牧场大数据可视化系统",
      backupCycle: "daily",
      logRetention: "30",
      maintenanceTime: "03:00",
    });
    const updateUserHa=async ()=>{
    
      
      const data=await updateUserApi(updateUser)
      if (data.data.code!=200){
        alert(data.data.message)
        showUpdateUserModal.value=false
        return 0
      }
      alert("修改成功")
      showUpdateUserModal.value=false
      users.value= (await get_users()).data.data
    }
 
    // 日志数据 - 移到最前面定义
    const logs = ref([
      {
        id: 1,
        time: "2024-02-01 10:00:00",
        content: "系统启动成功",
        type: "info",
      },
      {
        id: 2,
        time: "2024-02-01 10:05:00",
        content: "用户admin登录系统",
        type: "info",
      },
      {
        id: 3,
        time: "2024-02-01 10:30:00",
        content: "检测到异常登录尝试",
        type: "warning",
      },
      {
        id: 4,
        time: "2024-02-01 11:00:00",
        content: "数据库连接失败",
        type: "error",
      },
      {
        id: 5,
        time: "2024-02-01 11:05:00",
        content: "数据库恢复连接",
        type: "info",
      },
    ]);

    // 日志筛选
    const logFilter = ref({
      type: "all",
      date: "",
    });

    // 修改计算属性的定义
    const filteredLogs = computed(() => {
      if (!logs.value) return [];

      return logs.value.filter((log) => {
        if (
          logFilter.value.type !== "all" &&
          log.type !== logFilter.value.type
        ) {
          return false;
        }
        if (
          logFilter.value.date &&
          !log.time.startsWith(logFilter.value.date)
        ) {
          return false;
        }
        return true;
      });
    });

    const menuItems = [
      { key: "users", label: "用户管理", icon: "fas fa-users" },
      { key: "settings", label: "系统设置", icon: "fas fa-cog" },
      { key: "logs", label: "系统日志", icon: "fas fa-clipboard-list" },
      { key: "monitor", label: "系统监控", icon: "fas fa-desktop" },
      { key: "backup", label: "数据备份", icon: "fas fa-database" },
    ];

    // 添加日志的方法
    const addLog = (content, type = "info") => {
      const newLog = {
        id: logs.value.length + 1,
        time: new Date().toLocaleString(),
        content,
        type,
      };
      logs.value.push(newLog);
    };

    // 清除日志的方法
    const clearLogs = () => {
      if (confirm("确定要清除所有日志吗？")) {
        logs.value = [];
      }
    };

    // 导出日志的方法
    const exportLogs = () => {
      const logText = logs.value
        .map((log) => `${log.time} [${log.type}] ${log.content}`)
        .join("\n");

      const blob = new Blob([logText], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `系统日志_${new Date().toLocaleDateString()}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    };

    // 系统监控数据
    const systemStatus = ref({
      cpu: { usage: 45, warning: false },
      memory: { usage: 60, warning: false },
      disk: { usage: 75, warning: true },
      network: { status: "normal", bandwidth: "100MB/s" },
    });

    // 数据备份配置
    const backupConfig = ref({
      autoBackup: true,
      backupTime: "03:00",
      backupPath: "/backup",
      retention: 7,
      lastBackup: "2024-02-01 03:00:00",
    });

    // 更新系统状态
    const updateSystemStatus = () => {
      const interval = setInterval(() => {
        systemStatus.value.cpu.usage = Math.floor(Math.random() * 100);
        systemStatus.value.memory.usage = Math.floor(Math.random() * 100);
        systemStatus.value.cpu.warning = systemStatus.value.cpu.usage > 80;
        systemStatus.value.memory.warning =
          systemStatus.value.memory.usage > 80;
      }, 5000);

      onUnmounted(() => {
        clearInterval(interval);
      });
    };

    // 执行数据备份
    const performBackup = async () => {
      try {
        // 模拟备份过程
        await new Promise((resolve) => setTimeout(resolve, 2000));
        backupConfig.value.lastBackup = new Date().toLocaleString();
        return true;
      } catch (error) {
        console.error("备份失败:", error);
        return false;
      }
    };

    // 用户管理功能增强
    const users = ref([]);
    get_users().then((res) => {
      users.value = res.data.data;
    });
    // 权限管理
    const roles = ref([
      {
        name: "管理员",
        permissions: ["all"],
        description: "系统最高权限",
      },
      {
        name: "运维人员",
        permissions: ["monitor", "logs"],
        description: "系统运维权限",
      },
      {
        name: "普通用户",
        permissions: ["view"],
        description: "基础查看权限",
      },
    ]);

    // 新用户数据
    const newUser = ref({
      username: "",
      password: "",
      role: "user",
    });

    // 更新时间显示
    const updateTime = () => {
      const updateTimeString = () => {
        const now = new Date();
        currentTime.value = now.toLocaleString();
      };

      updateTimeString();
      const interval = setInterval(updateTimeString, 1000);

      onUnmounted(() => {
        clearInterval(interval);
      });
    };

    // 添加用户
    const addUser = async () => {

      if (!newUser.value.username || !newUser.value.password) {
        alert("用户名和密码不能为空");
        return;
      }

      const user = {
        id: users.value.length + 1,
        username: newUser.value.username,
        role: newUser.value.role,
        status: "active",
        createTime: new Date().toISOString().replace('T', ' ').slice(0, 19),
        lastLogin: "-",
        permissions: roles.value.find((r) => r.name === newUser.value.role)
          ?.permissions || ["view"],
      };
      const user_copy=JSON.parse(JSON.stringify(user));
      user_copy['password']=newUser.value.password;
      user_copy['role']='user'
      if (user_copy['role']!='普通用户'){
        user_copy['role']="admin";
      }
      const resData=await addUserApi(user_copy);
      console.log(resData.data);
      
      if (resData.data.code==200){

        users.value.push(user);
      showAddUserModal.value = false;
      newUser.value = { username: "", password: "", role: "普通用户" };
      alert("添加成功");
      return ;
      }
      alert("添加失败:",resData.data.message);
    };

    // 删除用户
    const deleteUser = async (user) => {
      if (user.username === "admin") {
        alert("不能删除超级管理员账号");
        return;
      }

      if (confirm(`确定要删除用户 ${user.username} 吗？`)) {
        const resData=await deleteUserApi(user.id);
        console.log(resData);
        
        if(resData.data.code==200){
          users.value = users.value.filter((u) => u.id !== user.id);
          alert("删除成功");
          return ;
        }
        alert("删除失败");
      }
    };
  
    // 系统设置
    const saveSettings = () => {
      // 实现保存设置功能
      alert("设置已保存");
    };

    onMounted(() => {
      updateTime();
      updateSystemStatus();
    });

    return {
      adminName,
      currentTime,
      currentMenu,
      menuItems,
      users,
      roles,
      systemStatus,
      backupConfig,
      showAddUserModal,
      showUpdateUserModal,
      updateUser,
      newUser,
      logFilter,
      filteredLogs,
      logs,
      settings,
      updateUserHa,
      switchMenu: (menu) => (currentMenu.value = menu),
      addUser,
      deleteUser,
      saveSettings,
      performBackup,
      addLog,
      clearLogs,
      exportLogs,
      editUser,
      
    };
  },
};
</script>

<style scoped>
.admin {
  min-height: 100vh;
  background-color: #0a1929;
  color: white;
}

.admin-header {
  padding: 20px;
  background-color: rgba(0, 30, 60, 0.5);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-info {
  display: flex;
  gap: 20px;
  color: #90caf9;
}

.admin-content {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.admin-nav {
  width: 200px;
  background-color: rgba(0, 30, 60, 0.5);
  border-radius: 8px;
  padding: 20px 0;
}

.nav-item {
  padding: 15px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

.nav-item.active {
  background-color: #004bcc;
}

.nav-item i {
  width: 20px;
  text-align: center;
}

.admin-main {
  flex: 1;
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

.add-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
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

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-badge.active {
  background-color: #4caf50;
}

.status-badge.inactive {
  background-color: #f44336;
}

.action-btn {
  padding: 6px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.action-btn.edit {
  background-color: #2196f3;
  color: white;
}

.action-btn.delete {
  background-color: #f44336;
  color: white;
}

.settings-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #90caf9;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background-color: rgba(0, 0, 0, 0.2);
  color: white;
  border-radius: 4px;
}

.save-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.log-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.log-filters {
  display: flex;
  gap: 10px;
}

.log-list {
  margin-top: 20px;
}

.log-item {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  display: flex;
  gap: 20px;
}

.log-item.info {
  background-color: rgba(33, 150, 243, 0.1);
}

.log-item.warning {
  background-color: rgba(255, 152, 0, 0.1);
}

.log-item.error {
  background-color: rgba(244, 67, 54, 0.1);
}

.log-time {
  color: #90caf9;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #0a1929;
  border-radius: 8px;
  width: 400px;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 20px;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-btn {
  background-color: #666;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.system-status {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.status-item {
  width: calc(50% - 10px);
}

.label {
  display: block;
  margin-bottom: 8px;
}
</style>
