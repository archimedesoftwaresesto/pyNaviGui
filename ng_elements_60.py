# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk


class NgElementsBase60:
    """Area elements: frames with border and title"""

    def _init_area_elements(self):
        """Initialize area variables"""
        self._area_stack = []
        self._area_positions = {}
        self._current_area = None
        self._orig_root = None
        self._current_root = None
        self._saved_default_s = []

    def area(self, title='', geometry=None, k='', s='', bg='', border_color='#888888', border_width=1,
             show_close_button=True, close_button_text='X'):
        """Create or close an area (frame with border and optional title)

        Args:
            title: Title for the area (empty string closes current area)
            geometry: Size in format 'WIDTHxHEIGHT' (e.g. '200x150')
            k: Element key
            s: Selection string
            bg: Background color
            border_color: Border color
            border_width: Border width in pixels
            show_close_button: If True, adds a close button to the area title bar
            close_button_text: Text to display on the close button (default 'X')

        Returns:
            self: For method chaining
        """
        s, _, bg, k = self._merge_defaults(s, '', bg, k)

        # If title is empty, close current area and return to parent context
        if not title:
            if self._area_stack:
                # Pop the current area from stack
                area_info = self._area_stack.pop()

                # Restore previous positioning context
                self.current_x = area_info['parent_x']
                self.current_y = area_info['parent_y']
                self.initial_x = area_info['parent_initial_x']

                # Restore original selection string
                if self._saved_default_s:
                    self.default_s = self._saved_default_s.pop()

                # Restore the original root for subsequent elements
                if not self._area_stack:
                    self._current_root = self._orig_root
                else:
                    self._current_root = self._area_stack[-1]['frame']

                return self
            else:
                # No areas to close
                return self

        # Parse geometry if provided
        width, height = 200, 150  # Default size
        if geometry and 'x' in geometry.lower():
            try:
                size_parts = geometry.lower().split('x')
                width = int(size_parts[0])
                height = int(size_parts[1])
            except (ValueError, IndexError):
                pass

        # Create main frame with border
        start_x = self.current_x
        start_y = self.current_y

        # Store original root if not already stored
        if self._orig_root is None:
            self._orig_root = self.root
            self._current_root = self.root

        # Create an effective key if none provided
        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self.element_counter += 1

        # Create outer frame (for border)
        outer_frame = tk.Frame(self._current_root, bd=border_width, relief=tk.GROOVE,
                               highlightbackground=border_color, highlightthickness=border_width)

        # Create inner frame for content
        inner_frame = tk.Frame(outer_frame, bg=bg if bg else self._current_root.cget('bg'))

        title_height = 0
        title_bar = None
        title_label = None
        close_button = None

        # Create title bar if title provided
        if title:
            title_bar = tk.Frame(outer_frame, bg=bg if bg else self._current_root.cget('bg'))
            title_bar.pack(side=tk.TOP, fill=tk.X, anchor=tk.W, padx=2, pady=2)

            # Create title label
            title_label = tk.Label(title_bar, text=title, anchor='w', bg=bg if bg else self._current_root.cget('bg'))
            title_label.pack(side=tk.LEFT, padx=3)

            # For access to button styles and event handling
            close_button = None
            close_button_key = f"{effective_key}_close_btn"

            # Reserve space for button but create it after the area setup is complete
            close_button_frame = None
            if show_close_button:
                close_button_frame = tk.Frame(title_bar, bg=bg if bg else self._current_root.cget('bg'))
                close_button_frame.pack(side=tk.RIGHT, padx=5, pady=2)

            title_bar.update_idletasks()
            title_height = title_bar.winfo_reqheight()

        # Position and size the frames
        inner_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Calculate total height including title and border
        total_height = height + title_height + (2 * border_width) + 10  # 10 for padding

        # Position the outer frame
        outer_frame.place(x=start_x, y=start_y, width=width, height=total_height)
        outer_frame.update_idletasks()

        # Save the current position context before changing
        parent_x = self.current_x
        parent_y = self.current_y
        parent_initial_x = self.initial_x

        # Set new positioning context inside the area
        new_x = 5  # Margin from border
        new_y = 5  # Margin from border

        # Register the area elements
        if title_bar:
            self._register_element(title_bar, '', s)
        if title_label:
            self._register_element(title_label, '', s)
        if close_button:
            self._register_element(close_button, '', s)

        self._register_element(outer_frame, effective_key, s)
        self._register_element(inner_frame, f"{effective_key}_inner", s)

        # Register the position of the area
        self._register_element_position(effective_key, start_x, start_y, width, total_height)

        # Save current selection string and set new one for all elements in this area
        self._saved_default_s.append(self.default_s)
        if s:
            self.default_s = s

        # Push this area onto the stack
        area_info = {
            'frame': inner_frame,
            'outer_frame': outer_frame,
            'title_bar': title_bar,
            'title_label': title_label,
            'close_button': close_button,
            'close_button_frame': close_button_frame,
            'key': effective_key,
            'parent_x': parent_x,
            'parent_y': parent_y,
            'parent_initial_x': parent_initial_x,
            'width': width,
            'height': height,
            'total_height': total_height,
            'selection_string': s
        }

        self._area_stack.append(area_info)

        # Update the root for subsequent elements
        self._current_root = inner_frame

        # Save in area positions for later reference
        self._area_positions[effective_key] = area_info

        # Update the current position to inside the area
        self.current_x = new_x
        self.current_y = new_y
        self.initial_x = new_x

        # Now add the close button using the standard button method if requested
        if show_close_button and close_button_frame:
            # Save current context
            temp_root = self.root
            temp_x = self.current_x
            temp_y = self.current_y

            # Set context for close button
            self.root = close_button_frame
            self.current_x = 0
            self.current_y = 0

            # Define close action
            def close_area_callback():
                if s:
                    self.delete(shas=s)
                else:
                    self.delete(k=effective_key)

            # Create standard button with the button method
            close_button = tk.Button(
                close_button_frame,
                text=close_button_text,
                command=close_area_callback
            )
            close_button.pack(side=tk.RIGHT)

            # Register button
            self._register_element(close_button, close_button_key, s)

            # Restore context
            self.root = temp_root
            self.current_x = temp_x
            self.current_y = temp_y

            # Update area info with close button
            area_info['close_button'] = close_button
            area_info['close_button_key'] = close_button_key

        # Override the element creation methods to use the inner frame
        self._override_element_methods()

        # Update row height for layout calculations
        self._update_row_height(total_height)

        return self

    def _override_element_methods(self):
        """Override element creation methods to use the current area frame"""
        # Save original methods if not already saved
        if not hasattr(self, '_orig_methods'):
            self._orig_methods = {}

            # Override each element creation method
            element_methods = [
                'text', 'input', 'button', 'checkboxes', 'radio', 'listbox',
                'combobox', 'multiline', 'table', 'image'
            ]

            for method_name in element_methods:
                if hasattr(self, method_name):
                    # Save original method
                    self._orig_methods[method_name] = getattr(self, method_name)

                    # Create wrapper method
                    def create_wrapper(orig_method):
                        def wrapper(*args, **kwargs):
                            # Temporarily replace root with current area
                            orig_root = self.root
                            self.root = self._current_root

                            # Call original method
                            result = orig_method(*args, **kwargs)

                            # Restore original root
                            self.root = orig_root

                            return result

                        return wrapper

                    # Apply wrapper
                    setattr(self, method_name, create_wrapper(self._orig_methods[method_name]))

    def _restore_element_methods(self):
        """Restore original element creation methods"""
        if hasattr(self, '_orig_methods'):
            for method_name, method in self._orig_methods.items():
                setattr(self, method_name, method)

            # Clean up
            del self._orig_methods