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
                        element.place(x=x, y=y)
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