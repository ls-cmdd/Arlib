"""
واجهة سطر الأوامر لمكتبة arabikit.

الاستخدام:
    arabikit clean input.txt -o output.txt
    arabikit clean input.txt --no-tashkeel
"""
import argparse
import sys

from . import __version__
from .normalize import normalize_text


def _cmd_clean(args):
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"خطأ: الملف غير موجود: {args.input}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"خطأ: لا توجد صلاحية لقراءة الملف: {args.input}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"خطأ: تعذّر قراءة الملف كنص UTF-8: {args.input}",
            file=sys.stderr,
        )
        sys.exit(1)

    cleaned = normalize_text(
        content,
        tashkeel=not args.no_tashkeel,
        tatweel=not args.no_tatweel,
        hamza=not args.no_hamza,
        alef_maqsura=not args.no_alef_maqsura,
    )

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(cleaned)
        except PermissionError:
            print(f"خطأ: لا توجد صلاحية للكتابة في: {args.output}", file=sys.stderr)
            sys.exit(1)
        print(f"تم الحفظ في: {args.output}")
    else:
        sys.stdout.write(cleaned)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="arabikit",
        description="أداة سطر أوامر لمعالجة وتنظيف النصوص العربية.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    clean_parser = subparsers.add_parser("clean", help="تنظيف وتطبيع ملف نصي عربي")
    clean_parser.add_argument("input", help="مسار الملف المدخل")
    clean_parser.add_argument("-o", "--output", help="مسار الملف الناتج (اختياري)")
    clean_parser.add_argument("--no-tashkeel", action="store_true", help="لا تزل التشكيل")
    clean_parser.add_argument("--no-tatweel", action="store_true", help="لا تزل التطويل")
    clean_parser.add_argument("--no-hamza", action="store_true", help="لا توحّد الهمزات")
    clean_parser.add_argument(
        "--no-alef-maqsura", action="store_true", help="لا توحّد الألف المقصورة مع الياء"
    )
    clean_parser.set_defaults(func=_cmd_clean)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
