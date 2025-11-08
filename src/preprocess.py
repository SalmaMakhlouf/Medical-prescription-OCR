import argparse, os, cv2, numpy as np

def deskew(gray):
    # Estimate skew via image moments
    coords = np.column_stack(np.where(gray < 255))
    if coords.size == 0:
        return gray
    angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = gray.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def enhance(gray):
    # CLAHE for contrast + bilateral filter to reduce noise while keeping edges
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    c = clahe.apply(gray)
    return cv2.bilateralFilter(c, 5, 50, 50)

def binarize(gray):
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 15)

def preprocess_one(src_path, out_dir):
    img = cv2.imread(src_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = enhance(gray)
    gray = deskew(gray)
    bw = binarize(gray)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(src_path))
    cv2.imwrite(out_path, bw)
    return out_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for name in os.listdir(args.input):
        if name.lower().endswith(('.png','.jpg','.jpeg','.tif','.tiff','.bmp')):
            preprocess_one(os.path.join(args.input, name), args.out)

if __name__ == "__main__":
    main()
