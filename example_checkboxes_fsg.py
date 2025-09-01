import FreeSimpleGUI as sg

sg.theme('DefaultNoMoreNagging')

KEY_NAME = 'name'
KEY_SURNAME = 'surname'
KEY_NOTE1 = 'note1'
KEY_NOTE2 = 'note2'
KEY_EMAIL = 'email'
KEY_BTN_RIASSUMI = 'btn_riassumi'
KEY_BTN_NASCONDI = 'btn_nascondi'

TEXT_SIZE = (12, 1)
INPUT_SIZE = (30, 1)
INPUT_SIZE_SHORT = (20, 1)

column1_layout = [
    [sg.Text('Preferred colours', size=(15, 1), key='txt_colors')],
    [sg.Checkbox('Red', key='color_red')],
    [sg.Checkbox('Yellow', key='color_yellow')],
    [sg.Checkbox('Brown', key='color_brown')]
]

column2_layout = [
    [sg.Text('Automobile used', size=(15, 1), key='txt_auto')],
    [sg.Checkbox('Maserati', key='auto_maser')],
    [sg.Checkbox('Ferrari', key='auto_ferrari')],
    [sg.Checkbox('Lamborghini', key='auto_lamb')],
    [sg.Checkbox('Fiat', key='auto_fiat')]
]

column3_layout = [
    [sg.Text('Email', size=(5, 1))],
    [sg.Input('', key=KEY_EMAIL, size=INPUT_SIZE)]
]

column4_layout = [
    [sg.Text('Choose', size=(12, 1))],
    [sg.Checkbox('First element', key='elem_first')],
    [sg.Checkbox('Second element', key='elem_second')]
]

layout = [
    [sg.Text('Name', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_NAME, size=INPUT_SIZE)],
    [sg.Text('Surname', size=TEXT_SIZE)],
    [sg.Input('', key=KEY_SURNAME, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],
    [sg.Text('Note', size=TEXT_SIZE), sg.Input('', key=KEY_NOTE1, size=INPUT_SIZE)],
    [sg.Text('Note altre', size=TEXT_SIZE), sg.Input('', key=KEY_NOTE2, size=INPUT_SIZE)],
    [sg.Text('', size=(1, 1))],
    [sg.Column(column1_layout, vertical_alignment='top', pad=(5, 0)),
     sg.Column(column2_layout, vertical_alignment='top', pad=(5, 0)),
     sg.Column(column3_layout, vertical_alignment='top', pad=(5, 0)),
     sg.Column(column4_layout, vertical_alignment='top', pad=(5, 0))],
    [sg.Text('', size=(1, 1))],
    [sg.Button('Riassumi valori', key=KEY_BTN_RIASSUMI)],
    [sg.Button('Nascondi/Mostra colonne', key=KEY_BTN_NASCONDI)]
]

window = sg.Window('Titolo della finestra', layout, size=(800, 600), location=(100, 100), finalize=True)

colonne_visibili = True

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event is None:
        print('Window closed')
        break
    if event == KEY_BTN_RIASSUMI:
        print('\n=== RIASSUNTO VALORI ===')
        print(f'Name: {values.get(KEY_NAME, "")}')
        print(f'Surname: {values.get(KEY_SURNAME, "")}')
        print(f'Note 1: {values.get(KEY_NOTE1, "")}')
        print(f'Note 2: {values.get(KEY_NOTE2, "")}')
        print(f'Email: {values.get(KEY_EMAIL, "")}')
        colors = []
        if values.get('color_red', False):
            colors.append('Red')
        if values.get('color_yellow', False):
            colors.append('Yellow')
        if values.get('color_brown', False):
            colors.append('Brown')
        if colors:
            print(colors)
            print(f'Preferred colours: {", ".join(colors)}')
        else:
            print('Preferred colours: Nessuna selezione')
        automobiles = []
        automobile_mapping = {
            'auto_maser': 'MASER',
            'auto_ferrari': 'FERRARI',
            'auto_lamb': 'LAMB',
            'auto_fiat': 'FIAT'
        }
        for key, value_mapped in automobile_mapping.items():
            if values.get(key, False):
                automobiles.append(value_mapped)
        if automobiles:
            print(automobiles)
            print(f'Automobile used: {", ".join(automobiles)}')
        else:
            print('Automobile used: Nessuna selezione')
        elements = []
        element_mapping = {
            'elem_first': 'FIRST',
            'elem_second': 'SECOND'
        }
        for key, value_mapped in element_mapping.items():
            if values.get(key, False):
                elements.append(value_mapped)
        if elements:
            print(elements)
            print(f'Elements used: {", ".join(elements)}')
        else:
            print('Elements used: Nessuna selezione')
        print('========================\n')
    if event == KEY_BTN_NASCONDI:
        colonne_visibili = not colonne_visibili
        for element_key in ['txt_colors', 'color_red', 'color_yellow', 'color_brown', 'txt_auto', 'auto_maser', 'auto_ferrari', 'auto_lamb', 'auto_fiat']:
            window[element_key].update(visible=colonne_visibili)

window.close()
