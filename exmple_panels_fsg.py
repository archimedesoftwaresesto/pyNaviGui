import FreeSimpleGUI as sg

# =============================================================================
# IMPOSTAZIONI GENERALI
# =============================================================================

# Imposta il tema
sg.theme('DefaultNoMoreNagging')

# Definisci le chiavi
KEY_NAME = 'name'
KEY_SURNAME = 'surname'
KEY_BORN = 'born'
KEY_WEIGHT = 'weight'
KEY_AGE = 'age'
KEY_EMAIL = 'email'
KEY_ADDRESS_1 = 'address_1'
KEY_ADDRESS_2 = 'address_2'
KEY_ADDRESS_3 = 'address_3'
KEY_NOTE_1 = 'note_1'
KEY_NOTE_2 = 'note_2'
KEY_NOTE_3 = 'note_3'

# Configurazioni layout
TEXT_SIZE = (15, 1)
INPUT_SIZE = (30, 1)

# =============================================================================
# LAYOUT DEI TAB
# =============================================================================

# Tab 1 - Informazioni personali (equivalente agli elementi con s='t1')
tab1_column1_layout = [
    [sg.Text('Name', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_NAME, size=INPUT_SIZE)],
    [sg.Text('Surname', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_SURNAME, size=INPUT_SIZE)],
    [sg.Text('Date of born', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_BORN, size=INPUT_SIZE)]
]

tab1_column2_layout = [
    [sg.Text('Weight', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_WEIGHT, size=INPUT_SIZE)],
    [sg.Text('Age', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_AGE, size=INPUT_SIZE)],
    [sg.Text('Email', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_EMAIL, size=INPUT_SIZE)]
]

# Layout completo del Tab 1 con due colonne affiancate
tab1_layout = [
    [sg.Column(tab1_column1_layout, vertical_alignment='top', pad=(20, 10)),
     sg.Column(tab1_column2_layout, vertical_alignment='top', pad=(50, 10))]
]

# Tab 2 - Indirizzi (equivalente agli elementi con s='t2')
tab2_layout = [
    [sg.Text('Address 1', size=TEXT_SIZE), sg.Input('', key=KEY_ADDRESS_1, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],  # Spazio equivalente a setRowHeigh(25)
    [sg.Text('Address 2', size=TEXT_SIZE), sg.Input('', key=KEY_ADDRESS_2, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],  # Spazio equivalente a setRowHeigh(25)
    [sg.Text('Address 3', size=TEXT_SIZE), sg.Input('', key=KEY_ADDRESS_3, size=INPUT_SIZE)]
]

# Tab 3 - Note (equivalente agli elementi con s='t3')
tab3_layout = [
    [sg.Text('Note 1', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_NOTE_1, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],  # Spazio equivalente a setRowHeigh(25)
    [sg.Text('Note 2', size=TEXT_SIZE), sg.Input('', key=KEY_NOTE_2, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],  # Spazio equivalente a setRowHeigh(25)
    [sg.Text('Note 3', size=TEXT_SIZE), sg.Input('', key=KEY_NOTE_3, size=INPUT_SIZE)]
]

# =============================================================================
# LAYOUT PRINCIPALE CON TAB NATIVI
# =============================================================================

# Layout principale usando TabGroup nativo di PySimpleGUI
layout = [
    [sg.TabGroup([
        [sg.Tab('Tab 1', tab1_layout, key='tab1', pad=(10, 10))],
        [sg.Tab('Tab 2', tab2_layout, key='tab2', pad=(10, 10))],
        [sg.Tab('Tab 3', tab3_layout, key='tab3', pad=(10, 10))]
    ],
        key='tabgroup',
        enable_events=True,
        tab_location='top',
        selected_title_color='white',
        selected_background_color='blue',
        title_color='black',
        background_color='lightgray',
        border_width=1,
        pad=(10, 10))]
]

# =============================================================================
# FINESTRA E LOOP PRINCIPALE
# =============================================================================

# Crea la finestra
window = sg.Window('Titolo della finestra', layout,
                   size=(800, 600),
                   location=(100, 100),
                   finalize=True,
                   resizable=True)

print("Applicazione avviata - usa i tab per navigare tra i pannelli")

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event is None:
        print('Window closed')
        break

    # Rileva quando viene cambiato tab
    if event == 'tabgroup':
        selected_tab = window['tabgroup'].get()
        print(f'Cambiato al: {selected_tab}')

        # Mostra i valori correnti quando si cambia tab (per debug)
        current_values = []
        for key, value in values.items():
            if value and not key.startswith('tab') and key != 'tabgroup':
                current_values.append(f"{key}: {value}")

        if current_values:
            print("Valori correnti:")
            for val in current_values:
                print(f"  {val}")
        else:
            print("Nessun valore inserito")

    # Debug per tutti gli altri eventi (opzionale)
    elif event:
        print(f"Evento: {event}")

window.close()
