import pytest
from backend.db_setup import KeyValue, KeyValueRevision

def test_insert_key_value(kv_store):
    """Test inserting a key-value pair."""
    response = kv_store.insert("test.key", {"value": "test_value"})
    assert response["status"] == "success"
    assert "inserted successfully" in response["message"]

    # Verify the key-value pair exists in the database
    entry = kv_store.session.query(KeyValue).filter(KeyValue.key == "test.key").first()
    assert entry is not None
    assert entry.value == {"value": "test_value"}

def test_insert_duplicate_key(kv_store):
    """Test inserting a duplicate key."""
    response = kv_store.insert("test.key", {"value": "test_value"})
    assert response["status"] == "error"
    assert "already exists" in response["message"]

def test_update_key_value(kv_store):
    """Test updating a key-value pair and managing revisions."""
    response = kv_store.update("test.key", {"value": "new_value"})
    assert response["status"] == "success"
    assert "updated successfully" in response["message"]

    # Verify the current value
    entry = kv_store.session.query(KeyValue).filter(KeyValue.key == "test.key").first()
    assert entry.value == {"value": "new_value"}

    # Verify the revision is recorded
    revisions = kv_store.session.query(KeyValueRevision).filter(KeyValueRevision.key_value_id == entry.id).all()
    assert len(revisions) == 1
    assert revisions[0].value == {"value": "test_value"}
    assert revisions[0].revision_number == 1

def test_get_key_value(kv_store):
    """Test retrieving a key-value pair."""
    response = kv_store.get("test.key")
    assert response["status"] == "success"
    assert response["data"]["key"] == "test.key"
    assert response["data"]["value"] == {"value": "new_value"}

def test_delete_key_value(kv_store):
    """Test deleting a key-value pair."""
    # Delete the key-value pair
    response = kv_store.delete("test.key")
    assert response["status"] == "success"
    assert "deleted successfully" in response["message"]

    # Ensure the key no longer exists
    response = kv_store.get("test.key")
    assert response["status"] == "error"
    assert "does not exist" in response["message"]

    # Ensure revisions are also deleted
    entry = kv_store.session.query(KeyValue).filter(KeyValue.key == "test.key").first()
    assert entry is None  # Main entry should no longer exist

    revisions = kv_store.session.query(KeyValueRevision).all()
    assert len(revisions) == 0  # All revisions should be removed

def test_revision_tracking(kv_store):
    """Test that revisions are correctly managed."""
    # Insert and update multiple times
    kv_store.insert("revision.key", {"value": "v1"})
    kv_store.update("revision.key", {"value": "v2"})
    kv_store.update("revision.key", {"value": "v3"})
    kv_store.update("revision.key", {"value": "v4"})

    # Verify the current value
    entry = kv_store.session.query(KeyValue).filter(KeyValue.key == "revision.key").first()
    assert entry.value == {"value": "v4"}

    # Verify the revision history
    revisions = kv_store.session.query(KeyValueRevision).filter(KeyValueRevision.key_value_id == entry.id).order_by(KeyValueRevision.revision_number).all()
    assert len(revisions) == 3
    assert revisions[0].value == {"value": "v1"}
    assert revisions[0].revision_number == 1
    assert revisions[1].value == {"value": "v2"}
    assert revisions[1].revision_number == 2
    assert revisions[2].value == {"value": "v3"}
    assert revisions[2].revision_number == 3
