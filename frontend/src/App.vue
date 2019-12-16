<template>

<el-container>
  <el-header class="header">
    <el-menu :default-active="$route.path" class="nav" mode="horizontal" @select="handleSelect">
      <el-menu-item index="/admin" v-show="logined && is_admin">管理</el-menu-item>
      <el-menu-item index="/query" v-show="logined">查询</el-menu-item>
      <el-menu-item index="/upload" v-show="logined">上传</el-menu-item>
      <el-submenu index="index_user" v-show="logined">
        <template slot="title">{{ username }}</template>
        <el-menu-item index="/logout">注销</el-menu-item>
      </el-submenu>
      <el-menu-item index="/login" v-show="!logined">登录</el-menu-item>
      <el-menu-item index="/register" v-show="!logined">注册</el-menu-item>
    </el-menu>

  </el-header>
  <el-main>
    <router-view/>
  </el-main>
</el-container>


</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      logined: false,
      username: "",
      is_admin: false,
    }
  },
  mounted() {
    this.logined = window.info.login;
    this.username = window.info.user_name;
    this.is_admin = window.info.is_admin;

    if (this.logined) {
      this.$router.push("/query");
    }
    else {
      this.$router.push("/login");
    }
  },
  methods: {
    handleSelect(it) {
      if (it == "/logout")  {
        this.axios.post("/logout");
        this.is_admin = false;
        this.logined = false;
        this.$router.push("/login");
        //document.location.reload();
      }
      else {
        this.$router.push(it);
      }
    }
  }
}
</script>

<style>
html, body, #app {
  margin: 0;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header {
  border-bottom: solid 1px #e6e6e6;
}


.nav {
  float: right;
  border-bottom: 0;
}

</style>
