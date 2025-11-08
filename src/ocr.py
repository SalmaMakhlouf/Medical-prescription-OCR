import argparse, os, json

def ocr_pytesseract(image_path):
    import pytesseract, cv2
    img = cv2.imread(image_path)
    data = pytesseract.image_to_data(img, lang='fra+eng', output_type=pytesseract.Output.DICT)
    words = []
    for i in range(len(data['text'])):
        txt = data['text'][i].strip()
        if not txt:
            continue
        x,y,w,h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        words.append({'text': txt, 'bbox': [int(x), int(y), int(w), int(h)]})
    return words

def ocr_easyocr(image_path):
    import easyocr
    reader = easyocr.Reader(['fr','en'], gpu=False)
    results = reader.readtext(image_path)  # [ [bbox, text, conf], ... ]
    words = []
    for (bbox, txt, conf) in results:
        (x1,y1),(x2,y2),(x3,y3),(x4,y4) = bbox
        x, y = min(x1,x2,x3,x4), min(y1,y2,y3,y4)
        w, h = max(x1,x2,x3,x4)-x, max(y1,y2,y3,y4)-y
        words.append({'text': txt.strip(), 'bbox': [int(x), int(y), int(w), int(h)], 'conf': float(conf)})
    return words

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='preprocessed images folder')
    ap.add_argument('--engine', choices=['pytesseract','easyocr'], default='pytesseract')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    out = []
    for name in os.listdir(args.input):
        if name.lower().endswith(('.png','.jpg','.jpeg','.tif','.tiff','.bmp')):
            path = os.path.join(args.input, name)
            if args.engine == 'pytesseract':
                words = ocr_pytesseract(path)
            else:
                words = ocr_easyocr(path)
            out.append({'image': name, 'words': words})

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
