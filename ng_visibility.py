# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

class NgVisibility:
    """Mixin per la gestione della visibilità e movimento degli elementi"""

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

                # Se non trovato, cerca nei gruppi di radiobutton
                if not element_found and hasattr(self, '_radio_element_positions'):
                    for group_key, elements_positions in self._radio_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break

                # Se non trovato, cerca nei gruppi di listbox
                if not element_found and hasattr(self, '_listbox_element_positions'):
                    for group_key, elements_positions in self._listbox_element_positions.items():
                        for el, pos in elements_positions:
                            if el == element:
                                x, y = pos
                                element.place(x=x, y=y)
                                element_found = True
                                break
                        if element_found:
                            break
                # Se non trovato, cerca nei gruppi di multiline
                if not element_found and hasattr(self, '_multiline_element_positions'):
                    for group_key, elements_positions in self._multiline_element_positions.items():
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