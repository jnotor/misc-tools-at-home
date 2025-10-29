from pathlib import Path
from PIL import Image
from typing import Optional
import argparse
import pillow_heif

def get_files(input_path: str) -> list[str]:
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        return []

    if input_path.is_file():
        return [input_path]

    files = [f for f in input_path.iterdir() if f.suffix.lower() == ".heic"]

    if not files:
        print("No .heic files found.")
        return []

    return files

def convert_heic_to_jpg(files: list[Path], output_dir: Optional[str] = None, delete_hiec: bool = False) -> None:
    pillow_heif.register_heif_opener()

    for file_path in files:
        img = Image.open(str(file_path))

        try:
            img = img.convert("RGB")
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}")
            continue

        output_dir_final = output_dir or file_path.parent
        output_dir_final.mkdir(parents=True, exist_ok=True)

        output_path = output_dir_final / (file_path.stem + ".jpg")

        img.save(output_path, "JPEG")
        print(f"Converted: {output_path}")

        if delete_hiec:
            file_path.unlink()

def main():
    parser = argparse.ArgumentParser(
        description="Convert HEIC images to JPG (Windows-friendly format)"
    )
    parser.add_argument("input", help="Path to HEIC file or folder. Note: requires full path")
    parser.add_argument(
        "-o", "--output", help="Output directory (optional)", default=''
    )
    parser.add_argument(
        "-d", "--delete",
        action="store_true",
        help="Delete original HEIC files after conversion (default: False)",
    )

    args = parser.parse_args()

    files = get_files(input_path=args.input)

    convert_heic_to_jpg(files=files, output_dir=args.output, delete_hiec=args.delete)

if __name__ == "__main__":
    main()