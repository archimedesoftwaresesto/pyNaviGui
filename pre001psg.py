import FreeSimpleGUI as sg

# =============================================================================
# IMPOSTAZIONI GENERALI
# =============================================================================

# Imposta il tema
sg.theme('DefaultNoMoreNagging')

# Definisci le chiavi
KEY_NOME = 'nome'
KEY_COGNOME = 'cognome'
KEY_DATA_NASCITA = 'data_nascita'
KEY_PESO = 'peso'
KEY_TELEFONO = 'telefono'
KEY_EMAIL = 'email'
KEY_BTN_VALUES = 'btn_values'
KEY_BTN_SPOSTA = 'btn_sposta'
KEY_BTN_VISIBLE = 'btn_visible'
KEY_CONTROLLO = 'btn_controllo'

# Configurazioni layout
TEXT_SIZE = (15, 1)
INPUT_SIZE = (30, 1)  # Corrispondente al setInputSize(30,1) di pyNaviGui

# =============================================================================
# PRIMA PARTE - Campi principali
# =============================================================================

layout_prima_parte = [
    # Nome e Cognome
    [sg.Text('Nome', size=TEXT_SIZE, key='txt_nome'),
     sg.Input('', key=KEY_NOME, size=INPUT_SIZE),
     sg.Text('Cognome', size=TEXT_SIZE, key='txt_cognome'),
     sg.Input('', key=KEY_COGNOME, size=INPUT_SIZE)],

    # Data nascita e Peso
    [sg.Text('Data di nascita', size=TEXT_SIZE, key='txt_data'),
     sg.Input('', key=KEY_DATA_NASCITA, size=INPUT_SIZE),
     sg.Text('Peso', size=TEXT_SIZE, key='txt_peso'),
     sg.Input('', key=KEY_PESO, size=INPUT_SIZE)]
]

# =============================================================================
# SECONDA PARTE - Email, Telefono e bottoni
# =============================================================================

layout_seconda_parte = [
    # Email e Telefono
    [sg.Text('Email', size=TEXT_SIZE),
     sg.Input('', key=KEY_EMAIL, size=INPUT_SIZE),
     sg.Text('Telefono', size=TEXT_SIZE),
     sg.Input('', key=KEY_TELEFONO, size=INPUT_SIZE)],

    # Bottoni di controllo
    [sg.Button('Get values', key=KEY_BTN_VALUES),
     sg.Button('Check fields', key=KEY_CONTROLLO)],

    # Bottoni di azione
    [sg.Button('Visible/invisible', key=KEY_BTN_VISIBLE),
     sg.Button('Sposta', key=KEY_BTN_SPOSTA)],

    # Spazio per i messaggi di errore
    [sg.Text('', key='error_email', text_color='white', background_color='red', visible=False)],
    [sg.Text('', key='error_peso', text_color='white', background_color='red', visible=False)]
]

# =============================================================================
# LAYOUT COMPLETO
# =============================================================================

# Combina tutte le parti
layout = layout_prima_parte + layout_seconda_parte

# Crea la finestra
window = sg.Window('Titolo della finestra', layout, size=(800, 600), location=(100, 100))

# =============================================================================
# LOGICA APPLICATIVA
# =============================================================================

# Variabili per la logica
sw_flip_flop = True
elementi_gruppo_a = ['txt_nome', KEY_NOME, 'txt_cognome', KEY_COGNOME, 'txt_data', KEY_DATA_NASCITA, 'txt_peso',
                     KEY_PESO]
elementi_gruppo_b = ['txt_nome', KEY_NOME, 'txt_data', KEY_DATA_NASCITA]

# Loop principale
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == None:
        print('Window closed')
        break

    # Bottone Visible/invisible
    if event == KEY_BTN_VISIBLE:
        sw_flip_flop = not sw_flip_flop
        # Nascondi/mostra gli elementi del gruppo B (equivalente di shas='-b-')
        for elemento in elementi_gruppo_b:
            try:
                window[elemento].update(visible=sw_flip_flop)
            except KeyError:
                pass  # Ignora se l'elemento non esiste

    # Bottone Sposta
    if event == KEY_BTN_SPOSTA:
        # PySimpleGUI non supporta facilmente il movimento di elementi
        # Mostriamo un messaggio invece
        sg.popup('Funzione "Sposta" non facilmente implementabile in PySimpleGUI',
                 title='Info', keep_on_top=True)

    # Bottone Get values
    if event == KEY_BTN_VALUES:
        print('You pressed GET VALUES button!')
        print('Values are:')
        for key, value in values.items():
            if not key.startswith('btn_') and not key.startswith('error_') and not key.startswith('txt_'):
                print(f"  {key}: {value}")

    # Bottone Check fields
    if event == KEY_CONTROLLO:
        # Nascondi eventuali messaggi di errore precedenti
        window['error_email'].update(visible=False)
        window['error_peso'].update(visible=False)

        # Controlla email
        email_value = values.get(KEY_EMAIL, '').strip()
        if not email_value or '@' not in email_value:
            window['error_email'].update('Email is not good!', visible=True)

        # Controlla peso
        weight_value = values.get(KEY_PESO, '').strip()
        if not weight_value:
            window['error_peso'].update('Weight must be a positive number!', visible=True)
        else:
            try:
                weight_float = float(weight_value)
                if weight_float <= 0:
                    window['error_peso'].update('Weight must be a positive number!', visible=True)
            except ValueError:
                window['error_peso'].update('Weight must be a valid number!', visible=True)

window.close()