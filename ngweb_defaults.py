# ngweb_defaults.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgWebDefaults:
    """Default parameters management for web version"""
    
    def _init_defaults(self):
        """Initialize default parameter variables"""
        self.default_s = ''
        self.default_fg = ''
        self.default_bg = ''
        self.default_k_prefix = ''
    
    def set(self, s=None, fg=None, bg=None, k_prefix=None):
        """Set default parameters for subsequent elements"""
        if s is not None:
            self.default_s = s
        if fg is not None:
            self.default_fg = fg
        if bg is not None:
            self.default_bg = bg
        if k_prefix is not None:
            self.default_k_prefix = k_prefix
        
        return self
    
    def _merge_defaults(self, s='', fg='', bg='', k=''):
        """Merge passed parameters with defaults"""
        merged_s = s if s else self.default_s
        merged_fg = fg if fg else self.default_fg
        merged_bg = bg if bg else self.default_bg
        
        merged_k = k
        if k and self.default_k_prefix:
            merged_k = self.default_k_prefix + k
        
        return merged_s, merged_fg, merged_bg, merged_k
    
    def reset_defaults(self):
        """Reset all default parameters"""
        self.default_s = ''
        self.default_fg = ''
        self.default_bg = ''
        self.default_k_prefix = ''
        return self
