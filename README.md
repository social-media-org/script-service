# 🎬 Script Generation Microservice

Microservice FastAPI intelligent pour la génération automatique de scripts vidéo structurés avec des agents LLM spécialisés.

## ✨ Fonctionnalités

- ✅ **Génération de scripts vidéo** avec agents LLM spécialisés
- ✅ **Transcription vidéo** (YouTube/Facebook) via AssemblyAI
- ✅ **Agents multiples** : Titre, Sections, Description, Keywords
- ✅ **Régénération partielle** (métadonnées uniquement)
- ✅ **Support multi-langues** (en, fr, es, de, it, pt)
- ✅ **Styles variés** (educational, inspirational, comedic, etc.)
- ✅ **API DeepSeek** (compatible OpenAI)
- ✅ **Architecture propre** avec séparation des responsabilités

## 🏗️ Architecture

```
app/
├── main.py                    # Point d'entrée FastAPI
├── core/
│   ├── config.py              # Configuration (Settings)
│   ├── llm_client.py          # Client LLM (DeepSeek/OpenAI)
│   ├── utils.py               # Utilitaires
│   ├── logging.py             # Configuration logging
│   ├── database.py            # Database (non utilisé)
│   └── exceptions.py          # Exceptions personnalisées
├── routes/
│   └── scripts.py             # Endpoints /scripts
├── models/
│   └── script.py              # Modèles Pydantic
├── services/
│   ├── title_agent.py         # Agent génération titre
│   ├── sections_agent.py      # Agent génération sections
│   ├── description_agent.py   # Agent génération description
│   ├── keywords_agent.py      # Agent génération keywords
│   ├── transcription_service.py  # Service transcription
│   └── script_orchestrator.py # Orchestrateur principal
└── llm/
    ├── base_agent.py          # Classe de base pour agents
    └── prompts/
        ├── title_prompt.txt
        ├── sections_prompt.txt
        ├── description_prompt.txt
        └── keywords_prompt.txt
```

### Flux de données

```
Requête → Route /scripts/{project_id}
         ↓
    Orchestrator
         ↓
    ┌─────────────────────────┐
    │ 1. Transcription Service  │ → YouTube/Facebook
    │ 2. Sections Agent         │ → Script structuré
    │ 3. Title Agent            │ → Titre optimisé
    │ 4. Keywords Agent         │ → Mots-clés SEO
    │ 5. Description Agent      │ → Description vidéo
    └─────────────────────────┘
         ↓
    Response JSON
```

## 🛠️ Technologies

- **Python 3.11+**
- **FastAPI** - Framework web moderne
- **Uvicorn** - Serveur ASGI
- **Pydantic v2** - Validation de données
- **OpenAI SDK** - Client LLM (compatible DeepSeek)
- **AssemblyAI** - Transcription audio
- **PyTubeFix** - Téléchargement YouTube

## 📚 Modèles de données

### ScriptGenerationRequest

```python
{
  "title": str,                    # Titre du projet
  "description": str,              # Description/prompt
  "video_inspirations": [str],     # URLs vidéos (optionnel)
  "use_case": str,                 # storytelling | youtube_short | ...
  "language": str,                 # en | fr | es | de | it | pt
  "style": str,                    # educational | inspirational | ...
  "keywords": str,                 # Mots-clés (optionnel)
  "script_text": str,              # Script existant (optionnel)
  "regenerer_script": bool,        # Régénérer le script (default: true)
  "duration": int,                 # Durée en secondes (default: 30)
  "nb_section": int                # Nombre de sections (default: 1)
}
```

### ScriptGenerationResponse

```python
{
  "script_sections": [str],        # Sections (si nb_section > 1)
  "script_text": str,              # Script complet concaténé
  "status": str,                   # "script_generated"
  "keywords": str,                 # Mots-clés générés
  "video_description": str,        # Description vidéo
  "title": str                     # Titre généré
}
```

## 🚀 Installation

### 1. Prérequis

- Python 3.11+
- pip
- Clé API DeepSeek
- Clé API AssemblyAI

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le template
cp .env.example .env

# Éditer .env avec vos clés API
nano .env
```

**Configuration dans .env:**

```env
# Application
APP_NAME="Script Generation Service"
APP_PORT=8000

# LLM API Keys
DEEPSEEK_API_KEY=sk-your-deepseek-key-here
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# Transcription
ASSEMBLYAI_API_KEY=your-assemblyai-key-here

# Defaults
DEFAULT_DURATION=30
DEFAULT_NB_SECTIONS=1
```

### 4. Lancement

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur: **http://localhost:8000**

## 🔌 API Endpoints

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "script-generation",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Script Service Health

```http
GET /scripts/health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "llm": "available",
    "transcription": "available"
  },
  "config": {
    "default_duration": 30,
    "default_nb_sections": 1,
    "llm_model": "deepseek-chat"
  }
}
```

### 3. Générer un script complet

```http
POST /scripts/{project_id}
Content-Type: application/json

{
  "title": "Comment apprendre Python en 30 jours",
  "description": "Un guide complet pour les débutants qui veulent maîtriser Python",
  "use_case": "educational",
  "language": "fr",
  "style": "professional",
  "duration": 60,
  "nb_section": 3,
  "video_inspirations": [
    "https://www.youtube.com/watch?v=example1",
    "https://www.youtube.com/watch?v=example2"
  ]
}
```

**Response:**
```json
{
  "script_sections": [
    "Introduction: Bienvenue dans ce guide...",
    "Section 2: Les fondamentaux de Python...",
    "Conclusion: Vous avez maintenant..."
  ],
  "script_text": "Introduction: Bienvenue...\n\nSection 2: Les fondamentaux...\n\nConclusion: Vous avez...",
  "status": "script_generated",
  "keywords": "python, programmation, tutorial, débutant, apprentissage",
  "video_description": "Découvrez comment maîtriser Python en 30 jours...",
  "title": "Maîtrisez Python en 30 Jours - Guide Complet"
}
```

### 4. Régénérer uniquement les métadonnées

```http
POST /scripts/{project_id}
Content-Type: application/json

