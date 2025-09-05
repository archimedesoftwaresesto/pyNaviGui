# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    print("ERROR: PIL/Pillow not installed. Install with: pip install Pillow")
    Image = None
    ImageTk = None

class NgElementsBase00:
    """Core elements management and basic UI elements"""

    def _init_elements(self):
        """Initialize element variables"""
        self.elements = []
        self.element_keys = {}
        self.element_positions = {}
        self.element_strings = {}
        self.element_counter = 0

    def _register_element(self, element, key, s=''):
        """Register element with key and selection string"""
        self.elements.append(element)

        if not key:
            key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        self.element_keys[key] = element

        if s:
            self.element_strings[key] = s

    def _register_element_position(self, key, x, y, width, height):
        """Register element position"""
        if key:
            self.element_positions[key] = (x, y, width, height)

    def text(self, text='', k='', s='', fg='', bg=''):
        """Create text element using Tkinter Label"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        label_options = {'text': text}
        if fg:
            label_options['fg'] = fg
        if bg:
            label_options['bg'] = bg

        if self.text_width_chars is not None:
            label_options['width'] = self.text_width_chars
            label_options['anchor'] = 'w'
        if self.text_height_lines is not None and self.text_height_lines > 1:
            label_options['height'] = self.text_height_lines

        label = tk.Label(self.root, **label_options)
        label.place(x=self.current_x, y=self.current_y)
        label.update_idletasks()
        width = label.winfo_reqwidth()
        height = label.winfo_reqheight()

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(label, k, s)

        return self

    def input(self, text='', k='', s='', set_focus=False, event_enter=False, event_tab=False):
        """Create input element with optional auto-focus and keyboard event handling"""
        s, _, _, k = self._merge_defaults(s, '', '', k)

        entry_options = {}
        if self.input_width_chars is not None:
            entry_options['width'] = self.input_width_chars

        entry = tk.Entry(self.root, **entry_options)
        if text:
            entry.insert(0, text)

        # Handle Enter key press event
        if event_enter and k:
            def enter_handler(event):
                values = self._get_values()
                self.event_queue.put((k, values))

            entry.bind("<Return>", enter_handler)

        # Handle Tab key press event
        if event_tab and k:
            def tab_handler(event):
                values = self._get_values()
                self.event_queue.put((f"{k}_TAB", values))
                # Allow focus to move to the next widget (don't return 'break')

            entry.bind("<Tab>", tab_handler)

        entry.place(x=self.current_x, y=self.current_y)
        entry.update_idletasks()
        width = entry.winfo_reqwidth()
        height = entry.winfo_reqheight()

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(entry, k, s)

        # Set focus if requested
        if set_focus and k:
            # Use after() to ensure the element is fully created before setting focus
            self.root.after(10, lambda: self.set_focus(k))

        return self

    def button(self, text='', k='', s='', command=None):
        """Create button using Tkinter Button"""
        s, _, _, k = self._merge_defaults(s, '', '', k)

        def button_callback():
            if k:
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        button = tk.Button(self.root, text=text, command=button_callback)
        button.place(x=self.current_x, y=self.current_y)
        button.update_idletasks()
        width = button.winfo_reqwidth()
        height = button.winfo_reqheight()

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(button, k, s)

        return self