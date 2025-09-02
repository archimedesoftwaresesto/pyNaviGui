# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk

class NgElementsBase30:
    """Text elements: multiline text input"""

    def multiline(self, title_or_text, text=None, k='', s='', nr_rows=5, nr_cols=40):
        """Create multiline input element using Tkinter Text with optional label"""
        s, _, _, k = self._merge_defaults(s, '', '', k)

        if text is None:
            title = None
            initial_text = title_or_text if title_or_text else ''
        else:
            title = title_or_text
            initial_text = text if text else ''

        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        text_widget = tk.Text(self.root, height=nr_rows, width=nr_cols, wrap=tk.WORD)

        scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        if initial_text:
            text_widget.insert('1.0', initial_text)

        text_widget.place(x=self.current_x, y=self.current_y)
        text_widget.update_idletasks()

        text_width = text_widget.winfo_reqwidth()
        text_height = text_widget.winfo_reqheight()

        scrollbar_width = 20
        scrollbar.place(x=self.current_x + text_width, y=self.current_y, height=text_height)

        total_width = text_width + scrollbar_width
        max_width = max(max_width, total_width)

        multiline_elements = []
        element_positions = []

        if title_element:
            multiline_elements.append(title_element)
            element_positions.append((start_x, start_y))

        multiline_elements.append(text_widget)
        multiline_elements.append(scrollbar)
        element_positions.append((self.current_x, self.current_y))
        element_positions.append((self.current_x + text_width, self.current_y))

        if k:
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        total_height = title_height + text_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        if not hasattr(self, '_multiline_groups'):
            self._multiline_groups = {}

        self._multiline_groups[effective_key] = text_widget

        if not hasattr(self, '_multiline_element_positions'):
            self._multiline_element_positions = {}

        self._multiline_element_positions[effective_key] = list(zip(multiline_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in multiline_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self