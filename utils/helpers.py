def is_valid_article(article_status_code: int, article_text: str) -> bool:
    if article_status_code == 200:
        return len(article_text) > 270
