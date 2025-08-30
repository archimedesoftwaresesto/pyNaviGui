import FreeSimpleGUI as sg

# =============================================================================
# IMPOSTAZIONI GENERALI
# =============================================================================

# Imposta il tema
sg.theme('DefaultNoMoreNagging')

# Definisci le chiavi (equivalente a set_keys() di pyNaviGui)
KEY_NAME = 'name'
KEY_SURNAME = 'surname'
KEY_BORN = 'born'
KEY_WEIGHT = 'weight'
KEY_AGE = 'age'
KEY_EMAIL = 'email'
KEY_BTN_ADD = 'btn_add'
KEY_FIELD1 = 'field1'
KEY_FIELD2 = 'field2'
KEY_FIELD3 = 'field3'

# Configurazioni layout (equivalente a setTextSize e setInputSize)
TEXT_SIZE = (12, 1)
INPUT_SIZE = (30, 1)

# =============================================================================
# LAYOUT INIZIALE
# =============================================================================

# Prima colonna (equivalente a gotoxy(80,30))
column1_layout = [
    [sg.Text('Name', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_NAME, size=INPUT_SIZE)],
    [sg.Text('Surname', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_SURNAME, size=INPUT_SIZE)],
    [sg.Text('Date of born', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_BORN, size=INPUT_SIZE)]
]

# Seconda colonna (equivalente a gotoxy(300,30))
column2_layout = [
    [sg.Text('Weight', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_WEIGHT, size=INPUT_SIZE)],
    [sg.Text('Age', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_AGE, size=INPUT_SIZE)],
    [sg.Text('Email', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_EMAIL, size=INPUT_SIZE)]
]

# Layout principale con le due colonne
main_layout = [
    # Due colonne affiancate
    [sg.Column(column1_layout, vertical_alignment='top', pad=(80, 30)),
     sg.Column(column2_layout, vertical_alignment='top', pad=(50, 30))],

    # Bottone in basso (equivalente a gotoxy(80,230))
    [sg.Text('', size=(1, 2))],  # Spazio verticale
    [sg.Button('Add elements', key=KEY_BTN_ADD, pad=((80, 0), (0, 0)))]
]

# =============================================================================
# FINESTRA E LOOP PRINCIPALE
# =============================================================================

# Crea la finestra (equivalente a winTitle e winGeometry)
window = sg.Window('Titolo della finestra', main_layout, size=(800, 600), location=(100, 100), finalize=True)

# Variabili per gestire gli elementi dinamici
dynamic_elements_added = False
dynamic_window = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event is None:
        print('Window closed')
        break

    if event == KEY_BTN_ADD:
        print('Adding dynamic elements...')

        # Se gli elementi dinamici sono già stati aggiunti, chiudi la finestra precedente
        if dynamic_window is not None:
            dynamic_window.close()

        # Crea un nuovo layout che include gli elementi originali + quelli dinamici
        # Prima colonna rimane uguale
        new_column1_layout = column1_layout.copy()

        # Seconda colonna con elementi aggiuntivi (equivalente a gotoBelow(KEY_EMAIL))
        new_column2_layout = column2_layout.copy() + [
            [sg.Text('', size=(1, 1))],  # Spazio
            [sg.Text('Field 1', size=TEXT_SIZE)],
            [sg.Input('', key=KEY_FIELD1, size=INPUT_SIZE)],
            [sg.Text('Filed 2', size=TEXT_SIZE)],  # Mantiene il typo dell'originale
            [sg.Input('', key=KEY_FIELD2, size=INPUT_SIZE)],
            [sg.Text('Field 3', size=TEXT_SIZE)],
            [sg.Input('', key=KEY_FIELD3, size=INPUT_SIZE)]
        ]

        # Nuovo layout completo
        new_main_layout = [
            [sg.Column(new_column1_layout, vertical_alignment='top', pad=(80, 30)),
             sg.Column(new_column2_layout, vertical_alignment='top', pad=(50, 30))],
            [sg.Text('', size=(1, 2))],
            [sg.Button('Add elements', key=KEY_BTN_ADD, pad=((80, 0), (0, 0)))]
        ]

        # Salva i valori correnti prima di chiudere la finestra
        current_values = values.copy()

        # Chiudi la finestra corrente
        window.close()

        # Crea una nuova finestra con il layout aggiornato
        dynamic_window = sg.Window('Titolo della finestra', new_main_layout,
                                   size=(800, 600), location=(100, 100), finalize=True)

        # Ripristina i valori nei campi (equivalente alla persistenza dei dati)
        for key, value in current_values.items():
            if key in dynamic_window.key_dict and value:
                try:
                    dynamic_window[key].update(value)
                except:
                    pass  # Ignora errori se l'elemento non può essere aggiornato

        # Aggiorna il riferimento alla finestra corrente
        window = dynamic_window
        dynamic_elements_added = True

        print('Dynamic elements added successfully!')

# Chiudi tutte le finestre alla fine
if dynamic_window is not None and dynamic_window != window:
    dynamic_window.close()
window.close()