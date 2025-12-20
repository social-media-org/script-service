# 🏗️ Structure du Projet - Script Generation Service

## 📁 Arborescence Complète

```
/app/
│
├── app/                            # Application principale
│   │
│   ├── main.py                     # Point d'entrée FastAPI
│   │
│   ├── core/                       # Configuration et utilitaires core
│   │   ├── __init__.py
│   │   ├── config.py               # Settings (Pydantic)
│   │   ├── llm_client.py           # Client LLM (DeepSeek/OpenAI)
│   │   ├── utils.py                # Fonctions utilitaires
│   │   ├── logging.py              # Configuration logging
│   │   ├── database.py             # Database (non utilisé)
│   │   └── exceptions.py           # Gestion d'exceptions
│   │
│   ├── routes/                     # Endpoints API
│   │   ├── __init__.py
│   │   └── scripts.py              # Routes /scripts
│   │
│   ├── models/                     # Modèles Pydantic
│   │   ├── __init__.py
│   │   └── script.py               # ScriptGenerationRequest/Response
│   │
│   ├── services/                   # Logique métier et agents
│   │   ├── __init__.py
│   │   ├── title_agent.py          # 🤖 Agent génération titre
│   │   ├── sections_agent.py       # 🤖 Agent génération sections
│   │   ├── description_agent.py    # 🤖 Agent génération description
│   │   ├── keywords_agent.py       # 🤖 Agent génération keywords
│   │   ├── transcription_service.py # 🎥 Service transcription vidéo
│   │   └── script_orchestrator.py  # 🎯 Orchestrateur principal
│   │
│   ├── llm/                        # Infrastructure LLM
│   │   ├── __init__.py
│   │   ├── base_agent.py           # Classe de base pour agents
│   │   └── prompts/                # Templates de prompts
│   │       ├── title_prompt.txt
│   │       ├── sections_prompt.txt
│   │       ├── description_prompt.txt
│   │       └── keywords_prompt.txt
│   │
│   └── helpers/                    # Helpers divers
│       └── datetime_utils.py
│
├── requirements.txt                # Dépendances Python
├── .env                           # Variables d'environnement (secret)
├── .env.example                   # Template pour .env
├── README.md                      # Documentation principale
├── QUICKSTART_SCRIPT_SERVICE.md   # Guide démarrage rapide
├── PROJECT_STRUCTURE.md           # Ce fichier
├── examples_requests.json         # Exemples de requêtes
├── test_api.py                    # Script de test
│
└── Dockerfile                     # (optionnel) Configuration Docker
```

## 🔄 Flux de Données

```
┌─────────────────────────────────────────────────────────────────┐
│                         REQUÊTE CLIENT                          │
│  POST /scripts/{project_id}                             │
│  Body: ScriptGenerationRequest                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ROUTE (scripts.py)                         │
│  - Validation Pydantic                                          │
│  - Appel orchestrateur                                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATEUR (script_orchestrator.py)             │
│  Coordonne tous les agents dans l'ordre                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├─► 1. TRANSCRIPTION (si vidéos fournies)
                         │   └─► TranscriptionService
                         │       ├─► PyTubeFix (YouTube)
                         │       └─► AssemblyAI (transcription)
                         │
                         ├─► 2. SECTIONS (si regenerer_script=true)
                         │   └─► SectionsAgent
                         │       └─► LLM (DeepSeek)
                         │
                         ├─► 3. TITRE
                         │   └─► TitleAgent
                         │       └─► LLM (DeepSeek)
                         │
                         ├─► 4. KEYWORDS
                         │   └─► KeywordsAgent
                         │       └─► LLM (DeepSeek)
                         │
                         └─► 5. DESCRIPTION
                             └─► DescriptionAgent
                                 └─► LLM (DeepSeek)
                         
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RÉPONSE CLIENT                             │
│  ScriptGenerationResponse (JSON)                                │
│  - script_text, script_sections                                 │
│  - title, keywords, video_description                           │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Architecture des Agents

### Hiérarchie

```
BaseAgent (llm/base_agent.py)
    │
    ├─► TitleAgent
    │   └─► Prompt: title_prompt.txt
    │
    ├─► SectionsAgent
    │   └─► Prompt: sections_prompt.txt
    │
    ├─► DescriptionAgent
    │   └─► Prompt: description_prompt.txt
    │
    └─► KeywordsAgent
        └─► Prompt: keywords_prompt.txt
