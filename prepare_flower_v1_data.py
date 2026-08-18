import hashlib
import json
import os
import shutil
from datetime import datetime

ROOT = r"C:\Users\陈\Desktop\ICHPattern_Competition_Submission_Final\02_训练数据集_去缓存版"
WORK = r"C:\Users\陈\Documents\Codex\2026-08-04\c-users-desktop-ichpattern-competition-submission\work"

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

CATS = {
    "peony": {
        "src": r"牡丹纹\01_牡丹英文标注训练集\10_peony",
        "trigger": "ichpattern_peony",
        "subclass": "peony",
        "meaning": "auspicious peony symbolizing wealth",
    },
    "lotus": {
        "src": r"莲花纹\01_莲花英文标注训练集\10_lotus",
        "trigger": "ichpattern_lotus",
        "subclass": "lotus",
        "meaning": "auspicious lotus symbolizing purity",
    },
    "chrysanthemum": {
        "src": r"菊花纹\01_菊花纹英文标注训练集\10_chrysanthemum",
        "trigger": "ichpattern_chrysanthemum",
        "subclass": "chrysanthemum",
        "meaning": "auspicious chrysanthemum symbolizing longevity",
    },
    "plum_blossom": {
        "src": r"梅花纹\01_梅花纹英文标注训练集\10_plum_blossom",
        "trigger": "ichpattern_plum_blossom",
        "subclass": "plum blossom",
        "meaning": "auspicious plum blossom symbolizing resilience",
    },
}

OTHER_SOURCES = [
    r"通用花卉\01_通用花卉英文标注训练集\10_generic_flower",
    r"植物纹\01_植物纹英文标注训练集\10_botanical",
    r"缠枝花纹\01_缠枝花纹英文标注训练集\10_scrolling_floral",
    r"卷草纹\01_卷草纹英文标注训练集\10_scroll_grass",
    r"其他花卉\01_其他花卉英文标注训练集\10_rare_floral",
    r"葫芦纹\01_葫芦纹英文标注训练集\10_gourd",
]

OTHER_DST = r"其他纹样\01_其他纹样英文标注训练集\10_other_motif"


def collect_images(folder):
    path = os.path.join(ROOT, folder)
    if not os.path.isdir(path):
        return []
    return sorted(
        os.path.join(path, n)
        for n in os.listdir(path)
        if os.path.splitext(n)[1].lower() in IMG_EXT
    )


def read_caption(image_path):
    txt = os.path.splitext(image_path)[0] + ".txt"
    if os.path.exists(txt):
        with open(txt, "r", encoding="utf-8") as fp:
            return fp.read().strip()
    return ""


def h(x):
    return int(hashlib.md5(x.encode("utf-8")).hexdigest()[:8], 16)


def pick(seed, options):
    return options[h(seed) % len(options)]


def texture(old):
    s = old.lower()
    if "embroidery" in s or "绣" in s:
        return "embroidery texture"
    if "woven" in s or "carpet" in s or "textile" in s or "brocade" in s or "织物" in s or "锦" in s:
        return "woven texture"
    if "lacquer" in s or "enamel" in s or "carved" in s or "漆" in s or "珐琅" in s or "雕" in s:
        return "carved relief texture"
    if "porcelain" in s or "ceramic" in s or "瓷" in s:
        return "flat pattern design, subtle surface hint"
    if "monochrome" in s or "line" in s or "ink" in s or "linework" in s or "白描" in s or "水墨" in s:
        return "flat pattern design, clean lines, no texture"
    return "flat pattern design, clean lines, no texture"


def density(old, name, seed):
    s = old.lower() + " " + name
    if any(k in s for k in ["dense", "seamless", "repeat", "scrolling", "entwined", "vine", "缠枝", "满铺", "繁复"]):
        return "dense elaborate full pattern, intricate detail"
    if any(k in s for k in ["minimal", "simple", "sparse", "极简", "简洁", "line art", "线稿"]):
        return "minimal geometric, simple sparse detail"
    if any(k in s for k in ["border", "single", "centered", "round", "medallion", "团", "折枝", "单独"]):
        return "medium detail, balanced density"
    return pick(seed, [
        "medium detail, balanced density",
        "dense elaborate full pattern, intricate detail",
        "minimal geometric, simple sparse detail",
    ])


def arrangement(old, name, seed):
    s = old.lower() + " " + name
    if any(k in s for k in ["seamless", "repeat", "continuous", "scrolling", "entwined", "缠枝", "四方"]):
        return "seamless repeat, tileable continuous pattern"
    if any(k in s for k in ["border", "panel", "fitted", "适合", "边饰", "框"]):
        return "fitted panel motif, shaped to border"
    if any(k in s for k in ["single", "centered", "round", "medallion", "单独", "团", "中心"]):
        return "single motif, centered medallion"
    return pick(seed, [
        "single motif, centered medallion",
        "fitted panel motif, shaped to border",
        "seamless repeat, tileable continuous pattern",
    ])


def symmetry(old, name, seed):
    s = old.lower() + " " + name
    if any(k in s for k in ["mirror", "symmetric", "对称", "对鸟", "成对", "pair"]):
        return "bilateral mirror symmetry"
    if any(k in s for k in ["radial", "rotational", "round", "medallion", "团", "旋转"]):
        return "radial rotational symmetry"
    if any(k in s for k in ["asymmetric", "free", "无规则"]):
        return "asymmetric free composition"
    return pick(seed, [
        "bilateral mirror symmetry",
        "radial rotational symmetry",
        "asymmetric free composition",
    ])


