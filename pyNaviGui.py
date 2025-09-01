# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import queue


class Ng:
    """Implementazione GUI basata su Tkinter - Versione unificata con funzione set()"""

    def __init__(self, geometry='800x600'):
        # Coordinata X iniziale per l'allineamento
        self.initial_x = 0

        # Altezza di riga di default (RIDOTTA per essere più compatta)
        self.row_height = 22  # Era 30, ora 22

        # CORREZIONE: Tracciamento dell'altezza effettiva della riga corrente
        self.current_row_height = 0  # Altezza dell'elemento più alto nella riga corrente
        self.current_row_start_y = 0  # Y di inizio della riga corrente
        self.current_row_max_height = 0  # NUOVO: altezza massima rilevata nella riga corrente

        # Dimensioni per i prossimi elementi text e input
        self.text_width_chars = None  # Larghezza in caratteri per i prossimi text
        self.text_height_lines = None  # Altezza in righe per i prossimi text
        self.input_width_chars = None  # Larghezza in caratteri per i prossimi input
        self.input_height_lines = None  # Altezza in righe per i prossimi input

        # NUOVE VARIABILI PER LA FUNZIONE set()
        # Parametri di default che verranno applicati automaticamente
        self.default_s = ''  # Stringa di selezione di default
        self.default_fg = ''  # Colore testo di default
        self.default_bg = ''  # Colore sfondo di default
        self.default_k_prefix = ''  # Prefisso per le chiavi di default

        # Inizializzazione attributi base
        self.title = 'pyNaviGui'
        self.geometry = geometry
        self.current_x = 0
        self.current_y = 0
        self.elements = []
        self.element_keys = {}  # Dizionario key -> element
        self.element_positions = {}  # Dizionario key -> (x, y, width, height)
        self.element_strings = {}  # Dizionario key -> stringa di selezione
        self.window_closed = False
        self.event_queue = queue.Queue()
        self.event_handlers = {}  # Dizionario per gli handler degli eventi
        self.initial_elements_count = 0  # Numero di elementi iniziali
        self.element_counter = 0  # Contatore per generare ID unici per elementi senza chiave

        # Inizializzazione Tkinter
        self.root = tk.Tk()

        # Applica le impostazioni iniziali
        self._update_title_impl()
        self._update_geometry_impl()

        # Gestione chiusura finestra
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

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

    def set_keys(self, max_nr_keys=100, key_start_with_string=''):
        return [key_start_with_string + str(i) for i in range(max_nr_keys)]

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

    def exists(self, k):
        """Controlla se un elemento con chiave k esiste (solo per chiavi definite dall'utente)"""
        return (k in self.element_keys and
                self.element_keys[k] is not None and
                not k.startswith('__auto_key_'))

    def delete(self, k):
        """Cancella un elemento con chiave k"""
        if not self.exists(k):
            return self

        element_to_remove = self.element_keys[k]

        # Rimuovi l'elemento dalla lista elements
        if element_to_remove in self.elements:
            self.elements.remove(element_to_remove)

        # Chiama l'implementazione specifica per rimuovere l'elemento dalla GUI
        self._delete_element_impl(element_to_remove)

        # Rimuovi dalle strutture dati
        del self.element_keys[k]
        if k in self.element_positions:
            del self.element_positions[k]
        if k in self.element_strings:
            del self.element_strings[k]

        return self

    def _update_position(self, width, height=20):
        """Aggiorna la posizione corrente dopo aver aggiunto un elemento"""
        # CORREZIONE: Aggiorna il tracciamento dell'altezza massima della riga
        self._update_row_height(height)

        self.current_x += width + 5  # Spazio tra elementi

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

    def register_event_handler(self, event_key, handler_func):
        """Registra un handler per un evento specifico"""
        self.event_handlers[event_key] = handler_func

    def process_event(self, event_key, values):
        """Processa un evento usando l'handler registrato"""
        if event_key in self.event_handlers:
            return self.event_handlers[event_key](values)
        return None

    def finalize_layout(self):
        """Finalizza il layout iniziale e memorizza il numero di elementi"""
        self.initial_elements_count = len(self.elements)
        return self

    def clear_error_messages(self):
        """Rimuove tutti gli elementi aggiunti dinamicamente (messaggi di errore)"""
        if self.initial_elements_count > 0:
            # Ottieni gli elementi da rimuovere (quelli aggiunti dinamicamente)
            elements_to_remove = self.elements[self.initial_elements_count:]

            # Rimuovi gli elementi dalla GUI usando l'implementazione specifica
            for element in elements_to_remove:
                self._delete_element_impl(element)

            # Mantieni solo gli elementi iniziali
            self.elements = self.elements[:self.initial_elements_count]

            # Rimuovi le chiavi e posizioni degli elementi dinamici
            keys_to_remove = []
            for key in list(self.element_keys.keys()):
                # Se l'elemento non è tra quelli iniziali, rimuovilo
                element = self.element_keys[key]
                if element not in self.elements:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                if key in self.element_keys:
                    del self.element_keys[key]
                if key in self.element_positions:
                    del self.element_positions[key]
                if key in self.element_strings:
                    del self.element_strings[key]
        return self

    def _get_matching_keys(self, k='', kstart='', shas=''):
        """Restituisce le chiavi degli elementi che soddisfano i criteri di selezione

        Args:
            k (str): Chiave specifica dell'elemento
            kstart (str): Prefisso per selezionare elementi le cui chiavi iniziano con questo valore
            shas (str): Seleziona elementi la cui stringa s CONTIENE questo valore
        """
        matching_keys = []

        if k:
            # Comportamento originale: singolo elemento
            if self.exists(k):
                matching_keys.append(k)

        elif kstart:
            # Seleziona per prefisso chiave (esclude chiavi auto-generate)
            matching_keys = [key for key in self.element_keys.keys()
                             if not key.startswith('__auto_key_') and key.startswith(kstart)]

        elif shas:
            # Seleziona per stringa s che CONTIENE - include tutti gli elementi
            matching_keys = [key for key, s_val in self.element_strings.items()
                             if shas in s_val]

        return matching_keys

    def visible(self, is_visible, shas='', k='', kstart=''):
        """Imposta la visibilità di un elemento o gruppo di elementi

        Args:
            is_visible (bool): True per rendere visibile, False per nascondere
            shas (str): [PREFERITO] Seleziona elementi la cui stringa s contiene questo valore
            k (str): Chiave specifica dell'elemento (per compatibilità)
            kstart (str): Prefisso per selezionare tutti gli elementi le cui chiavi iniziano con questo valore
        """
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        for key in matching_keys:
            if key in self.element_keys:  # Verifica che la chiave esista (include anche quelle auto-generate)
                element = self.element_keys[key]
                self._set_visible_impl(element, is_visible)

        return self

    def _set_visible_impl(self, element, is_visible):
        """Implementazione migliorata per impostare la visibilità in Tkinter"""
        if hasattr(element, 'place'):
            if is_visible:
                # Prima cerca nelle posizioni degli elementi normali
                element_found = False
                for key, el in self.element_keys.items():
                    if el == element and key in self.element_positions:
                        x, y, width, height = self.element_positions[key]
                        element.place(x=x, y=y)
                        element_found = True
                        break

                # Se non trovato, cerca nei gruppi di checkbox
                if not element_found and hasattr(self, '_checkbox_element_positions'):
                    for group_key, elements_positions in self._checkbox_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break
            else:
                # Nasconde l'elemento
                element.place_forget()

    def move(self, xAdd=0, yAdd=0, shas='', k='', kstart=''):
        """Sposta un elemento o gruppo di elementi

        Args:
            xAdd (int): Pixel da aggiungere alla coordinata X
            yAdd (int): Pixel da aggiungere alla coordinata Y
            shas (str): [PREFERITO] Seleziona elementi la cui stringa s contiene questo valore
            k (str): Chiave specifica dell'elemento (per compatibilità)
            kstart (str): Prefisso per selezionare tutti gli elementi le cui chiavi iniziano con questo valore
        """
        matching_keys = self._get_matching_keys(k=k, kstart=kstart, shas=shas)

        for key in matching_keys:
            if key in self.element_keys:  # Verifica che la chiave esista (include anche quelle auto-generate)
                element = self.element_keys[key]
                # Aggiorna la posizione salvata
                if key in self.element_positions:
                    x, y, width, height = self.element_positions[key]
                    new_x = x + xAdd
                    new_y = y + yAdd
                    self.element_positions[key] = (new_x, new_y, width, height)
                    self._move_element_impl(element, new_x, new_y)

        return self

    def _move_element_impl(self, element, new_x, new_y):
        """Implementazione specifica per spostare un elemento in Tkinter"""
        if hasattr(element, 'place'):
            element.place(x=new_x, y=new_y)

    def show(self):
        """Avvia il loop principale di Tkinter"""
        self.root.mainloop()
        return self

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


    def _get_values(self):
        """Raccoglie tutti i valori degli elementi input e checkbox"""
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

        return values

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
        """Chiude la finestra"""
        self.window_closed = True
        self._close_impl()

    def setRowHeigh(self, height):
        """Imposta l'altezza della riga corrente (virtuale)"""
        self.row_height = height
        return self