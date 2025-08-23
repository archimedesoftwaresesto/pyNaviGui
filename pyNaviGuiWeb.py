# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import webbrowser
import threading
import queue
import time
from bottle import Bottle, run, request, static_file, response

# Istanza globale per comunicare con Bottle
ng_instance = None

# Crea l'app Bottle
app = Bottle()


@app.route('/')
def index():
    """Serve la pagina principale"""
    global ng_instance
    if ng_instance:
        response.content_type = 'text/html'
        return ng_instance.get_html()
    return "No GUI instance"


@app.route('/event', method='POST')
def handle_event():
    """Gestisce gli eventi POST dal form"""
    global ng_instance
    if not ng_instance:
        return "No GUI instance"

    # Ottieni i dati del form
    event_key = request.forms.get('event', '')

    print(f"DEBUG: Received event: {event_key}")  # Debug
    print(f"DEBUG: Form data: {dict(request.forms)}")  # Debug

    # Raccogli tutti i valori degli input
    values = {}
    for key in request.forms:
        if key != 'event' and key.startswith('-') and key.endswith('-'):
            values[key] = request.forms.get(key, '')

    print(f"DEBUG: Processed values: {values}")  # Debug

    # Aggiungi l'evento alla coda
    ng_instance.event_queue.put((event_key, values))

    # Risposta per HTMX - più visibile
    return f'<div style="color: green; font-weight: bold;">Event {event_key} processed successfully!</div>'


@app.route('/events')
def events():
    """Server-Sent Events endpoint"""
    global ng_instance
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'
    response.connection = 'keep-alive'
    response.access_control_allow_origin = '*'

    def event_stream():
        while ng_instance and not ng_instance.window_closed:
            yield "data: ping\n\n"
            time.sleep(1)

    return event_stream()


class Ng:
    def __init__(self, geometry='800x600'):
        self.title = 'Window'
        self.geometry = geometry
        self.elements = []
        self.element_keys = {}
        self.event_queue = queue.Queue()
        self.window_closed = False
        self.server_thread = None
        self.server_started = False

        # Coordinate correnti
        self.current_x = 0
        self.current_y = 0
        self.x0 = 0
        self.y0 = 0

        # Port per il server HTTP
        self.port = 8000

        # Avvia automaticamente il server
        self._start_server()

    def _start_server(self):
        """Avvia il server Bottle in un thread separato"""
        global ng_instance
        ng_instance = self

        def run_server():
            try:
                run(app, host='localhost', port=self.port, quiet=True)
            except OSError:
                # Porta occupata, prova la successiva
                self.port += 1
                if self.port < 8010:  # Limita i tentativi
                    run(app, host='localhost', port=self.port, quiet=True)

        try:
            self.server_thread = threading.Thread(target=run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            time.sleep(1.0)  # Aspetta che il server si avvii
            self.server_started = True

            # Apri automaticamente il browser
            url = f'http://localhost:{self.port}'
            webbrowser.open(url)
            print(f"Server started at {url}")

            return True
        except:
            return False

    def show(self):
        """Compatibilità - il server è già avviato"""
        return self

    def winTitle(self, title):
        self.title = title
        return self

    def winGeometry(self, geometry):
        self.geometry = geometry
        return self

    def goto(self, x, y):
        self.current_x = x
        self.current_y = y
        return self

    def gotoy(self, value):
        self.current_x = self.x0
        self.current_y = value
        return self

    def setX(self, value):
        self.x0 = value
        self.current_x = value
        return self

    def setY(self, value):
        self.y0 = value
        self.current_y = value
        return self

    def text(self, text='', k=''):
        element = {
            'type': 'text',
            'text': text,
            'x': self.current_x,
            'y': self.current_y,
            'key': k
        }
        self.elements.append(element)

        # Stima approssimativa della larghezza del testo (8px per carattere)
        width = len(text) * 8 + 10
        self.current_x += width

        if k:
            self.element_keys[k] = element

        return self

    def input(self, text='', k=''):
        element = {
            'type': 'input',
            'value': text,
            'x': self.current_x,
            'y': self.current_y,
            'key': k
        }
        self.elements.append(element)

        # Larghezza standard di un input
        width = 120
        self.current_x += width

        if k:
            self.element_keys[k] = element

        return self

    def button(self, text='', k='', command=None):
        element = {
            'type': 'button',
            'text': text,
            'x': self.current_x,
            'y': self.current_y,
            'key': k,
            'command': command
        }
        self.elements.append(element)

        # Stima della larghezza del bottone
        width = len(text) * 8 + 30
        self.current_x += width

        if k:
            self.element_keys[k] = element

        return self

    def get_html(self):
        """Genera l'HTML della finestra"""
        # Estrai dimensioni dalla geometria
        if 'x' in self.geometry:
            width, height = self.geometry.split('x')
        else:
            width, height = '800', '600'

        # Raccogli tutte le chiavi degli input per il form
        input_keys = [elem['key'] for elem in self.elements if elem['type'] == 'input' and elem['key']]

        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            position: relative;
        }}
        .container {{
            position: relative;
            width: {width}px;
            height: {height}px;
            border: 1px solid #ccc;
            background: #f0f0f0;
        }}
        .element {{
            position: absolute;
            font-size: 12px;
            font-family: Arial, sans-serif;
        }}
        .text-element {{
            background: transparent;
            border: none;
            pointer-events: none;
        }}
        .input-element {{
            border: 1px solid #ccc;
            padding: 2px 4px;
            background: white;
            font-size: 12px;
        }}
        .button-element {{
            background: #e0e0e0;
            border: 1px solid #999;
            padding: 4px 8px;
            cursor: pointer;
            font-size: 12px;
        }}
        .button-element:hover {{
            background: #d0d0d0;
        }}
        .button-element:active {{
            background: #c0c0c0;
        }}
        #response {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #ffffcc;
            border: 1px solid #cccc00;
            padding: 5px;
            min-width: 200px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <form id="mainForm">
            <!-- Campo nascosto per l'evento -->
            <input type="hidden" name="event" value="">
