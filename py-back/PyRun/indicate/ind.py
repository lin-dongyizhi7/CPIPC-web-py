import sys
import os

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)


def generateInd(init_data):
    print('Generate ind')
    result = {'info': 'success'}
    return result