# ⚡ Guide de Démarrage Rapide

## 🎯 En 5 minutes

### 1. Prérequis
```bash
# Vérifier Python 3.13+
python3 --version

# Vérifier pip
pip --version
```

### 2. Installation
```bash
# Cloner le projet
git clone <your-repo-url>
cd fastapi-clean-arch

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration MongoDB

#### Option A: MongoDB Atlas (Recommandé - Gratuit)
1. Créer un compte: https://www.mongodb.com/cloud/atlas
2. Créer un cluster M0 (gratuit)
3. Créer un utilisateur DB
4. Whitelist IP: `0.0.0.0/0` (dev) ou votre IP
5. Copier la connection string

#### Option B: MongoDB Local
```bash
# Installer MongoDB localement
# macOS
brew install mongodb-community

# Ubuntu
sudo apt-get install mongodb

# Démarrer MongoDB
mongod --dbpath=/path/to/data
```

### 4. Configurer .env
```bash
# Copier le template
cp .env.example .env

# Éditer avec vos valeurs
nano .env
```

**Minimum requis:**
```env
APP_PORT=8000
MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/
DB_NAME=fastapi_db
```

### 5. Lancer l'application
```bash
# Avec Makefile
make run

# OU directement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Tester
```bash
# Ouvrir votre navigateur
http://localhost:8000/docs

# Ou tester avec curl
curl http://localhost:8000/health
```

**Résultat attendu:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

## 🐳 Avec Docker (Alternative)

### Si vous avez Docker installé

```bash
# Configuration
cp .env.example .env
# Éditer .env avec vos valeurs MongoDB

# Lancer
docker-compose up --build

# Ou avec Makefile
make run-docker
```

L'application sera disponible sur `http://localhost:8000`

## 📋 Tester l'API

### 1. Via Swagger UI (Recommandé)
- Ouvrir: http://localhost:8000/docs
- Tester les endpoints directement depuis l'interface

### 2. Via curl

**Créer un exemple:**
```bash
curl -X POST http://localhost:8000/api/v1/examples \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mon premier exemple",
    "description": "Test de création",
    "is_active": true
  }'
```

**Lister les exemples:**
```bash
curl http://localhost:8000/api/v1/examples
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## 🔧 Commandes utiles

```bash
# Démarrer l'application
make run

# Vérifier les types
make type-check

# Nettoyer les caches
make clean

# Installer les dépendances
make install

# Voir toutes les commandes
make help
```

## 🐛 Dépannage

### Problème: Port déjà utilisé
```bash
# Changer le port dans .env
APP_PORT=8001

# Relancer
make run
```

### Problème: MongoDB connection failed
```bash
# Vérifier la connection string dans .env
# Format: mongodb+srv://username:password@cluster.mongodb.net/

# Tester la connexion
mongosh "mongodb+srv://username:password@cluster.mongodb.net/"
```

### Problème: Module not found
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème: Permission denied (Docker)
```bash
# Ajouter votre user au groupe docker
sudo usermod -aG docker $USER
# Redémarrer la session
```

## 📚 Prochaines étapes

1. **Personnaliser** l'application:
   - Modifier `example_*` avec vos propres entités
   - Ajouter vos models, repositories, services

2. **Ajouter des tests**:
   ```bash
   pip install pytest pytest-asyncio httpx
   mkdir tests
   ```

3. **Déployer** (voir README.md pour plus de détails)

4. **Lire la documentation**:
   - README.md - Documentation complète
   - STRUCTURE.md - Architecture détaillée
   - PROJECT_COMPLETE.md - Vue d'ensemble

## 🆘 Besoin d'aide ?

- Consulter: README.md
- Vérifier: STRUCTURE.md
- Issues: <your-repo-url>/issues

---

**Bon développement !** 🚀
