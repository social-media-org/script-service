# 🚀 FastAPI Clean Architecture Template

Template de projet FastAPI prêt à l'emploi suivant les principes de **Clean Architecture** et **SOLID**.

## ✨ Caractéristiques

- ✅ **Clean Architecture** avec séparation claire des responsabilités
- ✅ **Principes SOLID** appliqués rigoureusement
- ✅ **Type Hints** complets avec validation mypy (modérée)
- ✅ **MongoDB Atlas** intégration async avec Motor
- ✅ **Dependency Injection** via FastAPI Depends
- ✅ **Logging structuré** JSON format
- ✅ **Gestion d'erreurs** centralisée et personnalisée
- ✅ **Docker multi-stage** optimisé pour production
- ✅ **Hot reload** pour développement
- ✅ **Port paramétrable** via variable d'environnement
- ✅ **API versioning** (v1)
- ✅ **Health check** endpoint

## 🏗️ Architecture

```
app/
├── api/                    # API Layer - Points d'entrée HTTP
│   ├── dependencies/       # Injection de dépendances
│   └── v1/
│       └── routes/         # Endpoints API
├── core/                   # Core Layer - Configuration et utilitaires
│   ├── config.py           # ConfigService (Settings)
│   ├── database.py         # Database service (Motor)
│   ├── logging.py          # Configuration logging
│   └── exceptions.py       # Exceptions personnalisées
├── services/               # Service Layer - Logique métier
│   └── example_service.py
├── repositories/           # Repository Layer - Accès données
│   └── example_repository.py
├── models/                 # Pydantic Models - Validation
│   └── example_model.py
└── main.py                 # Application FastAPI
```

### Flux de données

```
Request → Route → Service → Repository → MongoDB
             ↓       ↓         ↓
          Pydantic Business  Data Access
          Models   Logic     Layer
```

## 🛠️ Technologies

- **Python 3.13** (dernière version stable)
- **FastAPI** - Framework web moderne
- **Uvicorn** - Serveur ASGI
- **Motor** - MongoDB async driver
- **Pydantic v2** - Validation de données
- **mypy** - Type checking
- **Docker** - Containerisation

## 📦 Installation

### Prérequis

- Python 3.13+
- pip
- (Optionnel) Docker & Docker Compose

### Installation locale

```bash
# Cloner le repository
git clone <your-repo-url>
cd <project-name>

# Installer les dépendances
make install
# OU
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Configuration MongoDB Atlas

1. Créez un compte sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Créez un cluster gratuit
3. Créez un utilisateur database avec permissions lecture/écriture
4. Whitelist votre IP (ou 0.0.0.0/0 pour développement)
5. Récupérez votre connection string

### 2. Fichier .env

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec vos valeurs
nano .env
```

**Configuration dans .env:**

```env
# Application
APP_NAME="FastAPI Clean Architecture"
APP_VERSION="1.0.0"
DEBUG=false
ENVIRONMENT=development

# API
API_V1_PREFIX=/api/v1
ALLOWED_HOSTS=["*"]
APP_PORT=8000

# MongoDB Atlas
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=fastapi_db
MONGODB_MIN_POOL_SIZE=10
MONGODB_MAX_POOL_SIZE=100

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🚀 Utilisation

### Démarrage local

```bash
# Avec Makefile (utilise APP_PORT du .env)
make run

# OU directement avec uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur: **http://localhost:8000** (ou le port configuré dans .env)

### Documentation interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### Examples CRUD

**Créer un exemple**
```http
POST /api/v1/examples
Content-Type: application/json

{
  "name": "Mon exemple",
  "description": "Description optionnelle",
  "is_active": true
}
```

**Lister les exemples**
```http
GET /api/v1/examples?skip=0&limit=10
```

**Obtenir un exemple**
```http
GET /api/v1/examples/{id}
```

**Mettre à jour un exemple**
```http
PUT /api/v1/examples/{id}
Content-Type: application/json

{
  "name": "Nom modifié"
}
```

**Supprimer un exemple**
```http
DELETE /api/v1/examples/{id}
```

## 💻 Développement

### Commandes Makefile

