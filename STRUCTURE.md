# 📂 Structure du Projet

## Structure complète

```
fastapi-clean-arch/
├── .env                           # Variables d'environnement (local)
├── .env.example                   # Template des variables d'environnement
├── .gitignore                     # Fichiers à ignorer par git
├── Dockerfile                     # Build multi-stage optimisé
├── docker-compose.yml             # Configuration Docker Compose
├── Makefile                       # Commandes utiles (run, install, etc.)
├── README.md                      # Documentation principale
├── requirements.txt               # Dépendances Python
├── mypy.ini                       # Configuration type checking
│
└── app/                           # Application Python
    ├── __init__.py
    │
    ├── main.py                    # 🚀 Point d'entrée FastAPI
    │
    ├── api/                       # 🌐 API Layer - HTTP
    │   ├── __init__.py
    │   ├── dependencies/          # Dependency Injection
    │   │   └── __init__.py        # get_example_service, get_example_repository
    │   └── v1/                    # API Version 1
    │       ├── __init__.py
    │       └── routes/            # Routes/Endpoints
    │           ├── __init__.py
    │           └── example.py     # CRUD endpoints pour Example
    │
    ├── core/                      # ⚙️ Core Layer - Configuration
    │   ├── __init__.py
    │   ├── config.py              # ConfigService (Pydantic Settings)
    │   ├── database.py            # DatabaseService (Motor/MongoDB)
    │   ├── exceptions.py          # Exceptions personnalisées
    │   └── logging.py             # Configuration logging structuré
    │
    ├── models/                    # 📋 Pydantic Models
    │   ├── __init__.py
    │   └── example_model.py       # ExampleCreate, ExampleUpdate, ExampleResponse
    │
    ├── repositories/              # 💾 Repository Layer - Data Access
    │   ├── __init__.py
    │   └── example_repository.py  # ExampleRepository (CRUD MongoDB)
    │
    └── services/                  # 🎯 Service Layer - Business Logic
        ├── __init__.py
        └── example_service.py     # ExampleService (logique métier)
```

## Détail des couches

### 1. **API Layer** (`app/api/`)
- **Responsabilité**: Gestion des requêtes HTTP
- **Contenu**: Routes, validation des entrées, réponses HTTP
- **Principe**: Aucune logique métier, uniquement orchestration

### 2. **Service Layer** (`app/services/`)
- **Responsabilité**: Logique métier
- **Contenu**: Règles métier, orchestration des repositories
- **Principe**: Indépendant de l'API et de la DB

### 3. **Repository Layer** (`app/repositories/`)
- **Responsabilité**: Accès aux données
- **Contenu**: CRUD MongoDB, requêtes DB
- **Principe**: Abstraction de la source de données

### 4. **Core Layer** (`app/core/`)
- **Responsabilité**: Configuration et utilitaires
- **Contenu**: Settings, DB connection, logging, exceptions
- **Principe**: Utilisé par toutes les autres couches

### 5. **Models Layer** (`app/models/`)
- **Responsabilité**: Validation des données
- **Contenu**: Schémas Pydantic
- **Principe**: Contrats de données entre les couches

## Flux de requête

```
┌─────────────┐
│  HTTP GET   │
│ /api/v1/... │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────┐
│  API Layer (routes/example.py)      │
│  - Validation Pydantic              │
│  - Gestion HTTP                     │
└──────┬──────────────────────────────┘
       │ inject: ExampleService
       ↓
┌─────────────────────────────────────┐
│  Service Layer (example_service.py) │
│  - Logique métier                   │
│  - Orchestration                    │
└──────┬──────────────────────────────┘
       │ inject: ExampleRepository
       ↓
┌──────────────────────────────────────┐
│ Repository Layer (example_repository)│
│  - Requêtes MongoDB                  │
│  - CRUD operations                   │
└──────┬───────────────────────────────┘
       │
       ↓
┌─────────────┐
│  MongoDB    │
└─────────────┘
```

## Fichiers clés

### `app/main.py`
- Point d'entrée de l'application
- Configuration FastAPI
- Gestion du cycle de vie (startup/shutdown)
- Inclusion des routers
- Middleware CORS
- Health check

### `app/core/config.py`
- Configuration centralisée via Pydantic Settings
- Variables d'environnement
- Singleton pattern

### `app/core/database.py`
- Connexion MongoDB async (Motor)
- Gestion du client MongoDB
- Pool de connexions

### `app/api/dependencies/__init__.py`
- Dependency Injection
- Création des instances (Service, Repository)
- Pattern Factory

### `Dockerfile`
- Build multi-stage (builder + runtime)
- Python 3.13-slim
- Virtualenv isolé
- Utilisateur non-root
- Port paramétrable

### `docker-compose.yml`
- Service API
- Port mapping paramétrable
- Hot reload pour développement
- Health check

### `Makefile`
- Commandes simplifiées
- Port paramétrable depuis .env
- Commandes: run, install, type-check, clean

## Principe SOLID appliqués

1. **Single Responsibility**: Chaque fichier a une responsabilité unique
2. **Open/Closed**: Extension facile via nouveaux services/repositories
3. **Liskov Substitution**: Repositories interchangeables
4. **Interface Segregation**: Dépendances ciblées
5. **Dependency Inversion**: Injection de dépendances

## Pour ajouter une nouvelle entité

1. Créer le model dans `app/models/your_model.py`
2. Créer le repository dans `app/repositories/your_repository.py`
3. Créer le service dans `app/services/your_service.py`
4. Créer les routes dans `app/api/v1/routes/your_routes.py`
5. Ajouter les dependencies dans `app/api/dependencies/__init__.py`
6. Inclure le router dans `app/main.py`
