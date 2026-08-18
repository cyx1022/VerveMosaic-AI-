import importlib.util
import json
import os

spec = importlib.util.spec_from_file_location(
    "restructure",
    r"C:\Users\陈\Documents\Codex\2026-08-04\c-users-desktop-ichpattern-competition-submission\work\restructure_flower_dataset.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ROOT = mod.ROOT
FIRST = r"C:\Users\陈\Desktop\基于生成式AI的非遗纹样智能生成与文创产品设计系统\非遗纹样图像数据集（ICHPattern-1.0）\LoRA训练集_花卉细分_kohya"
WORK = mod.WORK

FIRST_CATEGORY_MAP = {
    "通用花卉": "1_通用花卉",
    "植物纹": "2_植物纹",
    "缠枝花纹": "4_缠枝花纹",
    "卷草纹": "10_卷草纹",
    "其他花卉": "12_其他花卉",
    "葫芦纹": "20_葫芦纹",
}


def read_txt(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read().strip()


def old_caption_map():
    out = {}
    # Peony old captions from the reorder manifest.
    peony_manifest = os.path.join(
        ROOT, "牡丹纹", "01_牡丹英文标注训练集", "_peony_reorder_manifest_20260804_155442.json"
    )
    if os.path.exists(peony_manifest):
        with open(peony_manifest, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        for item in data["order"]:
            out[os.path.join(ROOT, "牡丹纹", "01_牡丹英文标注训练集", "10_peony", item["new_image"])] = item["caption"]

    # Lotus old captions from the previous training copy.
    lotus_old_dir = r"C:\LoraTraining\ich_lotus_train_en\10_lotus"
    lotus_cur_dir = os.path.join(ROOT, "莲花纹", "01_莲花英文标注训练集", "10_lotus")
    if os.path.isdir(lotus_old_dir):
        for name in os.listdir(lotus_cur_dir):
            if os.path.splitext(name)[1].lower() in mod.IMG_EXT:
                old_txt = os.path.join(lotus_old_dir, os.path.splitext(name)[0] + ".txt")
                if os.path.exists(old_txt):
                    out[os.path.join(lotus_cur_dir, name)] = read_txt(old_txt)

    # Chrysanthemum and plum from the first dataset folder.
    for src, first_cat in [
        ("菊花纹", "20_菊花纹"),
        ("梅花纹", "6_梅花纹"),
    ]:
        cur_dir = os.path.join(ROOT, src, "01_" + ("菊花纹英文标注训练集" if src == "菊花纹" else "梅花纹英文标注训练集"), "10_" + ("chrysanthemum" if src == "菊花纹" else "plum_blossom"))
        first_dir = os.path.join(FIRST, first_cat)
        for name in os.listdir(cur_dir):
            if os.path.splitext(name)[1].lower() in mod.IMG_EXT:
                old_txt = os.path.join(first_dir, os.path.splitext(name)[0] + ".txt")
                if os.path.exists(old_txt):
                    out[os.path.join(cur_dir, name)] = read_txt(old_txt)

    # Other motif: map via restructure manifest back to first dataset captions.
    other_cur_dir = os.path.join(ROOT, "其他纹样", "01_其他纹样英文标注训练集", "10_other_motif")
    manifest_path = os.path.join(WORK, "flower_restructure_manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        for item in data["items"]:
            if item.get("category") != "other":
                continue
            orig_rel = item["original_image"].replace("\\", "/")
            top = orig_rel.split("/")[0]
            base = os.path.basename(orig_rel)
            first_cat = FIRST_CATEGORY_MAP.get(top)
            if not first_cat:
                continue
            old_txt = os.path.join(FIRST, first_cat, os.path.splitext(base)[0] + ".txt")
            if os.path.exists(old_txt):
                out[os.path.join(other_cur_dir, os.path.basename(item["new_image"]))] = read_txt(old_txt)

    return out


def subclass_from_old(old):
    s = old.lower()
    if "gourd" in s:
        return "gourd"
    if "scroll grass" in s:
        return "scroll grass"
    if "scrolling floral vine" in s or "vine" in s:
        return "scrolling floral vine"
    if "botanical" in s:
        return "botanical"
    if "pomegranate" in s or "peach" in s:
        return "rare floral"
    return "floral"


def main():
    old_map = old_caption_map()
    counts = {"peony": 0, "lotus": 0, "chrysanthemum": 0, "plum_blossom": 0, "other": 0}

    for key, cfg in mod.CATS.items():
        for image in mod.collect_images(cfg["src"]):
            old = old_map.get(image, read_txt(os.path.splitext(image)[0] + ".txt"))
            name = os.path.basename(image)
            cap = mod.build_caption(cfg["trigger"], cfg["subclass"], cfg["meaning"], old, name, name)
            with open(os.path.splitext(image)[0] + ".txt", "w", encoding="utf-8") as fp:
                fp.write(cap + "\n")
            counts[key] += 1

    other_dir = os.path.join(ROOT, "其他纹样", "01_其他纹样英文标注训练集", "10_other_motif")
    for name in sorted(os.listdir(other_dir)):
        if os.path.splitext(name)[1].lower() not in mod.IMG_EXT:
            continue
        image = os.path.join(other_dir, name)
        old = old_map.get(image, read_txt(os.path.splitext(image)[0] + ".txt"))
        seed = name
        subclass = subclass_from_old(old)
        meaning = mod.meaning_for_other(name, old)
        cap = mod.build_caption("ichpattern_other_flower", subclass, meaning, old, name, seed)
        with open(os.path.splitext(image)[0] + ".txt", "w", encoding="utf-8") as fp:
            fp.write(cap + "\n")
        counts["other"] += 1

    print(counts)
    print("peony_0001:", read_txt(os.path.join(ROOT, "牡丹纹", "01_牡丹英文标注训练集", "10_peony", "peony_0001.txt")))


if __name__ == "__main__":
    main()
