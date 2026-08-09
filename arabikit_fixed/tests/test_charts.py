import pytest

pytest.importorskip("matplotlib")
pytest.importorskip("arabic_reshaper")
pytest.importorskip("bidi")

import matplotlib
matplotlib.use("Agg")  # لا حاجة لواجهة رسومية أثناء الاختبار
import matplotlib.pyplot as plt

from arabikit.charts import arabic_label, fix_axis_labels, fix_tick_labels


def test_arabic_label_returns_string():
    result = arabic_label("المبيعات")
    assert isinstance(result, str)
    assert len(result) > 0


def test_fix_axis_labels_sets_title_and_axis_labels():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    fix_axis_labels(ax, xlabel="الأشهر", ylabel="المبيعات", title="تقرير المبيعات")

    assert ax.get_title() != ""
    assert ax.get_xlabel() != ""
    assert ax.get_ylabel() != ""
    plt.close(fig)


def test_fix_axis_labels_with_no_arguments_is_noop():
    fig, ax = plt.subplots()
    fix_axis_labels(ax)
    assert ax.get_title() == ""
    plt.close(fig)


def test_fix_tick_labels_x_axis():
    fig, ax = plt.subplots()
    ax.bar(["يناير", "فبراير", "مارس"], [10, 20, 15])
    fix_tick_labels(ax, axis="x")

    labels = [item.get_text() for item in ax.get_xticklabels()]
    assert len(labels) == 3
    assert all(isinstance(label, str) for label in labels)
    plt.close(fig)


def test_fix_tick_labels_invalid_axis_raises():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        fix_tick_labels(ax, axis="z")
    plt.close(fig)