{
  "title": "Python Tutorial",
  "description": "Learn Python programming",
  "use_case": "educational",
  "language": "en",
  "style": "professional",
  "script_text": "Welcome to this Python tutorial. In this video...",
  "regenerer_script": false
}
```

**Response:**
```json
{
  "script_sections": null,
  "script_text": "Welcome to this Python tutorial. In this video...",
  "status": "script_generated",
  "keywords": "python, tutorial, programming, learn",
  "video_description": "Learn Python programming with this comprehensive tutorial...",
  "title": "Complete Python Programming Tutorial for Beginners"
}
```

## 🤖 Agents LLM

### 1. Title Agent
**But:** Générer un titre accrocheur et optimisé SEO

**Entrées:**
- description
- use_case
- style
- language

**Sortie:** Titre (40-60 caractères)

### 2. Sections Agent
**But:** Créer les sections structurées du script

**Entrées:**
- description
- video_inspirations (transcriptions)
- duration
- nb_section
- style
- language
- use_case

**Sortie:** Sections + script concaténé

### 3. Description Agent
**But:** Générer une description YouTube/TikTok optimisée

**Entrées:**
- script_text
- keywords
- language

**Sortie:** Description avec hashtags et CTA

### 4. Keywords Agent
**But:** Extraire des mots-clés SEO pertinents

**Entrées:**
- script_text
- description
- use_case

**Sortie:** Liste de mots-clés (8-12)

## 📄 Use Cases supportés

- `storytelling` - Narration d'histoires
- `youtube_short` - Contenu court pour YouTube Shorts
- `explanation` - Vidéos explicatives
- `commercial` - Publicités et promotions
- `inspirational` - Contenu motivationnel
- `educational` - Tutoriels et formations
- `tutorial` - Guides pas-à-pas

## 🎨 Styles supportés

- `educational` - Éducatif et informatif
- `inspirational` - Inspirant et motivant
- `comedic` - Humoristique
- `dramatic` - Dramatique et émotionnel
- `casual` - Décontracté et conversationnel
- `professional` - Professionnel et formel

## 🌍 Langues supportées

- `en` - Anglais
- `fr` - Français
- `es` - Espagnol
- `de` - Allemand
- `it` - Italien
- `pt` - Portugais

## 📝 Documentation interactive

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Configuration des API Keys

### DeepSeek (LLM)

1. Créez un compte sur [DeepSeek](https://platform.deepseek.com/)
2. Générez une clé API
3. Ajoutez-la dans `.env` comme `DEEPSEEK_API_KEY`

### AssemblyAI (Transcription)

1. Créez un compte sur [AssemblyAI](https://www.assemblyai.com/)
2. Générez une clé API
3. Ajoutez-la dans `.env` comme `ASSEMBLYAI_API_KEY`

## ⚠️ Limitations

- **YouTube**: Supporté via PyTubeFix
- **Facebook**: Téléchargement limité (restrictions de la plateforme)
- **Durée de transcription**: Dépend de la longueur de la vidéo
- **Coûts**: AssemblyAI et DeepSeek sont des services payants

## 🐞 Dépannage

### Erreur "LLM client not initialized"

→ Vérifiez que `DEEPSEEK_API_KEY` est correctement configuré dans `.env`

### Erreur "Transcription service not initialized"

→ Vérifiez que `ASSEMBLYAI_API_KEY` est correctement configuré dans `.env`

### YouTube download fails

→ Certaines vidéos peuvent être protégées. Essayez une autre vidéo.

### Facebook videos not working

→ Le téléchargement Facebook est limité. Utilisez YouTube pour l'instant.

## 📚 Exemples d'utilisation

### Exemple 1: Vidéo courte (30s)

```bash
curl -X POST "http://localhost:8000/scripts/proj123" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quick Python Tip",
    "description": "Learn list comprehension in 30 seconds",
    "use_case": "youtube_short",
    "language": "en",
    "style": "casual"
  }'
```

### Exemple 2: Tutoriel long avec inspirations

```bash
curl -X POST "http://localhost:8000/scripts/proj456" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete Django Course",
    "description": "Full Django web development tutorial",
    "use_case": "tutorial",
    "language": "en",
    "style": "educational",
    "duration": 300,
    "nb_section": 5,
    "video_inspirations": [
      "https://www.youtube.com/watch?v=example"
    ]
  }'
```

### Exemple 3: Régénération métadonnées uniquement

```bash
curl -X POST "http://localhost:8000/scripts/proj789" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Video",
    "description": "Existing video content",
    "use_case": "educational",
    "language": "fr",
    "style": "professional",
    "script_text": "Bonjour et bienvenue dans cette vidéo...",
    "regenerer_script": false
  }'
```

## 🛡️ Sécurité

- Ne commitez **JAMAIS** vos clés API dans Git
- Utilisez `.env` pour les secrets (déjà dans `.gitignore`)
- En production, utilisez des gestionnaires de secrets (AWS Secrets Manager, etc.)

## 📝 Licence

MIT License - Libre d'utilisation pour vos projets.

---

**Créé avec ❤️ pour des scripts vidéo de qualité professionnelle**