```bash
make help          # Afficher l'aide
make install       # Installer les dépendances
make run           # Lancer l'application (utilise APP_PORT)
make run-docker    # Lancer avec Docker Compose
make stop          # Stopper les containers
make type-check    # Vérification des types (mypy)
make clean         # Nettoyer les caches
make dev           # Setup environnement dev
```

### Type Checking

```bash
make type-check
# OU
mypy app/
```

Configuration mypy dans `mypy.ini` (mode modéré, pas trop strict).

## 🐳 Docker

### Build et Run

```bash
# Avec Docker Compose (recommandé)
make run-docker
# OU
docker-compose up --build

# Stopper les containers
make stop
# OU
docker-compose down
```

### Variables d'environnement Docker

Le port est configurable via `APP_PORT` dans le fichier `.env`. Docker Compose et le Dockerfile utilisent automatiquement cette variable.

```bash
# Dans .env
APP_PORT=8080  # Changez le port ici

# Docker utilisera automatiquement ce port
docker-compose up
```

### Build image seule

```bash
docker build -t fastapi-clean-arch --build-arg APP_PORT=8000 .
docker run -p 8000:8000 --env-file .env fastapi-clean-arch
```

### Dockerfile Multi-stage

Le Dockerfile utilise un build multi-stage pour optimiser la taille de l'image:
- **Stage 1 (builder)**: Installation des dépendances dans un virtualenv
- **Stage 2 (runtime)**: Image légère avec uniquement le nécessaire
- Utilisateur non-root pour la sécurité
- Health check intégré

## 🧪 Tests

Pour ajouter des tests:

1. Installer pytest:
```bash
pip install pytest pytest-asyncio httpx
```

2. Créer le dossier `tests/`:
```bash
mkdir tests
touch tests/__init__.py
touch tests/test_example.py
```

3. Lancer les tests:
```bash
pytest tests/ -v
```

## 📐 Principes SOLID

### Single Responsibility Principle (SRP)
Chaque classe/module a **une seule responsabilité**:
- `ExampleRepository` → Accès données uniquement
- `ExampleService` → Logique métier uniquement
- `example.py` (routes) → Gestion HTTP uniquement

### Open/Closed Principle (OCP)
Le code est **ouvert à l'extension**, **fermé à la modification**:
- Nouvelles fonctionnalités via nouveaux services/repositories
- Pas de modification du code existant

### Liskov Substitution Principle (LSP)
Les abstractions peuvent être **substituées** par leurs implémentations:
- Repository pattern permet de changer de DB sans toucher au service
- Interfaces claires et respectées

### Interface Segregation Principle (ISP)
**Interfaces petites et spécifiques**:
- Dépendances injection ciblée (pas de God Object)
- Chaque layer ne dépend que de ce dont il a besoin

### Dependency Inversion Principle (DIP)
**Dépendance vers les abstractions**, pas les implémentations:
- Services reçoivent repositories via injection
- Configuration centralisée dans ConfigService
- Testabilité maximale (mock facile)

## 📝 Utiliser ce Template

### Pour un nouveau projet

1. **Cloner ce repository**
```bash
git clone <this-repo-url> my-new-project
cd my-new-project
```

2. **Supprimer l'historique git**
```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"
```

3. **Adapter le template**
- Renommer `example_*` par vos entités
- Ajouter vos models dans `app/models/`
- Créer vos repositories dans `app/repositories/`
- Implémenter vos services dans `app/services/`
- Créer vos routes dans `app/api/v1/routes/`

4. **Configuration**
```bash
cp .env.example .env
# Éditer .env avec vos valeurs (notamment MONGODB_URL et APP_PORT)
```

5. **Lancer**
```bash
make install
make run
```

## 🔧 Personnalisation du port

Le port est **entièrement paramétrable** depuis un seul endroit (`.env`):

```env
APP_PORT=8080  # Changez ici
```

Cette variable est automatiquement utilisée par:
- ✅ `make run` (Makefile)
- ✅ `docker-compose.yml`
- ✅ `Dockerfile`
- ✅ Health check

## 📄 License

MIT License - Libre d'utilisation pour vos projets.

---

**Créé avec ❤️ pour des architectures propres et maintenables**
