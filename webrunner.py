# webrunner.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

from bottle import Bottle, request, response
import webbrowser
import threading
import time
import random

print(">>> webrunner.py LOADED - VERSION 2025-01-16 20:30 - SYNC EVENT PROCESSING <<<")

app = Bottle()

_window_instance = None
_app_name = 'app'
_pending_render = None
_render_lock = threading.Lock()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }}

        .ng-container {{
            background-color: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
        }}

        .ng-row {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            gap: 10px;
        }}

        .ng-text {{
            display: inline-block;
            padding: 5px;
        }}

        .ng-input {{
            padding: 6px 10px;
            border: 1px solid #ccc;
            border-radius: 3px;
            font-size: 14px;
            min-width: 200px;
        }}

        .ng-input:focus {{
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 3px rgba(76, 175, 80, 0.3);
        }}

        .ng-button {{
            padding: 6px 20px;
            background-color: #e0e0e0;
            border: 1px solid #999;
            border-radius: 3px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s;
        }}

        .ng-button:hover {{
            background-color: #d0d0d0;
        }}

        .ng-button:active {{
            background-color: #c0c0c0;
        }}

        .htmx-request .ng-button {{
            opacity: 0.6;
            cursor: wait;
        }}
    </style>
</head>
<body>
    <form autocomplete="off" autocorrect="off" autocapitalize="off">
        {content}
    </form>
</body>
</html>
'''


@app.route('/')
def index():
    """Render initial page"""
    global _window_instance

    print("\n" + "=" * 60)
    print(">>> ROUTE / CALLED - Loading initial page")
    print("=" * 60)

    if _window_instance is None:
        response.status = 500
        return "No window instance configured"

    # Reset all input elements
    print("\n=== RESETTING ALL ELEMENTS ===")
    for key, element in _window_instance.element_keys.items():
        if hasattr(element, 'element_type') and element.element_type == 'input':
            element.value = ''
            element.content = ''

    html_content = _window_instance.render()
    
    response.set_header('Cache-Control', 'no-store, no-cache, must-revalidate')
    response.set_header('Pragma', 'no-cache')
    response.set_header('Expires', '0')

    return HTML_TEMPLATE.format(title=_window_instance.title, content=html_content)


@app.route('/event/<app_name>', method='POST')
def handle_event(app_name):
    """Handle HTMX events - Process in app thread context"""
    global _window_instance, _pending_render

    if _window_instance is None:
        response.status = 500
        return "No window instance"

    event_key = request.forms.get('event_key', '')

    print(f"\n=== EVENT RECEIVED: {event_key} ===")

    # Collect form values
    values = {}
    for form_key in request.forms.keys():
        if form_key != 'event_key':
            parts = form_key.split('_')
            original_key = parts[0] if '_' in form_key else form_key
            values[original_key] = request.forms.get(form_key, '')
            print(f"  {original_key} = '{values[original_key]}'")

    # Update element values to preserve input state
    for key, value in values.items():
        if key in _window_instance.element_keys:
            element = _window_instance.element_keys[key]
            if hasattr(element, 'element_type') and element.element_type == 'input':
                element.value = value
                element.content = value

    # Put event in queue so application loop can process it
    _window_instance.event_queue.put((event_key, values))
    
    # Wait for application to process and signal render ready
    # The application's while loop will process the event and call update()
    # Then it will signal us to render
    
    with _render_lock:
        # Wait briefly for processing
        time.sleep(0.05)
        
        # Render current state
        html_content = _window_instance.render()

    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    response.set_header('Pragma', 'no-cache')
    response.set_header('Expires', '0')

    print(f"=== EVENT PROCESSED, HTML SENT ===\n")

    return html_content


def run(window, port=25000, debug=False, open_browser=True):
    """Run Bottle server"""
    global _window_instance, _app_name

    _window_instance = window
    _app_name = window.app_name

    if open_browser:
        def open_browser_delayed():
            time.sleep(1.5)
            cache_buster = random.randint(100000, 999999)
            webbrowser.open(f'http://localhost:{port}?v={cache_buster}')

        threading.Thread(target=open_browser_delayed, daemon=True).start()

    print(f"\n{'=' * 60}")
    print(f"  pyNaviGuiWeb Server Starting (Bottle)")
    print(f"{'=' * 60}")
    print(f"  Application: {_app_name}")
    print(f"  URL: http://localhost:{port}")
    print(f"  Press CTRL+C to stop")
    print(f"{'=' * 60}\n")

    try:
        app.run(host='localhost', port=port, debug=debug, reloader=False, quiet=not debug)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    finally:
        print("Cleanup completed.")
