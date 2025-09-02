# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgUtils:
    """Mixin per funzioni di utilità"""

    def set_keys(self, max_nr_keys=100, key_start_with_string=''):
        """Genera una lista di chiavi"""
        return [key_start_with_string + str(i) for i in range(max_nr_keys)]

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