# CHALLENGE-TopONE
nexshop_sdk/                      # raiz do repositório
│
├── nexshop_sdk/                  # pacote principal do SDK ( código fonte )
│   ├── __init__.py               # exporta classes públicas, __version__
│   ├── __main__.py               # entrypoint para `python -m nexshop_sdk` (CLI)
│   ├── core.py                   # orquestrador - interface pública do SDK
│   ├── config.py                 # configuração: carregamento de env, arquivos, defaults
│   ├── logging_config.py         # configuração central de logging (struct log)
│   ├── utils.py                  # helpers genéricos (serialização, validators)
│   ├── exceptions.py             # exceções específicas do SDK
│   ├── types.py                  # dataclasses / pydantic models (UserData, DeviceInfo, ScoreResult)
│   │
│   ├── api/                      # adaptadores / middleware para frameworks web
│   │   ├── __init__.py
│   │   ├── fastapi_adapter.py    # funções para integrar com FastAPI (dependências, endpoints)
│   │   ├── flask_adapter.py      # blueprint/handlers para Flask
│   │   └── django_adapter.py     # hooks / middleware para Django
│   │
│   ├── data_collection/          # coleta de dados (apenas backend-side hooks)
│   │   ├── __init__.py
│   │   ├── device_info.py        # parser de user-agent, browser, OS, fingerprint server-side
│   │   ├── ip_location.py        # IP -> geolocalização (abstração / provider interface)
│   │   ├── session_behavior.py   # endpoints/handlers para eventos (click, scroll, timing)
│   │   └── storage_adapter.py    # abstração para persistência temporária (cache/db)
│   │
│   ├── biometrics/               # biometria backend (captura/validação delegada)
│   │   ├── __init__.py
│   │   ├── face_capture.py       # helpers para receber/validar imagens (base64/bytes)
│   │   ├── face_validation.py    # wrapper para modelos/serviços de verificação facial
│   │   └── providers/            # adaptadores para diferentes providers (local / cloud)
│   │       ├── __init__.py
│   │       ├── mock_provider.py
│   │       └── aws_rekognition.py
│   │
│   ├── risk_engine/              # cálculo do score e regras
│   │   ├── __init__.py
│   │   ├── scoring.py            # função principal calcular_score(dados) -> ScoreResult
│   │   ├── features.py           # extratores de features (device_risk, behavior_risk, geo_risk, bio_risk)
│   │   ├── rules.py              # regras fixas / thresholds e pipeline de decisão
│   │   ├── model/                # local para modelos ML/ML ops (pickles, configs)
│   │   │   └── README.md
│   │   └── explainability.py     # gerar razões/atribuições (why score = X)
│   │
│   ├── integrations/             # adaptadores para sistemas/fluxos externos
│   │   ├── __init__.py
│   │   ├── ecommerce_mock.py     # simula fluxo de checkout/login para testes
│   │   ├── webhook_sender.py     # enviar webhook para sistemas que consomem o resultado
│   │   └── adapters/             # adapters para plataformas reais (Shopify, Magento, Woo)
│   │       ├── __init__.py
│   │       └── shopify_adapter.py
│   │
│   ├── output/                   # formatação/serialização da saída (backend "page")
│   │   ├── __init__.py
│   │   ├── score_output.py       # monta ScoreResult (dict / JSON) com detalhes + reasons
│   │   ├── events.py             # eventos internos (Audit log, Decisions)
│   │   └── policies.py           # ações recomendadas (allow, step-up, block) e payloads
│   │
│   ├── persistence/              # interfaces para armazenamento (opcional)
│   │   ├── __init__.py
│   │   ├── cache.py              # interface Redis / in-memory
│   │   └── db_adapter.py         # interface para RDBMS / timeseries / data lake
│   │
│   ├── telemetry/                # métricas, tracing e health checks
│   │   ├── __init__.py
│   │   ├── metrics.py            # contadores / histogram (Prometheus)
│   │   └── tracing.py            # hooks de tracing (opentelemetry)
│   │
│   └── tests_support/            # utilitários para testes (mocks, fixtures)
│       ├── __init__.py
│       └── fixtures.py
│
├── examples/                      # exemplos de integração backend-only
│   ├── exemplo_login.py          # exemplo de chamada em login
│   ├── exemplo_checkout.py       # exemplo de chamada no checkout
│   └── run_simulation.py         # simula fluxo completo (coleta -> scoring -> webhook)
│
├── tests/                         # testes unitários / integração
│   ├── __init__.py
│   ├── test_scoring.py
│   ├── test_data_collection.py
│   ├── test_biometrics.py
│   └── test_output.py
│
├── docs/                          # documentação (README extenso, design doc)
│   ├── architecture.md
│   ├── integration_guide.md
│   └── api_reference.md
│
├── scripts/                       # scripts úteis (dev, build, lint)
│   ├── run_local.sh
│   └── generate_api_stub.sh
│
├── .github/                       # CI / templates
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile                     # containerização do SDK para testes/execução
├── pyproject.toml                 # build system / dependências (preferível moderno)
├── setup.cfg / setup.py           # empacotamento (opcional)
├── requirements.txt               # dependências (se não usar pyproject)
├── README.md
└── LICENSE
