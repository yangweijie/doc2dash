import os
import tempfile

from mock import patch

from doc2dash.parsers.base import _BaseParser


class TestParser(_BaseParser):
    pass


def test_toc_with_empty_db():
    p = TestParser('foo')
    toc = p.add_toc()
    toc.close()


def test_add_toc_single_entry(monkeypatch):
    entries = [
        ('foo', 'clm', 'bar.html#foo'),
        ('qux', 'cl', 'bar.html'),
    ]
    with tempfile.TemporaryDirectory() as td:
        monkeypatch.chdir(td)
        p = TestParser('foo')
        os.mkdir('foo')
        with open('foo/bar.html', 'w') as fp:
            fp.write('docs!')
        p.find_and_patch_entry = lambda x, y: True
        toc = p.add_toc()
        for e in entries:
            toc.send(e)
        toc.close()

        p.find_and_patch_entry = lambda x, y: False
        toc = p.add_toc()
        for e in entries:
            toc.send(e)
        with patch('builtins.print') as mock:
            toc.close()
            assert mock.call_count == 1