from pathlib import Path


CMS_PAGE = Path(__file__).resolve().parents[1] / "cms" / "src" / "pages" / "index.astro"


def _css_declarations(selector: str) -> list[str]:
    source = CMS_PAGE.read_text()
    prefix = f"{selector} {{"
    declarations = []
    start = 0

    while True:
        rule_start = source.find(prefix, start)
        if rule_start == -1:
            return declarations

        body_start = rule_start + len(prefix)
        body_end = source.find("}", body_start)
        declarations.append(source[body_start:body_end])
        start = body_end + 1


def test_document_title_column_uses_available_header_space() -> None:
    rules = _css_declarations(".document-heading-main")

    assert rules
    assert any("flex: 1 1 auto" in rule for rule in rules)
