import pyNaviGui as ng

window = ng.Ng()

(KEY_CLOSE, KEY_NAME, KEY_SURNAME, KEY_OPTIONS, KEY_CB_COLORS, KEY_NOTE1, KEY_NOTE2, KEY_CB_AUTOMOBILE, KEY_BTN_RIASSUMI,KEY_CB_ELEMENTS,
KEY_EMAIL, KEY_BTN_INVISIBILITA,  *_) = window.set_keys()

(window.winTitle('Titolo della finestra').winGeometry('800x600'))

(window.gotoxy(30, 20).setTextSize(10).setInputSize(30, 1).
 text('Name',s='ana').crlf().
 input('', k=KEY_NAME).crlf().
 text('Surname').crlf().
 input('', k=KEY_SURNAME).crlf().crlf().
 text('Note ').input('', k=KEY_NOTE1).crlf().
 text('Note altre').input('', k=KEY_NOTE2).crlf().crlf().
 set(s='c1').
 checkboxes('Preferred colours', ('Red', 'Yellow', 'Brown'), k=KEY_CB_COLORS).
 checkboxes('Automobile used', ('Maserati|MASER', 'Ferrari|FERRARI', 'Lamborghini|LAMB', 'Fiat|FIAT'), k=KEY_CB_AUTOMOBILE).
 set(s='').
 text('Email').input('', k=KEY_EMAIL).
 checkboxes('Choose', ('First element|FIRST', 'Secon element|SECOND'), k=KEY_CB_ELEMENTS).crlf().
 button('Riassumi valori', k=KEY_BTN_RIASSUMI).crlf().
button('Prime due colonne invisibili', k=KEY_BTN_INVISIBILITA)
 )

window.finalize_layout()

flipflopvisible = True

while True:
    event, values = window.read()

    if event == None:
        print('Window closed')
        break
    if event == KEY_BTN_INVISIBILITA:
        flipflopvisible = not flipflopvisible
        window.visible(flipflopvisible, shas='c1')


    if event == KEY_BTN_RIASSUMI:
        print('\n=== RIASSUNTO VALORI ===')
        print(f'Name: {values.get(KEY_NAME, "")}')
        print(f'Surname: {values.get(KEY_SURNAME, "")}')

        # Per i checkbox, i valori sono liste
        colors = values.get(KEY_CB_COLORS, [])
        if colors:
            print(colors)
            print(f'Preferred colours: {", ".join(colors)}')
        else:
            print('Preferred colours: Nessuna selezione')

        automobiles = values.get(KEY_CB_AUTOMOBILE, [])
        if automobiles:
            print(automobiles)
            print(f'Automobile used: {", ".join(automobiles)}')
        else:
            print('Automobile used: Nessuna selezione')

        elements = values.get(KEY_CB_ELEMENTS, [])
        if elements:
            print(elements)
            print(f'Elements used: {", ".join(elements)}')
        else:
            print('Elements used: Nessuna selezione')


        print('========================\n')

window.close()