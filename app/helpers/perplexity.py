
import requests

# 🔑 Remplace par ta clé API Perplexity
API_KEY = ""

# Sujet de recherche
topic = "Assurance auto au Canada 2025"

# 1️⃣ Étape 1 : Recherche en ligne avec le modèle online
search_payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": f"Trouve les 10 sources les plus pertinentes sur le sujet suivant : {topic}. Liste les titres et URLs."
        }
    ]
}

response_search = requests.post(
    "https://api.perplexity.ai/chat/completions",
    json=search_payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

search_result = response_search.json()
print(search_result)

sources_text = search_result["choices"][0]["message"]["content"]

print("🔍 Sources trouvées :")
print(sources_text)


# 2️⃣ Étape 2 : Génération d'un article SEO basé sur ces sources
article_payload = {
    "model": "sonar-pro",
    "messages": [
        {
            "role": "user",
            "content": (
                f"En te basant sur les sources suivantes :\n{sources_text}\n\n"
                f"Rédige un article SEO d'environ 1200 mots sur le sujet : {topic}. "
                "Le texte doit être structuré, avec des sous-titres, et prêt pour le web. Important! Comporter comme un vrai redacteur. L'article doit etre pro et agreable  à lire. Donne au lecteur l'impression qu'un vrai humain a ecrit l'article. Evite des phrase du genre : selon une des sources .... Tu peux plutot dire : selon l'observatoire canadien de la lune ..."
            )
        }
    ]
}

response_article = requests.post(
    "https://api.perplexity.ai/chat/completions",
    json=article_payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

article_text = response_article.json()["choices"][0]["message"]["content"]

print("\n📝 Article généré :")
print(article_text + "...")  # Affiche seulement les 2000 premiers caractères pour aperçu
