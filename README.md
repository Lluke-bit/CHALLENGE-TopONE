# DOCUMENTAÇÃO
> Segue documentação Oficial do projeto FIAP+HAKAI do grupo mais top da FIAP. Caso vcs não aceitem esse projeto como vencedor, vamos abrir uma startup e vender isso. Fica o aviso...
## Estrutura
> Falando um pouco sobre a estrutura do projeto. Temos tanto a parte do codigo back-end onde pode apenas ser instalada e configurar algumas coisas para que sua organização fique mais segura. Quanto o front-end, utilizado para facilitar a configuração do back-end para os usuários.
### Back-end
nexshop_sdk/                    .............................................# raiz do repositório <br>
│<br>
├── nexshop_sdk/                  .............................................# pacote principal do SDK ( código fonte )<br>
│   ├── __init__.py               .............................................# exporta classes públicas, __version__<br>
│   ├── __main__.py               .............................................# entrypoint para `python -m nexshop_sdk` (CLI)<br>
│   ├── core.py                   .............................................# orquestrador - interface pública do SDK<br>
│   ├── config.py                 .............................................# configuração: carregamento de env, arquivos, defaults<br>
│   ├── logging_config.py         .............................................# configuração central de logging (struct log)<br>
│   ├── utils.py                  .............................................# helpers genéricos (serialização, validators)<br>
│   ├── exceptions.py             .............................................# exceções específicas do SDK<br>
│   ├── types.py                  .............................................# dataclasses / pydantic models (UserData, DeviceInfo, ScoreResult)<br>
│   │<br>
│   ├── api/                      .............................................# adaptadores / middleware para frameworks web<br>
│   │   ├── __init__.py<br>
│   │   ├── fastapi_adapter.py    .............................................# funções para integrar com FastAPI (dependências, endpoints)<br>
│   │   ├── flask_adapter.py      .............................................# blueprint/handlers para Flask<br>
│   │   └── django_adapter.py     .............................................# hooks / middleware para Django<br>
│   │<br>
│   ├── data_collection/          .............................................# coleta de dados (apenas backend-side hooks)<br>
│   │   ├── __init__.py<br>
│   │   ├── device_info.py        .............................................# parser de user-agent, browser, OS, fingerprint server-side<br>
│   │   ├── ip_location.py        .............................................# IP -> geolocalização (abstração / provider interface)<br>
│   │   ├── session_behavior.py   .............................................# endpoints/handlers para eventos (click, scroll, timing)<br>
│   │   └── storage_adapter.py    .............................................# abstração para persistência temporária (cache/db)<br>
│   │<br>
│   ├── biometrics/               .............................................# biometria backend (captura/validação delegada)<br>
│   │   ├── __init__.py<br>
│   │   ├── face_capture.py       .............................................# helpers para receber/validar imagens (base64/bytes)<br>
│   │   ├── face_validation.py    .............................................# wrapper para modelos/serviços de verificação facial<br>
│   │   └── providers/            .............................................# adaptadores para diferentes providers (local / cloud)<br>
│   │       ├── __init__.py<br>
│   │       ├── mock_provider.py<br>
│   │       └── aws_rekognition.py<br>
│   │<br>
│   ├── risk_engine/              .............................................# cálculo do score e regras<br>
│   │   ├── __init__.py<br>
│   │   ├── scoring.py            .............................................# função principal calcular_score(dados) -> ScoreResult<br>
│   │   ├── features.py           .............................................# extratores de features (device_risk, behavior_risk, geo_risk, bio_risk)<br>
│   │   ├── rules.py              .............................................# regras fixas / thresholds e pipeline de decisão<br>
│   │   ├── model/                .............................................# local para modelos ML/ML ops (pickles, configs)<br>
│   │   │   └── README.md<br>
│   │   └── explainability.py     .............................................# gerar razões/atribuições (why score = X)<br>
│   │<br>
│   ├── integrations/             .............................................# adaptadores para sistemas/fluxos externos<br>
│   │   ├── __init__.py<br>
│   │   ├── ecommerce_mock.py     .............................................# simula fluxo de checkout/login para testes<br>
│   │   ├── webhook_sender.py     .............................................# enviar webhook para sistemas que consomem o resultado<br>
│   │   └── adapters/             .............................................# adapters para plataformas reais (Shopify, Magento, Woo)<br>
│   │       ├── __init__.py<br>
│   │       └── shopify_adapter.py<br>
│   │<br>
│   ├── output/                   .............................................# formatação/serialização da saída (backend "page")<br>
│   │   ├── __init__.py<br>
│   │   ├── score_output.py       .............................................# monta ScoreResult (dict / JSON) com detalhes + reasons<br>
│   │   ├── events.py             .............................................# eventos internos (Audit log, Decisions)<br>
│   │   └── policies.py           .............................................# ações recomendadas (allow, step-up, block) e payloads<br>
│   │<br>
│   ├── persistence/              .............................................# interfaces para armazenamento (opcional)<br>
│   │   ├── __init__.py<br>
│   │   ├── cache.py              .............................................# interface Redis / in-memory<br>
│   │   └── db_adapter.py         .............................................# interface para RDBMS / timeseries / data lake<br>
│   │<br>
│   ├── telemetry/                .............................................# métricas, tracing e health checks<br>
│   │   ├── __init__.py<br>
│   │   ├── metrics.py            .............................................# contadores / histogram (Prometheus)<br>
│   │   └── tracing.py            .............................................# hooks de tracing (opentelemetry)<br>
│   │<br>
│   └── tests_support/            .............................................# utilitários para testes (mocks, fixtures)<br>
│       ├── __init__.py<br>
│       └── fixtures.py<br>
│
├── examples/                     .............................................# exemplos de integração backend-only<br>
│   ├── exemplo_login.py          .............................................# exemplo de chamada em login<br>
│   ├── exemplo_checkout.py       .............................................# exemplo de chamada no checkout<br>
│   └── run_simulation.py         .............................................# simula fluxo completo (coleta -> scoring -> webhook)<br>
│<br>
├── tests/                         .............................................# testes unitários / integração<br>
│   ├── __init__.py<br>
│   ├── test_scoring.py<br>
│   ├── test_data_collection.py<br>
│   ├── test_biometrics.py<br>
│   └── test_output.py<br>
│<br>
├── docs/                          .............................................# documentação (README extenso, design doc)<br>
│   ├── architecture.md<br>
│   ├── integration_guide.md<br>
│   └── api_reference.md<br>
│<br>
├── scripts/                      .............................................# scripts úteis (dev, build, lint)<br>
│   ├── run_local.sh<br>
│   └── generate_api_stub.sh<br>
│<br>
├── .github/                       .............................................# CI / templates<br>
│   └── workflows/<br>
│       └── ci.yml<br>
│<br>
├── Dockerfile                     .............................................# containerização do SDK para testes/execução<br>
├── pyproject.toml                 .............................................# build system / dependências (preferível moderno)<br>
├── setup.cfg / setup.py           .............................................# empacotamento (opcional)<br>
├── requirements.txt               .............................................# dependências (se não usar pyproject)<br>
├── README.md<br>
└── LICENSE<br>
## Front-end
src/<br>
│<br>
├── front/<br>
│   ├── dashboard/<br>
│   │   ├── dashboard_screen.dart         # Explicação: Tela inicial com KPIs, gráficos e visão geral dos eventos<br>
│   │   ├── dashboard_controller.dart     # Explicação: Lógica para buscar dados do backend e atualizar a tela<br>
│   │   ├── widgets/<br>
│   │   │   ├── metric_card.dart          # Explicação: Card visual para exibir métricas rápidas (ex: bloqueios hoje)<br>
│   │   │   ├── activity_graph.dart       # Explicação: Gráfico mostrando evolução de eventos ao longo do tempo<br>
│   │   │   ├── user_table.dart           # Explicação: Tabela com usuários bloqueados, status e filtros<br>
│   │   │   └── real_time_log.dart        # Explicação: Lista de eventos atualizada em tempo real<br>
│   │<br>
│   ├── setup/<br>
│   │   ├── wizard_screen.dart            # Explicação: Assistente passo a passo para configuração inicial do sistema<br>
│   │   ├── storage_settings.dart         # Explicação: Configuração de armazenamento (Local, Cloud, Retenção de dados)<br>
│   │   ├── module_settings.dart          # Explicação: Escolha dos módulos ativos (biometria, análise de comportamento, etc.)<br>
│   │   ├── integration_settings.dart     # Explicação: Configuração de integrações externas (SIEM, SOAR, IAM, Webhooks)<br>
│   │   └── confirmation_screen.dart      # Explicação: Resumo final antes de aplicar as configurações<br>
│   │<br>
│   ├── auth/<br>
│   │   ├── login_screen.dart             # Explicação: Tela de login para administradores<br>
│   │   ├── register_screen.dart          # Explicação: Tela para cadastro de novos administradores<br>
│   │   └── forgot_password.dart          # Explicação: Tela para recuperação de senha via e-mail ou OTP<br>
│   │<br>
│   ├── reports/<br>
│   │   ├── reports_screen.dart           # Explicação: Lista e visualização de relatórios filtrados<br>
│   │   └── export_options.dart           # Explicação: Opções para exportar relatórios (CSV, PDF, JSON)<br>
│   │<br>
│   ├── monitoring/<br>
│   │   ├── real_time_monitor_screen.dart # Explicação: Tela com monitoramento ao vivo dos eventos de segurança<br>
│   │   └── event_details_modal.dart      # Explicação: Modal com detalhes completos de um evento<br>
│   │<br>
│   ├── settings/<br>
│   │   ├── general_settings.dart         # Explicação: Configurações gerais (idioma, tema, fuso horário)<br>
│   │   ├── security_settings.dart        # Explicação: Ajuste de thresholds, níveis de bloqueio e tempo de sessão<br>
│   │   └── permissions_settings.dart     # Explicação: Gerenciamento de usuários e permissões<br>
│   │<br>
│   └── shared/<br>
│       ├── styles.dart                   # Explicação: Definição de temas, cores, tipografia e espaçamentos<br>
│       ├── constants.dart                # Explicação: Variáveis fixas, chaves de API e URLs base<br>  
│       └── widgets/<br>
│           ├── custom_button.dart        # Explicação: Botão padronizado do sistema<br>
│           ├── custom_input_field.dart   # Explicação: Campo de texto padronizado do sistema<br>
│           └── page_header.dart          # Explicação: Cabeçalho de páginas com título e breadcrumbs<br>
