import os
import cv2


def extract_frames_fast_with_watermark(
    video_path, interval, output_dir="extracted_frames", start_sec=0
):
    """按固定帧间隔抽帧，并在每张截图上叠加时间水印。

    Args:
        video_path: 视频文件路径。
        interval: 每隔多少帧抽取一张。
        output_dir: 截图输出目录。
        start_sec: 从视频第几秒开始抽取（默认从 0 秒开始）。
    """
    # 校验视频文件是否存在
    if not os.path.exists(video_path):
        print(f"[-] 错误：找不到视频文件 '{video_path}'")
        return

    os.makedirs(output_dir, exist_ok=True)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[-] 错误：无法打开视频，请检查编码格式。")
        return

    # 获取视频元信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[+] 视频总帧数: {total_frames} | 帧率(FPS): {fps:.2f}")

    if fps <= 0:
        print("[-] 错误：视频 FPS 信息异常，无法计算时间水印。停止。")
        cap.release()
        return

    # 根据起始秒数计算起始帧号
    start_frame = int(start_sec * fps)
    if start_frame >= total_frames:
        print(
            f"[-] 错误：起始时间 ({start_sec}s -> 第 {start_frame} 帧) 已超过视频总帧数。"
        )
        cap.release()
        return

    # 生成待抽取的帧号列表
    target_frames = list(range(start_frame, total_frames, interval))
    total_to_extract = len(target_frames)
    print(
        f"[+] 设定起始时间: {start_sec} 秒 (第 {start_frame} 帧) | 计划抽取: {total_to_extract} 帧"
    )

    print("[+] 开始抽帧并添加水印...")

    saved_count = 0
    for idx, frame_idx in enumerate(target_frames):
        # 跳转到目标帧并读取
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if not ret:
            print(f"[-] 警告：未能读取到第 {frame_idx} 帧，可能已到达文件末尾。")
            continue

        # 计算当前帧对应的时间戳（HH:MM:SS）
        total_seconds = int(frame_idx / fps)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        timestamp_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # 水印字体与样式参数
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        color = (255, 255, 255)
        thickness = 2
        line_type = cv2.LINE_AA

        # 将水印定位在右下角
        height, width = frame.shape[:2]
        text_size = cv2.getTextSize(timestamp_str, font, font_scale, thickness)[0]
        text_w, text_h = text_size

        padding_x = 20
        padding_y = 20
        text_x = width - text_w - padding_x
        text_y = height - padding_y

        # 绘制时间水印
        cv2.putText(
            frame,
            timestamp_str,
            (text_x, text_y),
            font,
            font_scale,
            color,
            thickness,
            line_type,
        )

        # 保存截图
        filename = f"{saved_count + 1:06d}.jpg"
        filepath = os.path.join(output_dir, filename)

        cv2.imwrite(filepath, frame)
        saved_count += 1

        # 每完成约 10% 输出一次进度
        if (idx + 1) % max(1, total_to_extract // 10) == 0 or (
            idx + 1
        ) == total_to_extract:
            print(f"    进度: {idx + 1}/{total_to_extract} (已保存 {saved_count} 张)")

    cap.release()
    print(f"\n[+] 任务完成！所有截图已保存在目录: '{output_dir}'")
    print(f"[+] 实际成功保存: {saved_count} 张图片。")


if __name__ == "__main__":
    # ---- 参数配置 ----
    VIDEO_FILE = "VID_20260611_104405.mp4"
    FRAME_INTERVAL = 9000  # 帧
    OUTPUT_FOLDER = "video_snapshots_with_time"

    # 从视频第几秒开始抽取
    START_TIME_SECONDS = 0

    extract_frames_fast_with_watermark(
        VIDEO_FILE, FRAME_INTERVAL, OUTPUT_FOLDER, start_sec=START_TIME_SECONDS
    )