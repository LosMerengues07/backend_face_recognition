<template>
<div>
<div style="width: 1200px; margin-left: auto; margin-right: auto;">
  <p>输入时间段以筛选记录，不输入则不筛选此项</p>
  <el-form :inline="true" :model="formFilter" class="demo-form-inline" @submit.native.prevent>

    <el-form-item label="时间段：">
      <el-input style="width: 250px;" v-model="formFilter.date" placeholder="YYYY-MM-DD~YYYY-MM-DD" clearable></el-input>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="onSubmit" icon="el-icon-search">筛选</el-button>
      <el-button  @click="onReset" >重置</el-button>
    </el-form-item>

    <el-form-item style="  position:absolute;right:25%;">
      <el-button  @click="onDeleteAll" >批量删除</el-button>
    </el-form-item>
  </el-form>

  <transition-group name="list" tag="div">
    <div v-for="(item, index) in img_list.slice(currentPage * 5 - 5, currentPage * 5)" :key="item.id">
      <div>
        <el-divider content-position="left">{{ item.timestamp }}</el-divider>
        <el-row class="image-row">
          <el-col :span="8">
            <el-image :src="item.raw_url"
                  fit="cover" class="image-preview"
                  :preview-src-list="[ item.raw_url, item.cook1_url, item.cook2_url ]" >
              <div slot="placeholder" class="image-slot">
                加载中<span class="dot">...</span>
              </div>
            </el-image>
          </el-col>
          <el-col :span="8">
            <el-image :src="item.cook1_url"
                  fit="cover" class="image-preview"
                  :preview-src-list="[ item.raw_url, item.cook1_url, item.cook2_url ]" >
              <div slot="placeholder" class="image-slot">
                加载中<span class="dot">...</span>
              </div>
            </el-image>
          </el-col>
          <el-col :span="8">
            <el-image :src="item.cook2_url"
                  fit="cover" class="image-preview"
                  :preview-src-list="[ item.raw_url, item.cook1_url, item.cook2_url ]" >
              <div slot="placeholder" class="image-slot">
                加载中<span class="dot">...</span>
              </div>
            </el-image>
          </el-col>
        </el-row>
        <el-row style="text-align: right; font-size: 12px;">
          <span class="row-user">用户：{{ item.user }}</span>
          <el-link icon="el-icon-delete" @click="onDelete(item)">删除</el-link>
        </el-row>
      </div>
    </div>
  </transition-group>

  <el-divider></el-divider>
  <div class="block" style="text-align: center;">
    <el-pagination
      layout="prev, pager, next"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :total.sync="img_list.length"
      :page-size="5">
    </el-pagination>
  </div>
</div>
</div>
</template>

<script>
export default {
  data() {
    return {
      currentPage: 1,
      record_list: [],
      img_list: [],
      formFilter: {
        date: "",
      },
    }
  },
  mounted() {
    const loading = this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });

    this.axios.post("/record/user_query").then((res) => {
      res = res.data;
      loading.close();
      var lst = res.list;
      this.record_list = [];
      for (var i = 0; i < lst.length; ++ i) {
        this.record_list.push({
          id: lst[i].img_id,
          timestamp: lst[i].time,
          raw_url: lst[i].raw_url,
          cook1_url: lst[i].cook1_url,
          cook2_url: lst[i].cook2_url,
          user: lst[i].name
        });
      }
      this.img_list = this.record_list;
    }).catch((err) => {
      console.error(err);
      loading.close();
      this.$message({
        message: "错误_query1",
        type: 'error'
      });
    });
  },
  methods: {

    cvt2timestamp(date) {
      date = date.substring(0,19).replace(/-/g,'/'); 
      let timestamp = new Date(date).getTime();
      return timestamp
    },
    valid_date(date){
      var bagin_r = date.match(/^(\d{4})(-)([0][1-9]|[1][0-2])(-)([0][1-9]|[1-2][0-9]|[3][0-1])\~(\d{4})(-)([0][1-9]|[1][0-2])(-)([0][1-9]|[1-2][0-9]|[3][0-1])$/);
      return (bagin_r!=null)
    },

    onSubmit() {
      const that = this;
      this.currentPage = 1;
      if(that.formFilter.date!="" && !this.$options.methods.valid_date(that.formFilter.date)){
          this.formFilter.date = "";
          this.$message({
          message: "输入时间段格式有误",
          type: 'error'
          });
        }
      else{
        this.img_list = this.record_list.filter((item) => { 
        if(that.formFilter.date == ""){
          return true
        }else{
          let user_timestamp = this.$options.methods.cvt2timestamp(item.timestamp)

          let start_date = that.formFilter.date.split('~')[0]
          let start_timestamp = this.$options.methods.cvt2timestamp(start_date)

          let end_date = that.formFilter.date.split('~')[1]
          let end_timestamp = this.$options.methods.cvt2timestamp(end_date)

          return (user_timestamp>=start_timestamp) && (user_timestamp<=end_timestamp); 
          }
        });
      }
    },
    onReset() {
      this.img_list = this.record_list;
      this.currentPage = 1;
      this.formFilter.date = "";
    },

    handleCurrentChange() {
    },

    onDeleteAll(){
        const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });

      console.log(this.img_list)
      let ids = []
      for (let i in this.img_list){
        ids.push(this.img_list[i].id)
      }
      if (ids.length>0){
        let fmdata = new FormData();
        fmdata.append("ids", ids);
        let param = new URLSearchParams(fmdata);
        this.axios.post("/delete_all", param).then((res) => {
          loading.close();
          res = res.data;
          if (res.error) {
            this.$message({
              message: res.error,
              type: 'error'
            });
          }else{
            this.img_list = this.img_list.filter((it) => { return ids.indexOf(it.id)==-1 });
            this.record_list = this.record_list.filter((it) => { return ids.indexOf(it.id)==-1 });
          }
        }).catch((err) => {
          loading.close();
          this.$message({
            message: "删除错误_admin3",
            type: 'error'
          });
        });
      }else{
            loading.close();
            this.$message({
            message: "未选中任何记录",
            type: 'error'
          });
      }
    },

    onDelete(record) {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });

      var fmdata = new FormData();
      fmdata.append("id", record.id);
      var param = new URLSearchParams(fmdata);
      this.axios.post("/record/delete", param).then((res) => {
        res = res.data;
        loading.close();
        if (res.error) {
          this.$message({
            message: res.error,
            type: 'error'
          });
        }
        else {
          this.img_list = this.img_list.filter((it) => { return it.id != record.id; });
          this.record_list = this.record_list.filter((it) => { return it.id != record.id; });
        }
      }).catch((err) => {
        this.$message({
          message: "删除错误_query2",
          type: 'error'
        });
      });
    }
  }
}
</script>

<style scoped>
.image-row {
  text-align: center;
}

.image-preview,
.image-slot {
  width: 150px;
  height: 150px;
  line-height: 150px;
}

.image-slot {
  background: #f5f7fa;
  color: #909399;
  font-size: 14px;
}

.list-enter-active, .list-leave-active {
  transition: opacity .5s;
}
.list-enter, .list-leave-to {
  opacity: 0;
}

.list-leave-active {
    position: absolute;
}
.list-move {
    transition: transform .5s;
}
.row-user {
  float:left;
  margin-left: 50px;
  color: #666;
}
</style>
