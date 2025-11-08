import argparse, json, re
from rapidfuzz import fuzz

MED_UNITS = ['mg','g','ml','µg','mcg','cp','gél','fl','amp','ui']
FREQ_PAT = r'(\d+\s*/\s*j|\d+\s*x\s*/?j|\d+\s*fois\s*/?j)'
DOSE_PAT = r'(\d+(?:[\.,]\d+)?\s*(?:' + '|'.join(MED_UNITS) + r'))'

def join_words(words):
    words_sorted = sorted(words, key=lambda w: (w['bbox'][1], w['bbox'][0]))
    return ' '.join(w['text'] for w in words_sorted)

def parse_date(text):
    # Accept formats like 01/07/2022, 1-8-75, etc.
    m = re.search(r'(\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b)', text)
    return m.group(1) if m else None

def parse_patient(text):
    # Look for "NOM DU MALADE" or variants
    for pat in [r'NOM\s+DU\s+MALAD(E|E)\s*:?\s*([A-ZÉÈÊÂÎÔÙÇ][A-Za-zÉÈÊÂÎÔÙÇ\-\s]+)',
                r'Nom\s*:\s*([A-ZÉÈÊÂÎÔÙÇ][A-Za-zÉÈÊÂÎÔÙÇ\-\s]+)']:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return m.group(m.lastindex).strip()
    return None

def parse_doctor(text):
    # header often contains "Docteur" / "Dr" and a name
    m = re.search(r'(Docteur|Dr\.?)[\s:]+([A-ZÉÈÊÂÎÔÙÇ][A-Za-zÉÈÊÂÎÔÙÇ\-\s]+)', text, flags=re.IGNORECASE)
    return m.group(0).strip() if m else None

def parse_medications(text):
    # Extract lines that look like "1) xxx 1 cp 3/j" or "Paracetamol 500 mg 1x3j"
    meds = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        # Heuristic: lines that start with bullet/number or contain a dose unit
        if re.match(r'^(\d+\)|-)', ln) or re.search(DOSE_PAT, ln, flags=re.IGNORECASE):
            name = ln
            dose_m = re.search(DOSE_PAT, ln, flags=re.IGNORECASE)
            freq_m = re.search(FREQ_PAT, ln, flags=re.IGNORECASE)
            meds.append({
                'raw': ln,
                'name': name,
                'dose': dose_m.group(1) if dose_m else None,
                'frequency': freq_m.group(1) if freq_m else None
            })
    return meds

def parse_document(words):
    full_text = join_words(words)
    # Also build a rough paragraph text using line heuristic (y coordinate)
    text_by_line = []
    by_y = {}
    for w in words:
        y = w['bbox'][1] // 20  # bucket lines
        by_y.setdefault(y, []).append(w['text'])
    for y in sorted(by_y.keys()):
        text_by_line.append(' '.join(by_y[y]))
    paragraph = '\n'.join(text_by_line)

    out = {
        'date': parse_date(paragraph) or parse_date(full_text),
        'patient_name': parse_patient(paragraph),
        'physician': parse_doctor(paragraph) or parse_doctor(full_text),
        'medications': parse_medications(paragraph),
        'raw_text': paragraph
    }
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ocr', required=True, help='OCR JSON from src/ocr.py')
    ap.add_argument('--out', required=True, help='Output parsed JSON')
    args = ap.parse_args()

    with open(args.ocr, 'r', encoding='utf-8') as f:
        ocr = json.load(f)

    parsed = []
    for item in ocr:
        fields = parse_document(item['words'])
        parsed.append({'image': item['image'], **fields})

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
