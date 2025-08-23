from psglicenza import *

test = 2

if test == 2:
    import pyNaviGui as ng

if test == 3:
    import pyNaviGuiWeb as  ng

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