def culture(old, name):
    s = old.lower() + " " + name
    if any(k in s for k in ["abstract", "contemporary", "modern", "再创作", "抽象"]):
        return "recognizable traditional form with design refinement"
    return "classic authentic traditional form, clearly recognizable"


def color(old, name, seed):
    s = old.lower() + " " + name
    import re

    if any(k in s for k in ["blue and white", "indigo", "monochrome", "青花", "靛蓝"]):
        return "limited color palette, monochrome indigo"
    if re.search(r"\bred\b|coral|crimson|红地|红色|朱", s):
        return "limited color palette, red dominant"
    if any(k in s for k in ["multicolor", "colorful", "rich", "五彩", "粉彩", "多色"]):
        return "rich multicolor palette"
    if any(k in s for k in ["bright", "light", "white", "亮"]):
        return "bright clear colors"
    if any(k in s for k in ["dark", "black", "deep", "深"]):
        return "deep muted colors"
    return pick(seed, [
        "limited color palette",
        "rich multicolor palette",
        "bright clear colors",
        "deep muted colors",
    ])


def meaning_for_other(name, old):
    s = name + " " + old
    if "石榴" in s or "pomegranate" in s.lower():
        return "auspicious pomegranate symbolizing fertility"
    if "桃" in s or "peach" in s.lower():
        return "auspicious peach blossom symbolizing longevity"
    if "葫芦" in s or "gourd" in s.lower():
        return "auspicious gourd symbolizing good fortune"
    return "traditional auspicious floral blessing"


def subclass_for_other(src):
    if "10_botanical" in src:
        return "botanical"
    if "10_generic_flower" in src:
        return "floral"
    if "10_scrolling_floral" in src:
        return "scrolling floral vine"
    if "10_scroll_grass" in src:
        return "scroll grass"
    if "10_rare_floral" in src:
        return "rare floral"
    if "10_gourd" in src:
        return "gourd"
    return "floral"


def build_caption(trigger, subclass, meaning, old, name, seed):
    parts = [
        trigger,
        f"Chinese traditional {subclass} pattern",
        "decorative motif",
        texture(old),
        density(old, name, seed),
        arrangement(old, name, seed),
        symmetry(old, name, seed),
        culture(old, name),
        color(old, name, seed),
        meaning,
    ]
    return ", ".join(parts)


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(ROOT, f"_backup_flower_restructure_{stamp}")
    os.makedirs(backup, exist_ok=True)
    items = []

    for key, cfg in CATS.items():
        for image in collect_images(cfg["src"]):
            old = read_caption(image)
            name = os.path.basename(image)
            seed = name
            cap = build_caption(cfg["trigger"], cfg["subclass"], cfg["meaning"], old, name, seed)
            shutil.copy2(image, os.path.join(backup, key + "_" + name))
            txt = os.path.splitext(image)[0] + ".txt"
            with open(txt, "w", encoding="utf-8") as fp:
                fp.write(cap + "\n")
            items.append(
                {
                    "category": key,
                    "new_image": image,
                    "caption": cap,
                }
            )

    # Merge the six auxiliary flower folders into 其他纹样.
    other_dst = os.path.join(ROOT, OTHER_DST)
    os.makedirs(other_dst, exist_ok=True)
    other_idx = 1
    for src_rel in OTHER_SOURCES:
        src_dir = os.path.join(ROOT, src_rel)
        if not os.path.isdir(src_dir):
            continue
        for image in collect_images(src_rel):
            old = read_caption(image)
            name = os.path.basename(image)
            ext = os.path.splitext(image)[1]
            new_name = f"other_{other_idx:04d}{ext}"
            new_path = os.path.join(other_dst, new_name)
            seed = new_name
            subclass = subclass_for_other(src_rel)
            meaning = meaning_for_other(name, old)
            cap = build_caption(
                "ichpattern_other_flower",
                subclass,
                meaning,
                old,
                name,
                seed,
            )
            shutil.copy2(image, os.path.join(backup, "other_" + str(other_idx) + "_" + name))
            shutil.copy2(image, new_path)
            with open(os.path.splitext(new_path)[0] + ".txt", "w", encoding="utf-8") as fp:
                fp.write(cap + "\n")
            items.append(
                {
                    "category": "other",
                    "new_image": os.path.join(OTHER_DST, new_name),
                    "original_image": os.path.join(src_rel, name),
                    "caption": cap,
                }
            )
            other_idx += 1

    # Remove the six merged source category folders after backup + copy.
    for src_rel in OTHER_SOURCES:
        src_dir = os.path.join(ROOT, src_rel)
        if os.path.isdir(src_dir):
            shutil.rmtree(src_dir)

    manifest = {
        "created": stamp,
        "root": ROOT,
        "backup": backup,
        "flower_categories": ["牡丹纹", "莲花纹", "菊花纹", "梅花纹", "其他纹样"],
        "count": len(items),
        "items": items,
    }
    with open(os.path.join(ROOT, f"_flower_restructure_manifest_{stamp}.json"), "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)
    with open(os.path.join(WORK, "flower_restructure_manifest.json"), "w", encoding="utf-8") as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)

    print("items", len(items))
    print("other images", other_idx - 1)


if __name__ == "__main__":
    main()
