# ngweb_layout.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class WebElement:
    """Base class for all web elements"""
    
    def __init__(self, element_type, **kwargs):
        self.element_type = element_type
        self.attributes = kwargs
        self.key = kwargs.get('k', '')
        self.content = kwargs.get('text', '')
        self.value = kwargs.get('text', '')
        self.dirty = False
    
    def to_html(self):
        """Convert to HTML string - must be overridden"""
        return ''
    
    def get_value(self):
        """Get current value of element"""
        return self.value
    
    def set_value(self, value):
        """Set value and mark as dirty"""
        self.value = value
        self.dirty = True


class NgWebLayout:
    """Layout management for web interface"""
    
    def _init_layout(self):
        """Initialize layout variables"""
        self.current_x = 0
        self.current_y = 0
        self.initial_x = 0
        self.row_height = 22
        self.current_row_height = 0
        self.current_row_start_y = 0
        self.current_row_max_height = 0
        
        self.text_width_chars = None
        self.text_height_lines = None
        self.input_width_chars = None
        self.input_height_lines = None
    
    def move_to(self, x, y):
        """Move cursor to specified coordinates"""
        self.current_x = x
        self.current_y = y
        self.initial_x = x
        return self
    
    def br(self, spacing=0):
        """Line break - adds row separator"""
        self.current_y += self.row_height + spacing
        self.current_x = self.initial_x
        
        # Add break element for rendering
        break_element = WebElement('br', spacing=spacing)
        self.elements.append(break_element)
        return self
    
    def set_x(self, x):
        """Set current X coordinate"""
        self.current_x = x
        return self
    
    def set_y(self, y):
        """Set current Y coordinate"""
        self.current_y = y
        return self
    
    def set_text_size(self, width_chars, height_lines=1):
        """Set dimensions for next text elements"""
        self.text_width_chars = width_chars
        self.text_height_lines = height_lines
        return self
    
    def set_input_size(self, width_chars, height_lines=1):
        """Set dimensions for next input elements"""
        self.input_width_chars = width_chars
        self.input_height_lines = height_lines
        return self
    
    def move_y(self, y):
        """Go to Y coordinate and reset X"""
        self.current_y = y
        self.current_x = self.initial_x
        return self
    
    def set_row_height(self, height):
        """Set current row height"""
        self.row_height = height
        return self
