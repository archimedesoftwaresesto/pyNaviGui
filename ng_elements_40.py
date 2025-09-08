# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk

class NgElementsBase40:
    """Data display elements: table"""

    def table(self, title_or_conf, conf=None, data=None, nr_rows=5, k='', s='', rowcolors=None,
              event_click=False, event_dbclick=False):
        """Create table using Tkinter ttk.Treeview with optional click events"""
        try:
            import tkinter.ttk as ttk
        except ImportError:
            from tkinter import ttk

        s, _, _, k = self._merge_defaults(s, '', '', k)

        if conf is None:
            title = None
            table_conf = title_or_conf if title_or_conf else {'COL1': ['Column 1', 15]}
        else:
            title = title_or_conf
            table_conf = conf if conf else {'COL1': ['Column 1', 15]}

        if data is None:
            data = []

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

        column_keys = list(table_conf.keys())
        column_names = [table_conf[key][0] for key in column_keys]
        column_widths = [table_conf[key][1] * 10 for key in column_keys]

        table_widget = ttk.Treeview(self.root,
                                    columns=column_keys,
                                    show='headings',
                                    height=nr_rows)

        # Handle click and double-click events with proper coordination
        if (event_click or event_dbclick) and k:
            # Store timer reference in the widget itself
            table_widget.click_timer = None
            table_widget.double_click_pending = False

            if event_click:
                def table_click_handler(event):
                    # Cancel any pending timer
                    if table_widget.click_timer:
                        self.root.after_cancel(table_widget.click_timer)

                    # If double-click is also enabled, delay the click event
                    if event_dbclick:
                        table_widget.double_click_pending = False

                        # Wait 300ms to see if a double-click follows
                        def delayed_click():
                            if not table_widget.double_click_pending:
                                values = self._get_values()
                                self.event_queue.put((k, values))

                        table_widget.click_timer = self.root.after(300, delayed_click)
                    else:
                        # No double-click enabled, fire immediately
                        values = self._get_values()
                        self.event_queue.put((k, values))

                table_widget.bind("<<TreeviewSelect>>", table_click_handler)

            if event_dbclick:
                def table_dbclick_handler(event):
                    # Cancel the pending click timer
                    if table_widget.click_timer:
                        self.root.after_cancel(table_widget.click_timer)
                        table_widget.click_timer = None

                    # Mark that a double-click occurred
                    table_widget.double_click_pending = True

                    # Fire double-click event
                    values = self._get_values()
                    self.event_queue.put((f"{k}_DBCLICK", values))

                table_widget.bind("<Double-Button-1>", table_dbclick_handler)

        for i, col_key in enumerate(column_keys):
            table_widget.heading(col_key, text=column_names[i])
            table_widget.column(col_key, width=column_widths[i], minwidth=50)

        row_color_map = {}
        if rowcolors:
            for row_color_info in rowcolors:
                if len(row_color_info) == 2:
                    row_index, bg_color = row_color_info
                    row_color_map[row_index] = (bg_color, None)
                elif len(row_color_info) >= 3:
                    row_index, bg_color, fg_color = row_color_info[:3]
                    row_color_map[row_index] = (bg_color, fg_color)

        unique_color_combinations = set()
        if rowcolors:
            for row_index, color_info in row_color_map.items():
                unique_color_combinations.add(color_info)

        for bg_color, fg_color in unique_color_combinations:
            if fg_color is None:
                tag_name = f"bg_{bg_color}"
                table_widget.tag_configure(tag_name, background=bg_color)
            else:
                tag_name = f"bg_{bg_color}_fg_{fg_color}"
                table_widget.tag_configure(tag_name, background=bg_color, foreground=fg_color)

        inserted_items = []
        for row_index, row_data in enumerate(data):
            if len(row_data) >= len(column_keys):
                values_to_insert = row_data[:len(column_keys)]
            else:
                padded_row = list(row_data) + [''] * (len(column_keys) - len(row_data))
                values_to_insert = padded_row

            tags = ()
            if row_index in row_color_map:
                bg_color, fg_color = row_color_map[row_index]
                if fg_color is None:
                    tag_name = f"bg_{bg_color}"
                else:
                    tag_name = f"bg_{bg_color}_fg_{fg_color}"
                tags = (tag_name,)

            item_id = table_widget.insert('', 'end', values=values_to_insert, tags=tags)
            inserted_items.append(item_id)

        v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=table_widget.yview)
        h_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=table_widget.xview)

        table_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        table_widget.place(x=self.current_x, y=self.current_y)
        table_widget.update_idletasks()

        table_width = table_widget.winfo_reqwidth()
        table_height = table_widget.winfo_reqheight()

        scrollbar_width = 20
        v_scrollbar.place(x=self.current_x + table_width, y=self.current_y, height=table_height)
        h_scrollbar.place(x=self.current_x, y=self.current_y + table_height, width=table_width)

        total_width = table_width + scrollbar_width
        total_height = table_height + scrollbar_width

        max_width = max(max_width, total_width)

        table_elements = []
        element_positions = []

        if title_element:
            table_elements.append(title_element)
            element_positions.append((start_x, start_y))

        table_elements.extend([table_widget, v_scrollbar, h_scrollbar])
        element_positions.extend([
            (self.current_x, self.current_y),
            (self.current_x + table_width, self.current_y),
            (self.current_x, self.current_y + table_height)
        ])

        if k:
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        final_total_height = title_height + total_height
        if title_height > 0:
            final_total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, final_total_height)

        if not hasattr(self, '_table_groups'):
            self._table_groups = {}

        self._table_groups[effective_key] = (table_widget, column_keys)

        if not hasattr(self, '_table_element_positions'):
            self._table_element_positions = {}

        self._table_element_positions[effective_key] = list(zip(table_elements, element_positions))

        # Register main table widget in element_keys
        self.element_keys[effective_key] = table_widget

        if s:
            self.element_strings[effective_key] = s

        for element in table_elements:
            self._register_element(element, '', s)

        self._update_row_height(final_total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self