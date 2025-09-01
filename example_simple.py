import pyNaviGui as ng

window = ng.Ng()
(KEY_CLOSE, KEY_NAME, KEY_SURNAME, KEY_OPTIONS,
 *_ ) = window.set_keys()

# general settings of the window and other use, ful variables
(window.winTitle('Titolo della finestra').winGeometry('800x600'))

# first column
ref_y = 30
ref_x =

(window.gotoxy(30,80).setRowHeigh(20).setInputSize(30,1).
 text('Name').crlf().
 input('', k=KEY_NAME).crlf().
 text('Surname').crlf().
 input('', k=KEY_SURNAME).crlf().
 text('Preferred colours').crlf().
 checkboxes( ('Male','Female','Other') ).crlf().
 text('Atuomobile used').crlf().
 checkboxes(('Maserati', 'Ferrari', 'Lamborghini','Fiat')).crlf()

 )


window.finalize_layout()

while True:
    event, values = window.read()



    if event == None:
        print('Window closed')
        break

window.close()