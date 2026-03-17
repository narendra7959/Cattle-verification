import os
import shutil
import random

# ==============================
# CONFIGURATION
# ==============================

root_dir = r"E:\MSC PROJECT\cattle-1-dataset\New folder"
output_dir = r"E:\MSC PROJECT\cattle-1-dataset\cattle-1-identification"

train_ratio = 0.75
val_ratio = 0.10
test_ratio = 0.15

random.seed(42)

splits = ["train", "val", "test"]

# ==============================
# MAIN LOOP
# ==============================

for cattle_id in os.listdir(root_dir):

    cattle_path = os.path.join(root_dir, cattle_id)
    if not os.path.isdir(cattle_path):
        continue

    for part in ["face", "muzzle"]:

        part_path = os.path.join(cattle_path, part)
        if not os.path.exists(part_path):
            continue

        images = [f for f in os.listdir(part_path)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if len(images) == 0:
            continue

        random.shuffle(images)
        total = len(images)

        # -------- NORMAL SPLIT FIRST --------
        train_count = int(total * train_ratio)
        val_count = int(total * val_ratio)
        test_count = total - train_count - val_count

        train_imgs = images[:train_count]
        val_imgs = images[train_count:train_count + val_count]
        test_imgs = images[train_count + val_count:]

        split_dict = {
            "train": train_imgs,
            "val": val_imgs,
            "test": test_imgs
        }

        # -------- FIX EMPTY SPLITS BY COPYING --------
        for split_name in splits:

            if len(split_dict[split_name]) == 0:

                # find a non-empty split to copy from
                for other_split in splits:
                    if len(split_dict[other_split]) > 0:
                        img_to_copy = random.choice(split_dict[other_split])
                        split_dict[split_name].append(img_to_copy)
                        break

        # -------- COPY FILES --------
        for split_name in splits:

            dest_folder = os.path.join(output_dir, split_name, cattle_id, part)
            os.makedirs(dest_folder, exist_ok=True)

            for img in split_dict[split_name]:

                src_path = os.path.join(part_path, img)
                dst_path = os.path.join(dest_folder, img)

                # Rename if duplicate
                if os.path.exists(dst_path):
                    name, ext = os.path.splitext(img)
                    dst_path = os.path.join(dest_folder, name + "_dup" + ext)

                shutil.copy2(src_path, dst_path)

print("✅ Dataset split completed with correct copy-only logic!")