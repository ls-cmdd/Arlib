"""
تكامل مباشر مع matplotlib لحل مشكلة النص العربي المعكوس/المفكك بالرسوم البيانية.

هذا الملف اختياري ويحتاج تثبيت matplotlib و arabic-reshaper و python-bidi:
    pip install arabikit[charts]
"""
from .display import fix_arabic_display, _HAS_DISPLAY_DEPS

try:
    import matplotlib.pyplot as plt  # noqa: F401  (يُستخدم من قبل المستخدم، وليس هنا مباشرة)
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


def _require_chart_deps():
    missing = []
    if not _HAS_MPL:
        missing.append("matplotlib")
    if not _HAS_DISPLAY_DEPS:
        missing.append("arabic-reshaper/python-bidi")
    if missing:
        raise ImportError(
            f"هذه الميزة تحتاج: {', '.join(missing)}. "
            "ثبّتها عبر: pip install arabikit[charts]"
        )


def arabic_label(text: str) -> str:
    """يحوّل تسمية عربية واحدة (عنوان، محور، خانة) إلى نص جاهز للعرض بالرسم البياني.

    مثال:
        >>> plt.title(arabic_label("المبيعات الشهرية"))
    """
    _require_chart_deps()
    return fix_arabic_display(text)


def fix_axis_labels(ax, xlabel: str = None, ylabel: str = None, title: str = None):
    """يصلح دفعة واحدة عنوان الرسم وتسميات المحورين إن وُجدت.

    مثال:
        fig, ax = plt.subplots()
        fix_axis_labels(ax, xlabel="الأشهر", ylabel="المبيعات", title="تقرير المبيعات")
    """
    _require_chart_deps()
    if title:
        ax.set_title(arabic_label(title))
    if xlabel:
        ax.set_xlabel(arabic_label(xlabel))
    if ylabel:
        ax.set_ylabel(arabic_label(ylabel))
    return ax


def fix_tick_labels(ax, axis: str = "x"):
    """يصلح تسميات محور معيّن (مثل أسماء الفئات على المحور السيني) لتظهر بشكل صحيح.

    axis: 'x' أو 'y'
    """
    _require_chart_deps()
    if axis == "x":
        labels = [item.get_text() for item in ax.get_xticklabels()]
        # نثبّت مواضع الأعمدة (FixedLocator) قبل ضبط النصوص لتفادي
        # تحذير matplotlib: "FixedFormatter should only be used together
        # with FixedLocator"، ولضمان تطابق كل تسمية مع موضعها الصحيح.
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels([arabic_label(t) for t in labels])
    elif axis == "y":
        labels = [item.get_text() for item in ax.get_yticklabels()]
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels([arabic_label(t) for t in labels])
    else:
        raise ValueError("axis يجب أن تكون 'x' أو 'y'")
    return ax
