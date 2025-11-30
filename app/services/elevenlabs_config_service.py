"""
Service pour gérer la configuration et les statistiques ElevenLabs
"""

import json
from typing import Dict
import os
import traceback


class ElevenLabsConfigService:
    """
    Service pour gérer la configuration ElevenLabs et les statistiques
    """
    
    def __init__(self):
        pass
    
    async def get_keys_details(self) -> Dict:
        """
        Récupérer les détails de toutes les clés ElevenLabs configurées
        
        Returns:
            dict: Détails des clés ElevenLabs
        """
        try:
            from elevenlabs import ElevenLabs
            
            keys_details = []
            
            for i in range(1, 6):
                key = os.getenv(f"ELEVENLABS_API_KEY{i}")
                if key and key.startswith("sk_"):
                    try:
                        # Initialiser le client ElevenLabs
                        client = ElevenLabs(api_key=key)
                        
                        # Récupérer les infos du compte
                        user_info = client.user.get()
                        subscription = user_info.subscription
                        
                        keys_details.append({
                            "key_number": i,
                            "key": f"{key[:8]}...{key[-4:]}",  # Masquer la clé
                            "full_key": key,  # Pour usage interne seulement
                            "email": getattr(user_info, 'email', 'N/A'),
                            "first_name": getattr(user_info, 'first_name', 'N/A'),                
                            "character_count": subscription.character_count,
                            "character_limit": subscription.character_limit,
                            "characters_remaining": subscription.character_limit - subscription.character_count,
                            "tier": subscription.tier,
                            "status": subscription.status,
                            "next_character_count_reset_unix": subscription.next_character_count_reset_unix,
                        })
                    except Exception as e:
                        keys_details.append({
                            "key_number": i,
                            "key": f"{key[:8]}...{key[-4:]}",
                            "error": str(e),
                            "status": "error"
                        })
            
            return {
                "keys": keys_details,
                "total_keys": len(keys_details)
            }
            
        except Exception as e:
            print(f"❌ Error fetching ElevenLabs keys details: {str(e)}")
            traceback.print_exc()
            raise
        
if __name__ == "__main__":
    import asyncio
    import json
    
    async def main():
        service = ElevenLabsConfigService()
        config = await service.get_keys_details()
        print(json.dumps(config, indent=2, ensure_ascii=False))
    
    asyncio.run(main())
