import os
import shutil
import random
import math

def split_verification_dataset(base_dir, output_dir, train_ratio=0.75, val_ratio=0.10, test_ratio=0.15, seed=42):
    
    random.seed(seed)

    # Get all ID folders
    all_ids = [
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]

    total_ids = len(all_ids)
    print(f"Total ID folders found: {total_ids}")

    # Shuffle IDs
    random.shuffle(all_ids)

    # Calculate split counts
    train_count = int(total_ids * train_ratio)
    val_count = int(total_ids * val_ratio)
    test_count = total_ids - train_count - val_count

    train_ids = all_ids[:train_count]
    val_ids = all_ids[train_count:train_count + val_count]
    test_ids = all_ids[train_count + val_count:]

    print("\nSplit Summary:")
    print(f"Train: {len(train_ids)} folders ({(len(train_ids)/total_ids)*100:.2f}%)")
    print(f"Val  : {len(val_ids)} folders ({(len(val_ids)/total_ids)*100:.2f}%)")
    print(f"Test : {len(test_ids)} folders ({(len(test_ids)/total_ids)*100:.2f}%)")

    # Create output directories
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    # Function to copy folders
    def copy_folders(folder_list, split_name):
        for folder in folder_list:
            src = os.path.join(base_dir, folder)
            dst = os.path.join(output_dir, split_name, folder)
            shutil.copytree(src, dst)

    # Copy data
    copy_folders(train_ids, "train")
    copy_folders(val_ids, "val")
    copy_folders(test_ids, "test")

    print("\n✅ Folder-based split completed successfully!")


# ==============================
# 🔹 USE LIKE THIS
# ==============================

base_dir = r"E:\MSC PROJECT\cattle-1-dataset\New folder"
output_dir = r"E:\MSC PROJECT\cattle-1-dataset\cattle-1-verification"

split_verification_dataset(base_dir, output_dir)