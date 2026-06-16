"""
scan_assets.py - Cek ukuran dan padding transparan semua asset gambar
Jalankan: python scan_assets.py
Butuh: pip install Pillow
"""

from PIL import Image
import os

# Folder asset yang mau di-scan
ASSET_FOLDERS = [
    "asset_karakterjalan",
    "asset_karakterlari",
    "asset_karakterloncat",
    "asset_karakterjongkok",
    "asset_karakternembak",
    "asset_nembakjongkok",
    "asset_karaktermati",
    "asset_karakterlvel2jalan",
    "asset_karakterjongkoklevel2",
    "asset_karakternembaklevel2",
    "asset_karakternembakjongkoklevel2",
    "asset_musuhlevel1",
    "asset_musuhlevel1jongkok",
    "asset_musuhlevel2jalan",
    "asset_musuhnembaklevel2",
    "asset_musuhnembakjongkoklevel2",
    "asset_musuhjongkoklevel2",
]

def get_content_bbox(img):
    """Hitung bounding box konten non-transparan."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[3]  # channel alpha
    bbox = alpha.getbbox()  # (left, top, right, bottom) area non-transparan
    return bbox

def analyze_image(filepath):
    img = Image.open(filepath)
    w, h = img.size
    bbox = get_content_bbox(img)

    if bbox is None:
        padding = {"top": h, "bottom": h, "left": w, "right": w}
        content_w, content_h = 0, 0
    else:
        left, top, right, bottom = bbox
        padding = {
            "top":    top,
            "bottom": h - bottom,
            "left":   left,
            "right":  w - right,
        }
        content_w = right - left
        content_h = bottom - top

    return {
        "file":      os.path.basename(filepath),
        "size":      (w, h),
        "content":   (content_w, content_h),
        "padding":   padding,
        "bbox":      bbox,
    }

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    results = {}

    for folder in ASSET_FOLDERS:
        folder_path = os.path.join(base, folder)
        if not os.path.isdir(folder_path):
            print(f"[SKIP] Folder tidak ditemukan: {folder}")
            continue

        files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])

        if not files:
            continue

        results[folder] = []
        for fname in files:
            fpath = os.path.join(folder_path, fname)
            try:
                info = analyze_image(fpath)
                results[folder].append(info)
            except Exception as ex:
                print(f"[ERROR] {fpath}: {ex}")

    # === LAPORAN ===
    print("\n" + "="*70)
    print(f"{'FOLDER':<35} {'FILE':<30} {'SIZE':>12} {'CONTENT':>12} {'PAD T/B/L/R'}")
    print("="*70)

    for folder, items in results.items():
        print(f"\n[{folder}]")
        sizes = set()
        for info in items:
            w, h = info["size"]
            cw, ch = info["content"]
            p = info["padding"]
            pad_str = f"{p['top']}/{p['bottom']}/{p['left']}/{p['right']}"
            size_str = f"{w}x{h}"
            content_str = f"{cw}x{ch}"
            print(f"  {info['file']:<40} {size_str:>8}  content:{content_str:>8}  pad:{pad_str}")
            sizes.add((w, h))

        if len(sizes) > 1:
            print(f"  *** UKURAN TIDAK KONSISTEN: {sizes}")

    # === SUMMARY UKURAN PER FOLDER ===
    print("\n" + "="*70)
    print("SUMMARY UKURAN (width x height)")
    print("="*70)
    for folder, items in results.items():
        sizes = {}
        for info in items:
            s = info["size"]
            sizes[s] = sizes.get(s, 0) + 1
        size_summary = ", ".join([f"{w}x{h} ({n} file)" for (w,h), n in sizes.items()])
        konsisten = "OK" if len(sizes) == 1 else "*** BEDA UKURAN ***"
        print(f"  {folder:<40} {size_summary}  [{konsisten}]")

    # === PERBANDINGAN ANTAR FOLDER (walk vs animasi lain) ===
    print("\n" + "="*70)
    print("PERBANDINGAN DENGAN WALK LEVEL 1 (asset_karakterjalan)")
    print("="*70)
    ref_folder = "asset_karakterjalan"
    if ref_folder in results and results[ref_folder]:
        ref_w, ref_h = results[ref_folder][0]["size"]
        print(f"  Referensi walk: {ref_w}x{ref_h}")
        for folder, items in results.items():
            if folder == ref_folder or not items:
                continue
            for info in items:
                fw, fh = info["size"]
                match = "SAMA" if (fw == ref_w and fh == ref_h) else f"BEDA ({fw}x{fh})"
                print(f"  {folder}/{info['file']:<50} {match}")

if __name__ == "__main__":
    main()
