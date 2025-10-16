# pyNaviGuiWeb.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

from ngweb_core import NgWebCore
from ngweb_defaults import NgWebDefaults
from ngweb_layout import NgWebLayout
from ngweb_elements_00 import NgWebElementsBase00
from ngweb_utils import NgWebUtils


class NgWeb(NgWebCore, NgWebDefaults, NgWebLayout,
            NgWebElementsBase00, NgWebUtils):
    """Web-based GUI implementation using Flask + HTMX"""
    
    def __init__(self, geometry='800x600', app_name='app'):
        """Initialize pyNaviGuiWeb with all functionality"""
        # Make app_name optional (can be set later by runner)
        if app_name is None:
            import os
            import sys
            app_name = os.path.basename(sys.argv[0]).replace('.py', '')
        
        super().__init__(geometry, app_name)


# Alias for compatibility
Ng = NgWeb
