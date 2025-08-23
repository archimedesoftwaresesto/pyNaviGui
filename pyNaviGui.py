import tkinter as tk
from threading import Event as ThreadEvent
import queue


class Ng():
    def __init__(self, geometry=''):
        self.root = tk.Tk()
        self.elements = []
        self.element_keys = {}  # Mappa key -> elemento
        self.event_queue = queue.Queue()
        self.current_event = None
        self.window_closed = False

        # Gestione chiusura finestra
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        """Chiamata quando la finestra viene chiusa"""
        self.window_closed = True
        self.event_queue.put((None, {}))

    def show(self):
        self.root.mainloop()
        return self

    def winTitle(self, title):
        self.root.title(title)
        return self

    def winGeometry(self, geometry):
        self.root.geometry(geometry)
        return self

    def goto(self, x, y):
        self.x = x
        self.y = y
        return self

    def gotoy(self, value):
        self.x = self.x0
        self.y = value
        return self

    def setX(self, value):
        self.x0 = value
        return self

    def setY(self, value):
        self.y0 = value
        return self

    def text(self, text='', k=''):
        label = tk.Label(self.root, text=text)
        label.place(x=self.x, y=self.y)
        label.update_idletasks()
        width = label.winfo_width()

        self.x = self.x + width
        self.elements.append(label)

        if k:
            self.element_keys[k] = label

        return self

    def input(self, text='', k=''):
        entry = tk.Entry(self.root)
        if text:
            entry.insert(0, text)
        entry.place(x=self.x, y=self.y)
        entry.update_idletasks()
        width = entry.winfo_width()
        self.x = self.x + width
        self.elements.append(entry)

        if k:
            self.element_keys[k] = entry

        return self

    def button(self, text='', k='', command=None):
        def button_callback():
            if k:
                # Metti l'evento nella coda
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        button = tk.Button(self.root, text=text, command=button_callback)
        button.place(x=self.x, y=self.y)
        button.update_idletasks()
        width = button.winfo_width()

        self.x = self.x + width
        self.elements.append(button)

        if k:
            self.element_keys[k] = button

        return self

    def _get_values(self):
        """Raccoglie tutti i valori degli elementi input"""
        values = {}
        for key, element in self.element_keys.items():
            if isinstance(element, tk.Entry):
                values[key] = element.get()
        return values

    def read(self, timeout=None):
        """Legge il prossimo evento (simile a PySimpleGUI)"""
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
                # Se non ci sono eventi, restituisce None per ora
                # (in una versione più avanzata potresti implementare il timeout)
                return '', {}

        except tk.TclError:
            # Finestra è stata chiusa
            self.window_closed = True
            return None, {}

    def close(self):
        """Chiude la finestra"""
        if not self.window_closed:
            self.root.quit()
            self.root.destroy()
            self.window_closed = True