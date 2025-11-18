from typing import Any, Dict, Iterable, Iterator, Optional

class FeatureMap:
    """A keyed map initialized from a set/list of keys, all values default to None.
    - update(key, value): only updates existing keys; raises if key doesn't exist
    - get(key): returns value if key exists; returns None if key doesn't exist
    - No additions/removals beyond initialization.
    """

    def __init__(self, keys: Iterable[str]) -> None:
        # Freeze the allowed key universe
        self._keys = frozenset(keys)
        # Backing store
        self._data: Dict[str, Any] = {k: None for k in self._keys}

    # ---- required API ----
    def update(self, key: str, value: Any) -> None:
        if key not in self._data:
            raise KeyError(f"Cannot add new key: '{key}'. Allowed keys: {sorted(self._keys)}")
        self._data[key] = value

    def get(self, key: str) -> Optional[Any]:
        # Must return None if key doesn't exist
        return self._data.get(key, None)

    def containsNone(self) -> bool:
        """Return True if any required feature is still None."""
        return any(v is None for v in self._data.values())

    # ---- read-only helpers (nice to have) ----
    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the underlying dict (read-only to callers)."""
        return dict(self._data)

    def keys(self) -> Iterator[str]:
        return iter(self._data.keys())

    def values(self) -> Iterator[Any]:
        return iter(self._data.values())

    def items(self) -> Iterator[tuple[str, Any]]:
        return iter(self._data.items())

    # ---- Python niceties for debugging/iteration ----
    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data})"
