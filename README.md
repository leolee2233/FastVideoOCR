# FastVideoOCR

一个轻量级、零过度设计的**高效率大视频数字提取流水线**。

本项目通过 OpenCV 的跳跃式定位技术解决大视频处理缓慢的痛点，配合精准矩阵裁剪去除背景噪声，最终利用轻量级 AI (EasyOCR) 实现静态帧数字的结构化提取，直接落地为标准的 `.csv` 数据报表。

---

## 🛠️ 项目目录结构

整个流水线由三个逻辑极其扁平的独立脚本组成，按顺序串联执行：

```text
FastVideoOCR/
│
├── step1_frame_extractor.py   # 快速跳跃抽帧 + 时间水印
├── step2_image_cropper.py     # 批量图片矩阵裁剪
├── step3_ocr_processor.py     # AI 数字识别 + 数据导出
│
└── README.md                  # 本说明文档
