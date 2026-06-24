from pathlib import Path


CMS_SRC = Path(__file__).resolve().parents[1] / "cms" / "src"
CMS_PAGE = CMS_SRC / "pages" / "index.astro"
CMS_STYLES = CMS_SRC / "styles" / "context-studio.css"


def _css_declarations(selector: str) -> list[str]:
    source = CMS_STYLES.read_text()
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


def test_context_studio_assets_are_extracted_from_page_shell() -> None:
    source = CMS_PAGE.read_text()

    assert 'import "../styles/context-studio.css";' in source
    assert '<script src="../scripts/context-studio.js"></script>' in source
    assert "<style>" not in source
    assert len(source.splitlines()) < 300
    assert CMS_STYLES.exists()
