# AI Whisper 项目启动指南

## 项目介绍
AI Whisper 是一个基于FastAPI和OpenAI Whisper的语音转录服务项目。该项目旨在提供一个高效、易于部署的语音转录API，可以在多种环境中快速实现语音到文本的转换。

## 环境要求
- Python 3.10 或更高版本
- Poetry - Python 的依赖管理和包管理工具

## 安装指南
1. **克隆项目**
   使用Git克隆仓库到本地:
   ```bash
   git clone https://your-repository-link.git
   cd your-project-folder
   ```

2. **安装依赖**
   使用Poetry安装所有依赖:
   ```bash
   poetry install
   ```

## 启动项目
在安装了所有依赖之后，你可以通过以下命令来启动项目:
```bash
poetry run start
```
该命令将使用`uvicorn`作为ASGI服务器来运行你的FastAPI应用。默认情况下，应用将在本地的8000端口运行。

## 访问API文档
项目启动后，你可以通过访问以下URL来查看Swagger UI文档，该文档自动生成并提供了一个交互式的用户界面，用于直接在浏览器中测试API端点:
```
http://127.0.0.1:8000/docs
```

## 项目结构
项目的主要结构如下所示:
- `app/`: 包含FastAPI应用的主要代码和逻辑。
- `main.py`: FastAPI应用的入口文件，包含路由和API端点的定义。
- `poetry.toml`: 定义项目依赖和配置的Poetry文件。

## 如何贡献
我们欢迎所有形式的贡献，无论是新功能的建议、代码改进，还是文档更新。请遵循以下步骤进行贡献:
1. Fork 项目仓库。
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的改变 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个Pull Request。

## 联系方式
如果你有任何问题或者想要联系项目维护者，可以通过以下邮箱与我联系: 
`AceLin <xoxosos666@gmail.com>`

感谢你对AI Whisper项目的兴趣和支持！
