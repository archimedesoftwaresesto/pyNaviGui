# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgLayout:
    """Mixin per la gestione del layout e posizionamento"""

    def _init_layout(self):
        """Inizializza le variabili per il layout"""
        # Coordinata X iniziale per l'allineamento
        self.initial_x = 0
        self.row_height = 22
        self.current_row_height = 0
        self.current_row_start_y = 0
        self.current_row_max_height = 0

        # Dimensioni per i prossimi elementi text e input
        self.text_width_chars = None
        self.text_height_lines = None
        self.input_width_chars = None
        self.input_height_lines = None

        # Posizionamento corrente
        self.current_x = 0
        self.current_y = 0

    def _start_new_row(self):
        """Inizia una nuova riga virtuale, resettando il tracciamento dell'altezza"""
        self.current_row_start_y = self.current_y
        self.current_row_height = self.row_height  # Altezza minima di default
        self.current_row_max_height = 0  # RESET del massimo della riga

    def _update_row_height(self, element_height):
        """CORREZIONE: Aggiorna l'altezza massima della riga corrente"""
        # Traccia l'altezza dell'elemento più alto nella riga corrente
        if element_height > self.current_row_max_height:
            self.current_row_max_height = element_height

        # Aggiorna anche current_row_height per compatibilità 
        if element_height > self.current_row_height:
            self.current_row_height = element_height

    def _update_position(self, width, height=20):
        """Aggiorna la posizione corrente dopo aver aggiunto un elemento"""
        # CORREZIONE: Aggiorna il tracciamento dell'altezza massima della riga
        self._update_row_height(height)

        self.current_x += width + 5  # Spazio tra elementi

    def setX(self, x):
        """Imposta la coordinata X corrente"""
        self.current_x = x
        return self

    def setY(self, y):
        """Imposta la coordinata Y corrente"""
        self.current_y = y
        return self

    def setTextSize(self, width_chars, height_lines=1):
        """Imposta la dimensione per i prossimi elementi text

        Args:
            width_chars (int): Larghezza in caratteri
            height_lines (int): Altezza in righe (default 1)
        """
        self.text_width_chars = width_chars
        self.text_height_lines = height_lines
        return self

    def setInputSize(self, width_chars, height_lines=1):
        """Imposta la dimensione per i prossimi elementi input

        Args:
            width_chars (int): Larghezza in caratteri
            height_lines (int): Altezza in righe (default 1)
        """
        self.input_width_chars = width_chars
        self.input_height_lines = height_lines
        return self

    def gotoxy(self, x, y):
        """Va alle coordinate X,Y specificate e memorizza X come coordinata di inizio riga"""
        self.current_x = x
        self.current_y = y
        self.initial_x = x  # Memorizza la X iniziale per i successivi crlf()

        # Inizia una nuova riga virtuale
        self._start_new_row()

        return self

    def crlf(self, spacing=0):
        """CORREZIONE: Va a capo usando l'altezza dell'elemento più alto della riga corrente

        Args:
            spacing (int): Spazio aggiuntivo tra righe (default 0)
        """
        # USA L'ALTEZZA MASSIMA RILEVATA NELLA RIGA CORRENTE
        if self.current_row_max_height > 0:
            # Usa l'altezza dell'elemento più alto + un piccolo margine
            self.current_y = self.current_row_start_y + self.current_row_max_height + spacing + 3
        else:
            # Fallback: usa l'altezza di default se non sono stati aggiunti elementi
            self.current_y = self.current_row_start_y + self.row_height + spacing

        # Reset della X alla coordinata iniziale
        self.current_x = self.initial_x

        # Inizia una nuova riga virtuale
        self._start_new_row()

        return self

    def gotoy(self, y):
        """Va alla coordinata Y specificata e resetta X alla coordinata iniziale"""
        self.current_y = y
        self.current_x = self.initial_x  # Usa initial_x invece di 0

        # Inizia una nuova riga virtuale
        self._start_new_row()

        return self

    def gotoBelow(self, k):
        """Posiziona il cursore sotto l'elemento con la chiave specificata e
        aggiorna initial_x per mantenere l'allineamento in colonna"""
        if k in self.element_positions:
            x, y, width, height = self.element_positions[k]
            self.current_x = x
            self.current_y = y + height + 5  # Aggiunge un piccolo spazio sotto l'elemento
            # CORREZIONE: Aggiorna anche initial_x per mantenere l'allineamento della colonna
            self.initial_x = x
            # Inizia una nuova riga virtuale
            self._start_new_row()
        return self

    def setRowHeigh(self, height):
        """Imposta l'altezza della riga corrente (virtuale)"""
        self.row_height = height
        return self