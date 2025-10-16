# ngweb_runner.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

"""
Universal runner for pyNaviGui
Allows IDENTICAL code for desktop and web versions
Usage:
    python myapp.py        # Desktop mode
    python myapp.py --web  # Web mode
"""

import sys
import os


def is_web_mode():
    """Check if running in web mode"""
    return '--web' in sys.argv


# Make IS_WEB available as module attribute
IS_WEB = is_web_mode()


class SafeValueDict:
    """Dict wrapper that safely handles both desktop and web value access"""
    
    def __init__(self, data):
        self._data = data if isinstance(data, dict) else {}
    
    def __getitem__(self, key):
        """Allow dict[key] syntax - returns '' if key missing (web-safe)"""
        return self._data.get(key, '')
    
    def get(self, key, default=''):
        """Standard get method"""
        return self._data.get(key, default)
    
    def __contains__(self, key):
        return key in self._data
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()
    
    def __repr__(self):
        return f"SafeValueDict({self._data})"


def run_event_loop(window, event_handler_func):
    """
    Universal event loop runner
    
    Args:
        window: The Ng window instance
        event_handler_func: Function(event, values) -> bool/None
                           Return True if event handled
                           Return None to close app
    """
    
    if IS_WEB:
        # === WEB MODE ===
        print("Running in WEB mode...")
        
        # Store window creation function for re-initialization
        import sys
        import importlib
        
        # Get the module that created the window
        caller_frame = sys._getframe(1)
        caller_module = caller_frame.f_globals.get('__name__')
        
        # Wrap user's event handler for web
        def web_event_handler(event_key, values):
            # Convert to SafeValueDict so values[KEY] works safely
            safe_values = SafeValueDict(values)
            result = event_handler_func(event_key, safe_values)
            return result
        
        # Register handler
        window.set_event_handler(web_event_handler)
        
        # Set app_name if not already set
        if not hasattr(window, 'app_name') or not window.app_name:
            script_name = os.path.basename(sys.argv[0]).replace('.py', '')
            window.app_name = script_name
        
        # Store initial state factory
        window._initial_elements_state = {}
        for key, element in window.element_keys.items():
            if hasattr(element, 'value'):
                window._initial_elements_state[key] = element.value
        
        # Start web server
        import webrunner
        webrunner.run(window, port=25000)
    
    else:
        # === DESKTOP MODE ===
        print("Running in DESKTOP mode...")
        
        while True:
            event, values = window.read()
            
            # Call user's event handler
            result = event_handler_func(event, values)
            
            # Check if should close
            if result is None or event is None:
                break
        
        # Close window
        window.close()


# Shorthand alias
run = run_event_loop
