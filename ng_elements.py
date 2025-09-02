# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    print("ERRORE: PIL/Pillow non installato. Installare con: pip install Pillow")
    Image = None
    ImageTk = None

class NgElements:
    """Mixin per la gestione degli elementi UI"""

    def _init_elements(self):
        """Inizializza le variabili per gli elementi"""
        self.elements = []
        self.element_keys = {}
        self.element_positions = {}
        self.element_strings = {}
        self.element_counter = 0

    def _register_element(self, element, key, s=''):
        """Registra un elemento con la sua chiave e stringa di selezione"""
        self.elements.append(element)

        # Se non c'è chiave, genera un ID interno univoco
        if not key:
            key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        self.element_keys[key] = element

        if s:
            self.element_strings[key] = s

    def _register_element_position(self, key, x, y, width, height):
        """Registra la posizione di un elemento"""
        if key:
            self.element_positions[key] = (x, y, width, height)

    def text(self, text='', k='', s='', fg='', bg=''):
        """Crea un elemento di testo usando Tkinter Label"""
        # Applica i default
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        # Costruisci le opzioni per il Label
        label_options = {'text': text}
        if fg:  # Se il colore del testo è specificato
            label_options['fg'] = fg
        if bg:  # Se il colore di sfondo è specificato
            label_options['bg'] = bg

        # Applica le dimensioni se specificate
        if self.text_width_chars is not None:
            label_options['width'] = self.text_width_chars
            # Quando viene specificata una larghezza, allinea a sinistra
            label_options['anchor'] = 'w'  # 'w' = west = sinistra
        if self.text_height_lines is not None and self.text_height_lines > 1:
            label_options['height'] = self.text_height_lines

        label = tk.Label(self.root, **label_options)
        label.place(x=self.current_x, y=self.current_y)
        label.update_idletasks()
        width = label.winfo_reqwidth()
        height = label.winfo_reqheight()

        # Ottieni la chiave effettiva che verrà usata (potrebbe essere auto-generata)
        effective_key = k if k else f"__auto_key_{self.element_counter}"

        # Registra la posizione dell'elemento
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(label, k, s)

        return self

    def input(self, text='', k='', s=''):
        """Crea un elemento di input usando Tkinter Entry"""
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Costruisci le opzioni per l'Entry
        entry_options = {}

        # Applica le dimensioni se specificate
        if self.input_width_chars is not None:
            entry_options['width'] = self.input_width_chars

        entry = tk.Entry(self.root, **entry_options)
        if text:
            entry.insert(0, text)
        entry.place(x=self.current_x, y=self.current_y)
        entry.update_idletasks()
        width = entry.winfo_reqwidth()
        height = entry.winfo_reqheight()

        # Per gli input multi-riga (se height_lines > 1), potremmo usare Text invece di Entry
        # ma per ora manteniamo Entry anche per compatibilità 
        if self.input_height_lines is not None and self.input_height_lines > 1:
            # Nota: Entry in Tkinter è sempre single-line. Per multi-riga servirebbero modifiche più profonde
            # Per ora ignoriamo l'altezza in linee per gli Entry
            pass

        # Ottieni la chiave effettiva che verrà usata (potrebbe essere auto-generata)
        effective_key = k if k else f"__auto_key_{self.element_counter}"

        # Registra la posizione dell'elemento
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(entry, k, s)

        return self

    def button(self, text='', k='', s='', command=None):
        """Crea un bottone usando Tkinter Button"""
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        def button_callback():
            if k:
                # Metti l'evento nella coda
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        button = tk.Button(self.root, text=text, command=button_callback)
        button.place(x=self.current_x, y=self.current_y)
        button.update_idletasks()
        width = button.winfo_reqwidth()
        height = button.winfo_reqheight()

        # Ottieni la chiave effettiva che verrà usata (potrebbe essere auto-generata)
        effective_key = k if k else f"__auto_key_{self.element_counter}"

        # Registra la posizione dell'elemento
        self._register_element_position(effective_key, self.current_x, self.current_y, width, height)

        self._update_position(width, height)
        self._register_element(button, k, s)

        return self

    def checkboxes(self, title_or_options, options=None, k='', s=''):
        """Crea un gruppo di checkbox usando Tkinter Checkbutton"""
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no
        if options is None:
            title = None
            checkbox_options = title_or_options
        else:
            title = title_or_options
            checkbox_options = options

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        checkbox_height = 22
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        # Parsing delle opzioni
        parsed_options = []
        for option in checkbox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        if not hasattr(self, '_checkbox_groups'):
            self._checkbox_groups = {}

        checkbox_vars = []
        checkboxes_elements = []
        element_positions = []  # Lista per salvare le posizioni di ogni elemento

        # Se abbiamo un titolo, registralo
        if title_element:
            checkboxes_elements.append(title_element)
            element_positions.append((start_x, start_y))

        checkbox_start_y = self.current_y

        for i, (display_text, value) in enumerate(parsed_options):
            var = tk.BooleanVar()
            checkbox_vars.append((var, value))

            checkbox = tk.Checkbutton(
                self.root,
                text=display_text,
                variable=var,
                anchor='w'
            )

            checkbox.place(x=self.current_x, y=self.current_y)
            checkbox.update_idletasks()

            width = checkbox.winfo_reqwidth()
            height = max(checkbox.winfo_reqheight(), checkbox_height)

            checkboxes_elements.append(checkbox)
            element_positions.append((self.current_x, self.current_y))  # Salva posizione

            max_width = max(max_width, width)

            if i < len(parsed_options) - 1:
                self.current_y += height

        # Determina la chiave effettiva
        if k:
            self._checkbox_groups[k] = checkbox_vars
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._checkbox_groups[effective_key] = checkbox_vars

        total_height = title_height + len(parsed_options) * checkbox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        # CORREZIONE: Registra ogni elemento con la sua posizione per la visibilità 
        if not hasattr(self, '_checkbox_element_positions'):
            self._checkbox_element_positions = {}

        # Salva le posizioni di tutti gli elementi del gruppo
        self._checkbox_element_positions[effective_key] = list(zip(checkboxes_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in checkboxes_elements:
            self._register_element(element, '', s)

        # Aggiorna tracciamento altezza riga
        self._update_row_height(total_height)

        # Posizionamento per elemento successivo
        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    def radio(self, title_or_options, options=None, k='', s='', default=None):
        """Crea un gruppo di radio button usando Tkinter Radiobutton

        Args:
            title_or_options: Se options è None, è la lista delle opzioni; altrimenti è il titolo
            options: Lista delle opzioni (se title_or_options è il titolo)
            k: Chiave per identificare il gruppo di radio button
            s: Stringa di selezione per operazioni di visibilità
            default: Valore di default da selezionare inizialmente
        """
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no
        if options is None:
            title = None
            radio_options = title_or_options
        else:
            title = title_or_options
            radio_options = options

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        radio_height = 22
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        # Parsing delle opzioni
        parsed_options = []
        for option in radio_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        # Inizializza i gruppi di radio button se non esistono
        if not hasattr(self, '_radio_groups'):
            self._radio_groups = {}

        # Crea una variabile condivisa per tutti i radio button del gruppo
        radio_var = tk.StringVar()

        # Imposta il valore di default se specificato
        if default is not None:
            # Controlla se il valore di default esiste tra le opzioni
            default_found = False
            for display_text, value in parsed_options:
                if value == default:
                    radio_var.set(value)
                    default_found = True
                    break

            if not default_found:
                # Se il default non è trovato, usa il primo elemento
                if parsed_options:
                    radio_var.set(parsed_options[0][1])
        else:
            # Se non c'è default, seleziona il primo elemento
            if parsed_options:
                radio_var.set(parsed_options[0][1])

        radio_elements = []
        element_positions = []

        # Se abbiamo un titolo, registralo
        if title_element:
            radio_elements.append(title_element)
            element_positions.append((start_x, start_y))

        radio_start_y = self.current_y

        for i, (display_text, value) in enumerate(parsed_options):
            radiobutton = tk.Radiobutton(
                self.root,
                text=display_text,
                variable=radio_var,
                value=value,
                anchor='w'
            )

            radiobutton.place(x=self.current_x, y=self.current_y)
            radiobutton.update_idletasks()

            width = radiobutton.winfo_reqwidth()
            height = max(radiobutton.winfo_reqheight(), radio_height)

            radio_elements.append(radiobutton)
            element_positions.append((self.current_x, self.current_y))

            max_width = max(max_width, width)

            if i < len(parsed_options) - 1:
                self.current_y += height

        # Determina la chiave effettiva
        if k:
            self._radio_groups[k] = radio_var
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._radio_groups[effective_key] = radio_var

        total_height = title_height + len(parsed_options) * radio_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        # Gestione per la visibilità - simile ai checkbox
        if not hasattr(self, '_radio_element_positions'):
            self._radio_element_positions = {}

        # Salva le posizioni di tutti gli elementi del gruppo
        self._radio_element_positions[effective_key] = list(zip(radio_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in radio_elements:
            self._register_element(element, '', s)

        # Aggiorna tracciamento altezza riga
        self._update_row_height(total_height)

        # Posizionamento per elemento successivo
        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    def listbox(self, title_or_options, options=None, k='', s='', default=None, nr_rows=5, multi_select=False):
        """Crea una listbox usando Tkinter Listbox

        Args:
            title_or_options: Se options è None, è la lista delle opzioni; altrimenti è il titolo
            options: Lista delle opzioni (se title_or_options è il titolo)
            k: Chiave per identificare la listbox
            s: Stringa di selezione per operazioni di visibilità
            default: Valore di default da selezionare inizialmente (stringa per single, lista per multi)
            nr_rows: Numero di righe visibili nella listbox (default 5)
            multi_select: Se True, permette selezione multipla (default False)
        """
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no
        if options is None:
            title = None
            listbox_options = title_or_options
        else:
            title = title_or_options
            listbox_options = options

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        # Parsing delle opzioni
        parsed_options = []
        for option in listbox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))

        # Inizializza i gruppi di listbox se non esistono
        if not hasattr(self, '_listbox_groups'):
            self._listbox_groups = {}

        # Crea la listbox con il numero di righe specificato e modalità di selezione
        selectmode = tk.EXTENDED if multi_select else tk.SINGLE
        listbox = tk.Listbox(self.root, height=nr_rows, selectmode=selectmode)

        # Crea la scrollbar e collegala alla listbox
        scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        # Aggiungi gli elementi alla listbox
        for display_text, value in parsed_options:
            listbox.insert(tk.END, display_text)

        # Imposta la selezione di default se specificata
        if default is not None:
            if multi_select:
                # Per selezione multipla, default può essere una lista
                default_values = default if isinstance(default, (list, tuple)) else [default]
                for i, (display_text, value) in enumerate(parsed_options):
                    if value in default_values:
                        listbox.selection_set(i)
                        if i == 0 or value == default_values[0]:  # Assicura che il primo sia visibile
                            listbox.see(i)
            else:
                # Per selezione singola, comportamento originale
                for i, (display_text, value) in enumerate(parsed_options):
                    if value == default:
                        listbox.selection_set(i)
                        listbox.see(i)  # Assicura che l'elemento sia visibile
                        break

        # Posiziona la listbox e la scrollbar
        listbox.place(x=self.current_x, y=self.current_y)
        listbox.update_idletasks()

        listbox_width = listbox.winfo_reqwidth()
        listbox_height = listbox.winfo_reqheight()

        # Posiziona la scrollbar accanto alla listbox
        scrollbar_width = 20  # Larghezza standard scrollbar
        scrollbar.place(x=self.current_x + listbox_width, y=self.current_y, height=listbox_height)

        max_width = max(max_width, listbox_width + scrollbar_width)

        listbox_elements = []
        element_positions = []

        # Se abbiamo un titolo, registralo
        if title_element:
            listbox_elements.append(title_element)
            element_positions.append((start_x, start_y))

        # Registra sia la listbox che la scrollbar
        listbox_elements.append(listbox)
        listbox_elements.append(scrollbar)
        element_positions.append((self.current_x, self.current_y))
        element_positions.append((self.current_x + listbox_width, self.current_y))

        # Determina la chiave effettiva e salva il flag multi_select
        if k:
            self._listbox_groups[k] = (listbox, parsed_options, multi_select)
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._listbox_groups[effective_key] = (listbox, parsed_options, multi_select)

        total_height = title_height + listbox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        # Gestione per la visibilità - simile ai checkbox e radio
        if not hasattr(self, '_listbox_element_positions'):
            self._listbox_element_positions = {}

        # Salva le posizioni di tutti gli elementi del gruppo
        self._listbox_element_positions[effective_key] = list(zip(listbox_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in listbox_elements:
            self._register_element(element, '', s)

        # Aggiorna tracciamento altezza riga
        self._update_row_height(total_height)

        # Posizionamento per elemento successivo
        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    # Aggiungi questo metodo alla classe NgElements in ng_elements.py
    # Inseriscilo dopo il metodo listbox() e prima di _get_values()

    # IMPORTANTE: Aggiungi anche l'import di tkinter.constants all'inizio del file se non c'è già:
    # import tkinter.constants as tk_const
    # oppure usa direttamente tk.WORD, tk.VERTICAL, ecc.

    # Aggiungi questo metodo alla classe NgElements in ng_elements.py
    # Inseriscilo dopo il metodo listbox() e prima di _get_values()

    # IMPORTANTE: Aggiungi anche l'import di tkinter.constants all'inizio del file se non c'è già:
    # import tkinter.constants as tk_const
    # oppure usa direttamente tk.WORD, tk.VERTICAL, ecc.

    def multiline(self, title_or_text, text=None, k='', s='', nr_rows=5, nr_cols=40):
        """Crea un elemento di input multilinea usando Tkinter Text con label opzionale

        Args:
            title_or_text: Se text è None, è il testo iniziale; altrimenti è il titolo della label
            text (str): Testo iniziale da inserire (se title_or_text è il titolo)
            k (str): Chiave per identificare l'elemento
            s (str): Stringa di selezione per operazioni di visibilità
            nr_rows (int): Numero di righe visibili (default 5)
            nr_cols (int): Numero di colonne in caratteri (default 40)
        """
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no (stessa logica di checkbox/radio)
        if text is None:
            title = None
            initial_text = title_or_text if title_or_text else ''
        else:
            title = title_or_text
            initial_text = text if text else ''

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2  # Piccolo spazio tra titolo e text widget

        # Crea il widget Text con scrollbar
        text_widget = tk.Text(self.root, height=nr_rows, width=nr_cols, wrap=tk.WORD)

        # Crea la scrollbar verticale
        scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        # Inserisci il testo iniziale se specificato
        if initial_text:
            text_widget.insert('1.0', initial_text)

        # Posiziona il widget Text
        text_widget.place(x=self.current_x, y=self.current_y)
        text_widget.update_idletasks()

        # Calcola le dimensioni
        text_width = text_widget.winfo_reqwidth()
        text_height = text_widget.winfo_reqheight()

        # Posiziona la scrollbar accanto al Text widget
        scrollbar_width = 20  # Larghezza standard scrollbar
        scrollbar.place(x=self.current_x + text_width, y=self.current_y, height=text_height)

        # Larghezza totale comprende Text + scrollbar
        total_width = text_width + scrollbar_width
        max_width = max(max_width, total_width)

        multiline_elements = []
        element_positions = []

        # Se abbiamo un titolo, registralo
        if title_element:
            multiline_elements.append(title_element)
            element_positions.append((start_x, start_y))

        # Registra il Text widget e la scrollbar
        multiline_elements.append(text_widget)
        multiline_elements.append(scrollbar)
        element_positions.append((self.current_x, self.current_y))
        element_positions.append((self.current_x + text_width, self.current_y))

        # Determina la chiave effettiva
        if k:
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        # Calcola l'altezza totale (titolo + text widget + spacing)
        total_height = title_height + text_height
        if title_height > 0:
            total_height += 2  # Spazio tra titolo e text widget

        # Registra la posizione dell'elemento (usa posizione iniziale e dimensioni totali)
        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        # Inizializza il dizionario per i multiline se non esiste
        if not hasattr(self, '_multiline_groups'):
            self._multiline_groups = {}

        # Salva il riferimento al widget Text (non alla scrollbar) per recuperare i valori
        self._multiline_groups[effective_key] = text_widget

        # Per la gestione della visibilità, salviamo tutti gli elementi
        if not hasattr(self, '_multiline_element_positions'):
            self._multiline_element_positions = {}

        self._multiline_element_positions[effective_key] = list(zip(multiline_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in multiline_elements:
            self._register_element(element, '', s)  # Chiave vuota per evitare conflitti, usa s per selezione

        # IMPORTANTE: Aggiorna il tracciamento dell'altezza della riga
        self._update_row_height(total_height)

        # Posizionamento per elemento successivo (stessa logica di checkbox/radio)
        self.current_x = start_x + max_width + 10
        self.current_y = start_y  # Torna alla Y iniziale

        return self

    def combobox(self, title_or_options, options=None, k='', s='', default=None, nr_rows=5):
        """Crea una combobox usando Tkinter ttk.Combobox

        Args:
            title_or_options: Se options è None, è la lista delle opzioni; altrimenti è il titolo
            options: Lista delle opzioni (se title_or_options è il titolo)
            k: Chiave per identificare la combobox
            s: Stringa di selezione per operazioni di visibilità
            default: Valore di default da selezionare inizialmente
            nr_rows: Numero di righe visibili nel dropdown (default 5)
        """
        # Importa ttk se non è già disponibile
        try:
            import tkinter.ttk as ttk
        except ImportError:
            # Fallback per versioni molto vecchie
            from tkinter import ttk

        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no
        if options is None:
            title = None
            combobox_options = title_or_options
        else:
            title = title_or_options
            combobox_options = options

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2  # Piccolo spazio tra titolo e combobox

        # Parsing delle opzioni
        parsed_options = []
        display_values = []  # Solo i testi da mostrare nella combobox

        for option in combobox_options:
            if isinstance(option, str) and '|' in option:
                display_text, value = option.split('|', 1)
            else:
                display_text = value = str(option)
            parsed_options.append((display_text, value))
            display_values.append(display_text)

        # Inizializza i gruppi di combobox se non esistono
        if not hasattr(self, '_combobox_groups'):
            self._combobox_groups = {}

        # Crea la combobox
        combobox_widget = ttk.Combobox(self.root,
                                       values=display_values,
                                       height=nr_rows,
                                       state='readonly')  # Impedisce inserimento manuale

        # Imposta il valore di default se specificato
        if default is not None:
            # Cerca il valore di default nelle opzioni parsed
            default_found = False
            for i, (display_text, value) in enumerate(parsed_options):
                if value == default:
                    combobox_widget.current(i)  # Seleziona per indice
                    default_found = True
                    break

            if not default_found:
                # Se il default non è trovato, prova a cercare per display_text
                for i, (display_text, value) in enumerate(parsed_options):
                    if display_text == default:
                        combobox_widget.current(i)
                        break

        # Posiziona la combobox
        combobox_widget.place(x=self.current_x, y=self.current_y)
        combobox_widget.update_idletasks()

        combobox_width = combobox_widget.winfo_reqwidth()
        combobox_height = combobox_widget.winfo_reqheight()

        max_width = max(max_width, combobox_width)

        combobox_elements = []
        element_positions = []

        # Se abbiamo un titolo, registralo
        if title_element:
            combobox_elements.append(title_element)
            element_positions.append((start_x, start_y))

        # Registra la combobox
        combobox_elements.append(combobox_widget)
        element_positions.append((self.current_x, self.current_y))

        # Determina la chiave effettiva
        if k:
            self._combobox_groups[k] = (combobox_widget, parsed_options)
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1
            self._combobox_groups[effective_key] = (combobox_widget, parsed_options)

        total_height = title_height + combobox_height
        if title_height > 0:
            total_height += 2

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)

        # Gestione per la visibilità
        if not hasattr(self, '_combobox_element_positions'):
            self._combobox_element_positions = {}

        # Salva le posizioni di tutti gli elementi del gruppo
        self._combobox_element_positions[effective_key] = list(zip(combobox_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in combobox_elements:
            self._register_element(element, '', s)

        # Aggiorna tracciamento altezza riga
        self._update_row_height(total_height)

        # Posizionamento per elemento successivo
        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    # Aggiungi questo metodo alla classe NgElements in ng_elements.py
    # Inseriscilo dopo il metodo combobox() e prima di _get_values()
    # IMPORTANTE: Aggiungi anche l'import di ttk all'inizio del file se non c'è già

    # Aggiungi questo metodo alla classe NgElements in ng_elements.py
    # Inseriscilo dopo il metodo combobox() e prima di _get_values()
    # IMPORTANTE: Aggiungi anche l'import di ttk all'inizio del file se non c'è già

    # Modifica al metodo table() in ng_elements.py
    # Aggiungi il parametro rowcolors e la logica di colorazione

    # Modifica al metodo table() in ng_elements.py
    # Aggiungi il parametro rowcolors e la logica di colorazione

    def table(self, title_or_conf, conf=None, data=None, nr_rows=5, k='', s='', rowcolors=None):
        """Crea una tabella usando Tkinter ttk.Treeview con titolo opzionale

        Args:
            title_or_conf: Se conf è None, è la configurazione delle colonne; altrimenti è il titolo
            conf (dict): Configurazione colonne nel formato {'COL_KEY': ['Display Name', width], ...}
                        Esempio: {'NOME':['Nome',10], 'COGNOME':['Cognome',20], 'ANNI':['Anni',5]}
            data (list): Dati da mostrare come lista di liste. L'ordine deve corrispondere alle chiavi in conf
            nr_rows (int): Numero di righe visibili (default 5)
            k (str): Chiave per identificare la tabella
            s (str): Stringa di selezione per operazioni di visibilità
            rowcolors (list): Lista per colorare le righe con due formati supportati:
                             - [indice_riga, colore_sfondo]: solo colore di sfondo
                             - [indice_riga, colore_sfondo, colore_carattere]: sfondo e testo
                             Esempio: [[0, 'yellow'], [2, 'lightblue', 'red']]
        """
        # Importa ttk se non è già disponibile
        try:
            import tkinter.ttk as ttk
        except ImportError:
            from tkinter import ttk

        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Determina se abbiamo un titolo o no (stessa logica di checkbox/radio/listbox)
        if conf is None:
            title = None
            table_conf = title_or_conf if title_or_conf else {'COL1': ['Colonna 1', 15]}
        else:
            title = title_or_conf
            table_conf = conf if conf else {'COL1': ['Colonna 1', 15]}

        # Dati di default se non specificati
        if data is None:
            data = []

        # Posizione iniziale per il gruppo
        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        # Se c'è un titolo, crealo prima
        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2  # Piccolo spazio tra titolo e tabella

        # Estrai le informazioni dalle colonne
        column_keys = list(table_conf.keys())
        column_names = [table_conf[key][0] for key in column_keys]
        column_widths = [table_conf[key][1] * 10 for key in column_keys]  # Moltiplica per avere pixel circa

        # Crea il Treeview con le colonne
        table_widget = ttk.Treeview(self.root,
                                    columns=column_keys,
                                    show='headings',
                                    height=nr_rows)

        # Configura le colonne
        for i, col_key in enumerate(column_keys):
            table_widget.heading(col_key, text=column_names[i])
            table_widget.column(col_key, width=column_widths[i], minwidth=50)

        # NUOVA SEZIONE: Gestione dei colori delle righe
        # Crea un dizionario per mappare indice -> (colore_sfondo, colore_testo) per accesso veloce
        row_color_map = {}
        if rowcolors:
            for row_color_info in rowcolors:
                if len(row_color_info) == 2:
                    # Formato: [indice, colore_sfondo]
                    row_index, bg_color = row_color_info
                    row_color_map[row_index] = (bg_color, None)
                elif len(row_color_info) >= 3:
                    # Formato: [indice, colore_sfondo, colore_carattere]
                    row_index, bg_color, fg_color = row_color_info[:3]
                    row_color_map[row_index] = (bg_color, fg_color)

        # Configura i tag per le combinazioni di colori (crea un tag per ogni combinazione unica)
        unique_color_combinations = set()
        if rowcolors:
            for row_index, color_info in row_color_map.items():
                unique_color_combinations.add(color_info)

        # Configura i tag per ogni combinazione di colori
        for bg_color, fg_color in unique_color_combinations:
            if fg_color is None:
                # Solo colore di sfondo
                tag_name = f"bg_{bg_color}"
                table_widget.tag_configure(tag_name, background=bg_color)
            else:
                # Sia sfondo che testo
                tag_name = f"bg_{bg_color}_fg_{fg_color}"
                table_widget.tag_configure(tag_name, background=bg_color, foreground=fg_color)

        # Inserisci i dati con applicazione dei colori
        inserted_items = []  # Lista per tenere traccia degli item inseriti
        for row_index, row_data in enumerate(data):
            # Assicurati che la riga abbia il numero giusto di colonne
            if len(row_data) >= len(column_keys):
                values_to_insert = row_data[:len(column_keys)]
            else:
                # Riempi con stringhe vuote se la riga è più corta
                padded_row = list(row_data) + [''] * (len(column_keys) - len(row_data))
                values_to_insert = padded_row

            # Determina il tag da applicare (se c'è un colore per questa riga)
            tags = ()
            if row_index in row_color_map:
                bg_color, fg_color = row_color_map[row_index]
                if fg_color is None:
                    # Solo colore di sfondo
                    tag_name = f"bg_{bg_color}"
                else:
                    # Sia sfondo che testo
                    tag_name = f"bg_{bg_color}_fg_{fg_color}"
                tags = (tag_name,)

            # Inserisci la riga con il tag appropriato
            item_id = table_widget.insert('', 'end', values=values_to_insert, tags=tags)
            inserted_items.append(item_id)

        # Crea le scrollbar
        v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=table_widget.yview)
        h_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=table_widget.xview)

        table_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Posiziona la tabella
        table_widget.place(x=self.current_x, y=self.current_y)
        table_widget.update_idletasks()

        table_width = table_widget.winfo_reqwidth()
        table_height = table_widget.winfo_reqheight()

        # Posiziona le scrollbar
        scrollbar_width = 20
        v_scrollbar.place(x=self.current_x + table_width, y=self.current_y, height=table_height)
        h_scrollbar.place(x=self.current_x, y=self.current_y + table_height, width=table_width)

        # Calcola dimensioni totali (tabella + scrollbar)
        total_width = table_width + scrollbar_width
        total_height = table_height + scrollbar_width

        # Aggiorna max_width considerando la tabella
        max_width = max(max_width, total_width)

        # Lista degli elementi del gruppo tabella
        table_elements = []
        element_positions = []

        # Se abbiamo un titolo, registralo
        if title_element:
            table_elements.append(title_element)
            element_positions.append((start_x, start_y))

        # Aggiungi gli elementi della tabella
        table_elements.extend([table_widget, v_scrollbar, h_scrollbar])
        element_positions.extend([
            (self.current_x, self.current_y),
            (self.current_x + table_width, self.current_y),
            (self.current_x, self.current_y + table_height)
        ])

        # Determina la chiave effettiva
        if k:
            effective_key = k
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        # Registra la posizione dell'elemento (usa posizione iniziale e dimensioni totali)
        final_total_height = title_height + total_height
        if title_height > 0:
            final_total_height += 2  # Spazio tra titolo e tabella

        self._register_element_position(effective_key, start_x, start_y, max_width, final_total_height)

        # Inizializza il dizionario per le tabelle se non esiste
        if not hasattr(self, '_table_groups'):
            self._table_groups = {}

        # Salva il riferimento al widget Treeview per recuperare i valori della selezione
        self._table_groups[effective_key] = (table_widget, column_keys)

        # Per la gestione della visibilità
        if not hasattr(self, '_table_element_positions'):
            self._table_element_positions = {}

        self._table_element_positions[effective_key] = list(zip(table_elements, element_positions))

        # Registra la stringa s per il gruppo
        if s:
            self.element_strings[effective_key] = s

        # Registra tutti gli elementi del gruppo
        for element in table_elements:
            self._register_element(element, '', s)

        # Aggiorna tracciamento altezza riga
        self._update_row_height(final_total_height)

        # Posizionamento per elemento successivo (stessa logica di checkbox/radio/listbox)
        self.current_x = start_x + max_width + 10
        self.current_y = start_y  # Torna alla Y iniziale

        return self

    def image(self, image_path='', size='', k='', s='', command=None):
        """Crea un elemento immagine usando Tkinter Label con PhotoImage

        Args:
            image_path (str): Percorso del file immagine (se vuoto, crea un placeholder)
            size (str): Dimensioni nel formato 'WIDTHxHEIGHT' (es. '200x100')
            k (str): Chiave per identificare l'elemento
            s (str): Stringa di selezione per operazioni di visibilità
            command (callable): Funzione da chiamare quando si clicca sull'immagine (opzionale)
        """
        # Applica i default
        s, _, _, k = self._merge_defaults(s, '', '', k)

        # Parsing delle dimensioni
        width, height = 100, 100  # Dimensioni di default
        if size and 'x' in size.lower():
            try:
                size_parts = size.lower().split('x')
                width = int(size_parts[0])
                height = int(size_parts[1])
            except (ValueError, IndexError):
                pass  # Usa le dimensioni di default se il parsing fallisce

        # Crea l'immagine
        photo_image = None

        if image_path and os.path.exists(image_path):
            try:
                # Carica e ridimensiona l'immagine usando PIL
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Errore caricamento immagine {image_path}: {e}")
                photo_image = None

        # Se non c'è immagine o caricamento fallito, crea un placeholder
        if photo_image is None:
            # Crea un'immagine placeholder grigia
            placeholder_image = Image.new('RGB', (width, height), color='lightgray')

            # Aggiungi una X al centro per indicare immagine mancante
            try:
                from PIL import ImageDraw
                draw = ImageDraw.Draw(placeholder_image)
                # Disegna una X
                draw.line([(0, 0), (width - 1, height - 1)], fill='gray', width=2)
                draw.line([(0, height - 1), (width - 1, 0)], fill='gray', width=2)
                # Bordo
                draw.rectangle([(0, 0), (width - 1, height - 1)], outline='gray', width=1)
            except ImportError:
                pass  # Se ImageDraw non è disponibile, usa solo il rettangolo grigio

            photo_image = ImageTk.PhotoImage(placeholder_image)

        # Callback per il click sull'immagine
        def image_callback(event):
            if k:
                # Metti l'evento nella coda
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        # Crea il Label con l'immagine
        image_label = tk.Label(self.root, image=photo_image)

        # IMPORTANTE: Mantieni un riferimento all'immagine per evitare garbage collection
        image_label.image = photo_image  # Trucco per mantenere il riferimento

        # Se c'è un comando o una chiave, rendi l'immagine cliccabile
        if command or k:
            image_label.bind("<Button-1>", image_callback)
            image_label.config(cursor="hand2")  # Cambia cursore per indicare che è cliccabile

        # Posiziona l'elemento
        image_label.place(x=self.current_x, y=self.current_y)
        image_label.update_idletasks()

        # Le dimensioni sono quelle specificate, non quelle calcolate
        actual_width = width
        actual_height = height

        # Ottieni la chiave effettiva
        effective_key = k if k else f"__auto_key_{self.element_counter}"

        # Registra la posizione dell'elemento
        self._register_element_position(effective_key, self.current_x, self.current_y, actual_width, actual_height)

        self._update_position(actual_width, actual_height)
        self._register_element(image_label, k, s)

        return self

    def _get_values(self):
        """Raccoglie tutti i valori degli elementi input, checkbox, radio button e listbox"""
        values = {}

        # Valori degli input (implementazione esistente)
        for key, element in self.element_keys.items():
            if not key.startswith('__auto_key_') and isinstance(element, tk.Entry):
                values[key] = element.get()

        # Valori dei gruppi di checkbox
        if hasattr(self, '_checkbox_groups'):
            for key, checkbox_vars in self._checkbox_groups.items():
                if not key.startswith('__auto_key_'):
                    selected_values = []
                    for var, value in checkbox_vars:
                        if var.get():  # Se il checkbox è selezionato
                            selected_values.append(value)
                    values[key] = selected_values

        # Valori dei gruppi di radio button
        if hasattr(self, '_radio_groups'):
            for key, radio_var in self._radio_groups.items():
                if not key.startswith('__auto_key_'):
                    # Per i radio button, restituisce il valore selezionato come stringa singola
                    selected_value = radio_var.get()
                    values[key] = selected_value if selected_value else ''

        # Valori delle listbox con supporto per selezione multipla
        if hasattr(self, '_listbox_groups'):
            for key, listbox_data in self._listbox_groups.items():
                if not key.startswith('__auto_key_'):
                    # Gestisce sia il formato vecchio (2 elementi) che nuovo (3 elementi)
                    if len(listbox_data) == 3:
                        listbox_widget, parsed_options, multi_select = listbox_data
                    else:
                        # Compatibilità con versione precedente
                        listbox_widget, parsed_options = listbox_data
                        multi_select = False

                    selection = listbox_widget.curselection()

                    if multi_select:
                        # Selezione multipla: restituisce una lista di valori
                        selected_values = []
                        for selected_index in selection:
                            if selected_index < len(parsed_options):
                                _, selected_value = parsed_options[selected_index]
                                selected_values.append(selected_value)
                        values[key] = selected_values
                    else:
                        # Selezione singola: restituisce una stringa
                        if selection:
                            selected_index = selection[0]
                            if selected_index < len(parsed_options):
                                _, selected_value = parsed_options[selected_index]
                                values[key] = selected_value
                            else:
                                values[key] = ''
                        else:
                            values[key] = ''

        # Valori dei widget multiline
        if hasattr(self, '_multiline_groups'):
            for key, text_widget in self._multiline_groups.items():
                if not key.startswith('__auto_key_'):
                    # Recupera tutto il testo dal widget Text (da inizio '1.0' a fine 'end-1c')
                    text_content = text_widget.get('1.0',
                                                   'end-1c')  # 'end-1c' esclude l'ultimo newline automatico
                    values[key] = text_content

        # Valori delle combobox (da aggiungere nel metodo _get_values() dopo la sezione multiline)
        if hasattr(self, '_combobox_groups'):
            for key, combobox_data in self._combobox_groups.items():
                if not key.startswith('__auto_key_'):
                    combobox_widget, parsed_options = combobox_data

                    # Ottieni l'indice della selezione corrente
                    current_selection = combobox_widget.current()

                    if current_selection >= 0 and current_selection < len(parsed_options):
                        # Restituisce il valore (non il display_text)
                        _, selected_value = parsed_options[current_selection]
                        values[key] = selected_value
                    else:
                        # Nessuna selezione valida
                        values[key] = ''

        # Valori delle tabelle (selezioni)
        if hasattr(self, '_table_groups'):
            for key, table_data in self._table_groups.items():
                if not key.startswith('__auto_key_'):
                    table_widget, column_keys = table_data

                    # Ottieni le righe selezionate
                    selection = table_widget.selection()

                    if selection:
                        # Restituisci sempre una lista di indici
                        selected_indices = []
                        for item_id in selection:
                            # Ottieni l'indice della riga nel treeview
                            index = table_widget.index(item_id)
                            selected_indices.append(index)

                        values[key] = selected_indices
                    else:
                        # Nessuna selezione - lista vuota
                        values[key] = []
        return values