# Extraction d'informations depuis des ordonnances (démo reproductible)

**But.** Extraire médicaments/posologies à partir d'images d'ordonnances, même manuscrites.  
**Méthode.** Pré-traitement (binarisation, deskew), OCR (PyTesseract / EasyOCR), règles simples de parsing + correction orthographique.  
**Éval.** Precision / Recall / F1 sur données *synthétiques* (aucune donnée réelle patients).

> ⚠️ Confidentialité : n'ajoutez aucune donnée réelle. Utilisez des échantillons synthétiques floutés ou générés.

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

## À faire
- Ajouter 5–10 images *synthétiques* d'ordonnances dans `data/samples/`.
- Compléter `data/annotations.json` avec les champs cibles (patient, médecin, date, médicaments, posologies, durée).
- Implémenter les TODOs dans `src/*.py` (voir squelettes).
- Lancer l'OCR et l'évaluation, puis reporter les métriques dans le README.
