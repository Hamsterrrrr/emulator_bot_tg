from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI(title="Telegram Link Processor", description="API для обработки Telegram-ссылок и запуска тестов.")

class LinkRequest(BaseModel):
    link: str

@app.post("/links/")
async def receive_link(request: LinkRequest):
    """
    Принимает ссылку и запускает pytest.
    """
    link = request.link
    if not link.startswith("https://t.me/"):
        raise HTTPException(status_code=400, detail="Неверный формат ссылки.")
    
    print(f"Получена ссылка: {link}")
    try:
        # Запускаем pytest с передачей ссылки как параметра
        subprocess.run(
    ["pytest", "tests/test_tg_links.py", f"--link={link}"],
    check=True,
    cwd="/media/ham/X/appium_bot"  # Укажите абсолютный путь к корню проекта
)

        return {"status": "success", "message": f"Тесты запущены для ссылки {link}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка запуска тестов: {e}")

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API для обработки Telegram-ссылок!"}

