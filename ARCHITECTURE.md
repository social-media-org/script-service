# 🏗️ Architecture Améliorée - Script Generation Service

## 📂 Structure du Projet

```
app/
├── agents/                         # 🤖 Agents LLM spécialisés
│   ├── title_agent.py              # Génération de titres
│   ├── sections_agent.py           # Génération de sections (dynamique)
│   ├── description_agent.py        # Génération de descriptions
│   ├── keywords_agent.py           # Extraction de keywords
│   └── translation_agent.py        # Traduction des prompts
│
├── services/                       # 🔧 Services métier
│   ├── video_download_service.py   # Téléchargement vidéos (avec cache)
│   ├── transcription_service.py    # Transcription audio (avec cache)
│   └── script_orchestrator.py      # Orchestration du pipeline
│
├── llm/                           # 📝 Infrastructure LLM
│   ├── base_agent.py              # Classe de base des agents
│   └── prompts/                   # Templates de prompts
│       ├── title_prompt.txt
│       ├── description_prompt.txt
│       ├── keywords_prompt.txt
│       ├── sections_prompt_single.txt      # Pour 1 section
│       └── sections_prompt_multiple.txt    # Pour N sections
│
├── core/                          # ⚙️ Configuration
│   ├── config.py                  # Settings (avec VIDEOS_STORAGE_PATH)
│   ├── llm_client.py              # Client DeepSeek
│   └── utils.py                   # Fonctions utilitaires
│
├── models/                        # 📦 Modèles Pydantic
│   └── script.py
│
└── routes/                        # 🌐 API REST
    └── scripts.py
```

## 🚀 Améliorations Implémentées

### 1. Séparation Agents / Services ✅

**Avant:** Tout dans `/services/`

**Maintenant:**
- `/agents/` - Agents LLM purs (TitleAgent, SectionsAgent, etc.)
- `/services/` - Services métier (téléchargement, transcription, orchestration)

**Avantage:** Séparation claire des responsabilités

---

### 2. Service de Téléchargement Vidéo (avec Cache) ✅

**Fichier:** `services/video_download_service.py`

**Fonctionnalités:**
```python
# Téléchargement avec vérification de cache
audio_path = await video_service.download_youtube_audio(url, project_title)
# → resources/videos/{slug-title}/video-inspiration/{video_id}.mp3
```

**Cache intelligent:**
- ✅ Vérifie si le fichier existe avant de télécharger
- ✅ Slugification du titre pour noms de dossiers sûrs
- ✅ Organisation par projet
- ✅ Path configurable via `VIDEOS_STORAGE_PATH`

**Exemple de structure:**
```
resources/videos/
├── quick-python-tip/
│   └── video-inspiration/
│       ├── dQw4w9WgXcQ.mp3    # YouTube video
│       └── abc123xyz.mp3
└── python-tutorial-series/
    └── video-inspiration/
        └── xyz789abc.mp3
```

---

### 3. Service de Transcription (avec Cache) ✅

**Fichier:** `services/transcription_service.py`

**Fonctionnalités:**
```python
# Transcription avec vérification de cache
text = await transcription_service.transcribe_video_url(url, project_title)
# → resources/videos/{slug-title}/video-inspiration/{video_id}.txt
```

**Cache intelligent:**
- ✅ Vérifie si la transcription existe avant d'appeler AssemblyAI
- ✅ Sauvegarde automatique après transcription
- ✅ Réutilisation instantanée si déjà transcrit
- ✅ Économie de coûts API

**Pipeline complet:**
1. Vérifier cache transcription → Si existe, retourner
2. Télécharger audio (avec cache)
3. Transcrire avec AssemblyAI
4. Sauvegarder transcription dans cache
5. Retourner texte

---

### 4. Génération Dynamique des Sections ✅

**Fichier:** `agents/sections_agent.py`

**Amélioration:** Prompts construits dynamiquement selon `nb_section`

**Avant:**
```
Prompt unique avec conditions:
- If nb_section = 1: ...
- If nb_section > 1: ...
```

**Maintenant:**
```python
if nb_section == 1:
    # Utiliser sections_prompt_single.txt
    prompt = "Create a complete script as ONE continuous text..."
else:
    # Utiliser sections_prompt_multiple.txt
    prompt = f"Create EXACTLY {nb_section} distinct sections..."
```

**Avantages:**
- ✅ Instructions claires et spécifiques au LLM
- ✅ Pas de logique conditionnelle dans le prompt
- ✅ Meilleure qualité de génération
- ✅ Code plus maintenable

**Prompts séparés:**
- `sections_prompt_single.txt` - Pour script continu
- `sections_prompt_multiple.txt` - Pour sections multiples

---

### 5. Traduction des Prompts ✅

**Fichier:** `agents/translation_agent.py`

**Principe:** Prompts écrits en anglais → Traduits dans la langue cible avant l'appel LLM

**Pipeline:**
1. Écrire prompt en anglais (langue par défaut)
2. Avant d'appeler LLM, traduire le prompt dans `language`
3. LLM reçoit le prompt dans sa langue de réponse

