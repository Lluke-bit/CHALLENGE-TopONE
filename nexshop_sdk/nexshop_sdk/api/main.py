from fastapi import FastAPI
from api.routers import auth, biometrics
from database import config

app = FastAPI(
    title="API de Autenticação Biométrica",
    description="API para gerenciamento e autenticação de usuários via biometria facial.",
    version="1.0.0"
)

# Incluir os roteadores com os endpoints
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(biometrics.router, prefix="/biometrics", tags=["Biometria"])

# Eventos de startup/shutdown do banco de dados (se usar SQLAlchemy Async)
@app.on_event("startup")
async def startup_event():
    await config.init_db() # Inicializa a conexão com o banco

@app.on_event("shutdown")
async def shutdown_event():
    await config.close_db() # Fecha a conexão