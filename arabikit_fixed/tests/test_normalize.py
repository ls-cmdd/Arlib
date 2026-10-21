from arabikit.normalize import (
    remove_tashkeel,
    remove_tatweel,
    normalize_hamza,
    normalize_alef_maqsura,
    normalize_text,
)


def test_remove_tashkeel():
    assert remove_tashkeel("الْعَرَبِيَّة") == "العربية"


def test_remove_tashkeel_includes_additional_arabic_marks():
    marks = "".join(chr(codepoint) for codepoint in range(0x0653, 0x0660))
    assert remove_tashkeel("ب" + marks + "ت") == "بت"


def test_remove_tashkeel_empty_string():
    assert remove_tashkeel("") == ""


def test_remove_tatweel():
    assert remove_tatweel("مرحبـــا") == "مرحبا"


def test_normalize_hamza():
    assert normalize_hamza("إسلام أحمد") == "اسلام احمد"


def test_normalize_hamza_does_not_touch_alef_maqsura():
    # الألف المقصورة (ى) ليست همزة، ويجب ألا تتأثر بهذه الدالة
    assert normalize_hamza("إلى") == "الى"


def test_normalize_hamza_waw_and_ya_seats():
    assert normalize_hamza("سؤال") == "سوال"
    assert normalize_hamza("قارئ") == "قاري"


def test_normalize_alef_maqsura():
    assert normalize_alef_maqsura("إلى متى") == "إلي متي"


def test_normalize_text_all():
    result = normalize_text("إلـــى الْأَمَامِ")
    assert result == "الي الامام"
    assert "ـ" not in result
    assert "أ" not in result
    assert "إ" not in result
    assert "ى" not in result


def test_normalize_text_can_disable_alef_maqsura():
    result = normalize_text("إلى", alef_maqsura=False)
    assert result == "الى"


def test_normalize_text_can_disable_all_options():
    text = "إلـــى الْأَمَامِ"
    result = normalize_text(
        text, tashkeel=False, tatweel=False, hamza=False, alef_maqsura=False
    )
    assert result == text


def test_normalize_text_rejects_non_string():
    import pytest

    with pytest.raises(TypeError):
        normalize_text(None)
