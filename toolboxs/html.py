from bs4 import BeautifulSoup


class Html:
    @staticmethod
    def remove_html_tags(context: str, truncate: int = None) -> str:
        context = BeautifulSoup(context, "html.parser")
        for tag in context(["script", "style", "noscript", "iframe"]):
            tag.decompose()

        context = context.get_text(separator=" ", strip=True)

        if truncate:
            context = context[:truncate]

        return context
