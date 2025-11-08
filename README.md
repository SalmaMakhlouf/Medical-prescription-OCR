# Extraction d'informations depuis des ordonnances (démo reproductible)

- **Problème** : extraire automatiquement *patient, médecin, date, médicaments, dose, fréquence, durée* à partir d’ordonnances **difficiles à lire** (manuscrits, scans, artefacts).
- **Méthodes** : prétraitement (CLAHE, deskew, binarisation adaptative), OCR multi-moteur (pytesseract / easyocr), parsing via règles + regex (units, patterns de fréquence).
- **Évaluation** : métriques **macro Precision/Recall/F1** (token-level) sur **corpus synthétique** annoté.
- **Reproductibilité** : `Main.py` (runner), `requirements.txt`, scripts d’éval, structure claire, seeds/configs figés.

**Démo reproductible d’extraction d’informations depuis des ordonnances médicales (manuscrites / scannées).**  
Pipeline E2E : *prétraitement → OCR (pytesseract/easyocr) → parsing heuristique → JSON → évaluation (Precision/Recall/F1)*.



## Reproduire
```bash
pip install -r requirements.txt
python src/preprocess.py --input data/samples --out outputs/preprocessed
python src/ocr.py --input outputs/preprocessed --engine pytesseract --out outputs/ocr.json
python eval/evaluate.py --pred outputs/ocr.json --gold data/annotations.json
```

## Arborescence
```
medical-prescription-ocr/
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ preprocess.py
│  ├─ ocr.py
│  └─ postprocess.py
├─ data/
│  ├─ samples/           # images *synthétiques* (placeholders)
│  └─ annotations.json   # labels synthétiques (à compléter)
├─ eval/
│  └─ evaluate.py
├─ notebooks/
│  └─ demo.ipynb
└─ outputs/              # résultats générés (.json, images, etc.)
```


## ⚡️ Installation rapide
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

---
```
## ▶️ Exécution de bout en bout

# 1) Placez 5–10 images synthétiques dans data/samples/ + remplissez data/annotations.json
python Main.py --input data/samples --workdir outputs --engine pytesseract
# ou : --engine easyocr

# 2) Évaluation (si annotations disponibles)
python eval/evaluate.py --pred outputs/parsed.json --gold data/annotations.json

## 🧪 Format d’annotation (exemple)
{
  "schema": {
    "image": "string",
    "patient_name": "string",
    "physician_name": "string",
    "date": "YYYY-MM-DD",
    "medications": [
{"name": "string", "dose": "string", "frequency": "string", "duration": "string"}
  
  },
  "items": [
    {
      "image": "001.jpg",
      "patient_name": "A. A.",
      "physician_name": "Dr B. X.",
      "date": "2022-07-01",
      "medications": [{"name": "Duphalac", "dose": "1 fl", "frequency": "2/j", "duration": "7 j"},{"name": "Colospa",  "dose": "1 cp", "frequency": "3/j", "duration": "5 j"]
    }
  ]
}

## 📊 Métriques
Token-level Precision/Recall/F1 sur les noms de médicaments (macro).

Facile à étendre : ajoutez métriques par champ (dose, fréquence, durée), ou une évaluation entity-level (exact match / partial match).

## 🗺️ Roadmap (idées “recherche”)

HTR / modèles de handwritten text recognition (TrOCR, PARSeq)

Layout-aware parsing (detectron2/DocLayNet/Donut/LAION-doc)

Lexiques médicaux + fuzzy matching (rapidfuzz) pour robustifier name/dose

Calibration d’incertitude (confs OCR + règles) et détection d’erreurs

Ablations (impact du prétraitement, taille des chunks OCR, moteurs OCR)

## 📄 Citation

Un fichier CITATION.cff est fourni :
Makhlouf, S. (2025). medical-prescription-ocr: démo reproductible d'extraction d'information. MIT License.

## 👩‍💻 Contact

Salma Makhlouf — Grenoble (FR)
GitHub: https://github.com/
<votre-user> · LinkedIn: https://www.linkedin.com/in/
