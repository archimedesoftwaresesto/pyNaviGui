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

    def delete(self, k):
        """Delete element with key k"""
        if not self.exists(k):
            return self

        # Special handling for navtable groups
        if hasattr(self, '_navtable_groups') and k in self._navtable_groups:
            navtable_data = self._navtable_groups[k]

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
            del self._navtable_groups[k]

            # Remove from navtable element positions
            if hasattr(self, '_navtable_element_positions') and k in self._navtable_element_positions:
                # Delete remaining elements from element positions (like title)
                elements_positions = self._navtable_element_positions[k]
                for element, pos in elements_positions:
                    # Only delete if not already deleted above
                    try:
                        if element.winfo_exists():
                            self._delete_element_impl(element)
                            if element in self.elements:
                                self.elements.remove(element)
                    except:
                        pass  # Element already destroyed

                del self._navtable_element_positions[k]

        # Special handling for other group types
        if hasattr(self, '_checkbox_groups') and k in self._checkbox_groups:
            del self._checkbox_groups[k]
            if hasattr(self, '_checkbox_element_positions') and k in self._checkbox_element_positions:
                elements_positions = self._checkbox_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._checkbox_element_positions[k]

        if hasattr(self, '_radio_groups') and k in self._radio_groups:
            del self._radio_groups[k]
            if hasattr(self, '_radio_element_positions') and k in self._radio_element_positions:
                elements_positions = self._radio_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._radio_element_positions[k]

        if hasattr(self, '_listbox_groups') and k in self._listbox_groups:
            del self._listbox_groups[k]
            if hasattr(self, '_listbox_element_positions') and k in self._listbox_element_positions:
                elements_positions = self._listbox_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._listbox_element_positions[k]

        if hasattr(self, '_multiline_groups') and k in self._multiline_groups:
            del self._multiline_groups[k]
            if hasattr(self, '_multiline_element_positions') and k in self._multiline_element_positions:
                elements_positions = self._multiline_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._multiline_element_positions[k]

        if hasattr(self, '_combobox_groups') and k in self._combobox_groups:
            del self._combobox_groups[k]
            if hasattr(self, '_combobox_element_positions') and k in self._combobox_element_positions:
                elements_positions = self._combobox_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._combobox_element_positions[k]

        if hasattr(self, '_table_groups') and k in self._table_groups:
            del self._table_groups[k]
            if hasattr(self, '_table_element_positions') and k in self._table_element_positions:
                elements_positions = self._table_element_positions[k]
                for element, pos in elements_positions:
                    self._delete_element_impl(element)
                    if element in self.elements:
                        self.elements.remove(element)
                del self._table_element_positions[k]

        # Handle single elements
        if k in self.element_keys:
            element_to_remove = self.element_keys[k]

            if element_to_remove in self.elements:
                self.elements.remove(element_to_remove)

            self._delete_element_impl(element_to_remove)
            del self.element_keys[k]

        # Clean up positions and strings
        if k in self.element_positions:
            del self.element_positions[k]
        if k in self.element_strings:
            del self.element_strings[k]

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