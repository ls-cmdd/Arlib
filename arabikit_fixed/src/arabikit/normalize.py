"""
أدوات تطبيع النصوص العربية.

هذه الوحدة لا تحتاج أي اعتماديات خارجية (pure Python).
"""
import re

# نطاق حركات التشكيل العربي (فتحة، ضمة، كسرة، سكون، شدة، تنوين... إلخ)
# يشمل أيضًا علامات U+0653–U+065F مثل المدّة والهمزة فوق/تحت الحرف.
_TASHKEEL_PATTERN = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")
_TATWEEL_PATTERN = re.compile(r"\u0640+")

# أشكال الهمزة المختلفة (على الألف والواو والياء) -> الشكل المجرّد المناسب
_HAMZA_MAP = {
    "أ": "ا",  # همزة على ألف
    "إ": "ا",  # همزة تحت ألف
    "آ": "ا",  # ألف مدّة
    "ؤ": "و",  # همزة على واو
    "ئ": "ي",  # همزة على ياء (بدون نقطتين تحتها في الشكل المطبّع)
}

# الألف المقصورة ليست همزة، لكنها تُوحَّد غالبًا مع الياء لتسهيل البحث والمطابقة
_ALEF_MAQSURA_MAP = {
    "ى": "ي",
}


def remove_tashkeel(text: str) -> str:
    """يزيل جميع علامات التشكيل من النص العربي.

    مثال:
        >>> remove_tashkeel("الْعَرَبِيَّة")
        'العربية'
    """
    return _TASHKEEL_PATTERN.sub("", text)


def remove_tatweel(text: str) -> str:
    """يزيل حرف التطويل (ـ) المستخدم لتمديد الحروف.

    مثال:
        >>> remove_tatweel("مرحبـــا")
        'مرحبا'
    """
    return _TATWEEL_PATTERN.sub("", text)


def normalize_hamza(text: str) -> str:
    """يوحّد أشكال الهمزة المختلفة (على الألف والواو والياء) إلى شكل واحد
    مجرّد، لتسهيل المطابقة والبحث. لا تغيّر هذه الدالة الألف المقصورة (ى)
    لأنها ليست همزة أصلًا — استخدم normalize_alef_maqsura لذلك.

    يحول: أ، إ، آ -> ا | ؤ -> و | ئ -> ي

    مثال:
        >>> normalize_hamza("إسلام أحمد")
        'اسلام احمد'
    """
    for src, dst in _HAMZA_MAP.items():
        text = text.replace(src, dst)
    return text


def normalize_alef_maqsura(text: str) -> str:
    """يوحّد الألف المقصورة (ى) مع الياء (ي).

    مفيدة للبحث والمطابقة النصية حيث تُكتب الكلمة أحيانًا بالشكلين.

    مثال:
        >>> normalize_alef_maqsura("إلى متى")
        'إلي متي'
    """
    for src, dst in _ALEF_MAQSURA_MAP.items():
        text = text.replace(src, dst)
    return text


def normalize_text(text: str, *, tashkeel: bool = True, tatweel: bool = True,
                    hamza: bool = True, alef_maqsura: bool = True) -> str:
    """يطبّق كل عمليات التطبيع دفعة واحدة، مع إمكانية تعطيل أي منها.

    مثال:
        >>> normalize_text("إلـــى الْأَمَامِ")
        'الي الامام'
    """
    if tashkeel:
        text = remove_tashkeel(text)
    if tatweel:
        text = remove_tatweel(text)
    if hamza:
        text = normalize_hamza(text)
    if alef_maqsura:
        text = normalize_alef_maqsura(text)
    return text
