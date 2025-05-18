import os

# 获取当前文件的绝对路径（即 config.py 的路径）
current_file_path = os.path.abspath(__file__)
# 推导到项目根目录（假设 config.py 在项目根目录下）
project_root = os.path.dirname(current_file_path)

class Config:
    # 使用项目根目录下的 marine.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(project_root, 'marine.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False