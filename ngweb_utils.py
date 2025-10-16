# ngweb_utils.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgWebUtils:
    """Utility functions for web version"""
    
    def set_keys(self, max_nr_keys=100, key_start_with_string=''):
        """Generate a list of keys"""
        return [key_start_with_string + str(i) for i in range(max_nr_keys)]
    
    def exists(self, k):
        """Check if element with key k exists"""
        return (k in self.element_keys and
                self.element_keys[k] is not None and
                not k.startswith('__auto_key_'))
    
    def update(self, k='', **kwargs):
        """Update existing elements"""
        if not self.exists(k):
            return self
        
        element = self.element_keys[k]
        
        # Handle text updates
        if 'text' in kwargs:
            if hasattr(element, 'content'):
                element.content = kwargs['text']
                element.dirty = True
            if hasattr(element, 'value'):
                element.value = kwargs['text']
                element.dirty = True
        
        return self
    
    def finalize_layout(self):
        """Store initial element count"""
        self.initial_elements_count = len(self.elements)
        return self
