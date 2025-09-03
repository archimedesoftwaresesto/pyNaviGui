# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk


class NgElementsBase60:
    """Panel element implementation - groups elements with optional border"""

    def _init_panel_elements(self):
        """Initialize panel variables"""
        self._panel_stack = []
        self._panel_groups = {}
        self._current_panel_key = None
        self._panel_padding = 15  # Default horizontal padding inside panels

    # Updated panel method in ng_elements_60.py
    # This code shows modifications to enable customization of panel background color
    # and ensure child elements inherit this color

    def panel(self, title='', geometry='200x150', k='', s='', padding=5, vpadding=5, bg='lightgray', visible=True):
        """Start or end a panel group with customizable background color and visibility"""
        if not title:
            # End panel mode - restore original context
            if hasattr(self, '_panel_stack') and self._panel_stack:
                panel_data = self._panel_stack.pop()
                self.current_x = panel_data['end_x']
                self.current_y = panel_data['end_y']
                self.default_s = panel_data['prev_s']
                self.default_bg = panel_data['prev_bg']
                self._current_panel_key = None

                # Make sure to complete positioning of the last row
                self._start_new_row()
            return self

        # Start new panel
        s, _, merged_bg, k = self._merge_defaults(s, '', bg, k)

        # Use provided bg parameter with fallback to merged_bg from defaults
        panel_bg = bg or merged_bg or 'lightgray'

        # Store padding for this panel
        self._panel_padding = padding

        # Parse geometry
        width, height = 200, 150
        if 'x' in geometry:
            parts = geometry.split('x')
            if len(parts) == 2:
                try:
                    width = int(parts[0])
                    height = int(parts[1])
                except ValueError:
                    pass

        # Create panel rectangle
        start_x = self.current_x
        start_y = self.current_y

        rect = tk.Frame(self.root, width=width, height=height, bg=panel_bg,
                        highlightbackground='gray', highlightthickness=1)
        rect.place(x=start_x, y=start_y)

        # Create close button
        close_btn = tk.Button(self.root, text="×", width=2, height=1, bg=panel_bg,
                              command=lambda: self._toggle_panel_visibility(k, s))
        close_btn.place(x=start_x + width - 25, y=start_y + 2)

        # Create title if provided
        title_label = None
        if title:
            title_label = tk.Label(self.root, text=title, bg=panel_bg)
            title_label.place(x=start_x + 10, y=start_y + 2)

        # Register elements
        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, start_x, start_y, width, height)

        # Create panel elements tracking if not exists
        if not hasattr(self, '_panel_groups'):
            self._panel_groups = {}

        # Ensure we have a selection string for the panel
        panel_s = s if s else f"panel_{effective_key}"

        # Store panel data for internal reference
        self._panel_groups[effective_key] = {
            'rect': rect,
            'close_btn': close_btn,
            'title': title_label,
            'width': width,
            'height': height,
            'elements': [],
            'element_keys': [],
            'start_x': start_x,
            'start_y': start_y,
            'padding': padding,
            'background': panel_bg,
            'selection_string': panel_s
        }

        # Store original default_s and default_bg to restore it later
        prev_s = self.default_s
        prev_bg = getattr(self, 'default_bg', '')

        # Setup panel stack if not exists
        if not hasattr(self, '_panel_stack'):
            self._panel_stack = []

        # Save current context to restore when panel ends
        self._panel_stack.append({
            'key': effective_key,
            'prev_s': prev_s,
            'prev_bg': prev_bg,
            'start_x': start_x,
            'start_y': start_y,
            'end_x': self.current_x,
            'end_y': self.current_y + height + 5
        })

        # Set current panel key so new elements can be tracked
        self._current_panel_key = effective_key

        # Set vertical padding based on parameter or use default values
        vpadding = vpadding if vpadding is not None else (25 if title else 5)

        # Move current position inside panel with proper padding
        self.current_x = start_x + padding
        self.current_y = start_y + vpadding

        # Save initial X position inside the panel
        self.initial_x = self.current_x

        # Explicitly reset row tracking for proper layout inside panel
        self._start_new_row()

        # Set default selection string to panel's selection string
        # This ensures all elements inside get the same selection string
        self.default_s = panel_s

        # Set default background color to panel's background color
        # This ensures all elements inside inherit the same background
        self.default_bg = panel_bg

        # Register main elements with the panel's selection string
        self._register_element(rect, effective_key, panel_s)
        self._register_element(close_btn, f"{effective_key}_close", panel_s)
        if title_label:
            self._register_element(title_label, f"{effective_key}_title", panel_s)

        # Set visibility if requested to be hidden
        if not visible:
            # Use deferred execution to ensure all elements are created before hiding
            self.root.after(10, lambda: self.visible(False, shas=panel_s))

        return self

    # Updated _register_element method to apply panel's background color to child elements
    def _register_element(self, element, key, s=''):
        """Track elements inside panels and apply panel background color"""
        # Call the original method first
        self.elements.append(element)

        if not key:
            key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        self.element_keys[key] = element

        if s:
            self.element_strings[key] = s

        # If we're inside a panel, add this element to the panel's list
        if hasattr(self, '_current_panel_key') and self._current_panel_key:
            if self._current_panel_key in self._panel_groups:
                panel_data = self._panel_groups[self._current_panel_key]
                panel_data['elements'].append(element)
                panel_data['element_keys'].append(key)

                # Apply panel background color to applicable elements
                if hasattr(self, 'default_bg') and self.default_bg and hasattr(element, 'config'):
                    # Check if element type can accept background color
                    element_class = element.__class__.__name__.lower()
                    if any(cls in element_class for cls in ['label', 'frame', 'button', 'text', 'entry']):
                        try:
                            # Only set if the element has a config method that accepts bg
                            element.config(bg=self.default_bg)
                        except:
                            pass

    # Updated _merge_defaults method to handle default_bg properly
    def _merge_defaults(self, s='', fg='', bg='', k=''):
        """Merge passed parameters with defaults"""
        merged_s = s if s else self.default_s
        merged_fg = fg if fg else self.default_fg
        merged_bg = bg if bg else getattr(self, 'default_bg', '')

        merged_k = k
        if k and self.default_k_prefix:
            merged_k = self.default_k_prefix + k

        return merged_s, merged_fg, merged_bg, merged_k

    def _register_element(self, element, key, s=''):
        """Override to track elements inside panels"""
        # Call the original method first
        self.elements.append(element)

        if not key:
            key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        self.element_keys[key] = element

        if s:
            self.element_strings[key] = s

        # If we're inside a panel, add this element to the panel's list
        if hasattr(self, '_current_panel_key') and self._current_panel_key:
            if self._current_panel_key in self._panel_groups:
                self._panel_groups[self._current_panel_key]['elements'].append(element)
                self._panel_groups[self._current_panel_key]['element_keys'].append(key)

    def _toggle_panel_visibility(self, panel_key, panel_s=None):
        """Toggle panel visibility when close button is clicked

        Args:
            panel_key: Key of the panel to toggle
            panel_s: Selection string of the panel (optional)
        """
        if not hasattr(self, '_panel_groups') or panel_key not in self._panel_groups:
            return

        panel_data = self._panel_groups[panel_key]

        # Check if panel is visible
        is_visible = True
        try:
            is_visible = panel_data['rect'].winfo_viewable()
        except:
            is_visible = False

        # Get the selection string from the panel data
        selection_string = panel_s if panel_s else panel_data.get('selection_string', '')

        # Toggle visibility using the selection string
        if selection_string:
            # Use the visible method to toggle all elements with this selection string
            self.visible(not is_visible, shas=selection_string)
        else:
            # If no selection string available, toggle only the panel elements directly
            if is_visible:
                # Hide panel frame and controls
                if hasattr(panel_data['rect'], 'place_forget'):
                    panel_data['rect'].place_forget()
                if hasattr(panel_data['close_btn'], 'place_forget'):
                    panel_data['close_btn'].place_forget()
                if panel_data['title'] and hasattr(panel_data['title'], 'place_forget'):
                    panel_data['title'].place_forget()

                # Hide all elements in the panel
                for element in panel_data['elements']:
                    if hasattr(element, 'place_forget'):
                        element.place_forget()
            else:
                # Show panel frame and controls
                start_x, start_y, width, height = self.element_positions.get(panel_key, (0, 0, 100, 100))
                panel_data['rect'].place(x=start_x, y=start_y, width=width, height=height)
                panel_data['close_btn'].place(x=start_x + width - 25, y=start_y + 2)

                if panel_data['title']:
                    panel_data['title'].place(x=start_x + 10, y=start_y + 2)

                # Show all elements in the panel
                for element_key in panel_data['element_keys']:
                    element = self.element_keys.get(element_key)
                    if element and hasattr(element, 'place') and element_key in self.element_positions:
                        x, y, width, height = self.element_positions[element_key]

                        # Make sure the element is visible when shown again
                        if width and height:
                            element.place(x=x, y=y, width=width, height=height)
                        else:
                            element.place(x=x, y=y)

    def _hide_elements_by_selection_string(self, s):
        """Hide all elements with matching selection string"""
        # Skip if empty selection string
        if not s:
            return

        # Find all keys with matching selection string
        matching_keys = []
        for key, stored_s in self.element_strings.items():
            if stored_s == s:
                matching_keys.append(key)

        # Hide all matching elements
        for key in matching_keys:
            if key in self.element_keys:
                element = self.element_keys[key]
                if hasattr(element, 'place_forget'):
                    element.place_forget()