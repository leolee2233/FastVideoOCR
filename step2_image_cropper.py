import os
import cv2


def crop_images_in_folder(src_dir, dst_dir, crop_box):
    """读取文件夹中所有 JPG 图片，按指定范围统一裁剪并保存。

    Args:
        src_dir: 源图片文件夹路径。
        dst_dir: 裁剪结果输出文件夹路径。
        crop_box: 裁剪坐标 (y_start, y_end, x_start, x_end)。
    """
    # 校验源目录
    if not os.path.exists(src_dir):
        print(f"[-] 错误：找不到源文件夹 '{src_dir}'，请检查路径。")
        return

    # 创建输出目录
    os.makedirs(dst_dir, exist_ok=True)

    y_start, y_end, x_start, x_end = crop_box

    # 收集并排序所有 JPG 文件
    img_files = [f for f in os.listdir(src_dir) if f.lower().endswith(".jpg")]
    if not img_files:
        print(f"[-] 错误：在 '{src_dir}' 中未找到任何 .jpg 图片。")
        return

    img_files.sort()
    total_imgs = len(img_files)
    print(f"[+] 找到 {total_imgs} 张图片，开始统一裁剪...")

    success_count = 0
    for idx, filename in enumerate(img_files):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)

        # 读取图片
        img = cv2.imread(src_path)
        if img is None:
            print(f"[-] 警告：无法读取图片 {filename}，跳过。")
            continue

        # 按坐标切片裁剪：img[y_start:y_end, x_start:x_end]
        cropped_img = img[y_start:y_end, x_start:x_end]

        # 裁剪后为空说明坐标越界
        if cropped_img.size == 0:
            print(
                f"[-] 错误：第 {filename} 张图片裁剪结果为空，请检查 CROP_BOX 坐标是否超出原图分辨率！"
            )
            return

        # 写入输出目录
        cv2.imwrite(dst_path, cropped_img)
        success_count += 1

        # 每完成约 10% 输出一次进度
        if (idx + 1) % max(1, total_imgs // 10) == 0 or (idx + 1) == total_imgs:
            print(f"    进度: {idx + 1}/{total_imgs}")

    print(f"\n[+] 任务完成！裁剪后的图片已保存至: '{dst_dir}'")
    print(f"[+] 实际成功裁剪: {success_count} 张图片。")


if __name__ == "__main__":
    # ---- 参数配置 ----
    # 从 step1 输出的截图文件夹
    SRC_FOLDER = "video_snapshots_with_time"
    # 裁剪结果输出文件夹
    NEW_FOLDER = "video_snapshots_cropped"

    # 裁剪范围：(y_start, y_end, x_start, x_end)
    # 示例：原图 1920×1080，截取 y:330~420, x:100~380 的区域
    CROP_BOX = (330, 420, 100, 380)

    crop_images_in_folder(SRC_FOLDER, NEW_FOLDER, CROP_BOX)