```

### Responsabilités

| Agent | Input | Output | Temperature |
|-------|-------|--------|-------------|
| **TitleAgent** | description, use_case, style, language | Titre optimisé (40-60 chars) | 0.8 (créatif) |
| **SectionsAgent** | description, inspirations, duration, nb_section, style, language | Sections + script_text | 0.7 (équilibré) |
| **DescriptionAgent** | script_text, keywords, language | Description avec hashtags | 0.7 (équilibré) |
| **KeywordsAgent** | script_text, description, use_case | Liste mots-clés SEO | 0.6 (précis) |

## 🔧 Configuration (core/config.py)

### Variables d'environnement

```python
# Application
APP_NAME: str               # Nom du service
APP_VERSION: str            # Version
DEBUG: bool                 # Mode debug
ENVIRONMENT: str            # dev/prod

# API
API_V1_PREFIX: str          # Préfixe routes ()
ALLOWED_HOSTS: list[str]    # CORS
APP_PORT: int               # Port serveur

# LLM
DEEPSEEK_API_KEY: str       # Clé API DeepSeek
OPENAI_API_BASE: str        # URL API (DeepSeek compatible)
OPENAI_MODEL: str           # Modèle (deepseek-chat)

# Transcription
ASSEMBLYAI_API_KEY: str     # Clé API AssemblyAI

# Defaults
DEFAULT_DURATION: int       # Durée par défaut (30s)
DEFAULT_NB_SECTIONS: int    # Sections par défaut (1)

# Logging
LOG_LEVEL: str              # INFO/DEBUG/ERROR
LOG_FORMAT: str             # text/json
```

## 📦 Modèles de Données (models/script.py)

### ScriptGenerationRequest

```python
{
    "title": str,                     # ✅ Requis
    "description": str,               # ✅ Requis
    "use_case": Literal[...],         # ✅ Requis
    "language": Literal[...],         # ✅ Requis
    "style": Literal[...],            # ✅ Requis
    "video_inspirations": list[str],  # ⚪ Optionnel
    "keywords": str,                  # ⚪ Optionnel
    "script_text": str,               # ⚪ Optionnel (regeneration)
    "regenerer_script": bool,         # ⚪ Default: true
    "duration": int,                  # ⚪ Default: 30
    "nb_section": int                 # ⚪ Default: 1
}
```

### ScriptGenerationResponse

```python
{
    "script_sections": list[str],     # Null si nb_section=1
    "script_text": str,               # ✅ Toujours présent
    "status": str,                    # "script_generated"
    "keywords": str,                  # Mots-clés générés
    "video_description": str,         # Description générée
    "title": str                      # Titre généré
}
```

## 🎯 Points d'Entrée

### Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/health` | Health check global |
| `GET` | `/scripts/health` | Health check détaillé |
| `POST` | `/scripts/{project_id}` | Génération de script |
| `GET` | `/docs` | Documentation Swagger |
| `GET` | `/redoc` | Documentation ReDoc |

## 🧩 Dépendances

### Production

```
fastapi         # Framework web
uvicorn         # Serveur ASGI
pydantic        # Validation données
openai          # Client LLM (compatible DeepSeek)
assemblyai      # Transcription audio
pytubefix       # Download YouTube
httpx           # HTTP client
```

### Dev/Test

```
mypy            # Type checking
json-logging    # Structured logs
```

## 🔐 Sécurité

- ✅ Validation Pydantic stricte
- ✅ Variables d'environnement pour secrets
- ✅ .env dans .gitignore
- ✅ CORS configuré
- ✅ Error handling centralisé

## 📊 Performance

- ⚡ Async/await partout
- ⚡ Singleton pour clients (LLM, Transcription)
- ⚡ Streaming pas encore implémenté (roadmap)

## 🚀 Prochaines Étapes (Roadmap)

- [ ] Streaming des réponses LLM
- [ ] Cache des transcriptions
- [ ] Support Facebook vidéos (limitations API)
- [ ] Métriques et monitoring
- [ ] Tests unitaires complets
- [ ] Docker Compose multi-services
- [ ] Rate limiting
- [ ] Authentication/Authorization

---

**Dernière mise à jour:** Novembre 2024
