import pyNaviGui as ng

window = ng.Ng()
(KEY_CLOSE, KEY_NAME, KEY_SURNAME, KEY_OPTIONS, KEY_CB_COLORS, KEY_CB_AUTOMOBILE,
 *_ ) = window.set_keys()

(window.winTitle('Titolo della finestra').winGeometry('800x600'))

(window.gotoxy(30,80).setRowHeigh(20).setInputSize(30,1).
 text('Name').crlf().
 input('', k=KEY_NAME).crlf().
 text('Surname').crlf().
 input('', k=KEY_SURNAME).crlf().
 text('Preferred colours').crlf().
 checkboxes( ('Male','Female','Other'), k=KEY_CB_COLORS ).crlf().
 text('Atuomobile used').crlf().
 checkboxes(('Maserati|MASER', 'Ferrari|FERRARI', 'Lamborghini|LAMB','Fiat|FIAT'),k=KEY_CB_AUTOMOBILE).crlf()
 )

window.finalize_layout()

while True:
    event, values = window.read()

    if event == None:
        print('Window closed')
        break

window.close()