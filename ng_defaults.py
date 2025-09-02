# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgDefaults:
    """Mixin per la gestione dei parametri di default"""

    def _init_defaults(self):
        """Inizializza le variabili per la funzione set()"""
        self.default_s = ''
        self.default_fg = ''
        self.default_bg = ''
        self.default_k_prefix = ''

    def set(self, s=None, fg=None, bg=None, k_prefix=None):
        """Imposta parametri di default per tutti gli elementi successivi

        Args:
            s (str): Stringa di selezione di default (per visible, move, etc.)
            fg (str): Colore del testo di default
            bg (str): Colore dello sfondo di default
            k_prefix (str): Prefisso da aggiungere automaticamente alle chiavi

        Per resettare un parametro, passa una stringa vuota ''
        Per non modificare un parametro, non passarlo o passa None
        """
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
        """Unisce i parametri passati con quelli di default

        I parametri espliciti hanno sempre precedenza sui default
        """
        merged_s = s if s else self.default_s
        merged_fg = fg if fg else self.default_fg
        merged_bg = bg if bg else self.default_bg

        # Per le chiavi, aggiungi il prefisso solo se c'è una chiave
        merged_k = k
        if k and self.default_k_prefix:
            merged_k = self.default_k_prefix + k

        return merged_s, merged_fg, merged_bg, merged_k

    def resetDefaults(self):
        """Resetta tutti i parametri di default"""
        self.default_s = ''
        self.default_fg = ''
        self.default_bg = ''
        self.default_k_prefix = ''
        return self