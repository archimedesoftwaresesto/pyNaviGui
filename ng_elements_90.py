# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk

class NgElementsBase90:
    """Values management: collecting data from all elements"""

    def _get_values(self):
        """Collect all values from input elements, checkboxes, radio buttons and listboxes"""
        values = {}

        # Input values
        for key, element in self.element_keys.items():
            if not key.startswith('__auto_key_') and isinstance(element, tk.Entry):
                values[key] = element.get()

        # Checkbox group values
        if hasattr(self, '_checkbox_groups'):
            for key, checkbox_vars in self._checkbox_groups.items():
                if not key.startswith('__auto_key_'):
                    selected_values = []
                    for var, value in checkbox_vars:
                        if var.get():
                            selected_values.append(value)
                    values[key] = selected_values

        # Radio button group values
        if hasattr(self, '_radio_groups'):
            for key, radio_var in self._radio_groups.items():
                if not key.startswith('__auto_key_'):
                    selected_value = radio_var.get()
                    values[key] = selected_value if selected_value else ''

        # Listbox values with multi-select support
        if hasattr(self, '_listbox_groups'):
            for key, listbox_data in self._listbox_groups.items():
                if not key.startswith('__auto_key_'):
                    if len(listbox_data) == 3:
                        listbox_widget, parsed_options, multi_select = listbox_data
                    else:
                        listbox_widget, parsed_options = listbox_data
                        multi_select = False

                    selection = listbox_widget.curselection()

                    if multi_select:
                        selected_values = []
                        for selected_index in selection:
                            if selected_index < len(parsed_options):
                                _, selected_value = parsed_options[selected_index]
                                selected_values.append(selected_value)
                        values[key] = selected_values
                    else:
                        if selection:
                            selected_index = selection[0]
                            if selected_index < len(parsed_options):
                                _, selected_value = parsed_options[selected_index]
                                values[key] = selected_value
                            else:
                                values[key] = ''
                        else:
                            values[key] = ''

        # Multiline widget values
        if hasattr(self, '_multiline_groups'):
            for key, text_widget in self._multiline_groups.items():
                if not key.startswith('__auto_key_'):
                    text_content = text_widget.get('1.0', 'end-1c')
                    values[key] = text_content

        # Combobox values
        if hasattr(self, '_combobox_groups'):
            for key, combobox_data in self._combobox_groups.items():
                if not key.startswith('__auto_key_'):
                    combobox_widget, parsed_options = combobox_data

                    current_selection = combobox_widget.current()

                    if current_selection >= 0 and current_selection < len(parsed_options):
                        _, selected_value = parsed_options[current_selection]
                        values[key] = selected_value
                    else:
                        values[key] = ''

        # Table values (selections)
        if hasattr(self, '_table_groups'):
            for key, table_data in self._table_groups.items():
                if not key.startswith('__auto_key_'):
                    table_widget, column_keys = table_data

                    selection = table_widget.selection()

                    if selection:
                        selected_indices = []
                        for item_id in selection:
                            index = table_widget.index(item_id)
                            selected_indices.append(index)

                        values[key] = selected_indices
                    else:
                        values[key] = []

        # Navigation table values - Using English key names
        if hasattr(self, '_navtable_groups'):
            for key, navtable_data in self._navtable_groups.items():
                if not key.startswith('__auto_key_'):
                    values[key] = {
                        'current_page': navtable_data['current_page'],
                        'total_pages': navtable_data['total_pages'],
                        'rows_per_page': navtable_data['nr_rows'],
                        'total_data': len(navtable_data['data']),
                        'current_page_data': self._get_current_page_data_navtable(navtable_data)
                    }

        return values