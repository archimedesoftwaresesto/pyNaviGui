# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgElementsUpdate:
    """Update functionality for all element types"""

    def update(self, k='', **kwargs):
        """Update existing elements based on their type"""
        if not self.exists(k):
            return self

        # Handle table updates
        if hasattr(self, '_table_groups') and k in self._table_groups:
            return self._update_table(k, **kwargs)

        # Handle text updates
        if k in self.element_keys:
            element = self.element_keys[k]
            if hasattr(element, 'configure') and 'text' in kwargs:
                element.configure(text=kwargs['text'])

        # Handle input updates
        if k in self.element_keys:
            element = self.element_keys[k]
            if hasattr(element, 'delete') and hasattr(element, 'insert') and 'text' in kwargs:
                element.delete(0, 'end')
                element.insert(0, kwargs['text'])

        # Add more element types as needed

        return self

    def _update_table(self, k, data=None, rowcolors=None, **kwargs):
        """Update table with new data and row colors"""
        if not hasattr(self, '_table_groups') or k not in self._table_groups:
            return self

        try:
            table_widget, column_keys = self._table_groups[k]

            # Clear existing items
            for item in table_widget.get_children():
                table_widget.delete(item)

            if data is None:
                return self

            # Reset existing tags - CORREZIONE: Usiamo il metodo corretto per i tags di Treeview
            try:
                # Otteniamo tutti i tag definiti
                all_tags = set()
                try:
                    # Se disponibile, otteniamo i tag dai metodi del widget
                    if hasattr(table_widget, 'tag_configure'):
                        for item in table_widget.get_children():
                            all_tags.update(table_widget.item(item, 'tags'))
                except:
                    pass

                # Resettiamo ogni tag trovato
                for tag in all_tags:
                    if tag and tag != "":
                        try:
                            table_widget.tag_configure(tag, background="", foreground="")
                        except:
                            pass
            except Exception as e:
                print(f"Warning: error resetting tags: {e}")

            # Set up color mapping
            row_color_map = {}
            if rowcolors:
                for row_color_info in rowcolors:
                    if len(row_color_info) == 2:
                        row_index, bg_color = row_color_info
                        row_color_map[row_index] = (bg_color, None)
                    elif len(row_color_info) >= 3:
                        row_index, bg_color, fg_color = row_color_info[:3]
                        row_color_map[row_index] = (bg_color, fg_color)

            # Configure color tags
            for row_index, color_info in row_color_map.items():
                bg_color, fg_color = color_info
                if fg_color is None:
                    tag_name = f"bg_{bg_color}"
                    table_widget.tag_configure(tag_name, background=bg_color)
                else:
                    tag_name = f"bg_{bg_color}_fg_{fg_color}"
                    table_widget.tag_configure(tag_name, background=bg_color, foreground=fg_color)

            # Insert new data
            for row_index, row_data in enumerate(data):
                # Ensure data fits column count
                if len(row_data) >= len(column_keys):
                    values_to_insert = row_data[:len(column_keys)]
                else:
                    padded_row = list(row_data) + [''] * (len(column_keys) - len(row_data))
                    values_to_insert = padded_row

                # Determine tags for this row
                tags = ()
                if row_index in row_color_map:
                    bg_color, fg_color = row_color_map[row_index]
                    if fg_color is None:
                        tag_name = f"bg_{bg_color}"
                    else:
                        tag_name = f"bg_{bg_color}_fg_{fg_color}"
                    tags = (tag_name,)

                # Insert the row
                item_id = table_widget.insert('', 'end', values=values_to_insert, tags=tags)

            # Force UI update
            table_widget.update()
            print("Tabella aggiornata con successo")

        except Exception as e:
            print(f"Error updating table {k}: {e}")
            import traceback
            traceback.print_exc()

        return self