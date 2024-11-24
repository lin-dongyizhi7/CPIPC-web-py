<template>
  <page>
    <template #input>
      <el-form :model="formModel" :rules="formRules" ref="formRef">
        <div class="file-receive">
          <div class="info-tip">下面两种方式二选一即可</div>
          <el-form-item label="输入待处理文件夹路径" label-position="top" prop="filePath">
            <el-input
              v-model="formModel.filePath"
              placeholder="C:\Users\Desktop\my-files"
            ></el-input>
          </el-form-item>
          <el-form-item label="" label-position="top">
            <el-upload
              ref="upload"
              class="upload-file"
              drag
              :limit="1"
              :http-request="uploadRequest"
              :before-upload="handleBeforeUpload"
              :on-change="handleOnChange"
              :on-remove="handleOnRemove"
              :on-exceed="handleExceed"
            >
              <el-icon class="el-icon--upload">
                <upload-filled />
              </el-icon>
              <div class="el-upload__text">拖拽文件到此处 或者 <em>点击此处</em></div>
              <div class="el-upload__tip">小于10MB的csv/xlsx/xls文件</div>
            </el-upload>
          </el-form-item>
          <el-form-item label="选择模型" label-position="left" prop="filePath">
            <el-select @focus="getModels" placeholder="" v-model="formModel.model">
              <el-option v-for="item in models" :label="item" :value="item"> </el-option>
              <template #label="{ label, value }">
                <span style="font-size: 12px">{{ transPath(label) }}</span>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="预测长度">
            <el-input-number
              v-model="formModel.pred_len"
              :step="1"
              :min="1"
              :max="1000"
              show-input
              size="small"
            />
          </el-form-item>
          <el-form-item label="画图风格">
            <el-select v-model="formModel.drawStyle">
              <el-option v-for="item in styles" :label="item.label" :value="item.value">
                <div style="display: flex; align-items: center">
                  <color-style :colors="item.colors"></color-style>
                  {{ item.label }}
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </div>
      </el-form>
    </template>
    <template #process>
      <opt-btn-progress
        opt-name="预测"
        :disbled="!formModel.file && !formModel.filePath"
        :reset="reset"
        @start="startPredictModel"
        @success="success = true"
      >
      </opt-btn-progress>
    </template>
    <template #output>
      <div v-if="!reset">
        <div v-if="starting">预测中...</div>
      </div>
      <div v-if="!starting && success && finished">
        <div>预测完成，保存到opt目录下</div>
      </div>
    </template>
  </page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { UploadFilled } from "@element-plus/icons-vue";
import type {
  UploadProps,
  UploadFile,
  UploadRawFile,
  UploadInstance,
} from "element-plus";
import { ElMessage, genFileId } from "element-plus";
import Papa from "papaparse";

import Page from "../page.vue";
import OptBtnProgress from "../../components/opt-btn-progress.vue";
import ColorStyle from "../../components/color-style.vue";

import { styles } from "../../enum/options";

import { startPredict, getModelsList } from "../../api/api.ts";

const formModel = reactive({
  filePath: "",
  file: null,
  model: "",
  pred_len: 1,
  drawStyle: "common",
});
const formRef = ref();

const formRules = {
  //   filePath: [{ required: true, message: "未上传文件" }],
  model: [{ required: true, message: "未上传文件" }],
};

const models = ref([]);

onMounted(async () => {
  await getModels();
});

const getModels = async () => {
  let res = await getModelsList();
  models.value = res.data;
};

function transPath(path) {
  // 获取最后两个部分
  return path.split("\\").slice(-2).join("\\");
}

const handleBeforeUpload: UploadProps["beforeUpload"] = (rawFile) => {
  if (
    rawFile.type.endsWith("csv") &&
    rawFile.type.endsWith("xlsx") &&
    rawFile.type.endsWith("xls")
  ) {
    ElMessage.error("文件必须是csv/xlsx/xls格式!");
    return false;
  } else if (rawFile.size / 1024 / 1024 > 10) {
    ElMessage.error("文件大小超出限制!");
    return false;
  }
  return true;
};

let fileData: any;
let file: any;

const upload = ref<UploadInstance>();
const handleExceed: UploadProps["onExceed"] = (files) => {
  upload.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  upload.value!.handleStart(file);
};

const handleOnChange = (uploadFile: UploadFile) => {
  file = uploadFile;
  reset.value = false;
  Papa.parse(uploadFile.raw, {
    header: true,
    dynamicTyping: true,
    complete: function (results: any) {
      console.log("解析结果:", results.data);
      // 在这里处理解析后的内容
      fileData = results.data;
    },
  });
};

const reset = ref(false);
const handleOnRemove = (uploadFile: UploadFile, uploadFiles: UploadFile[]) => {
  if (uploadFiles.length === 0) {
    reset.value = true;
  }
};

const uploadRequest = () => {};

const startPredictModel = () => {
  starting.value = true;
  const config = {
    model: formModel.model,
    pred_len: formModel.pred_len,
    drawStyle: formModel.drawStyle,
  };
  if (formModel.filePath) {
    let paths = formModel.filePath.split("/");
    let name = paths[paths.length - 1].split(".")[0];
    startPredict({
      name: name,
      type: "path",
      filePath: formModel.filePath,
      ...config,
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
      reset.value = true;
    });
  } else {
    startPredict({
      name: file.name.split(".")[0],
      type: "file",
      data: fileData,
      ...config,
    }).then((results: any) => {
      finished.value = true;
      starting.value = false;
      reset.value = true;
    });
  }
};

const starting = ref(false);
const finished = ref(false);
const success = ref(false);
</script>

<style scoped lang="less">
.info-tip {
  margin-bottom: 8px;
}

.upload-file {
  width: 100%;
}
</style>
