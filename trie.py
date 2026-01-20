from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class TrieNode:
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    value: Any = None
    terminal: bool = False

class Trie:
    """
    Мінімальна реалізація Trie. Підтримує put(key, value), що використовують тести.
    """
    def __init__(self):
        self.root = TrieNode()

    def put(self, key: str, value: Any = None) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if key == "":
            # дозволимо зберігати порожній рядок як слово (опційно)
            self.root.terminal = True
            self.root.value = value
            return

        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.terminal = True
        node.value = value

    def get(self, key: str) -> Optional[Any]:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        node = self.root
        for ch in key:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node.value if node.terminal else None
