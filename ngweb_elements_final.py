# ngweb_elements_00.py
# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

from ngweb_layout import WebElement
import random
import time

# CRITICAL: Version marker for debugging
print(">>> ngweb_elements_00.py LOADED - VERSION 2025-01-16 15:30 - WITH ANTI-CACHE FIX <<<")


class TextElement(WebElement):
    """Text label element"""

    def to_html(self):
        key_attr = f' id="{self.key}"' if self.key else ''
        style = self._build_style()
        font_style = self._build_font_style()
        all_styles = style + font_style
        return f'<span{key_attr} class="ng-text"{all_styles}>{self.content}</span>'

    def _build_style(self):
        styles = []
        if self.attributes.get('fg'):
            styles.append(f"color: {self.attributes['fg']}")
        if self.attributes.get('bg'):
            styles.append(f"background-color: {self.attributes['bg']}")
        return f' style="{"; ".join(styles)}"' if styles else ''

    def _build_font_style(self):
        font = self.attributes.get('font')
        if not font:
            return ''

        styles = []
        if isinstance(font, str):
            styles.append(f"font: {font}")
        elif isinstance(font, tuple):
            if len(font) >= 2:
                family, size = font[0], font[1]
                styles.append(f"font-family: {family}")
                styles.append(f"font-size: {size}px")
                if len(font) >= 3:
                    style_part = ' '.join(font[2:])
                    if 'bold' in style_part.lower():
                        styles.append("font-weight: bold")
                    if 'italic' in style_part.lower():
                        styles.append("font-style: italic")

        return f' style="{"; ".join(styles)}"' if styles else ''


class InputElement(WebElement):
    """Input field element"""

    def to_html(self):
        key_attr = f' id="{self.key}"' if self.key else ''
        
        # CRITICAL: Make name unique with timestamp + random to prevent browser autofill
        unique_suffix = f"_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        unique_name = f"{self.key}{unique_suffix}"
        name_attr = f' name="{unique_name}"' if self.key else ''
        
        # Store original key for form submission
        data_key_attr = f' data-original-key="{self.key}"' if self.key else ''

        # CRITICAL: ALWAYS render with empty value - ignore stored value
        value_attr = ' value=""'

        style = self._build_style()

        # HTMX attributes for events
        htmx_attrs = []
        if self.attributes.get('event_enter'):
            htmx_attrs.append('hx-trigger="keyup[key==\'Enter\']"')
            htmx_attrs.append(f'hx-post="/event/{self.attributes.get("app_name")}"')
            htmx_attrs.append('hx-include="[data-original-key]"')
            htmx_attrs.append(f'hx-vals=\'{{"event_key": "{self.key}"}}\'')
            htmx_attrs.append('hx-target="#ng-container"')
            htmx_attrs.append('hx-swap="outerHTML"')

        htmx_str = ' ' + ' '.join(htmx_attrs) if htmx_attrs else ''

        # CRITICAL: Use type="search" to prevent browser autofill (browsers don't autofill search fields)
        return f'<input type="search"{key_attr}{name_attr}{data_key_attr}{value_attr} class="ng-input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"{style}{htmx_str} />'

    def _build_style(self):
        styles = []
        if self.attributes.get('fg'):
            styles.append(f"color: {self.attributes['fg']}")
        if self.attributes.get('bg'):
            styles.append(f"background-color: {self.attributes['bg']}")

        width_chars = self.attributes.get('width_chars')
        if width_chars:
            styles.append(f"width: {width_chars}ch")

        return f' style="{"; ".join(styles)}"' if styles else ''


class ButtonElement(WebElement):
    """Button element"""

    def to_html(self):
        key_attr = f' id="{self.key}"' if self.key else ''
        style = self._build_style()

        # HTMX for button click - use data-original-key selector
        htmx_attrs = f'''hx-post="/event/{self.attributes.get('app_name')}" 
                        hx-vals='{{"event_key": "{self.key}"}}' 
                        hx-include="[data-original-key]"
                        hx-target="#ng-container"
                        hx-swap="outerHTML"'''

        return f'<button{key_attr} class="ng-button"{style} {htmx_attrs}>{self.content}</button>'

    def _build_style(self):
        styles = []
        if self.attributes.get('fg'):
            styles.append(f"color: {self.attributes['fg']}")
        if self.attributes.get('bg'):
            styles.append(f"background-color: {self.attributes['bg']}")
        return f' style="{"; ".join(styles)}"' if styles else ''


class NgWebElementsBase00:
    """Web implementation of basic elements"""

    def text(self, text='', k='', s='', fg='', bg='', font=None):
        """Create text label"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        element = TextElement('text', text=text, k=k, s=s, fg=fg, bg=bg, font=font)

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self.element_counter += 1

        self.elements.append(element)
        self.element_keys[effective_key] = element

        if s:
            self.element_strings[effective_key] = s

        return self

    def input(self, text='', k='', s='', fg='', bg='', font=None,
              set_focus=False, event_enter=False, event_tab=False, event_change=0):
        """Create input field - text parameter is IGNORED for rendering"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        width_chars = self.input_width_chars

        # CRITICAL: Never store initial text value - always start empty
        element = InputElement('input', text='', k=k, s=s, fg=fg, bg=bg,
                               event_enter=event_enter, app_name=self.app_name,
                               width_chars=width_chars)

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self.element_counter += 1

        self.elements.append(element)
        self.element_keys[effective_key] = element

        if s:
            self.element_strings[effective_key] = s

        return self

    def button(self, text='', k='', s='', fg='', bg='', command=None, font=None):
        """Create button"""
        s, fg, bg, k = self._merge_defaults(s, fg, bg, k)

        element = ButtonElement('button', text=text, k=k, s=s, fg=fg, bg=bg,
                                app_name=self.app_name)

        effective_key = k if k else f"__auto_key_{self.element_counter}"
        self.element_counter += 1

        self.elements.append(element)
        self.element_keys[effective_key] = element

        if s:
            self.element_strings[effective_key] = s

        return self
