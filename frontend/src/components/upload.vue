<template>
<div>
  <el-card v-if="show" class="upload-card" v-loading="loading">
    <el-tabs v-model="uploadType" v-if="!uploadSuccess">
      <el-tab-pane label="从本地上传" name="local">
        <el-form ref="form" :model="form" label-width="60px" style="margin-top: 25px;">
          <el-form-item label="文件名">
            <el-input v-model="form.name" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item style="text-align: right;">
            <el-button @click="onUpload" type="primary" icon="el-icon-upload" :disabled="form.name == ''">上传</el-button>
            <el-button @click="onSelectFile" icon="el-icon-search">选择文件</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="从网址上传" name="remote">
        <el-row style="margin-top: 25px;">
          <el-input placeholder="请输入图片网址" v-model="imageUrl">
            <template slot="prepend">图片网址</template>
          </el-input>
        </el-row>
        <el-row style="text-align: right; margin-top: 20px;margin-bottom: 20px;">
          <el-button @click="onUploadURL" type="primary" icon="el-icon-upload" :disabled="imageUrl == ''">上传</el-button>
        </el-row>
      </el-tab-pane>
    </el-tabs>
    <div v-else>
      <el-alert
        title="上传成功"
        type="success"
        description="即将自动跳转到结果页面"
        show-icon></el-alert>
    </div>
  </el-card>

  <div v-if="hide"> 
    <h4>原图：</h4> 
    <div v-if="show_img0"> 
      <img :src="raw_url" width="35%">
    </div>
    <p></p>
  </div>

  <div v-if="hide"> 
    <h4>人脸识别结果：</h4> 
    <div v-if="show_img1"> 
      <img :src="cook1_url" width="35%">
    </div>
    <p></p>
  </div>

  <div v-if="hide"> 
    <h4>脸部框架结果：</h4> 
    <div v-if="show_img2"> 
      <img :src="cook2_url" width="35%">
    </div> 
    <p></p>
  </div>

</div>
</template>

<script>
export default {
  data() {
    return {
      uploadType: "local",
      imageUrl: "",
      form: {
        name: "",
        file: null
      },
      loading: false,
      uploadSuccess: false,
      show: true,
      hide: false,
      show_img0: false,
      raw_url: '',
      show_img1: false,
      cook1_url: '',
      show_img2: false,
      cook2_url: '',
    }
  },
  methods: {

    onUpload() {
      this.loading = true;
      const that = this;

      let fmdata = new FormData();
      fmdata.append("img", this.form.file);

      this.axios.post("/upload", fmdata).then((res) => {
        res = res.data;

        if (res.error) {
          this.uploadSuccess = false;
          this.$message({
            message: res.error,
            type: 'error'
          });
        }else {
          this.raw_url = res.raw_path
          this.show_img0 = true
          this.show = false;
          this.hide = true;
          let fmdata = new FormData();
          fmdata.append("raw_path", res.raw_path);
          let param = new URLSearchParams(fmdata);
          
          this.axios.post("/cook1", param).then((res) => {
            res = res.data;
            if (res.error) {
              this.uploadSuccess = false;
              this.$message({
                message: res.error,
                type: 'error'
              });
            }else {
              this.cook1_url = res.cook1_path
              this.uploadSuccess = true;
              this.show = false;
              this.hide = true;
              this.show_img1 = true;
            }
          }).catch((err) => {
          console.error(err);
          this.loading = false;
          this.uploadSuccess = false;
          this.$message({
            message: "文件不合法或格式错误",
            type: 'error'
          });
        });

          this.axios.post("/cook2", param).then((res) => {
            res = res.data;
            if (res.error) {
              this.uploadSuccess = false;
              this.$message({
                message: res.error,
                type: 'error'
              });
            }else {
              this.cook2_url = res.cook2_path
              this.uploadSuccess = true;
              this.show = false;
              this.hide = true;
              this.show_img2 = true;
            }
          }).catch((err) => {
          console.error(err);
          this.loading = false;
          this.uploadSuccess = false;
          this.$message({
            message: "文件不合法或格式错误",
            type: 'error'
          });
        });

        }
      }).catch((err) => {
        console.error(err);
        this.loading = false;
        this.uploadSuccess = false;
        this.$message({
          message: "文件不合法或格式错误",
          type: 'error'
        });
      });
    },

    onUploadURL() {
      var fmdata = new FormData();
      this.loading = true;
      fmdata.append("url", this.imageUrl);
      var param = new URLSearchParams(fmdata);
      this.axios.post("/upload_url", param).then((res) => {
        res = res.data;
        if (res.error) {
          this.uploadSuccess = false;
          this.$message({
            message: res.error,
            type: 'error'
          });
        }else {
          this.raw_url = res.raw_path;
          this.show_img0 = true;
          this.show = false;
          this.hide = true;
          let fmdata = new FormData();
          fmdata.append("raw_path", res.raw_path);
          let param = new URLSearchParams(fmdata);
          
          this.axios.post("/cook1", param).then((res) => {
            res = res.data;
            if (res.error) {
              this.uploadSuccess = false;
              this.$message({
                message: res.error,
                type: 'error'
              });
            }else {
              this.cook1_url = res.cook1_path
              this.uploadSuccess = true;
              this.show = false;
              this.hide = true;
              this.show_img1 = true;
            }
          }).catch((err) => {
          console.error(err);
          this.loading = false;
          this.uploadSuccess = false;
          this.$message({
            message: "文件不合法或格式错误",
            type: 'error'
          });
        });

          this.axios.post("/cook2", param).then((res) => {
            res = res.data;
            if (res.error) {
              this.uploadSuccess = false;
              this.$message({
                message: res.error,
                type: 'error'
              });
            }else {
              this.cook2_url = res.cook2_path
              this.uploadSuccess = true;
              this.show = false;
              this.hide = true;
              this.show_img2 = true;
            }
          }).catch((err) => {
          console.error(err);
          this.loading = false;
          this.uploadSuccess = false;
          this.$message({
            message: "文件不合法或格式错误",
            type: 'error'
          });
        });

        }
      }).catch((err) => {
        console.error(err);
        this.loading = false;
        this.uploadSuccess = false;
        this.$message({
          message: "文件不合法或格式错误",
          type: 'error'
        });
      });
    },


    onSelectFile() {
      var inp = document.createElement("input");
      inp.setAttribute("type", "file");
      inp.setAttribute("accept", "image/jpeg");

      const that = this;
      inp.onchange = function() {
        that.form.file = inp.files[0];
        that.form.name = inp.files[0].name;
      }
      inp.click();
    }
  }
}
</script>

<style scoped>
.upload-card {
  width: 650px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 45px;
}

.img-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.img-uploader .el-upload:hover {
  border-color: #409EFF;
}
.img-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.img {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
