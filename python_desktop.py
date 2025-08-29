from flask import Flask, Response, render_template_string, request, jsonify
import cv2, pyautogui, mss, time
import numpy as np

app = Flask(__name__)
pyautogui.FAILSAFE = False  # Disable crash-causing check on moveTo

HTML = """
<!doctype html>
<html>
<head>
    <title>Desktop Live Stream</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
            background: black;
            font-family: sans-serif;
        }

        #controls {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 10;
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 5px;
            color: white;
        }

        #stream-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
        }

        #stream {
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
            aspect-ratio: 16 / 9;
            cursor: crosshair;
        }
    </style>
</head>
<body>
    <div id="controls">
        <label>
            Quality:
            <select id="quality">
                <option value="30">Low</option>
                <option value="50" selected>Medium</option>
                <option value="70">High</option>
            </select>
        </label>
        <div>FPS: <span id="fps">0</span></div>
    </div>

    <div id="stream-container">
        <img id="stream" src="{{ url_for('video_feed') }}">
    </div>

    <script>
    // Save selected quality
    document.getElementById('quality').addEventListener('change', function() {
        document.cookie = 'quality=' + this.value;
        location.reload();
    });

    // FPS counter
    let lastTime = performance.now();
    let frameCount = 0;
    function updateFPS() {
        const now = performance.now();
        frameCount++;
        if (now - lastTime >= 1000) {
            document.getElementById('fps').innerText = frameCount;
            frameCount = 0;
            lastTime = now;
        }
        requestAnimationFrame(updateFPS);
    }
    updateFPS();

    // Mouse click coordinates
    const img = document.getElementById('stream');
    img.addEventListener('click', function(e) {
        const rect = img.getBoundingClientRect();
        const x = (e.clientX - rect.left) / img.width;
        const y = (e.clientY - rect.top) / img.height;
        fetch('/mouse_click', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({x, y})
        });
    });

    // Keyboard input
    document.addEventListener('keydown', function(e) {
        fetch('/key_press', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ key: e.key })
        });
    });

    // Mouse dragging
    let isDragging = false;
    img.addEventListener('mousedown', () => isDragging = true);
    img.addEventListener('mouseup', () => isDragging = false);
    img.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        const rect = img.getBoundingClientRect();
        const x = (e.clientX - rect.left) / img.width;
        const y = (e.clientY - rect.top) / img.height;
        fetch('/mouse_drag', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({x, y})
        });
    });
    </script>
</body>
</html>
"""

def capture_screen(quality):
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        while True:
            screenshot = sct.grab(monitor)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/video_feed')
def video_feed():
    quality = int(request.cookies.get('quality', 50))
    return Response(capture_screen(quality),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mouse_click', methods=['POST'])
def mouse_click():
    data = request.get_json()
    x_ratio = data['x']
    y_ratio = data['y']
    screen_w, screen_h = pyautogui.size()
    x = int(x_ratio * screen_w)
    y = int(y_ratio * screen_h)
    pyautogui.click(x, y)
    return jsonify(success=True)
    
@app.route('/mouse_drag', methods=['POST'])
def mouse_drag():
    data = request.get_json()
    x_ratio = data['x']
    y_ratio = data['y']
    screen_w, screen_h = pyautogui.size()
    x = int(x_ratio * screen_w)
    y = int(y_ratio * screen_h)
    try:
        pyautogui.moveTo(x, y)
        return jsonify(success=True)
    except Exception as e:
        print(f"[mouse_drag ERROR] {e}")
        return jsonify(success=False, error=str(e))


    
@app.route('/key_press', methods=['POST'])
def key_press():
    data = request.get_json()
    key = data['key']
    try:
        pyautogui.press(key)
    except Exception as e:
        return jsonify(success=False, error=str(e))
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
