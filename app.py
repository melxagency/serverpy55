from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import os

app = Flask(__name__)
CORS(app)

sessions = {}

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=NetworkService")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver

def execute_selenium_command(driver, command):
    try:
        if command.startswith('driver.'):
            command = command.replace('driver.', '')

        if command.startswith('get('):
            url = command.split('"')[1] if '"' in command else command.split("'")[1]
            driver.get(url)
            return {"result": f"Navigated to {url}", "success": True}

        elif command == 'title':
            return {"result": driver.title, "success": True}

        elif command == 'current_url':
            return {"result": driver.current_url, "success": True}

        elif command == 'page_source':
            return {"result": driver.page_source[:1000] + "...", "success": True}

        elif command.startswith('find_element'):
            parts = command.split(',')
            by_type = parts[0].split('By.')[1].split(')')[0].strip()
            selector = parts[1].split('"')[1] if '"' in parts[1] else parts[1].split("'")[1]

            by_map = {
                'ID': By.ID,
                'NAME': By.NAME,
                'CLASS_NAME': By.CLASS_NAME,
                'TAG_NAME': By.TAG_NAME,
                'CSS_SELECTOR': By.CSS_SELECTOR,
                'XPATH': By.XPATH
            }

            element = driver.find_element(by_map.get(by_type, By.ID), selector)

            if '.send_keys(' in command:
                text = command.split('send_keys(')[1].split('"')[1] if '"' in command else command.split('send_keys(')[1].split("'")[1]
                element.send_keys(text)
                return {"result": f"Sent keys: {text}", "success": True}

            elif '.click()' in command:
                element.click()
                return {"result": "Element clicked", "success": True}

            elif '.text' in command:
                return {"result": element.text, "success": True}

            else:
                return {"result": "Element found", "success": True}

        elif command == 'back()':
            driver.back()
            return {"result": "Navigated back", "success": True}

        elif command == 'forward()':
            driver.forward()
            return {"result": "Navigated forward", "success": True}

        elif command == 'refresh()':
            driver.refresh()
            return {"result": "Page refreshed", "success": True}

        elif command.startswith('execute_script'):
            script = command.split('"')[1] if '"' in command else command.split("'")[1]
            result = driver.execute_script(script)
            return {"result": str(result), "success": True}

        else:
            result = eval(f'driver.{command}')
            return {"result": str(result), "success": True}

    except Exception as e:
        return {"result": None, "success": False, "error": str(e)}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Selenium backend is running"})

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.json
        session_id = data.get('session_id')
        command = data.get('command')

        if not session_id or not command:
            return jsonify({
                "success": False,
                "error": "Missing session_id or command"
            }), 400

        if session_id not in sessions:
            sessions[session_id] = create_driver()

        driver = sessions[session_id]
        result = execute_selenium_command(driver, command)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/close-session', methods=['POST'])
def close_session():
    try:
        data = request.json
        session_id = data.get('session_id')

        if session_id in sessions:
            sessions[session_id].quit()
            del sessions[session_id]
            return jsonify({"success": True, "message": "Session closed"})

        return jsonify({"success": False, "error": "Session not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
