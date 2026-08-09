# arabikit

مكتبة بايثون شاملة لمعالجة النصوص العربية: تطبيع، إصلاح عرض (reshaping + bidi)، وتكامل مباشر مع matplotlib للرسوم البيانية.

## لماذا arabikit؟

مطوّر بايثون الذي يتعامل مع نصوص عربية غالبًا يحتاج يجمع عدة مكتبات متفرقة
(`arabic_reshaper`، `python-bidi`، تطبيع يدوي) بدل مكتبة واحدة متكاملة وموثقة.
`arabikit` تجمع كل هذا بواجهة بسيطة.

## التثبيت

```bash
# التطبيع الأساسي فقط (لا اعتماديات إضافية على الإطلاق)
pip install arabikit

# مع دعم إصلاح عرض النص (reshaping + bidi)
pip install arabikit[display]

# مع دعم الرسوم البيانية (matplotlib + reshaping + bidi)
pip install arabikit[charts]
```

## الاستخدام

### تطبيع النصوص

```python
from arabikit import normalize_text

normalize_text("إلـــى الْأَمَامِ")
# 'الي الامام'

# تعطيل خيار معيّن، مثلًا الإبقاء على الألف المقصورة كما هي:
normalize_text("إلى", alef_maqsura=False)
# 'الى'
```

الدوال المتاحة: `remove_tashkeel`، `remove_tatweel`، `normalize_hamza`
(توحيد أشكال الهمزة فقط: أ إ آ ؤ ئ)، `normalize_alef_maqsura`
(توحيد ى مع ي بشكل منفصل عن الهمزة)، و `normalize_text` التي تجمعها كلها.

### إصلاح عرض النص (لبيئات لا تدعم العربية)

يحتاج `pip install arabikit[display]`.

```python
from arabikit import fix_arabic_display

fix_arabic_display("مرحبا بالعالم")
```

### تكامل مع matplotlib

يحتاج `pip install arabikit[charts]`.

```python
import matplotlib.pyplot as plt
from arabikit.charts import fix_axis_labels

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
fix_axis_labels(ax, xlabel="الأشهر", ylabel="المبيعات", title="تقرير المبيعات")
plt.show()
```

### سطر الأوامر

```bash
arabikit clean input.txt -o output.txt
arabikit clean input.txt --no-tashkeel
arabikit clean input.txt --no-alef-maqsura
arabikit --version
```

## ملاحظة حول الاعتماديات

`normalize_text` وبقية دوال `arabikit.normalize` لا تحتاج أي مكتبة خارجية.
أما `fix_arabic_display` (ووحدة `charts`) فتُستورد بشكل كسول ولا تحتاج
`arabic-reshaper`/`python-bidi`/`matplotlib` إلا عند استدعائها فعليًا.

## الاختبارات

```bash
pip install -e ".[dev,charts]"
pytest
```

## الترخيص

MIT
