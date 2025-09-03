# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk


class NgElementsBase10:
    """Selection elements: checkboxes and radio buttons"""

    def checkboxes(self, title_or_options, options=None, k='', s=''):
        """Create checkbox group using Tkinter Checkbutton"""
        s, fg, bg, k = self._merge_defaults(s, '', '', k)

        if options is None:
            title = None
            checkbox_options = title_or_options
        else:
            title = title_or_options
            checkbox_options = options

        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        checkbox_height = 22
        title_height = 0

        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w', bg=bg if bg else None)
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        parsed_options = []
        for option in checkbox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        if not hasattr(self, '_checkbox_groups'):
            self._checkbox_groups = {}

        checkbox_vars = []
        checkboxes_elements = []
        element_positions = []

        if title_element:
            checkboxes_elements.append(title_element)
            element_positions.append((start_x, start_y))

        checkbox_start_y = self.current_y

        # Determina il colore di sfondo per i checkbox
        checkbox_bg = bg if bg else getattr(self, 'default_bg', None)

        for i, (display_text, value) in enumerate(parsed_options):
            var = tk.BooleanVar()
            checkbox_vars.append((var, value))

            # Aggiungi il parametro bg al checkbox
            checkbox_options = {
                'text': display_text,
                'variable': var,
                'anchor': 'w'
            }

            # Applica lo sfondo solo se è stato specificato
            if checkbox_bg:
                checkbox_options['bg'] = checkbox_bg

            checkbox = tk.Checkbutton(
                self.root,
                **checkbox_options
            )

            checkbox.place(x=self.current_x, y=self.current_y)
            checkbox.update_idletasks()

            width = checkbox.winfo_reqwidth()
            height = max(checkbox.winfo_reqheight(), checkbox_height)

            checkboxes_elements.append(checkbox)
            element_positions.append((self.current_x, self.current_y))

            max_width = max(max_width, width)

            if i < len(parsed_options) - 1:
                self.current_y += height

        if k:
            self._checkbox_groups[k] = checkbox_vars
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._checkbox_groups[effective_key] = checkbox_vars

        total_height = title_height + len(parsed_options) * checkbox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        if not hasattr(self, '_checkbox_element_positions'):
            self._checkbox_element_positions = {}

        self._checkbox_element_positions[effective_key] = list(zip(checkboxes_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in checkboxes_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    def radio(self, title_or_options, options=None, k='', s='', default=None):
        """Create radio button group using Tkinter Radiobutton"""
        s, fg, bg, k = self._merge_defaults(s, '', '', k)

        if options is None:
            title = None
            radio_options = title_or_options
        else:
            title = title_or_options
            radio_options = options

        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        radio_height = 22
        title_height = 0

        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w', bg=bg if bg else None)
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        parsed_options = []
        for option in radio_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        if not hasattr(self, '_radio_groups'):
            self._radio_groups = {}

        radio_var = tk.StringVar()

        if default is not None:
            default_found = False
            for display_text, value in parsed_options:
                if value == default:
                    radio_var.set(value)
                    default_found = True
                    break

            if not default_found:
                if parsed_options:
                    radio_var.set(parsed_options[0][1])
        else:
            if parsed_options:
                radio_var.set(parsed_options[0][1])

        radio_elements = []
        element_positions = []

        if title_element:
            radio_elements.append(title_element)
            element_positions.append((start_x, start_y))

        radio_start_y = self.current_y

        # Determina il colore di sfondo per i radiobutton
        radio_bg = bg if bg else getattr(self, 'default_bg', None)

        for i, (display_text, value) in enumerate(parsed_options):
            # Aggiungi il parametro bg al radiobutton
            radio_options = {
                'text': display_text,
                'variable': radio_var,
                'value': value,
                'anchor': 'w'
            }

            # Applica lo sfondo solo se è stato specificato
            if radio_bg:
                radio_options['bg'] = radio_bg

            radiobutton = tk.Radiobutton(
                self.root,
                **radio_options
            )

            radiobutton.place(x=self.current_x, y=self.current_y)
            radiobutton.update_idletasks()

            width = radiobutton.winfo_reqwidth()
            height = max(radiobutton.winfo_reqheight(), radio_height)

            radio_elements.append(radiobutton)
            element_positions.append((self.current_x, self.current_y))

            max_width = max(max_width, width)

            if i < len(parsed_options) - 1:
                self.current_y += height

        if k:
            self._radio_groups[k] = radio_var
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._radio_groups[effective_key] = radio_var

        total_height = title_height + len(parsed_options) * radio_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        if not hasattr(self, '_radio_element_positions'):
            self._radio_element_positions = {}

        self._radio_element_positions[effective_key] = list(zip(radio_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in radio_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self