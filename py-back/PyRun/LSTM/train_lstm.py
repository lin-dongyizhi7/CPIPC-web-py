import sys
import os

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')


def train_lstm(params):
    name = params['file_info']['name']
    # 指定模型文件路径
    model_path = params['model']
    
    print('Train LSTM')
    return True