import pyNaviGui as ng

window = ng.Ng()
(KEY_CLOSE, KEY_NAME, KEY_SURNAME, KEY_BORN, KEY_WEIGHT, KEY_AGE, KEY_EMAIL, KEY_BTN_ADD,
KEY_FIELD1, KEY_FIELD2, KEY_FIELD3,
 *_ ) = window.set_keys()

# general settings of the window and other use, ful variables
(window.winTitle('Titolo della finestra').winGeometry('800x600'))

# first column
ref_y = 30
ref_x = 80

(window.gotoxy(ref_x,ref_y).setRowHeigh(20).setInputSize(30,1).
 text('Name').crlf().
 input('', k=KEY_NAME).crlf().
 text('Surname').crlf().
 input('', k=KEY_SURNAME).crlf().
 text('Date of born').crlf().
 input('', k=KEY_BORN)
 )

# second column
(window.gotoxy(ref_x + 220 ,ref_y).setRowHeigh(20).setInputSize(30,1).
 text('Weight').crlf().
 input('', k=KEY_WEIGHT).crlf().
 text('Age').crlf().
 input('', k=KEY_AGE).crlf().
 text('Email').crlf().
 input('', k=KEY_EMAIL)
 )

# last line with commands
(window.gotoxy(80,230).setRowHeigh(30).setInputSize(30,1).
 button('Add elements',k=KEY_BTN_ADD)
 )

window.finalize_layout()

while True:
    event, values = window.read()

    if event == KEY_BTN_ADD:

        # deleting the elements
        window.delete(k=KEY_FIELD1).delete(k=KEY_FIELD2).delete(k=KEY_FIELD3)

        # adding the elements
        (window.gotoBelow(k=KEY_EMAIL).setRowHeigh(20).setInputSize(30, 1).
         text('Field 1').crlf().
         input('', k=KEY_FIELD1).crlf().
         text('Filed 2').crlf().
         input('', k=KEY_FIELD2).crlf().
         text('Field 3').crlf().
         input('', k=KEY_FIELD3)
         )

    if event == None:
        print('Window closed')
        break

window.close()