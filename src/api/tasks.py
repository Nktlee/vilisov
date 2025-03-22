from fastapi import APIRouter
from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime

router = APIRouter()


tasks = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str
    deadline: str

    @field_validator('deadline')
    def validate_deadline(cls, v):
        try:
            datetime.strptime(v, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Deadline must be in the format DD-MM-YYYY")
        return v

@router.post("/tasks", response_model=Task)
def add_task(task: Task):
    global task_id_counter
    task_data = task.model_dump()
    task_data['id'] = task_id_counter
    tasks.append(task_data)
    task_id_counter += 1
    return task_data

@router.get("/tasks", response_model=List[Task])
def get_tasks():
    return sorted(tasks, key=lambda x: datetime.strptime(x['deadline'], "%d-%m-%Y"))

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return {"status": "ok"}


# Напиши 3-5 строк комментариев, объясняющих, как ты придумал структуру данных.
# структура данных была придумана исходя из моего пет проекта. в нем была реализована похожая структура


# В конце файла добавь абзац (5-7 предложений), где объяснишь, как бы ты улучшил проект для продакшена.
# чтобы улучшить проект нужно сделать его масштабируемым. добавить структуру проекта, больше папок, больше файлов, распределить все по тому, где все должно лежать, а не так в одном месте и логика, и работа с данными, и валидация. также добавил бы кеширование, базу данных, celery, контейнеризацию (docker)
