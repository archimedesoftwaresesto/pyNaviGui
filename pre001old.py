from psglicenza import *

test = 2

if test == 2:
    import pyNaviGui as ng
    window = ng.Ng()
    (window.winTitle('Titolo della finestra').winGeometry('800x600').setX(20).
     gotoy(20).text('Nome').input('', k='-NOME-').text('Cognome').input('', k='-COGNOME-').
     gotoy(50).text('Data di nascita').input('', k='-DATA_NASCITA-').text('Peso').input('', k='-PESO-').
     gotoy(80).text('Email').input('', k='-EMAIL-').text('Telefono').input('', k='-TELEFONO-').
     gotoy(110).button('Add', k='-ADD-')
     )
    while True:
        event, values = window.read()
        if event == '-ADD-':
            print('You pressed ADD button!')
            print('Values are:')
            for key, value in values.items():
                print(f"  {key}: {value}")
        if event == None:  # Finestra chiusa
            print('Window closed')
            break
    window.close()

if test == 2.1:
    # Demo che mostra come passare da Tkinter a Web semplicemente cambiando import

    # Per usare Tkinter (versione originale):
    # import pyNaviGUI as ng

    # Per usare la versione Web:
    import pyNaviGuiWeb as ng


    def main():
        # Il codice rimane identico!
        window = ng.Ng()
        (window.winTitle('Titolo della finestra').winGeometry('800x600').setX(20).
         gotoy(20).text('Nome').input('', k='-NOME-').text('Cognome').input('', k='-COGNOME-').
         gotoy(50).text('Data di nascita').input('', k='-DATA_NASCITA-').text('Peso').input('', k='-PESO-').
         gotoy(80).text('Email').input('', k='-EMAIL-').text('Telefono').input('', k='-TELEFONO-').
         gotoy(110).button('Add', k='-ADD-')
         )

        # Avvia il server e apre il browser
        window.show()

        # Loop degli eventi identico alla versione Tkinter
        while True:
            event, values = window.read()
            if event == '-ADD-':
                print('You pressed ADD button!')
                print('Values are:')
                for key, value in values.items():
                    print(f"  {key}: {value}")
            if event == None:  # Finestra chiusa
                print('Window closed')
                break

        window.close()


    main()

if test == 3:
    import PySimpleGUI as sg
    layout = [
        [sg.Text('Nome'), sg.Input(key='-NOME-'), sg.Text('Cognome'), sg.Input(key='-COGNOME-')],
        [sg.Text('Data di nascita'), sg.Input(key='-DATA_NASCITA-'),  sg.Text('Peso'), sg.Input(key='-PESO-')],
        [sg.Text('Email'), sg.Input(key='-EMAIL-'), sg.Text('Telefono'), sg.Input(key='-TELEFONO-')],
        [sg.Button('add',k='-ADD-')]
    ]
    window = sg.Window('Titolo della finestra', layout, size=(800, 600))
    while True:
        event, values = window.read()
        if event == '-ADD-':
            print('You pressed ADD button!')
            print('Values are:')
            for key, value in values.items():
                print(f"  {key}: {value}")
        if event == None:
            print('Window closed')
            break
    window.close()

