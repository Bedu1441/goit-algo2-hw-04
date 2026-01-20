from trie import Trie

class Homework(Trie):
    def __init__(self):
        super().__init__()
        self._suffix_count = {}   # suffix -> count
        self._prefixes = set()    # all prefixes that exist
        self._words_total = 0     # total inserted words (unique/не unique залежить від put у Trie)

    def put(self, key, value=None):
        # базова валідація
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        super().put(key, value)

        # оновлення індексів для швидких запитів
        self._words_total += 1

        # prefixes: "a", "ap", "app", ...
        for i in range(1, len(key) + 1):
            self._prefixes.add(key[:i])

        # suffixes: "e", "le", "ple", ...
        for i in range(len(key)):
            suf = key[i:]
            self._suffix_count[suf] = self._suffix_count.get(suf, 0) + 1

        # порожній суфікс: кожне слово закінчується на ""
        self._suffix_count[""] = self._suffix_count.get("", 0) + 1

    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        # якщо pattern="" — це всі слова
        return int(self._suffix_count.get(pattern, 0))

    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")
        if prefix == "":
            return self._words_total > 0
        return prefix in self._prefixes

if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # suffix tests
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat
    assert trie.count_words_with_suffix("zzz") == 0

    # prefix tests
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True

    print("All tests passed ✅")

