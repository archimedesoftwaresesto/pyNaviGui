# ngweb_core.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import queue
import threading
import time

print(">>> ngweb_core.py LOADED - VERSION 2025-01-16 20:30 - QUEUE-BASED EVENTS <<<")

class NgWebCore:
    """Core class for web-based pyNaviGui"""
    
    def __init__(self, geometry='800x600', app_name=None):
        self.title = 'pyNaviGui Web'
        self.geometry = geometry
        
        if app_name is None:
            import os
            import sys
            app_name = os.path.basename(sys.argv[0]).replace('.py', '')
        
        self.app_name = app_name
        self.event_queue = queue.Queue()
        self.event_handler = None
        
        # Virtual DOM
        self.elements = []
        self.element_keys = {}
        self.element_positions = {}
        self.element_strings = {}
        self.element_counter = 0
        self.initial_elements_count = 0
        
        # Server management
        self._server_started = False
        self._server_thread = None
        self._server_ready = threading.Event()
        
        if hasattr(self, '_init_defaults'):
            self._init_defaults()
        if hasattr(self, '_init_layout'):
            self._init_layout()
    
    def render(self):
        """Generate complete HTML"""
        html_parts = ['<div id="ng-container" class="ng-container">']
        
        current_row = []
        
        for element in self.elements:
            if hasattr(element, 'element_type') and element.element_type == 'br':
                if current_row:
                    html_parts.append('<div class="ng-row">')
                    html_parts.extend(current_row)
                    html_parts.append('</div>')
                    current_row = []
                
                spacing = element.attributes.get('spacing', 0)
                if spacing > 0:
                    html_parts.append(f'<div style="height: {spacing}px;"></div>')
            else:
                current_row.append(element.to_html())
        
        if current_row:
            html_parts.append('<div class="ng-row">')
            html_parts.extend(current_row)
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        return '\n'.join(html_parts)
    
    def read(self, timeout=None):
        """Read next event from queue"""
        
        # Start server on first call
        if not self._server_started:
            self._start_web_server()
            self._server_started = True
            self._server_ready.wait(timeout=5)
        
        # Wait for events from HTTP requests
        try:
            event, values = self.event_queue.get(timeout=0.5 if timeout is None else timeout)
            return event, values
        except queue.Empty:
            return '', {}
        except KeyboardInterrupt:
            return None, {}
    
    def _start_web_server(self):
        """Start web server in background thread"""
        import webrunner
        
        print("\n" + "="*60)
        print("  Starting Web Server...")
        print("="*60)
        
        if not hasattr(self, 'app_name') or not self.app_name:
            import os
            import sys
            script_name = os.path.basename(sys.argv[0]).replace('.py', '')
            self.app_name = script_name
        
        def run_server():
            self._server_ready.set()
            webrunner.run(self, port=25001, open_browser=True)
        
        self._server_thread = threading.Thread(target=run_server, daemon=True)
        self._server_thread.start()
        
        print("  Server thread started, waiting for events...")
        print("="*60 + "\n")
    
    def close(self):
        """Cleanup resources"""
        self.event_queue.put((None, {}))
    
    def win_title(self, title):
        """Set window title"""
        self.title = title
        return self
    
    def win_size(self, geometry):
        """Set window size"""
        self.geometry = geometry
        return self
    
    def set_event_handler(self, handler_func):
        """Set event handler"""
        self.event_handler = handler_func
        return self
    
    def _get_values(self):
        """Collect all values from input elements"""
        values = {}
        
        for key, element in self.element_keys.items():
            if not key.startswith('__auto_key_'):
                if hasattr(element, 'value'):
                    values[key] = element.value
        
        return values
    
    def finalize_layout(self):
        """Store initial element count"""
        self.initial_elements_count = len(self.elements)
        return self
