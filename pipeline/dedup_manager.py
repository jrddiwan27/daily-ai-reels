import os
import json
import datetime

HISTORY_FILE = "history/published_history.json"

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error reading {HISTORY_FILE}: {e}")
    return []

def save_history(history: list):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def normalize_key(val: str) -> str:
    if not val:
        return ""
    # strip protocol, trailing slashes, spaces, lowercase
    v = val.lower().strip()
    v = v.replace("https://", "").replace("http://", "").rstrip("/")
    # if github.com/owner/name -> owner/name
    if "github.com/" in v:
        v = v.split("github.com/")[-1]
    return v

def is_duplicate(item_identifier: str, max_days: int = 60) -> bool:
    """
    Checks if item_identifier has been published within the last max_days.
    """
    history = load_history()
    target_key = normalize_key(item_identifier)
    if not target_key:
        return False
        
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=max_days)

    for entry in history:
        # Check publication timestamp
        pub_time_str = entry.get("timestamp_utc")
        if pub_time_str:
            try:
                pub_time = datetime.datetime.fromisoformat(pub_time_str)
                if pub_time < cutoff:
                    continue
            except Exception:
                pass
                
        # Check against entry's items
        for itm in entry.get("items", []):
            keys_to_check = [
                normalize_key(itm.get("id", "")),
                normalize_key(itm.get("name", "")),
                normalize_key(itm.get("url", "")),
                normalize_key(itm.get("full_name", ""))
            ]
            if target_key in keys_to_check:
                return True
                
    return False

def filter_non_duplicates(candidates: list, key_field: str = "full_name", max_days: int = 60) -> list:
    """
    Filters candidates list and returns only non-duplicate items.
    """
    fresh = []
    for c in candidates:
        ident = c.get(key_field) or c.get("name") or c.get("url") or str(c)
        if not is_duplicate(ident, max_days=max_days):
            fresh.append(c)
        else:
            print(f"[🛡️ DEDUP] Skipping duplicate item: {ident}")
    return fresh

def record_published(slot_id: int, slot_name: str, items: list, post_id: str = None):
    """
    Records a completed publication event in the persistent ledger.
    """
    history = load_history()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    ist_offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_ist = now_utc.astimezone(ist_offset)

    record = {
        "slot_id": slot_id,
        "slot_name": slot_name,
        "timestamp_utc": now_utc.isoformat(),
        "date_ist": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "buffer_post_id": post_id,
        "items": []
    }

    for itm in items:
        record["items"].append({
            "id": itm.get("id") or itm.get("full_name") or itm.get("name"),
            "name": itm.get("name"),
            "url": itm.get("url", ""),
            "title": itm.get("title") or itm.get("description", "")[:80]
        })

    history.append(record)
    save_history(history)
    print(f"[✓ DEDUP] Recorded {len(items)} published items to {HISTORY_FILE}")
