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

    def text(self, text='', k='', s='', fg='', bg='', font=None):
        """Create text element using Tkinter Label"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        label_options = {'text': text}
        if fg:
            label_options['fg'] = fg
        if bg:
            label_options['bg'] = bg

        # Handle font parameter
        if font is not None:
            # Support both string format ('Arial 12 bold') and tuple format (('Arial', 12, 'bold'))
            if isinstance(font, str):
                label_options['font'] = font
            elif isinstance(font, tuple):
                # Convert the tuple to the format tkinter expects
                if len(font) == 2:  # ('Arial', 12)
                    family, size = font
                    label_options['font'] = (family, size)
                elif len(font) >= 3:  # ('Arial', 12, 'bold') or ('Arial', 12, 'bold italic')
                    family, size = font[0], font[1]
                    style = ' '.join(font[2:])
                    label_options['font'] = (family, size, style)

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

        # Update the row height based on actual element height
        self._update_row_height(height)

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(label, k, s)

        return self

    def input(self, text='', k='', s='', fg='', bg='', font=None, set_focus=False, event_enter=False, event_tab=False,
              event_change=0):
        """Create input element with event handling"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        entry_options = {}
        if self.input_width_chars is not None:
            entry_options['width'] = self.input_width_chars

        # Apply colors if provided
        if fg:
            entry_options['fg'] = fg
        if bg:
            entry_options['bg'] = bg

        # Handle font parameter
        if font is not None:
            # Support both string format ('Arial 12 bold') and tuple format (('Arial', 12, 'bold'))
            if isinstance(font, str):
                entry_options['font'] = font
            elif isinstance(font, tuple):
                # Convert the tuple to the format tkinter expects
                if len(font) == 2:  # ('Arial', 12)
                    family, size = font
                    entry_options['font'] = (family, size)
                elif len(font) >= 3:  # ('Arial', 12, 'bold') or ('Arial', 12, 'bold italic')
                    family, size = font[0], font[1]
                    style = ' '.join(font[2:])
                    entry_options['font'] = (family, size, style)

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
                # Allow focus to move to the next widget

            entry.bind("<Tab>", tab_handler)

        # Handle content change event with delay
        if event_change > 0 and k:
            # Store the previous value to detect actual changes
            entry.previous_value = text
            # Variable to store the timer ID
            entry.after_id = None

            def content_changed(event=None):
                current_value = entry.get()
                # Only trigger if value actually changed
                if current_value != entry.previous_value:
                    entry.previous_value = current_value
                    values = self._get_values()
                    self.event_queue.put((f"{k}_CHANGE", values))

            def on_key_release(event):
                # Cancel previous timer if exists
                if hasattr(entry, 'after_id') and entry.after_id:
                    self.root.after_cancel(entry.after_id)
                # Start new timer
                entry.after_id = self.root.after(event_change, content_changed)

            entry.bind("<KeyRelease>", on_key_release)

        # Improved vertical alignment logic
        y_offset = 0
        if hasattr(self, 'last_element_height'):
            # Get entry's required height before placing it
            entry.pack()
            entry_height = entry.winfo_reqheight()
            entry.pack_forget()

            # Calculate vertical center alignment between the label and entry
            if self.last_element_height > entry_height:
                y_offset = (self.last_element_height - entry_height) // 2
            elif entry_height > self.last_element_height:
                # If entry is taller than label, adjust position upward
                y_offset = -(entry_height - self.last_element_height) // 2

        entry.place(x=self.current_x, y=self.current_y + y_offset)
        entry.update_idletasks()
        width = entry.winfo_reqwidth()
        height = entry.winfo_reqheight()

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y + y_offset, width, height)

        self._update_position(width, height)
        self._register_element(entry, k, s)

        # Set focus if requested
        if set_focus and k:
            # Use after() to ensure the element is fully created before setting focus
            self.root.after(10, lambda: self.set_focus(k))

        return self

    def button(self, text='', k='', s='', fg='', bg='', command=None, font=None):
        """Create button with color and font support, macOS compatible using Canvas"""
        import platform

        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        def button_callback(event=None):
            if k:
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        # Check if we're on macOS and background color is specified
        is_macos = platform.system() == 'Darwin'

        if is_macos and bg:
            # Create a Canvas-based button for macOS with background color support

            # First create a temporary label to measure text size
            temp_label = tk.Label(self.root, text=text)
            if font is not None:
                if isinstance(font, str):
                    temp_label.config(font=font)
                elif isinstance(font, tuple):
                    if len(font) == 2:
                        family, size = font
                        temp_label.config(font=(family, size))
                    elif len(font) >= 3:
                        family, size = font[0], font[1]
                        style_part = ' '.join(font[2:])
                        temp_label.config(font=(family, size, style_part))

            temp_label.update_idletasks()
            text_width = temp_label.winfo_reqwidth()
            text_height = temp_label.winfo_reqheight()
            temp_label.destroy()

            # Create canvas with padding
            padding_x = 20
            padding_y = 8
            canvas_width = text_width + padding_x
            canvas_height = text_height + padding_y

            canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height,
                               highlightthickness=0, bd=0)

            # Draw button background
            canvas.create_rectangle(0, 0, canvas_width, canvas_height,
                                    fill=bg, outline='gray', width=1)

            # Configure text options
            text_options = {
                'text': text,
                'fill': fg if fg else 'black'
            }

            if font is not None:
                if isinstance(font, str):
                    text_options['font'] = font
                elif isinstance(font, tuple):
                    if len(font) == 2:
                        family, size = font
                        text_options['font'] = (family, size)
                    elif len(font) >= 3:
                        family, size = font[0], font[1]
                        style_part = ' '.join(font[2:])
                        text_options['font'] = (family, size, style_part)

            # Draw text centered
            canvas.create_text(canvas_width // 2, canvas_height // 2, **text_options)

            # Bind click events
            canvas.bind("<Button-1>", button_callback)
            canvas.bind("<Enter>", lambda e: canvas.config(cursor="hand2"))
            canvas.bind("<Leave>", lambda e: canvas.config(cursor=""))

            # Add pressed effect
            def on_press(event):
                canvas.configure(relief="sunken", bd=2)

            def on_release(event):
                canvas.configure(relief="flat", bd=0)
                button_callback()

            canvas.bind("<ButtonPress-1>", on_press)
            canvas.bind("<ButtonRelease-1>", on_release)

            button = canvas

        else:
            # Use regular tk.Button for non-macOS or when no background color is specified
            button_options = {'text': text, 'command': button_callback}

            # Apply colors if provided
            if fg:
                button_options['fg'] = fg
            if bg:
                button_options['bg'] = bg

            # Handle font parameter
            if font is not None:
                if isinstance(font, str):
                    button_options['font'] = font
                elif isinstance(font, tuple):
                    if len(font) == 2:
                        family, size = font
                        button_options['font'] = (family, size)
                    elif len(font) >= 3:
                        family, size = font[0], font[1]
                        style_part = ' '.join(font[2:])
                        button_options['font'] = (family, size, style_part)

            button = tk.Button(self.root, **button_options)

        # Common positioning and registration code
        button.place(x=self.current_x, y=self.current_y)
        button.update_idletasks()
        width = button.winfo_reqwidth()
        height = button.winfo_reqheight()

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(button, k, s)

        return self