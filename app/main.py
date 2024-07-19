from fastapi import FastAPI, File, Query, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import TemporaryDirectory
import whisper
from whisper import tokenizer
import torch
import os
from typing import Union, List

# 检查是否有NVIDIA GPU可用
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 加载Whisper模型
model_name = os.getenv("MODEL", "small")
model = whisper.load_model(model_name, device=DEVICE)
LANGUAGE_CODES = sorted(tokenizer.LANGUAGES.keys())

app = FastAPI()
print(DEVICE, model_name)


def save_uploaded_file(upload_file: UploadFile, destination: str) -> None:
    """将上传的文件保存到指定的路径"""
    try:
        with open(destination, "wb") as out_file:
            out_file.write(upload_file.file.read())
    except PermissionError as e:
        raise HTTPException(status_code=500, detail=f"Permission denied: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


def transcribe_file(file_path: str, language: Union[str, None]) -> dict:
    """使用Whisper模型转录文件"""
    try:
        transcribe_language = language if language is not None else None
        result = model.transcribe(file_path, language=transcribe_language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发生错误: {str(e)}")


@app.post("/whisper/")
async def handler(
        files: List[UploadFile] = File(...),
        language: Union[str, None] = Query(default=None, enum=LANGUAGE_CODES),
):
    print('started', language)
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided")

    results = []

    # 使用TemporaryDirectory创建临时目录
    with TemporaryDirectory() as temp_dir:
        for file in files:
            try:
                temp_file_path = os.path.join(temp_dir, file.filename)
                save_uploaded_file(file, temp_file_path)
                result = transcribe_file(temp_file_path, language)
                results.append({
                    'filename': file.filename,
                    'transcript': result['text'],
                    'language': result['language'] if language is None else language,
                })
            except HTTPException as e:
                raise e  # 重新抛出 HTTP 异常
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process file {file.filename}: {str(e)}")

    return JSONResponse(content={'data': results})


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
