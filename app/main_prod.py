import os
from dotenv import load_dotenv
import uvicorn
from controllers.fastapi.app import run_fastapi_app

load_dotenv()


def main():
    """FastAPI 서버를 프로덕션 모드로 실행"""
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        run_fastapi_app(),
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    main()

