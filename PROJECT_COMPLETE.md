# 🎯 Template FastAPI Clean Architecture - COMPLET

Ce document contient la structure complète du projet, prête à être copiée dans un nouveau repository GitHub.

## 📁 Structure des fichiers

```
fastapi-clean-arch/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
├── requirements.txt
├── mypy.ini
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   ├── dependencies/
    │   │   └── __init__.py
    │   └── v1/
    │       ├── __init__.py
    │       └── routes/
    │           ├── __init__.py
    │           └── example.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── exceptions.py
    │   └── logging.py
    ├── models/
    │   ├── __init__.py
    │   └── example_model.py
    ├── repositories/
    │   ├── __init__.py
    │   └── example_repository.py
    └── services/
        ├── __init__.py
        └── example_service.py
```

## 🚀 Démarrage rapide

```bash
# 1. Cloner et configurer
git clone <your-repo>
cd fastapi-clean-arch

# 2. Configuration
cp .env.example .env
# Éditer .env avec vos valeurs MongoDB

# 3. Installation et lancement
make install
make run

# Ou avec Docker
make run-docker
```

## 🔑 Points clés

- ✅ **Python 3.13** dernière version
- ✅ **Architecture Clean** avec séparation stricte des couches
- ✅ **SOLID principles** appliqués
- ✅ **MongoDB async** avec Motor
- ✅ **Type hints** complets + mypy
- ✅ **Logging structuré** JSON
- ✅ **Docker multi-stage** optimisé
- ✅ **Port paramétrable** depuis .env
- ✅ **Dependency Injection** via FastAPI
- ✅ **Health check** endpoint
- ✅ **Structure simplifiée** (pas de pre-commit, pas de formatage)

## 📝 Configuration .env

Variables essentielles à configurer dans `.env`:

```env
# Port de l'application (paramétrable)
APP_PORT=8000

# MongoDB Atlas (IMPORTANT: remplacer par votre connection string)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=fastapi_db
```

## 🎯 Utilisation

### Développement local
```bash
make run          # Lance sur le port configuré dans .env
```

### Avec Docker
```bash
make run-docker   # Utilise docker-compose avec port paramétrable
make stop         # Arrête les containers
```

### Type checking
```bash
make type-check   # Vérification mypy
```

### Nettoyage
```bash
make clean        # Supprime les caches Python
```

## 📚 Endpoints disponibles

- `GET /health` - Health check
- `POST /examples` - Créer un exemple
- `GET /examples` - Lister les exemples (pagination)
- `GET /examples/{id}` - Obtenir un exemple
- `PUT /examples/{id}` - Mettre à jour un exemple
- `DELETE /examples/{id}` - Supprimer un exemple

## 🔄 Ajouter une nouvelle entité

1. **Model** (`app/models/your_entity.py`)
   - Définir les schémas Pydantic (Create, Update, Response)

2. **Repository** (`app/repositories/your_entity_repository.py`)
   - Implémenter les opérations CRUD MongoDB

3. **Service** (`app/services/your_entity_service.py`)
   - Ajouter la logique métier

4. **Routes** (`app/routes/your_entity.py`)
   - Créer les endpoints HTTP

5. **Dependencies** (`app/api/dependencies/__init__.py`)
   - Ajouter les fonctions d'injection

6. **Main** (`app/main.py`)
   - Inclure le nouveau router

## 🧪 Tests (à ajouter)

```bash
# Installer pytest
pip install pytest pytest-asyncio httpx

# Créer tests/
mkdir tests
touch tests/__init__.py
touch tests/test_example.py

# Lancer
pytest tests/ -v
```

## 🏗️ Architecture

### Flux de requête
```
HTTP Request
    ↓
Route (validation)
    ↓
Service (logique métier)
    ↓
Repository (accès données)
    ↓
MongoDB
```

### Principes SOLID
- **S**: Une responsabilité par classe
- **O**: Extension sans modification
- **L**: Repositories interchangeables
- **I**: Dépendances ciblées
- **D**: Injection de dépendances

## 🐳 Docker

Le Dockerfile utilise un build multi-stage:
- **Builder**: Installation des dépendances dans virtualenv
- **Runtime**: Image slim avec uniquement l'essentiel
- Port paramétrable via `APP_PORT`
- Health check intégré
- Utilisateur non-root pour sécurité

## 📄 License

MIT License - Libre d'utilisation

---

**Template prêt pour production** 🚀
