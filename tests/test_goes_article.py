import importlib.util
import re
from pathlib import Path


def _builder():
    spec = importlib.util.spec_from_file_location('build_goes_article', Path('scripts/build_goes_article.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def test_article_and_methods_are_rendered_from_current_code():
    m = _builder()
    for path, text in m.render().items():
        assert path.read_text() == text, f'{path.name} is stale: run python scripts/build_goes_article.py'


def test_article_length_and_sources():
    text = Path('docs/article/americas-hidden-transformer-steel-dependence.md').read_text()
    words = len(text.split())
    assert 1300 <= words <= 1700, words
    assert '{' not in text and '}' not in text                 # no unfilled placeholders
    assert len(re.findall(r'\]\(https?://', text)) >= 15        # numbers carry links
    assert 'figures/goes_foreign_share.svg' in text             # the one chart
