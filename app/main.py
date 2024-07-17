from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile, TemporaryDirectory
import whisper
import torch
import os

from typing import List

# 检查是否有NVIDIA GPU可用
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 加载Whisper模型
model = whisper.load_model("base", device=DEVICE)

app = FastAPI()


@app.post("/whisper/")
async def handler(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided")

    # 对于每个文件，存储结果在一个字典列表中
    results = []

    # 使用TemporaryDirectory创建临时目录
    with TemporaryDirectory() as temp_dir:
        for file in files:
            # 在临时目录中创建一个临时文件
            temp_file_path = os.path.join(temp_dir, file.filename)
            with open(temp_file_path, "wb") as temp_file:
                # 将用户上传的文件写入临时文件
                temp_file.write(file.file.read())
                temp_file.flush()  # 确保所有数据写入磁盘

            # 确保文件在转录前已关闭
            result = model.transcribe(temp_file_path)

            # 存储该文件的结果对象
            results.append({
                'filename': file.filename,
                'transcript': result['text'],
            })

    # 返回包含结果的JSON响应
    return JSONResponse(content={'results': results})


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
