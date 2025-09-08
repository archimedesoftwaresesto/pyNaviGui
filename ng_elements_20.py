# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk


class NgElementsBase20:
    """List elements: listbox and combobox"""

    def listbox(self, title_or_options, options=None, k='', s='', default=None, nr_rows=5, multi_select=False,
                event_click=False, event_dbclick=False):
        """Create listbox using Tkinter Listbox with optional click and double-click events"""
        s, _, _, k = self._merge_defaults(s, '', '', k)

        if options is None:
            title = None
            listbox_options = title_or_options
        else:
            title = title_or_options
            listbox_options = options

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

        parsed_options = []
        for option in listbox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        if not hasattr(self, '_listbox_groups'):
            self._listbox_groups = {}

        selectmode = tk.EXTENDED if multi_select else tk.SINGLE
        listbox = tk.Listbox(self.root, height=nr_rows, selectmode=selectmode)

        # Handle click and double-click events with proper coordination
        if (event_click or event_dbclick) and k:
            # Store timer reference in the widget itself
            listbox.click_timer = None
            listbox.double_click_pending = False

            if event_click:
                def listbox_click_handler(event):
                    # Cancel any pending timer
                    if listbox.click_timer:
                        self.root.after_cancel(listbox.click_timer)

                    # If double-click is also enabled, delay the click event
                    if event_dbclick:
                        listbox.double_click_pending = False

                        # Wait 300ms to see if a double-click follows
                        def delayed_click():
                            if not listbox.double_click_pending:
                                values = self._get_values()
                                self.event_queue.put((k, values))

                        listbox.click_timer = self.root.after(300, delayed_click)
                    else:
                        # No double-click enabled, fire immediately
                        values = self._get_values()
                        self.event_queue.put((k, values))

                listbox.bind("<<ListboxSelect>>", listbox_click_handler)

            if event_dbclick:
                def listbox_dbclick_handler(event):
                    # Cancel the pending click timer
                    if listbox.click_timer:
                        self.root.after_cancel(listbox.click_timer)
                        listbox.click_timer = None

                    # Mark that a double-click occurred
                    listbox.double_click_pending = True

                    # Fire double-click event
                    values = self._get_values()
                    self.event_queue.put((f"{k}_DBCLICK", values))

                listbox.bind("<Double-Button-1>", listbox_dbclick_handler)

        scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        for display_text, value in parsed_options:
            listbox.insert(tk.END, display_text)

        if default is not None:
            if multi_select:
                default_values = default if isinstance(default, (list, tuple)) else [default]
                for i, (display_text, value) in enumerate(parsed_options):
                    if value in default_values:
                        listbox.selection_set(i)
                        if i == 0 or value == default_values[0]:
                            listbox.see(i)
            else:
                for i, (display_text, value) in enumerate(parsed_options):
                    if value == default:
                        listbox.selection_set(i)
                        listbox.see(i)
                        break

        listbox.place(x=self.current_x, y=self.current_y)
        listbox.update_idletasks()

        listbox_width = listbox.winfo_reqwidth()
        listbox_height = listbox.winfo_reqheight()

        scrollbar_width = 20
        scrollbar.place(x=self.current_x + listbox_width, y=self.current_y, height=listbox_height)

        max_width = max(max_width, listbox_width + scrollbar_width)

        listbox_elements = []
        element_positions = []

        if title_element:
            listbox_elements.append(title_element)
            element_positions.append((start_x, start_y))

        listbox_elements.append(listbox)
        listbox_elements.append(scrollbar)
        element_positions.append((self.current_x, self.current_y))
        element_positions.append((self.current_x + listbox_width, self.current_y))

        if k:
            self._listbox_groups[k] = (listbox, parsed_options, multi_select)
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._listbox_groups[effective_key] = (listbox, parsed_options, multi_select)

        total_height = title_height + listbox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        if not hasattr(self, '_listbox_element_positions'):
            self._listbox_element_positions = {}

        self._listbox_element_positions[effective_key] = list(zip(listbox_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in listbox_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    def combobox(self, title_or_options, options=None, k='', s='', default=None, nr_rows=5, event_change=False):
        """Create combobox with optional change event support"""
        try:
            import tkinter.ttk as ttk
        except ImportError:
            from tkinter import ttk

        s, _, _, k = self._merge_defaults(s, '', '', k)

        if options is None:
            title = None
            combobox_options = title_or_options
        else:
            title = title_or_options
            combobox_options = options

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

        parsed_options = []
        display_values = []

        for option in combobox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))
            display_values.append(display_text)

        if not hasattr(self, '_combobox_groups'):
            self._combobox_groups = {}

        combobox_widget = ttk.Combobox(self.root,
                                       values=display_values,
                                       height=nr_rows,
                                       state='readonly')

        # Add change event support
        if event_change and k:
            def combobox_change_handler(event):
                values = self._get_values()
                self.event_queue.put((k, values))

            combobox_widget.bind("<<ComboboxSelected>>", combobox_change_handler)

        if default is not None:
            default_found = False
            for i, (display_text, value) in enumerate(parsed_options):
                if value == default:
                    combobox_widget.current(i)
                    default_found = True
                    break

            if not default_found:
                for i, (display_text, value) in enumerate(parsed_options):
                    if display_text == default:
                        combobox_widget.current(i)
                        break

        combobox_widget.place(x=self.current_x, y=self.current_y)
        combobox_widget.update_idletasks()

        combobox_width = combobox_widget.winfo_reqwidth()
        combobox_height = combobox_widget.winfo_reqheight()

        max_width = max(max_width, combobox_width)

        combobox_elements = []
        element_positions = []

        if title_element:
            combobox_elements.append(title_element)
            element_positions.append((start_x, start_y))

        combobox_elements.append(combobox_widget)
        element_positions.append((self.current_x, self.current_y))

        if k:
            self._combobox_groups[k] = (combobox_widget, parsed_options)
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._combobox_groups[effective_key] = (combobox_widget, parsed_options)

        total_height = title_height + combobox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        if not hasattr(self, '_combobox_element_positions'):
            self._combobox_element_positions = {}

        self._combobox_element_positions[effective_key] = list(zip(combobox_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in combobox_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self