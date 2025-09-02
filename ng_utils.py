# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgUtils:
    """Utility functions mixin"""

    def set_keys(self, max_nr_keys=100, key_start_with_string=''):
        """Generate a list of keys"""
        return [key_start_with_string + str(i) for i in range(max_nr_keys)]

    def exists(self, k):
        """Check if element with key k exists"""
        return (k in self.element_keys and
                self.element_keys[k] is not None and
                not k.startswith('__auto_key_'))

    def delete(self, k='', kstart='', shas=''):
        """Delete elements matching criteria

        Args:
            k: Delete element with this specific key
            kstart: Delete elements with keys starting with this string
            shas: Delete elements with selection string containing this value
        """
        # If no criteria provided, do nothing
        if not k and not kstart and not shas:
            return self

        # Get all keys matching the criteria
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        # Process each key
        for key in matching_keys:
            if not self.exists(key):
                continue

            # Special handling for navtable groups
            if hasattr(self, '_navtable_groups') and key in self._navtable_groups:
                navtable_data = self._navtable_groups[key]

                # Delete navigation buttons and page label
                if 'btn_back' in navtable_data and navtable_data['btn_back']:
                    self._delete_element_impl(navtable_data['btn_back'])
                    if navtable_data['btn_back'] in self.elements:
                        self.elements.remove(navtable_data['btn_back'])

                if 'btn_forward' in navtable_data and navtable_data['btn_forward']:
                    self._delete_element_impl(navtable_data['btn_forward'])
                    if navtable_data['btn_forward'] in self.elements:
                        self.elements.remove(navtable_data['btn_forward'])

                if 'lbl_page' in navtable_data and navtable_data['lbl_page']:
                    self._delete_element_impl(navtable_data['lbl_page'])
                    if navtable_data['lbl_page'] in self.elements:
                        self.elements.remove(navtable_data['lbl_page'])

                # Delete all row elements
                if 'row_elements' in navtable_data:
                    for row_list in navtable_data['row_elements']:
                        for element in row_list:
                            self._delete_element_impl(element)
                            if element in self.elements:
                                self.elements.remove(element)

                # Remove from navtable groups
                del self._navtable_groups[key]

                # Remove from navtable element positions
                if hasattr(self, '_navtable_element_positions') and key in self._navtable_element_positions:
                    # Delete remaining elements from element positions (like title)
                    elements_positions = self._navtable_element_positions[key]
                    for element, pos in elements_positions:
                        # Only delete if not already deleted above
                        try:
                            if element.winfo_exists():
                                self._delete_element_impl(element)
                                if element in self.elements:
                                    self.elements.remove(element)
                        except:
                            pass  # Element already destroyed

                    del self._navtable_element_positions[key]

            # Special handling for other group types
            if hasattr(self, '_checkbox_groups') and key in self._checkbox_groups:
                del self._checkbox_groups[key]
                if hasattr(self, '_checkbox_element_positions') and key in self._checkbox_element_positions:
                    elements_positions = self._checkbox_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._checkbox_element_positions[key]

            if hasattr(self, '_radio_groups') and key in self._radio_groups:
                del self._radio_groups[key]
                if hasattr(self, '_radio_element_positions') and key in self._radio_element_positions:
                    elements_positions = self._radio_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._radio_element_positions[key]

            if hasattr(self, '_listbox_groups') and key in self._listbox_groups:
                del self._listbox_groups[key]
                if hasattr(self, '_listbox_element_positions') and key in self._listbox_element_positions:
                    elements_positions = self._listbox_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._listbox_element_positions[key]

            if hasattr(self, '_multiline_groups') and key in self._multiline_groups:
                del self._multiline_groups[key]
                if hasattr(self, '_multiline_element_positions') and key in self._multiline_element_positions:
                    elements_positions = self._multiline_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._multiline_element_positions[key]

            if hasattr(self, '_combobox_groups') and key in self._combobox_groups:
                del self._combobox_groups[key]
                if hasattr(self, '_combobox_element_positions') and key in self._combobox_element_positions:
                    elements_positions = self._combobox_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._combobox_element_positions[key]

            if hasattr(self, '_table_groups') and key in self._table_groups:
                del self._table_groups[key]
                if hasattr(self, '_table_element_positions') and key in self._table_element_positions:
                    elements_positions = self._table_element_positions[key]
                    for element, pos in elements_positions:
                        self._delete_element_impl(element)
                        if element in self.elements:
                            self.elements.remove(element)
                    del self._table_element_positions[key]

            # Handle area groups
            if hasattr(self, '_area_positions') and key in self._area_positions:
                area_info = self._area_positions[key]

                # Delete all elements in the area
                if 'outer_frame' in area_info:
                    self._delete_element_impl(area_info['outer_frame'])
                if 'title_bar' in area_info:
                    self._delete_element_impl(area_info['title_bar'])
                if 'title_label' in area_info:
                    self._delete_element_impl(area_info['title_label'])
                if 'close_button' in area_info:
                    self._delete_element_impl(area_info['close_button'])

                # Remove from area positions
                del self._area_positions[key]

            # Handle single elements
            if key in self.element_keys:
                element_to_remove = self.element_keys[key]

                if element_to_remove in self.elements:
                    self.elements.remove(element_to_remove)

                self._delete_element_impl(element_to_remove)
                del self.element_keys[key]

            # Clean up positions and strings
            if key in self.element_positions:
                del self.element_positions[key]
            if key in self.element_strings:
                del self.element_strings[key]

        return self

    def finalize_layout(self):
        """Store initial element count"""
        self.initial_elements_count = len(self.elements)
        return self

    def clear_error_messages(self):
        """Remove dynamically added elements"""
        if self.initial_elements_count > 0:
            elements_to_remove = self.elements[self.initial_elements_count:]

            for element in elements_to_remove:
                self._delete_element_impl(element)

            self.elements = self.elements[:self.initial_elements_count]

            keys_to_remove = []
            for key in list(self.element_keys.keys()):
                element = self.element_keys[key]
                if element not in self.elements:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                if key in self.element_keys:
                    del self.element_keys[key]
                if key in self.element_positions:
                    del self.element_positions[key]
                if key in self.element_strings:
                    del self.element_strings[key]
        return self