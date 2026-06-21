import csv
import os
import easyocr


def recognize_numbers_to_csv(src_dir, output_csv_path):
    """读取裁剪后的图片，用 OCR 识别其中的数字并导出为 CSV。

    Args:
        src_dir: 裁剪后图片所在的文件夹路径。
        output_csv_path: 输出的 CSV 文件路径。
    """
    # 校验输入目录
    if not os.path.exists(src_dir):
        print(f"[-] 错误：找不到裁剪后的文件夹 '{src_dir}'")
        return

    # 收集并排序图片文件
    img_files = [f for f in os.listdir(src_dir) if f.lower().endswith(".jpg")]
    if not img_files:
        print(f"[-] 错误：在 '{src_dir}' 中没有找到 .jpg 图片。")
        return
    img_files.sort()

    # 初始化 EasyOCR（首次运行会自动下载模型）
    print("[+] 正在初始化 AI OCR 模型（首次运行会自动下载模型权重文件）...")
    reader = easyocr.Reader(["en"], gpu=True)

    print(f"[+] 开始识别 {len(img_files)} 张图片中的数字...")

    # 流式写入 CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Number", "Data"])

        for idx, filename in enumerate(img_files):
            img_path = os.path.join(src_dir, filename)

            # 文件名（不含后缀）作为编号
            img_id = os.path.splitext(filename)[0]

            try:
                # OCR 识别，allowlist 限定只识别数字、冒号和小数点
                results = reader.readtext(img_path, allowlist="0123456789:.")

                if results:
                    # 拼接所有识别到的文本片段
                    detected_text = "".join([res[1] for res in results])
                else:
                    detected_text = "ERROR: 未检测到数字"

            except Exception as e:
                detected_text = f"ERROR: 识别失败({str(e)})"

            # 写入一行结果
            writer.writerow([img_id, detected_text])

            # 每完成约 10% 输出一次进度
            if (idx + 1) % max(1, len(img_files) // 10) == 0 or (idx + 1) == len(
                img_files
            ):
                print(f"    已完成: {idx + 1}/{len(img_files)}")

    print(f"\n[+] 任务完成！数据已成功保存至 CSV 文件: '{output_csv_path}'")


if __name__ == "__main__":
    # ---- 参数配置 ----
    # step2 输出的裁剪图片文件夹
    CROP_FOLDER = "video_snapshots_cropped"
    # 识别结果导出的 CSV 文件路径
    OUTPUT_CSV = "recognized_data.csv"

    recognize_numbers_to_csv(CROP_FOLDER, OUTPUT_CSV)