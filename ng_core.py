# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import queue

class NgCore:
    """Classe base per pyNaviGui - gestisce finestra, eventi e logica base"""

    def __init__(self, geometry='800x600', embed_mode=False, parent_root=None):
        """Implementazione GUI basata su Tkinter con supporto per modalità embedded

        Args:
            geometry (str): Geometria della finestra (ignorata in embed_mode)
            embed_mode (bool): Se True, non crea una finestra propria
            parent_root: Root Tkinter genitore (richiesto se embed_mode=True)
        """
        # Inizializzazione attributi base
        self.title = 'pyNaviGui'
        self.geometry = geometry
        self.window_closed = False
        self.event_queue = queue.Queue()
        self.event_handlers = {}
        self.initial_elements_count = 0

        # MODALITÀ EMBEDDED
        self.embed_mode = embed_mode

        if embed_mode:
            if parent_root is None:
                raise ValueError("parent_root è richiesto quando embed_mode=True")
            self.root = parent_root
            # Non applicare geometria o titolo in modalità embedded
        else:
            # Inizializzazione Tkinter normale
            self.root = tk.Tk()
            self._update_title_impl()
            self._update_geometry_impl()
            # Gestione chiusura finestra solo se non in embed_mode
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Inizializza i mixin (gli altri mixin devono implementare questi metodi)
        if hasattr(self, '_init_defaults'):
            self._init_defaults()
        if hasattr(self, '_init_layout'):
            self._init_layout()
        if hasattr(self, '_init_elements'):
            self._init_elements()

    def _on_closing(self):
        """Chiamata quando la finestra viene chiusa"""
        self.window_closed = True
        self.event_queue.put((None, {}))

    def _update_title_impl(self):
        """Implementazione specifica per aggiornare il titolo"""
        if hasattr(self, 'root'):
            self.root.title(self.title)

    def _update_geometry_impl(self):
        """Implementazione specifica per aggiornare la geometria"""
        if hasattr(self, 'root') and self.geometry:
            self.root.geometry(self.geometry)

    def _close_impl(self):
        """Implementazione specifica per la chiusura"""
        if hasattr(self, 'root') and not self.window_closed:
            self.root.quit()
            self.root.destroy()

    def _delete_element_impl(self, element):
        """Implementazione specifica per rimuovere un elemento dalla GUI Tkinter"""
        if hasattr(element, 'destroy'):
            element.destroy()

    def winTitle(self, title):
        """Imposta il titolo della finestra"""
        self.title = title
        self._update_title_impl()
        return self

    def winGeometry(self, geometry):
        """Imposta la geometria della finestra"""
        self.geometry = geometry
        self._update_geometry_impl()
        return self

    def register_event_handler(self, event_key, handler_func):
        """Registra un handler per un evento specifico"""
        self.event_handlers[event_key] = handler_func

    def process_event(self, event_key, values):
        """Processa un evento usando l'handler registrato"""
        if event_key in self.event_handlers:
            return self.event_handlers[event_key](values)
        return None

    def show(self):
        """Avvia il loop principale di Tkinter"""
        self.root.mainloop()
        return self

    def read(self, timeout=None):
        """Legge il prossimo evento (versione Tkinter)"""
        if self.window_closed:
            return None, {}

        try:
            # Aggiorna la GUI
            self.root.update()

            # Controlla se c'è un evento in coda
            if not self.event_queue.empty():
                event, values = self.event_queue.get_nowait()
                return event, values
            else:
                # Se non ci sono eventi, restituisce stringa vuota
                return '', {}

        except tk.TclError:
            # Finestra è stata chiusa
            self.window_closed = True
            return None, {}

    def close(self):
        """Chiude la finestra (solo se non in modalità embedded)"""
        if not self.embed_mode:
            self.window_closed = True
            self._close_impl()
        # In modalità embedded non chiudere il root perché appartiene al genitore