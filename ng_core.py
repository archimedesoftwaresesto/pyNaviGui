# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import queue

class NgCore:
    """Base class for pyNaviGui - manages window, events and core logic"""

    def __init__(self, geometry='800x600', embed_mode=False, parent_root=None):
        """Initialize GUI with embedded mode support"""
        self.title = 'pyNaviGui'
        self.geometry = geometry
        self.window_closed = False
        self.event_queue = queue.Queue()
        self.event_handlers = {}
        self.initial_elements_count = 0

        self.embed_mode = embed_mode

        if embed_mode:
            if parent_root is None:
                raise ValueError("parent_root is required when embed_mode=True")
            self.root = parent_root
        else:
            self.root = tk.Tk()
            self._update_title_impl()
            self._update_geometry_impl()
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        if hasattr(self, '_init_defaults'):
            self._init_defaults()
        if hasattr(self, '_init_layout'):
            self._init_layout()
        if hasattr(self, '_init_elements'):
            self._init_elements()

    def _on_closing(self):
        """Handle window closing"""
        self.window_closed = True
        self.event_queue.put((None, {}))

    def _update_title_impl(self):
        """Update window title"""
        if hasattr(self, 'root'):
            self.root.title(self.title)

    def _update_geometry_impl(self):
        """Update window geometry"""
        if hasattr(self, 'root') and self.geometry:
            self.root.geometry(self.geometry)

    def _close_impl(self):
        """Close implementation"""
        if hasattr(self, 'root') and not self.window_closed:
            self.root.quit()
            self.root.destroy()

    def _delete_element_impl(self, element):
        """Remove element from GUI"""
        if hasattr(element, 'destroy'):
            element.destroy()

    def win_title(self, title):
        """Set window title"""
        self.title = title
        self._update_title_impl()
        return self

    def win_size(self, geometry):
        """Set window geometry"""
        self.geometry = geometry
        self._update_geometry_impl()
        return self

    def register_event_handler(self, event_key, handler_func):
        """Register event handler"""
        self.event_handlers[event_key] = handler_func

    def process_event(self, event_key, values):
        """Process event with registered handler"""
        if event_key in self.event_handlers:
            return self.event_handlers[event_key](values)
        return None

    def show(self):
        """Start main loop"""
        self.root.mainloop()
        return self

    def read(self, timeout=None):
        """Read next event"""
        if self.window_closed:
            return None, {}

        try:
            self.root.update()

            if not self.event_queue.empty():
                event, values = self.event_queue.get_nowait()
                return event, values
            else:
                return '', {}

        except tk.TclError:
            self.window_closed = True
            return None, {}

    def close(self):
        """Close window if not in embedded mode"""
        if not self.embed_mode:
            self.window_closed = True
            self._close_impl()