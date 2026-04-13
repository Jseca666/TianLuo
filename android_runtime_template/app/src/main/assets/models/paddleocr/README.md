# PaddleOCR Assets Layout

This directory is reserved for app-bundled PaddleOCR model assets.

Expected structure:

- `det/` for detection model assets
- `rec/` for recognition model assets
- `cls/` for classification model assets
- `labels/ppocr_keys_v1.txt` for OCR labels

Current status:

- Real PaddleOCR model files are not committed to the repository.
- Use the repository host-side preparation scripts to download official PaddleOCR assets and then copy or package them into the Android project when needed.