'''

        # Aggiungi tutti gli input nascosti per mantenere i valori
        for key in input_keys:
            html += f'            <input type="hidden" name="{key}" value="">\n'

        # Genera gli elementi
        for element in self.elements:
            if element['type'] == 'text':
                html += f'''        <div class="element text-element" style="left: {element['x']}px; top: {element['y']}px;">
            {element['text']}
        </div>
'''
            elif element['type'] == 'input':
                html += f'''        <input class="element input-element" style="left: {element['x']}px; top: {element['y']}px;" 
               type="text" name="{element['key']}" value="{element['value']}"
               oninput="updateHiddenField(this)">
'''
            elif element['type'] == 'button':
                html += f'''        <button class="element button-element" style="left: {element['x']}px; top: {element['y']}px;"
               type="button"
               onclick="submitEvent('{element['key']}')">
            {element['text']}
        </button>
'''

        html += '''        </form>
        <div id="response"></div>
    </div>

    <script>
        function updateHiddenField(input) {
            const hiddenField = document.querySelector(`input[type="hidden"][name="${input.name}"]`);
            if (hiddenField) {
                hiddenField.value = input.value;
            }
        }

        function submitEvent(eventKey) {
            // Aggiorna il campo evento
            document.querySelector('input[name="event"]').value = eventKey;

            // Aggiorna tutti i campi nascosti con i valori correnti
            const visibleInputs = document.querySelectorAll('input.input-element');
            visibleInputs.forEach(input => {
                updateHiddenField(input);
            });

            // Raccogli i dati del form
            const formData = new FormData(document.getElementById('mainForm'));

            // Debug: mostra i dati inviati
            console.log('Sending data:');
            for (let [key, value] of formData.entries()) {
                console.log(key + ': ' + value);
            }

            // Invia la richiesta
            fetch('/event', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('response').innerHTML = html;
                document.getElementById('response').style.display = 'block';

                // Nascondi il messaggio dopo 3 secondi
                setTimeout(() => {
                    document.getElementById('response').style.display = 'none';
                }, 3000);
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('response').innerHTML = '<div style="color: red;">Error processing event</div>';
                document.getElementById('response').style.display = 'block';
            });
        }

        // Chiudi la finestra quando si chiude il browser
        window.addEventListener('beforeunload', function() {
            fetch('/event', {
                method: 'POST',
                body: 'event=close',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                keepalive: true
            });
        });
    </script>
</body>
</html>'''
        return html

    def read(self, timeout=None):
        """Legge il prossimo evento"""
        if self.window_closed:
            return None, {}

        try:
            # Usa un timeout più breve per essere più reattivo
            if timeout is None:
                timeout = 0.1

            try:
                event, values = self.event_queue.get(timeout=timeout)
                if event == 'close':
                    self.window_closed = True
                    return None, {}
                return event, values
            except queue.Empty:
                # Nessun evento disponibile, restituisce stringa vuota
                return '', {}

        except:
            return '', {}

    def close(self):
        """Chiude la finestra"""
        self.window_closed = True
        global ng_instance
        ng_instance = None