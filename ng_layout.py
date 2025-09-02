# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgLayout:
    """Layout and positioning management mixin"""

    def _init_layout(self):
        """Initialize layout variables"""
        self.initial_x = 0
        self.row_height = 22
        self.current_row_height = 0
        self.current_row_start_y = 0
        self.current_row_max_height = 0

        self.text_width_chars = None
        self.text_height_lines = None
        self.input_width_chars = None
        self.input_height_lines = None

        self.current_x = 0
        self.current_y = 0

    def _start_new_row(self):
        """Start new virtual row"""
        self.current_row_start_y = self.current_y
        self.current_row_height = self.row_height
        self.current_row_max_height = 0

    def _update_row_height(self, element_height):
        """Update maximum height of current row"""
        if element_height > self.current_row_max_height:
            self.current_row_max_height = element_height

        if element_height > self.current_row_height:
            self.current_row_height = element_height

    def _update_position(self, width, height=20):
        """Update position after adding element"""
        self._update_row_height(height)
        self.current_x += width + 5

    def setX(self, x):
        """Set current X coordinate"""
        self.current_x = x
        return self

    def setY(self, y):
        """Set current Y coordinate"""
        self.current_y = y
        return self

    def setTextSize(self, width_chars, height_lines=1):
        """Set dimensions for next text elements"""
        self.text_width_chars = width_chars
        self.text_height_lines = height_lines
        return self

    def setInputSize(self, width_chars, height_lines=1):
        """Set dimensions for next input elements"""
        self.input_width_chars = width_chars
        self.input_height_lines = height_lines
        return self

    def gotoxy(self, x, y):
        """Go to specified coordinates"""
        self.current_x = x
        self.current_y = y
        self.initial_x = x

        self._start_new_row()
        return self

    def crlf(self, spacing=0):
        """Go to new line using tallest element height"""
        if self.current_row_max_height > 0:
            self.current_y = self.current_row_start_y + self.current_row_max_height + spacing + 3
        else:
            self.current_y = self.current_row_start_y + self.row_height + spacing

        self.current_x = self.initial_x
        self._start_new_row()
        return self

    def gotoy(self, y):
        """Go to Y coordinate and reset X"""
        self.current_y = y
        self.current_x = self.initial_x

        self._start_new_row()
        return self

    def gotoBelow(self, k):
        """Position below element with key k"""
        if k in self.element_positions:
            x, y, width, height = self.element_positions[k]
            self.current_x = x
            self.current_y = y + height + 5
            self.initial_x = x
            self._start_new_row()
        return self

    def setRowHeigh(self, height):
        """Set current row height"""
        self.row_height = height
        return self