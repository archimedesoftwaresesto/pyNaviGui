# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgVisibility:
    """Visibility and movement management mixin"""

    def _get_matching_keys(self, k='', kstart='', shas=''):
        """Return keys of elements matching criteria"""
        matching_keys = []

        if k:
            if self.exists(k):
                matching_keys.append(k)
        elif kstart:
            matching_keys = [key for key in self.element_keys.keys()
                             if not key.startswith('__auto_key_') and key.startswith(kstart)]
        elif shas:
            matching_keys = [key for key, s_val in self.element_strings.items()
                             if shas in s_val]

        return matching_keys

    def visible(self, is_visible, shas='', k='', kstart=''):
        """Set visibility of elements"""
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        for key in matching_keys:
            if key in self.element_keys:
                element = self.element_keys[key]
                self._set_visible_impl(element, is_visible)

        return self

    def _set_visible_impl(self, element, is_visible):
        """Tkinter visibility implementation"""
        if hasattr(element, 'place'):
            if is_visible:
                element_found = False
                for key, el in self.element_keys.items():
                    if el == element and key in self.element_positions:
                        x, y, width, height = self.element_positions[key]
                        element.place(x=x, y=y, width=width, height=height)
                        element_found = True
                        break

                if not element_found and hasattr(self, '_checkbox_element_positions'):
                    for group_key, elements_positions in self._checkbox_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break

                if not element_found and hasattr(self, '_radio_element_positions'):
                    for group_key, elements_positions in self._radio_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break

                if not element_found and hasattr(self, '_listbox_element_positions'):
                    for group_key, elements_positions in self._listbox_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break

                if not element_found and hasattr(self, '_multiline_element_positions'):
                    for group_key, elements_positions in self._multiline_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break
            else:
                element.place_forget()

        # Force window refresh on macOS with micro-resize
        geo_parts = self.root.geometry().split('+')
        size_part = geo_parts[0]  # e.g., "300x300"
        width, height = size_part.split('x')
        width, height = int(width), int(height)

        # Micro resize and back to force macOS window manager redraw
        self.root.geometry(f"{width + 1}x{height}")
        self.root.update()
        self.root.geometry(f"{width}x{height}")
        self.root.update()

    def is_visible(self, k='', kstart='', shas=''):
        """Check if elements matching criteria are visible"""
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        # If no elements found, return False
        if not matching_keys:
            return False

        # Check visibility status of matching elements
        for key in matching_keys:
            if key in self.element_keys:
                element = self.element_keys[key]
                try:
                    # Use winfo_viewable() which returns 1 if the widget is viewable
                    if hasattr(element, 'winfo_viewable'):
                        if element.winfo_viewable():
                            return True
                except:
                    pass

        return False

    def move(self, xAdd=0, yAdd=0, shas='', k='', kstart=''):
        """Move elements by adding offset to coordinates"""
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        for key in matching_keys:
            if key in self.element_keys:
                element = self.element_keys[key]
                if key in self.element_positions:
                    x, y, width, height = self.element_positions[key]
                    new_x = x + xAdd
                    new_y = y + yAdd
                    self.element_positions[key] = (new_x, new_y, width, height)
                    self._move_element_impl(element, new_x, new_y)

        return self

    def _move_element_impl(self, element, new_x, new_y):
        """Tkinter movement implementation"""
        if hasattr(element, 'place'):
            element.place(x=new_x, y=new_y)

    def to_front(self, shas='', k='', kstart=''):
        """Bring elements matching criteria to front of stacking order"""
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        # First collect all elements, including panel rects
        elements_to_lift = []

        # Check if any of the matching keys are panels
        panel_keys = []
        if hasattr(self, '_panel_groups'):
            for key in matching_keys:
                if key in self._panel_groups:
                    panel_keys.append(key)

        # For panel keys, we need to lift the rect first, then all elements
        for panel_key in panel_keys:
            panel_data = self._panel_groups[panel_key]

            # Add rect first (it should be at the bottom)
            if 'rect' in panel_data and panel_data['rect']:
                elements_to_lift.append(panel_data['rect'])

            # Then add all panel elements
            for element in panel_data['elements']:
                elements_to_lift.append(element)

            # Make sure title and close button are included
            if 'title' in panel_data and panel_data['title']:
                elements_to_lift.append(panel_data['title'])

            if 'close_btn' in panel_data and panel_data['close_btn']:
                elements_to_lift.append(panel_data['close_btn'])

        # Add standard elements that match but aren't in panels
        for key in matching_keys:
            if key in self.element_keys:
                element = self.element_keys[key]
                if element not in elements_to_lift:
                    elements_to_lift.append(element)

        # Now lift all elements in order - first background rects, then content
        for element in elements_to_lift:
            if hasattr(element, 'lift'):
                element.lift()

        return self