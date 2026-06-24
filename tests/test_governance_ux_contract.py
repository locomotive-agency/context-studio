from pathlib import Path


CMS_PAGE = Path(__file__).resolve().parents[1] / "cms" / "src" / "pages" / "index.astro"


def test_supporting_sources_fields_are_hidden_for_controlled_metadata() -> None:
    source = CMS_PAGE.read_text()

    assert 'title:"Supporting sources"' in source
    assert 'hideWhenCriticality:"controlled"' in source
    assert "visibleMetadataGroups" in source
    assert "effectiveCriticality" in source


def test_controlled_metadata_prunes_supporting_sources_before_save() -> None:
    source = CMS_PAGE.read_text()

    assert "function pruneControlledSupportingSources" in source
    assert "pruneControlledSupportingSources(prefix, target);" in source
