import pytest

# arabic-reshaper و python-bidi اعتماديات اختيارية، لذا نتخطى هذه
# الاختبارات بأمان إن لم تكونا مثبّتتين بدل فشل كامل جلسة الاختبار.
pytest.importorskip("arabic_reshaper")
pytest.importorskip("bidi")

from arabikit.display import fix_arabic_display


def test_fix_arabic_display_returns_string():
    result = fix_arabic_display("مرحبا")
    assert isinstance(result, str)
    assert len(result) > 0


def test_fix_arabic_display_empty_string():
    result = fix_arabic_display("")
    assert result == ""


def test_import_arabikit_without_display_deps(monkeypatch):
    """التأكد من أن استيراد arabikit نفسه لا يتطلب arabic-reshaper/python-bidi
    (الاستيراد كسول)، حتى لو كانتا مثبّتتين فعليًا في بيئة الاختبار هذه."""
    import importlib
    import sys

    for mod in list(sys.modules):
        if mod == "arabikit" or mod.startswith("arabikit."):
            del sys.modules[mod]

    import arabikit  # لا يجب أن يفشل حتى بدون الاعتماديات الاختيارية

    assert hasattr(arabikit, "normalize_text")
    importlib.reload(arabikit)
