import argparse, json, re
from collections import Counter

def normalize(s):
    if s is None:
        return ""
    s = s.lower()
    s = re.sub(r'[^a-z0-9éèêàâîôûç\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def token_f1(pred, gold):
    tp = 0
    fp = 0
    fn = 0
    for p, g in zip(pred, gold):
        p_tokens = Counter(normalize(p).split())
        g_tokens = Counter(normalize(g).split())
        common = sum((p_tokens & g_tokens).values())
        tp += common
        fp += sum((p_tokens - g_tokens).values())
        fn += sum((g_tokens - p_tokens).values())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.0
    return precision, recall, f1

def evaluate(parsed, gold_items):
    # Map by image
    gold_map = {it['image']: it for it in gold_items}
    P=R=F=0; n=0
    results = []
    for item in parsed:
        gold = gold_map.get(item['image'])
        if not gold:
            continue
        pred_meds = [m.get('name','') for m in item.get('medications',[])]
        gold_meds = [m.get('name','') for m in gold.get('medications',[])]
        p,r,f = token_f1([ ' '.join(pred_meds) ], [ ' '.join(gold_meds) ])
        results.append({'image': item['image'], 'precision': p, 'recall': r, 'f1': f})
        P+=p; R+=r; F+=f; n+=1
    macro = {'precision': P/max(n,1), 'recall': R/max(n,1), 'f1': F/max(n,1), 'n': n}
    return {'macro': macro, 'details': results}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pred', required=True)
    ap.add_argument('--gold', required=True)
    args = ap.parse_args()
    parsed = json.load(open(args.pred, 'r', encoding='utf-8'))
    gold = json.load(open(args.gold, 'r', encoding='utf-8'))
    metrics = evaluate(parsed, gold.get('items', []))
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    main()
