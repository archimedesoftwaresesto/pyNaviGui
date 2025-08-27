import pyNaviGui as ng

window = ng.Ng()
(KEY_NOME, KEY_COGNOME, KEY_DATA_NASCITA, KEY_PESO , KEY_TELEFONO, KEY_BTN_VALUES,
KEY_BTN_SPOSTA, KEY_CONTROLLO, KEY_BTN_VISIBLE, KEY_EMAIL, *_ ) = window.set_keys()

# impostazioni genrali
(window.winTitle('Titolo della finestra').winGeometry('800x600').
 gotoxy(80,30).setRowHeigh(50).setTextSize(15,1).setInputSize(30,1))

# prima parte
(window.text('Nome',s='-a-b-').input('', k=KEY_NOME,s='-a-b-').text('Cognome',s='-a-').input('', k=KEY_COGNOME,s='-a-').
 crlf().text('Data di nascita',s='-a-b-').input('', k=KEY_DATA_NASCITA,s='-a-b-').text('Peso',s='-a-').input('', k=KEY_PESO,s='-a-')
 )

# seconda parte
(window. crlf().text('Email').input('', k=KEY_EMAIL).text('Telefono').input('', k=KEY_TELEFONO).
 crlf().button('Get values', k=KEY_BTN_VALUES).button('Check fields', k=KEY_CONTROLLO).
 crlf().button('Visible/invisible', k=KEY_BTN_VISIBLE).button('Sposta', k=KEY_BTN_SPOSTA).
 finalize_layout())

sw_flip_flop=True
while True:
    event, values = window.read()

    if event == KEY_BTN_VISIBLE:
        sw_flip_flop = not sw_flip_flop
        window.visible(sw_flip_flop, shas='-b-')

    if event == KEY_BTN_SPOSTA:
        window.move(xAdd=10, yAdd=20, shas='-a-')

    if event ==KEY_BTN_VALUES:

        print('You pressed ADD button!')
        print('Values are:')
        for key, value in values.items():
            print(f"  {key}: {value}")


    if event == KEY_CONTROLLO:

        # Controlla email

        email_value = values.get(KEY_EMAIL, '').strip()
        if window.exists(k=KEY_EMAIL+'VALIDATE'):
            window.delete(k=KEY_EMAIL+'VALIDATE')
        if not email_value or '@' not in email_value:
            window.gotoBelow(KEY_EMAIL).text('Email is not good!', fg='white', bg='red', k=KEY_EMAIL+'VALIDATE')

        # Controlla peso

        weight_value = values.get(KEY_PESO, '').strip()
        if window.exists(k=KEY_PESO+'VALIDATE'):
            window.delete(k=KEY_PESO+'VALIDATE')

        if not weight_value:
            window.gotoBelow(KEY_PESO).text('Must be a positive!', fg='white', bg='red',k=KEY_PESO+'VALIDATE')
        else:
            try:
                weight_float = float(weight_value)
                if weight_float <= 0:
                    window.gotoBelow(KEY_PESO).text('Must be a positive!', fg='white', bg='red',k=KEY_PESO+'VALIDATE')
            except ValueError:
                window.gotoBelow(KEY_PESO).text('Must be valid!', fg='white', bg='red',k=KEY_PESO+'VALIDATE' )

    if event == None:  # Finestra chiusa
        print('Window closed')
        break


window.close()