from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .db_setup import KeyValue, KeyValueRevision

class KVStore:
    def __init__(self, session: Session):
        self.session = session

    def insert(self, key: str, value: dict):
        """Insert a new key-value pair."""
        try:
            entry = KeyValue(key=key, value=value)
            self.session.add(entry)
            self.session.commit()
            return {"status": "success", "message": f"Key '{key}' inserted successfully."}
        except IntegrityError:
            self.session.rollback()
            return {"status": "error", "message": f"Key '{key}' already exists."}

    def update(self, key: str, value: dict):
        """Update an existing key-value pair and track revisions."""
        entry = self.session.query(KeyValue).filter(KeyValue.key == key).first()
        if not entry:
            return {"status": "error", "message": f"Key '{key}' does not exist."}

        # Create a new revision
        revision_number = (
            self.session.query(KeyValueRevision)
            .filter(KeyValueRevision.key_value_id == entry.id)
            .count() + 1
        )
        revision = KeyValueRevision(
            key_value_id=entry.id, revision_number=revision_number, value=entry.value
        )
        self.session.add(revision)

        # Update the current value
        entry.value = value
        self.session.commit()
        return {"status": "success", "message": f"Key '{key}' updated successfully."}

    def get(self, key: str):
        """Retrieve the value for a given key."""
        entry = self.session.query(KeyValue).filter(KeyValue.key == key).first()
        if not entry:
            return {"status": "error", "message": f"Key '{key}' does not exist."}
        return {"status": "success", "data": {"key": entry.key, "value": entry.value}}

    def get_revisions(self, key: str):
        """Retrieve all revisions for a given key."""
        entry = self.session.query(KeyValue).filter(KeyValue.key == key).first()
        if not entry:
            return {"status": "error", "message": f"Key '{key}' does not exist."}

        revisions = (
            self.session.query(KeyValueRevision)
            .filter(KeyValueRevision.key_value_id == entry.id)
            .order_by(KeyValueRevision.revision_number)
            .all()
        )
        return {
            "status": "success",
            "data": [
                {"revision_number": rev.revision_number, "value": rev.value, "created_at": rev.created_at}
                for rev in revisions
            ],
        }

    def delete(self, key: str):
        """Delete a key-value pair."""
        entry = self.session.query(KeyValue).filter(KeyValue.key == key).first()
        if not entry:
            return {"status": "error", "message": f"Key '{key}' does not exist."}
        
        # Delete associated revisions
        self.session.query(KeyValueRevision).filter(KeyValueRevision.key_value_id == entry.id).delete()

        # Delete the main entry
        self.session.delete(entry)
        self.session.commit()
        return {"status": "success", "message": f"Key '{key}' deleted successfully."}
