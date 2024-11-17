from .kv_store import KVStore

class ConfigStore:
    def __init__(self, kv_store: KVStore):
        self.kv_store = kv_store

    def set_config(self, key: str, value: dict):
        """Set a configuration in the config store."""
        return self.kv_store.update(key, value)

    def get_config(self, key: str):
        """Retrieve a configuration from the config store."""
        return self.kv_store.get(key)

    def delete_config(self, key: str):
        """Delete a configuration from the config store."""
        return self.kv_store.delete(key)
