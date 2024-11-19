import request from "../utils/request.js";

const baseUrl = ''

// 指标构建
export const generateInd = (data: any) => {
  return request({
    url: baseUrl + "/generateInd",
    method: "post",
    data
  });
}
// 开始训练
export const startTrain = (data: any) => {
  return request({
    url: baseUrl + "/train",
    method: "post",
    data
  });
}
// 预测
export const startPredict = (data: any) => {
  return request({
    url: baseUrl + "/predict",
    method: "post",
    data
  });
}

// 获取模型列表
export const getModelsList = () => {
  return request({
    url: baseUrl + '/getModelsList',
    method: "get"
  });
}