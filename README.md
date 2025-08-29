# 🖥️ Remote Desktop Streamer (Flask + PyAutoGUI)

A lightweight Flask application to **live-stream your desktop**, and **remotely control mouse and keyboard** from any browser.

Supports:
- 🖼️ Live screen streaming (MJPEG)
- 🖱️ Mouse clicks and dragging
- ⌨️ Keyboard input
- 🎛️ Adjustable stream quality
- 🎯 Accurate screen-to-browser coordinate mapping
- 📏 Responsive UI (screen scales to fit browser)

---

## 🚀 Features

| Feature             | Description                                      |
|---------------------|--------------------------------------------------|
| ✅ Live stream       | Real-time screen feed over HTTP                 |
| ✅ Mouse control     | Click and drag anywhere from browser            |
| ✅ Keyboard control  | Type keystrokes remotely                        |
| ✅ Quality control   | Switch stream compression on-the-fly            |
| ✅ FPS counter       | Shows current frame rate in browser             |
| ✅ Responsive UI     | Image auto-scales to browser size               |

---

## 📸 Demo Screenshot

![screenshot](https://via.placeholder.com/800x450?text=Live+Stream+Preview)

---

## 🛠 Requirements

- Python 3.7+
- GUI-enabled Linux (X11), macOS, or Windows
- `pip install` the following:

```bash
pip install flask opencv-python-headless pyautogui mss
```

## ▶️ Run the App
```bash
python app.py
```
Then open:
```bash
http://<your-ip>:5000
```
Replace <your-ip> with your local IP address if accessing from another device.
