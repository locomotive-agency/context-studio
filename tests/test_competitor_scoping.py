from __future__ import annotations

from pathlib import Path

from context_system.okf import parse_document


ROOT = Path(__file__).resolve().parents[1] / "context_repo"

PRODUCT_SCOPE_BY_OVERLAP = {
    "APIs & MCP": "product-zoominfo-mcp",
    "Chorus": "product-chorus",
    "CRM Enrichment": "product-crm-enrichment",
    "Data": "product-data",
    "Data (Pillar 1)": "product-data",
    "Data as a Service": "product-data-as-a-service",
    "FormComplete": "product-form-optimization",
    "GTM Context Graph": "product-gtm-context-graph",
    "GTM Studio": "product-gtm-studio",
    "GTM Workspace": "product-gtm-workspace",
    "Intent Data": "product-intent-data",
    "WebSights": "product-identify-website-visitors",
    "ZoomInfo Chat": "product-chat",
    "ZoomInfo Marketing": "product-marketing",
    "ZoomInfo Operations": "product-operations",
    "ZoomInfo Sales": "product-sales",
}


def _frontmatter(path: Path) -> dict:
    return parse_document(path.read_text(encoding="utf-8")).frontmatter


def test_competitor_sub_products_use_product_scope_when_overlap_maps_cleanly():
    mismatches = []
    for path in sorted((ROOT / "competitors" / "sub-products").glob("*.md")):
        if path.name == "index.md":
            continue
        frontmatter = _frontmatter(path)
        expected = PRODUCT_SCOPE_BY_OVERLAP.get(frontmatter.get("zi_overlap_product"))
        if expected and frontmatter.get("scope_id") != expected:
            mismatches.append((path.name, frontmatter.get("zi_overlap_product"), frontmatter.get("scope_id"), expected))

    assert mismatches == []


def test_competitor_crossovers_use_product_scope_when_product_maps_cleanly():
    mismatches = []
    for path in sorted((ROOT / "competitors" / "crossovers").glob("*.md")):
        if path.name == "index.md":
            continue
        frontmatter = _frontmatter(path)
        expected = PRODUCT_SCOPE_BY_OVERLAP.get(frontmatter.get("zi_product"))
        if expected and frontmatter.get("scope_id") != expected:
            mismatches.append((path.name, frontmatter.get("zi_product"), frontmatter.get("scope_id"), expected))

    assert mismatches == []


def test_competitor_brands_and_categories_remain_broad():
    for folder in ["brands", "categories"]:
        scopes = {_frontmatter(path).get("scope_id") for path in (ROOT / "competitors" / folder).glob("*.md")}
        assert scopes == {"zoominfo"}


def test_competitor_progressive_disclosure_indexes_exist():
    for path in [
        ROOT / "competitors" / "index.md",
        ROOT / "competitors" / "sub-products" / "index.md",
        ROOT / "competitors" / "crossovers" / "index.md",
    ]:
        assert path.is_file()
