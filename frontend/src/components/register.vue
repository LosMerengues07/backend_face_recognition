<template>
<div>
  <el-card class="login-card">
    <div slot="header" class="clearfix">
      <span>注册</span>
    </div>
    <el-form label-position="right" label-width="60px" :model="loginForm">
      <el-form-item label="用户名">
        <el-input placeholder="请输入用户名" v-model="loginForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input placeholder="请输入密码" v-model="loginForm.password" show-password></el-input>
      </el-form-item>
      <el-form-item style="text-align: right;">
        <el-button  type="primary" :loading="loading" @click="onSubmit">注册</el-button>
        <el-button @click="onReset">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</div>
</template>

<script>
export default {
  data () {
    return {
      loginForm: {
        username: "",
        password: ""
      },
      loading: false
    }
  },
  mounted() {
  },
  methods: {
    onSubmit() {
      this.loading = true;
      var fmdata = new FormData();
      fmdata.append("username", this.loginForm.username);
      fmdata.append("password", this.loginForm.password);
      var param = new URLSearchParams(fmdata);
      this.axios.post("/logon", param).then((res) => {
        res = res.data;
        this.loading = false;
        if (res.error) {
          this.$message({
            message: res.error,
            type: 'error'
          });
        }
        else {
          this.$router.push("/login");
          // 跳转到登录页面
        }
      }).catch((err) => {
        this.loading = false;
        this.$message({
          message: "服务器内部错误_register",
          type: 'error'
        });
      });

    },
    onReset() {
      this.loginForm = {
        username: "",
        password: ""
      };
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login-card {
  width: 450px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 50px;
}
</style>
