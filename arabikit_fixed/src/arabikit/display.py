"""
إصلاح عرض النص العربي في البيئات التي لا تدعم العربية بشكل صحيح
(مثل matplotlib، بعض مكتبات PDF، أو واجهات رسومية قديمة).

يجمع هذا الملف بين arabic_reshaper (لربط الحروف بأشكالها الصحيحة)
و python-bidi (لترتيب اتجاه النص من اليمين لليسار) بدالة واحدة بسيطة.

هذه الاعتماديات اختيارية: ثبّتها عبر `pip install arabikit[display]`.
استخدام normalize_text وحدها لا يحتاج تثبيت أي شيء إضافي.
"""
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _HAS_DISPLAY_DEPS = True
except ImportError:
    _HAS_DISPLAY_DEPS = False


def _require_display_deps():
    if not _HAS_DISPLAY_DEPS:
        raise ImportError(
            "هذه الميزة تحتاج arabic-reshaper و python-bidi. "
            "ثبّتهما عبر: pip install arabikit[display]"
        )


def fix_arabic_display(text: str) -> str:
    """يحوّل نصًا عربيًا عاديًا إلى نص جاهز للعرض الصحيح في بيئات لا تدعم
    تشكيل الحروف العربية أو اتجاه RTL تلقائيًا (مثل matplotlib أو PIL).

    مثال:
        >>> fix_arabic_display("مرحبا بالعالم")
        # يعيد النص بترتيب واتصال حروف صحيح للعرض

    Raises:
        ImportError: إذا لم تكن arabic-reshaper و python-bidi مثبّتتين.
    """
    _require_display_deps()
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
