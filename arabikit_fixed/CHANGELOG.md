# سجل التغييرات

## 0.2.0

### إصلاحات
- **اعتماديات إجبارية غير ضرورية**: كان `import arabikit` يفشل بدون تثبيت
  `arabic-reshaper` و `python-bidi` حتى لو كنت تستخدم `normalize_text` فقط.
  أصبح `fix_arabic_display` يُستورد بشكل كسول (lazy import عبر `__getattr__`
  في `__init__.py`)، وأصبحت الاعتماديتان اختياريتين ضمن `arabikit[display]`.
- **`fix_tick_labels` في charts.py**: كانت تستدعي `set_xticklabels` دون تثبيت
  المواضع (`set_xticks`) أولًا، ما يسبب تحذير matplotlib
  (`FixedFormatter should only be used together with FixedLocator`) وقد يؤدي
  لعدم تطابق التسميات مع مواضعها. تم إصلاحها.
- **CLI بدون معالجة أخطاء**: أصبح `arabikit clean` يعرض رسالة خطأ عربية
  واضحة (بدل traceback كاملة) عند عدم وجود الملف، أو عدم صلاحية القراءة/الكتابة،
  أو فشل ترميز UTF-8.

### تحسينات
- فصل `normalize_hamza` عن الألف المقصورة: أصبحت دالة جديدة
  `normalize_alef_maqsura` مسؤولة عن توحيد (ى -> ي) بشكل مستقل ومُسمّى بدقة،
  بدل تضمينها ضمن دالة "الهمزة" رغم أنها ليست همزة.
- أضيف خيار `--no-alef-maqsura` و `--version` لسطر الأوامر.
- توسّعت تغطية الاختبارات لتشمل `charts.py` و `cli.py` (لم تكن مغطاة إطلاقًا
  في الإصدار السابق)، إضافة لحالات حافة جديدة في اختبارات `normalize.py`
  و `display.py`.
- تحديث `pyproject.toml`: `dependencies` أصبحت فارغة، مع إضافة extra جديد
  باسم `display` بجانب `charts` الموجود مسبقًا.

### معروف ولم يُغيَّر
- بيانات المؤلف والروابط في `pyproject.toml`/`LICENSE` ما زالت نائبة
  (`اسمك هنا`، `yourusername`) — يجب استبدالها ببياناتك الفعلية قبل النشر
  على PyPI/GitHub.
