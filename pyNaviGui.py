# pyNaviGui.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

from ng_core import NgCore
from ng_defaults import NgDefaults
from ng_layout import NgLayout
from ng_elements_00 import NgElementsBase00
from ng_elements_05 import NgElementsBase05
from ng_elements_10 import NgElementsBase10
from ng_elements_20 import NgElementsBase20
from ng_elements_30 import NgElementsBase30
from ng_elements_40 import NgElementsBase40
from ng_elements_50 import NgElementsBase50
from ng_elements_60 import NgElementsBase60
from ng_elements_90 import NgElementsBase90
from ng_elements_nav import NgNavElements
from ng_elements_update import NgElementsUpdate
from ng_visibility import NgVisibility
from ng_utils import NgUtils


class Ng(NgCore, NgDefaults, NgLayout,
         NgElementsBase00, NgElementsBase05, NgElementsBase10, NgElementsBase20, NgElementsBase30,
         NgElementsBase40, NgElementsBase50, NgElementsBase60, NgElementsBase90,
         NgNavElements, NgElementsUpdate, NgVisibility, NgUtils):
    """Tkinter-based GUI implementation - Unified modular version

    Combines all mixins to provide complete pyNaviGui interface"""

    def __init__(self, geometry='800x600', embed_mode=False, parent_root=None):
        """Initialize pyNaviGui with all functionality"""
        super().__init__(geometry, embed_mode, parent_root)

        # Initialize panel functionality if available
        if hasattr(self, '_init_panel_elements'):
            self._init_panel_elements()