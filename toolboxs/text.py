class Text:
    @staticmethod
    def remove_duplicate_words_from_string(context: str = " ") -> str:
        seen = set()
        result = []

        for word in context.split():
            key = word.lower()

            if key not in seen:
                seen.add(key)
                result.append(word)

        result = " ".join(result)

        return result
