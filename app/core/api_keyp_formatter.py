class ApiKeyFormatter:
    @staticmethod
    def mask(key: str, start: int = 4, end: int = 4) -> str:
        """Return the API key with only the beginning and end visible."""
        if not key:
            return ""

        key = key.strip()

        # If the key is too short, return it unchanged
        if len(key) <= start + end:
            return key

        return f"{key[:start]}...{key[-end:]}"
