"""
arabikit
========
مكتبة شاملة لمعالجة النصوص العربية بلغة بايثون.

الوحدات الرئيسية:
- normalize: تطبيع النصوص (إزالة تشكيل، توحيد همزات، توحيد ألف مقصورة، إزالة تطويل)
  — لا تحتاج أي اعتماديات خارجية.
- display: إصلاح عرض النص العربي (reshaping + bidi) للاستخدام بواجهات لا تدعم
  العربية — تحتاج `pip install arabikit[display]`.
- charts: تكامل مباشر مع matplotlib لعرض تسميات عربية صحيحة بالرسوم البيانية
  — تحتاج `pip install arabikit[charts]`.
"""

from .normalize import (
    normalize_hamza,
    normalize_alef_maqsura,
    remove_tashkeel,
    remove_tatweel,
    normalize_text,
)

__version__ = "0.2.0"

__all__ = [
    "normalize_hamza",
    "normalize_alef_maqsura",
    "remove_tashkeel",
    "remove_tatweel",
    "normalize_text",
    "fix_arabic_display",
]


def __getattr__(name):
    # استيراد كسول: fix_arabic_display يعتمد على arabic-reshaper و python-bidi
    # (اعتماديات اختيارية)، لذا لا نستوردها إلا عند الحاجة الفعلية إليها.
    # هذا يسمح باستخدام normalize_text وحدها دون تثبيت أي شيء إضافي.
    if name == "fix_arabic_display":
        from .display import fix_arabic_display
        return fix_arabic_display
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
