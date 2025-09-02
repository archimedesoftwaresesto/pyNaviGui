# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

from ng_core import NgCore
from ng_defaults import NgDefaults
from ng_layout import NgLayout
from ng_elements import NgElements
from ng_visibility import NgVisibility
from ng_utils import NgUtils


class Ng(NgCore, NgDefaults, NgLayout, NgElements, NgVisibility, NgUtils):
    """Implementazione GUI basata su Tkinter - Versione modulare unificata
    
    Questa classe combina tutti i mixin per fornire l'interfaccia completa di pyNaviGui:
    - NgCore: Gestione finestra, eventi, logica base
    - NgDefaults: Sistema di parametri di default (set, _merge_defaults)
    - NgLayout: Posizionamento e layout (gotoxy, crlf, setTextSize)
    - NgElements: Elementi UI (text, input, button, checkboxes)
    - NgVisibility: Visibilità e movimento (visible, move)
    - NgUtils: Funzioni di utilità (exists, delete, finalize_layout)
    """

    def __init__(self, geometry='800x600', embed_mode=False, parent_root=None):
        """Inizializza pyNaviGui con tutte le funzionalità
        
        Args:
            geometry (str): Geometria della finestra (ignorata in embed_mode)
            embed_mode (bool): Se True, non crea una finestra propria
            parent_root: Root Tkinter genitore (richiesto se embed_mode=True)
        """
        # L'inizializzazione è gestita da NgCore che chiama tutti i _init_* dei mixin
        super().__init__(geometry, embed_mode, parent_root)