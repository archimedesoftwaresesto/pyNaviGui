# Copyright (c) 2025 Dario Giacomelli
# Licensed under the MIT License

import tkinter as tk
import os
try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    print("ERROR: PIL/Pillow not installed. Install with: pip install Pillow")
    Image = None
    ImageTk = None
    ImageDraw = None

class NgElementsBase50:
    """Media elements: images"""

    def image(self, image_path='', size='', k='', s='', command=None):
        """Create image element using Tkinter Label with PhotoImage"""
        s, _, _, k = self._merge_defaults(s, '', '', k)

        width, height = 100, 100
        if size and 'x' in size.lower():
            try:
                size_parts = size.lower().split('x')
                width = int(size_parts[0])
                height = int(size_parts[1])
            except (ValueError, IndexError):
                pass

        photo_image = None

        if image_path and os.path.exists(image_path):
            try:
                pil_image = Image.open(image_path)
                pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Image loading error {image_path}: {e}")
                photo_image = None

        if photo_image is None:
            placeholder_image = Image.new('RGB', (width, height), color='lightgray')

            try:
                if ImageDraw:
                    draw = ImageDraw.Draw(placeholder_image)
                    draw.line([(0, 0), (width - 1, height - 1)], fill='gray', width=2)
                    draw.line([(0, height - 1), (width - 1, 0)], fill='gray', width=2)
                    draw.rectangle([(0, 0), (width - 1, height - 1)], outline='gray', width=1)
            except ImportError:
                pass

            photo_image = ImageTk.PhotoImage(placeholder_image)

        def image_callback(event):
            if k:
                values = self._get_values()
                self.event_queue.put((k, values))
            elif command:
                command()

        image_label = tk.Label(self.root, image=photo_image)
        image_label.image = photo_image

        if command or k:
            image_label.bind("<Button-1>", image_callback)
            image_label.config(cursor="hand2")

        image_label.place(x=self.current_x, y=self.current_y)
        image_label.update_idletasks()

        actual_width = width
        actual_height = height

        effective_key = k if k else f"__auto_key_{self.element_counter}"

        self._register_element_position(effective_key, self.current_x, self.current_y, actual_width, actual_height)

        self._update_position(actual_width, actual_height)
        self._register_element(image_label, k, s)

        return self