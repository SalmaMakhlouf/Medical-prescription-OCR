import argparse, os, json, pathlib, subprocess, sys

def run(cmd):
    print(">>", " ".join(cmd))
    res = subprocess.run(cmd, check=True)
    return res.returncode

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='Folder with raw images (JPEG/PNG/TIFF)')
    ap.add_argument('--workdir', default='outputs', help='Working/output directory')
    ap.add_argument('--engine', default='pytesseract', choices=['pytesseract','easyocr'])
    args = ap.parse_args()

    raw = pathlib.Path(args.input)
    work = pathlib.Path(args.workdir)
    pre = work / "preprocessed"
    work.mkdir(exist_ok=True, parents=True)

    run([sys.executable, "src/preprocess.py", "--input", str(raw), "--out", str(pre)])
    ocr_json = work / "ocr.json"
    run([sys.executable, "src/ocr.py", "--input", str(pre), "--engine", args.engine, "--out", str(ocr_json)])
    parsed_json = work / "parsed.json"
    run([sys.executable, "src/postprocess.py", "--ocr", str(ocr_json), "--out", str(parsed_json)])

    print("\nPipeline terminé. Résultats :")
    print(" - OCR brut :", ocr_json)
    print(" - Champs extraits :", parsed_json)

if __name__ == "__main__":
    main()
