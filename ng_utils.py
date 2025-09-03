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
        """Delete elements matching criteria"""
        # If no criteria provided, do nothing
        if not k and not kstart and not shas:
            return self

        # Get all keys matching the criteria
        matching_keys = []
        if k:
            # For tables, bypass the exists() check
            if hasattr(self, '_table_groups') and k in self._table_groups:
                matching_keys.append(k)
            elif self.exists(k):
                matching_keys.append(k)
            # Debugging output
            print(
                f"Delete requested for key: {k}, Found in _table_groups: {hasattr(self, '_table_groups') and k in self._table_groups}")
        elif kstart:
            matching_keys = [key for key in self.element_keys.keys()
                             if not key.startswith('__auto_key_') and key.startswith(kstart)]
        elif shas:
            matching_keys = [key for key, s_val in self.element_strings.items()
                             if shas in s_val]

        # Print matching keys for debugging
        print(f"Matching keys for deletion: {matching_keys}")

        # Process each key
        for key in matching_keys:
            # Special handling for table groups - most comprehensive approach
            if hasattr(self, '_table_groups') and key in self._table_groups:
                print(f"Cleaning up table with key: {key}")
                self._cleanup_table(key)
                continue  # Skip standard element deletion since we've handled it comprehensively

            # Special handling for navtable groups
            if hasattr(self, '_navtable_groups') and key in self._navtable_groups:
                self._cleanup_navtable(key)
                continue  # Skip standard element deletion

            # Special handling for checkbox groups
            if hasattr(self, '_checkbox_groups') and key in self._checkbox_groups:
                self._cleanup_element_group(key, '_checkbox_groups', '_checkbox_element_positions')
                continue

            # Special handling for radio groups
            if hasattr(self, '_radio_groups') and key in self._radio_groups:
                self._cleanup_element_group(key, '_radio_groups', '_radio_element_positions')
                continue

            # Special handling for listbox groups
            if hasattr(self, '_listbox_groups') and key in self._listbox_groups:
                self._cleanup_element_group(key, '_listbox_groups', '_listbox_element_positions')
                continue

            # Special handling for multiline groups
            if hasattr(self, '_multiline_groups') and key in self._multiline_groups:
                self._cleanup_element_group(key, '_multiline_groups', '_multiline_element_positions')
                continue

            # Special handling for combobox groups
            if hasattr(self, '_combobox_groups') and key in self._combobox_groups:
                self._cleanup_element_group(key, '_combobox_groups', '_combobox_element_positions')
                continue

            # Handle single elements
            if key in self.element_keys:
                element_to_remove = self.element_keys[key]
                self._safe_destroy_element(element_to_remove)
                if element_to_remove in self.elements:
                    self.elements.remove(element_to_remove)
                del self.element_keys[key]

            # Clean up positions and strings
            if key in self.element_positions:
                del self.element_positions[key]
            if key in self.element_strings:
                del self.element_strings[key]

        return self

    def _cleanup_table(self, key):
        """Thoroughly clean up a table and all its elements"""
        print(f"Starting _cleanup_table for key: {key}")

        if not hasattr(self, '_table_groups'):
            print("No _table_groups attribute found")
            return

        if key not in self._table_groups:
            print(f"Key {key} not found in _table_groups")
            print(f"Available keys in _table_groups: {list(self._table_groups.keys())}")
            return

        # First, get the main table widget and all related widgets
        try:
            table_widget, _ = self._table_groups[key]
            print(f"Table widget found: {table_widget}")

            # CRITICAL: Hide the widget first before destroying it
            if hasattr(table_widget, 'place_forget'):
                table_widget.place_forget()
                print("Table widget hidden")

            # Get all the elements from the positions dict
            if hasattr(self, '_table_element_positions') and key in self._table_element_positions:
                elements_positions = self._table_element_positions[key]
                print(f"Found {len(elements_positions)} elements in positions")

                for element, _ in elements_positions:
                    # CRITICAL: Hide each element first
                    if hasattr(element, 'place_forget'):
                        element.place_forget()

                    # Then destroy it
                    self._safe_destroy_element(element)
                    if element in self.elements:
                        self.elements.remove(element)

                # Remove the positions entry
                del self._table_element_positions[key]
                print("Table element positions cleaned up")

            # Destroy the main table widget
            self._safe_destroy_element(table_widget)
            if table_widget in self.elements:
                self.elements.remove(table_widget)
                print("Table widget removed from elements list")

            # Remove from table groups
            del self._table_groups[key]
            print(f"Key {key} removed from _table_groups")

            # Clean up from main tracking structures
            if key in self.element_keys:
                del self.element_keys[key]
                print(f"Key {key} removed from element_keys")

            if key in self.element_positions:
                del self.element_positions[key]
                print(f"Key {key} removed from element_positions")

            if key in self.element_strings:
                del self.element_strings[key]
                print(f"Key {key} removed from element_strings")

            print(f"Table cleanup for key {key} completed successfully")
        except Exception as e:
            print(f"Error cleaning up table {key}: {e}")

    def _cleanup_element_group(self, key, groups_attr, positions_attr):
        """Clean up a group of elements"""
        # Delete from positions
        if hasattr(self, positions_attr) and key in getattr(self, positions_attr):
            elements_positions = getattr(self, positions_attr)[key]
            for element, _ in elements_positions:
                # CRITICAL: Hide the element first
                if hasattr(element, 'place_forget'):
                    element.place_forget()

                # Then destroy it
                self._safe_destroy_element(element)
                if element in self.elements:
                    self.elements.remove(element)

            # Remove from positions
            delattr(getattr(self, positions_attr), key)

        # Remove from groups
        if hasattr(self, groups_attr) and key in getattr(self, groups_attr):
            del getattr(self, groups_attr)[key]

        # Clean up from main tracking structures
        if key in self.element_keys:
            del self.element_keys[key]
        if key in self.element_positions:
            del self.element_positions[key]
        if key in self.element_strings:
            del self.element_strings[key]

    def _safe_destroy_element(self, element):
        """Safely destroy a Tkinter element"""
        try:
            # Important: always check if element exists before destroying
            if hasattr(element, 'winfo_exists'):
                if element.winfo_exists():
                    if hasattr(element, 'destroy'):
                        element.destroy()
            elif hasattr(element, 'destroy'):
                element.destroy()
        except Exception:
            # Just ignore any errors during destruction
            pass

    def finalize_layout(self):
        """Store initial element count"""
        self.initial_elements_count = len(self.elements)
        return self

    def clear_error_messages(self):
        """Remove dynamically added elements"""
        if self.initial_elements_count > 0:
            elements_to_remove = self.elements[self.initial_elements_count:]

            for element in elements_to_remove:
                # CRITICAL: Hide the element first
                if hasattr(element, 'place_forget'):
                    element.place_forget()

                # Then destroy it
                self._safe_destroy_element(element)

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