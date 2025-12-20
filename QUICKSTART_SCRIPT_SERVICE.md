# 🚀 Démarrage Rapide - Script Generation Service

## 📋 Prérequis

1. **Python 3.11+** installé
2. **Clés API** :
   - DeepSeek API Key: https://platform.deepseek.com/
   - AssemblyAI API Key: https://www.assemblyai.com/

## ⚡ Installation en 3 étapes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer les clés API

Éditez le fichier `.env` :

```bash
nano .env
```

Ajoutez vos clés API :

```env
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
ASSEMBLYAI_API_KEY=your-assemblyai-key-here
```

### 3. Lancer le service

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Le service est maintenant disponible sur **http://localhost:8000**

## 🧪 Test rapide

### Vérifier la santé du service

```bash
curl http://localhost:8000/health
```

### Générer un script simple

```bash
curl -X POST "http://localhost:8000/scripts/test-1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quick Python Tip",
    "description": "Learn Python list comprehension in 30 seconds",
    "use_case": "youtube_short",
    "language": "en",
    "style": "casual"
  }'
```

## 📖 Documentation complète

Consultez **README.md** pour plus d'exemples et la documentation complète.