**Exemple:**
```python
# Prompt original (anglais)
prompt_en = "Generate a catchy video title about Python..."

# Si language = "fr"
translation_agent.translate_prompt(prompt_en, "fr")
# → "Générez un titre accrocheur pour une vidéo sur Python..."

# LLM reçoit le prompt français → répond en français
```

**Avantages:**
- ✅ Meilleure qualité de réponse (LLM comprend mieux dans la langue cible)
- ✅ Cohérence linguistique
- ✅ Prompts maintenus en anglais (standard)
- ✅ Support multi-langues automatique

**Intégration dans BaseAgent:**
```python
async def generate(self, language: str = "en", **kwargs):
    prompt = self._format_prompt(**kwargs)
    
    # Traduction automatique si besoin
    if self.translate_prompt and language != "en":
        translation_agent = get_translation_agent()
        prompt = await translation_agent.translate_prompt(prompt, language)
    
    # Appel LLM...
```

---

## 🔄 Flux de Données Complet

```
┌─────────────────────────────────────────────────────────────┐
│            POST /api/v1/scripts/{project_id}                │
│            ScriptGenerationRequest                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATEUR                               │
└────────────────────────┬────────────────────────────────────┘
                         │
    ┌────────────────────┴────────────────────┐
    │                                         │
    ▼                                         ▼
┌──────────────────┐                  ┌─────────────────┐
│ VideoDownload    │                  │ Transcription   │
│ Service          │──────audio──────→│ Service         │
│                  │                  │                 │
│ • Cache check    │                  │ • Cache check   │
│ • PyTubeFix      │                  │ • AssemblyAI    │
│ • Save .mp3      │                  │ • Save .txt     │
└──────────────────┘                  └─────────────────┘
                                              │
                                              │ transcriptions
                                              ▼
                                      ┌──────────────────┐
                                      │ SectionsAgent    │
                                      │ • Dynamic prompt │
                                      │ • Translation    │
                                      └──────────────────┘
                                              │
                                              │
            ┌─────────────────────────────────┴───────────────┐
            │                                                 │
            ▼                                                 ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │ TitleAgent   │    │ Keywords     │    │ Description  │
    │ • Translate  │    │ Agent        │    │ Agent        │
    └──────────────┘    └──────────────┘    └──────────────┘
            │                   │                     │
            └───────────────────┴─────────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ ScriptGeneration       │
                    │ Response (JSON)        │
                    └────────────────────────┘
```

---

## 💾 Système de Cache

### Structure de Cache
```
resources/videos/
└── {slugified-project-title}/
    └── video-inspiration/
        ├── {video_id}.mp3      # Audio téléchargé
        └── {video_id}.txt      # Transcription
```

### Avantages
- ⚡ Pas de re-téléchargement si audio existe
- ⚡ Pas de re-transcription si texte existe
- 💰 Économie de coûts API (AssemblyAI)
- 🚀 Génération ultra-rapide en cas de cache hit

### Configuration
```env
VIDEOS_STORAGE_PATH=resources/videos  # Modifiable
```

---

## 🌐 Support Multi-langues

### Langues Supportées
- `en` - English
- `fr` - Français
- `es` - Español
- `de` - Deutsch
- `it` - Italiano
- `pt` - Português

### Pipeline de Traduction
1. Prompts écrits en anglais (base)
2. TranslationAgent traduit si `language != "en"`
3. LLM reçoit prompt traduit
4. Réponse dans la langue cible

---

## 🎯 Agents Spécialisés

| Agent | Traduction | Température | Max Tokens |
|-------|-----------|-------------|------------|
| **TranslationAgent** | N/A | 0.3 | 2000 |
| **TitleAgent** | ✅ | 0.8 | 100 |
| **SectionsAgent** | ✅ | 0.7 | 2000 |
| **DescriptionAgent** | ✅ | 0.7 | 500 |
| **KeywordsAgent** | ❌ | 0.6 | 200 |

---

## 🔧 Configuration Requise

### Variables d'Environnement
```env
# LLM
DEEPSEEK_API_KEY=sk-xxx
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# Transcription
ASSEMBLYAI_API_KEY=xxx

# Storage (nouveau!)
VIDEOS_STORAGE_PATH=resources/videos
```

### Dépendances Ajoutées
```
python-slugify==8.0.4  # Pour slugification des titres
```

---

## 📊 Comparaison Avant/Après

| Aspect | Avant | Après |
|--------|-------|-------|
| **Structure** | Agents mélangés avec services | Agents et services séparés |
| **Téléchargement** | À chaque fois | Cache intelligent |
| **Transcription** | À chaque fois | Cache intelligent |
| **Prompts sections** | Conditions dans prompt | Construction dynamique |
| **Multi-langues** | Prompts statiques | Traduction dynamique |
| **Coûts API** | Élevés (répétitions) | Optimisés (cache) |
| **Performance** | Lente | Rapide (cache hits) |

---

**Dernière mise à jour:** Novembre 2024
