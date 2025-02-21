from pydantic import BaseModel

# 定义请求模型
class OutlineRequest(BaseModel):
    tech_content: str
    score_content: str

class ContentRequest(BaseModel):
    outline: dict