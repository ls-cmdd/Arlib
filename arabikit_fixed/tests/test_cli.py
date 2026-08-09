import pytest

from arabikit.cli import build_parser, main


def test_clean_writes_to_stdout(tmp_path, capsys):
    input_file = tmp_path / "input.txt"
    input_file.write_text("الْعَرَبِيَّة", encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(["clean", str(input_file)])
    args.func(args)

    captured = capsys.readouterr()
    assert captured.out == "العربية"


def test_clean_writes_to_output_file(tmp_path, capsys):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    input_file.write_text("إلـــى", encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(["clean", str(input_file), "-o", str(output_file)])
    args.func(args)

    assert output_file.read_text(encoding="utf-8") == "الي"
    captured = capsys.readouterr()
    assert "تم الحفظ" in captured.out


def test_clean_no_hamza_flag(tmp_path, capsys):
    input_file = tmp_path / "input.txt"
    input_file.write_text("أحمد", encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(["clean", str(input_file), "--no-hamza"])
    args.func(args)

    captured = capsys.readouterr()
    assert captured.out == "أحمد"


def test_clean_no_alef_maqsura_flag(tmp_path, capsys):
    input_file = tmp_path / "input.txt"
    input_file.write_text("إلى", encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(["clean", str(input_file), "--no-alef-maqsura"])
    args.func(args)

    captured = capsys.readouterr()
    assert captured.out == "الى"


def test_clean_missing_file_exits_with_error(capsys):
    parser = build_parser()
    args = parser.parse_args(["clean", "/tmp/does_not_exist_arabikit.txt"])

    with pytest.raises(SystemExit) as exc_info:
        args.func(args)

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "الملف غير موجود" in captured.err


def test_version_flag(capsys):
    parser = build_parser()
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])
    assert exc_info.value.code == 0
