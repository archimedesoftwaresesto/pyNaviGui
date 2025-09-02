# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

"""
pyNaviGui - Una libreria GUI semplice e intuitiva basata su Tkinter

Esempi di uso:
    import pyNaviGui as ng
    
    window = ng.Ng()
    window.text('Hello').input('', k='name').button('OK', k='ok')
    
    while True:
        event, values = window.read()
        if event == 'ok':
            print(f"Name: {values['name']}")
        if event == None:
            break
            
    window.close()
"""

from pyNaviGui import Ng

__version__ = "1.0.0"
__author__ = "Dario Giacomelli"
__license__ = "MIT"

# Esponi solo la classe principale
__all__ = ['Ng']