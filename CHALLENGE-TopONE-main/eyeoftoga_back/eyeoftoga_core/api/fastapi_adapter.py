# nexshop_sdk/api/fastapi_adapter.py

from fastapi import FastAPI, APIRouter

# Função para criar a aplicação FastAPI
def create_fastapi_app():
    app = FastAPI(title="Nexshop API - FastAPI Adapter")
    router = APIRouter()

    @router.get("/healthcheck")
    async def healthcheck():
        """
        Endpoint de verificação de saúde.
        """
        return {"status": "ok", "framework": "FastAPI"}

    # Incluímos o roteador
    app.include_router(router)
    return app


# Apenas para execução local, use `uvicorn fastapi_adapter:create_fastapi_app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_fastapi_app(), host="0.0.0.0", port=8000)
