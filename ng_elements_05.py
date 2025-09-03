# ng_elements_05.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk


class NgElementsBase05:
    """Rectangle element implementation"""

    def rectangle(self, width=100, height=100, k='', s='', fg='', bg='lightgray'):
        """Create a rectangle shape as background element"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        # Create a frame to represent our rectangle
        rect = tk.Frame(self.root, width=width, height=height, bg=bg, highlightbackground=fg,
                        highlightthickness=1 if fg else 0)
        rect.place(x=self.current_x, y=self.current_y)

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)
        self._register_element(rect, k, s)

        return self