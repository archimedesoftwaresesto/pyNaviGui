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


class NgNavElements:
    """Mixin for complex navigable GUI elements"""

    def navtable(self, title_or_conf, conf=None, data=None, nr_rows=5, k='', s='', folder_images='', size_img='50x50',
                 vgap=0, vnavgap=10, alternate_rowcolor=''):
        """Create navigable table with images and automatic pagination"""
        # Set default vertical gap if not provided
        if vgap is None:
            vgap = 0
        if vnavgap is None:
            vnavgap = 10
        s, _, _, k = self._merge_defaults(s, '', '', k)

        if conf is None:
            title = None
            table_conf = title_or_conf if title_or_conf else {'COL1': ['Column 1', 15]}
        else:
            title = title_or_conf
            table_conf = conf if conf else {'COL1': ['Column 1', 15]}

        if data is None:
            data = []

        start_x = self.current_x
        start_y = self.current_y
        max_width = 0
        title_height = 0

        title_element = None
        if title:
            title_element = tk.Label(self.root, text=title, anchor='w')
            title_element.place(x=start_x, y=start_y)
            title_element.update_idletasks()

            title_width = title_element.winfo_reqwidth()
            title_height = title_element.winfo_reqheight()
            max_width = max(max_width, title_width)
            self.current_y += title_height + 2

        # Parse image size
        img_width, img_height = 50, 50  # Default size
        if size_img:
            try:
                size_parts = size_img.lower().split('x')
                if len(size_parts) == 2:
                    img_width = int(size_parts[0])
                    img_height = int(size_parts[1])
            except (ValueError, IndexError):
                # If parsing fails, use default values
                pass

        # Calculate row height based on image height with minimal padding
        if img_height <= 20:
            row_height = max(img_height + 2, 22)  # For small images, keep rows compact
        else:
            row_height = max(img_height + 4, 25)  # For larger images, add a bit more space

        # Add vertical gap between rows if specified
        row_spacing = row_height + vgap

        if k:
            effective_key = k
            # Clean any existing navtable with same key before creating new one
            if hasattr(self, '_navtable_groups') and effective_key in self._navtable_groups:
                self._cleanup_navtable(effective_key)
        else:
            effective_key = f"__auto_key_{self.element_counter}"
            self.element_counter += 1

        # Initialize dictionaries for navigable table if they don't exist
        if not hasattr(self, '_navtable_groups'):
            self._navtable_groups = {}
        if not hasattr(self, '_navtable_element_positions'):
            self._navtable_element_positions = {}

        # Calculate pagination parameters
        rows_per_page = nr_rows
        total_pages = (len(data) + rows_per_page - 1) // rows_per_page if data else 1
        current_page = 0

        navtable_elements = []
        element_positions = []

        if title_element:
            navtable_elements.append(title_element)
            element_positions.append((start_x, start_y))

        content_start_y = self.current_y

        # Create row background frames if alternating colors are requested
        row_frames = []
        max_column_width = 0
        for col_key in table_conf:
            max_column_width += table_conf[col_key][1] * 10 + 5
        # Add width for the image column and padding
        total_width = max_column_width + img_width + 15

        # Create ALWAYS nr_rows rows to avoid display bugs
        row_elements = []

        for i in range(nr_rows):
            row_y = content_start_y + i * row_spacing
            row_elements_list = []

            # Create background frame for alternating colors if needed
            row_frame = None
            if alternate_rowcolor and i % 2 == 1:  # Apply color to even-indexed rows (0-indexed)
                row_frame = tk.Frame(self.root, background=alternate_rowcolor,
                                     width=total_width, height=row_height)
                row_frame.place(x=start_x, y=row_y)
                navtable_elements.append(row_frame)
                element_positions.append((start_x, row_y))
                row_frames.append(row_frame)
                # Make sure the frame stays below other elements
                row_frame.lower()
            else:
                row_frames.append(None)

            # Determine if this row has initial data to show
            has_initial_data = i < len(data) if data else False

            # Image for the row - ALWAYS last column contains the filename
            if has_initial_data and data[i]:
                image_filename = data[i][-1]  # Last column = image name
                image_path = os.path.join(folder_images, image_filename) if folder_images else image_filename
                if not os.path.exists(image_path):
                    image_path = ''
            else:
                image_path = ''

            # Create image element - Center image vertically in the row
            img_y = row_y + (row_height - img_height) // 2
            img_element = self._create_image_element(image_path, img_width, img_height, start_x, img_y,
                                                     f"{effective_key}_IMG_ROW_{i}", f"{effective_key}_row_{i}")
            navtable_elements.append(img_element)
            element_positions.append((start_x, img_y))
            row_elements_list.append(img_element)

            # Create text elements for columns (exclude last column which is always the image)
            current_x_text = start_x + img_width + 10  # Distance from image edge to text
            keylist = list(table_conf.keys())

            for j, col_key in enumerate(keylist):
                if has_initial_data and j < len(data[i]) - 1:  # -1 to exclude last column (image)
                    text_content = str(data[i][j])
                else:
                    text_content = ''

                text_width = table_conf[col_key][1] * 10

                # Calculate vertical center of the row for text alignment
                text_y = row_y + (row_height - 16) // 2  # 16 is approximate height of text

                text_element = tk.Label(self.root, text=text_content, width=table_conf[col_key][1], anchor='w')
                # If alternate row color is set, apply background to label
                if alternate_rowcolor and i % 2 == 1:
                    text_element.config(background=alternate_rowcolor)

                text_element.place(x=current_x_text, y=text_y)
                text_element.update_idletasks()

                navtable_elements.append(text_element)
                element_positions.append((current_x_text, text_y))
                row_elements_list.append(text_element)

                current_x_text += text_width + 5

            # If there's no initial data, hide the row immediately
            if not has_initial_data:
                for element in row_elements_list:
                    if hasattr(element, 'place_forget'):
                        element.place_forget()
                if row_frames[i]:
                    row_frames[i].place_forget()

            row_elements.append(row_elements_list)
            max_width = max(max_width, current_x_text - start_x)

        # Create navigation buttons with proper closure capture
        # Position them below the last row with specified gap
        nav_y = content_start_y + nr_rows * row_spacing + vnavgap

        def create_nav_callback(key, direction):
            """Create navigation callback with proper closure"""
            return lambda: self._navtable_navigate(key, direction)

        btn_back = tk.Button(self.root, text="  <<  ",
                             command=create_nav_callback(effective_key, -1))
        btn_back.place(x=start_x, y=nav_y)
        btn_back.update_idletasks()
        navtable_elements.append(btn_back)
        element_positions.append((start_x, nav_y))

        btn_forward_x = start_x + btn_back.winfo_reqwidth() + 5
        btn_forward = tk.Button(self.root, text="  >>  ",
                                command=create_nav_callback(effective_key, 1))
        btn_forward.place(x=btn_forward_x, y=nav_y)
        btn_forward.update_idletasks()
        navtable_elements.append(btn_forward)
        element_positions.append((btn_forward_x, nav_y))

        # Updated page label to include total rows
        lbl_page_x = btn_forward_x + btn_forward.winfo_reqwidth() + 10
        lbl_page = tk.Label(self.root, text=f"Page 1/{total_pages} - total rows {len(data)}", width=25, anchor='w')
        lbl_page.place(x=lbl_page_x, y=nav_y)
        lbl_page.update_idletasks()
        navtable_elements.append(lbl_page)
        element_positions.append((lbl_page_x, nav_y))

        # Calculate total height (title + rows + navigation)
        total_height = (title_height + 2 if title_height > 0 else 0) + \
                       nr_rows * row_spacing - vgap + \
                       vnavgap + \
                       btn_back.winfo_reqheight() + 5

        # Save all necessary information for table management
        navtable_data = {
            'conf': table_conf,
            'data': data,
            'nr_rows': rows_per_page,
            'folder_images': folder_images,
            'current_page': current_page,
            'total_pages': total_pages,
            'row_elements': row_elements,
            'btn_back': btn_back,
            'btn_forward': btn_forward,
            'lbl_page': lbl_page,
            'size_img': size_img,
            'img_width': img_width,
            'img_height': img_height,
            'vgap': vgap,
            'vnavgap': vnavgap,
            'alternate_rowcolor': alternate_rowcolor,
            'row_frames': row_frames,
            'start_positions': {
                'start_x': start_x,
                'content_start_y': content_start_y,
                'row_height': row_height
            }
        }

        self._navtable_groups[effective_key] = navtable_data

        self._register_element_position(effective_key, start_x, start_y, max_width, total_height)
        self._navtable_element_positions[effective_key] = list(zip(navtable_elements, element_positions))

        if s:
            self.element_strings[effective_key] = s

        for element in navtable_elements:
            self._register_element(element, '', s)

        self._update_row_height(total_height)

        self.current_x = start_x + max_width + 10
        self.current_y = start_y

        return self

    def _cleanup_navtable(self, table_key):
        """Clean up existing navtable completely"""
        if table_key not in self._navtable_groups:
            return

        navtable_data = self._navtable_groups[table_key]

        # Delete navigation buttons and page label
        try:
            if 'btn_back' in navtable_data and navtable_data['btn_back']:
                navtable_data['btn_back'].destroy()
        except:
            pass

        try:
            if 'btn_forward' in navtable_data and navtable_data['btn_forward']:
                navtable_data['btn_forward'].destroy()
        except:
            pass

        try:
            if 'lbl_page' in navtable_data and navtable_data['lbl_page']:
                navtable_data['lbl_page'].destroy()
        except:
            pass

        # Delete row frames if they exist
        if 'row_frames' in navtable_data:
            for frame in navtable_data['row_frames']:
                try:
                    if frame:
                        frame.destroy()
                except:
                    pass

        # Delete all row elements
        if 'row_elements' in navtable_data:
            for row_list in navtable_data['row_elements']:
                for element in row_list:
                    try:
                        element.destroy()
                    except:
                        pass

        # Clean up from element positions
        if hasattr(self, '_navtable_element_positions') and table_key in self._navtable_element_positions:
            elements_positions = self._navtable_element_positions[table_key]
            for element, pos in elements_positions:
                try:
                    element.destroy()
                except:
                    pass
            del self._navtable_element_positions[table_key]

        # Remove from navtable groups
        del self._navtable_groups[table_key]

        # Clean up from main tracking structures
        if table_key in self.element_keys:
            del self.element_keys[table_key]
        if table_key in self.element_positions:
            del self.element_positions[table_key]
        if table_key in self.element_strings:
            del self.element_strings[table_key]

    def _create_image_element(self, image_path, width, height, x, y, key, s):
        """Helper method to create image element for navtable"""
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
            try:
                placeholder_image = Image.new('RGB', (width, height), color='lightgray')

                if ImageDraw:
                    draw = ImageDraw.Draw(placeholder_image)
                    draw.line([(0, 0), (width - 1, height - 1)], fill='gray', width=2)
                    draw.line([(0, height - 1), (width - 1, 0)], fill='gray', width=2)
                    draw.rectangle([(0, 0), (width - 1, height - 1)], outline='gray', width=1)

                photo_image = ImageTk.PhotoImage(placeholder_image)
            except ImportError:
                # Create a text label as fallback when PIL is not available
                image_label = tk.Label(self.root, text="IMG", width=6, height=3, bg='lightgray')
                image_label.place(x=x, y=y)
                return image_label

        def image_callback(event):
            parts = key.split('_')
            if len(parts) >= 4:  # format: "key_IMG_ROW_i"
                clicked_row = int(parts[-1])
                base_key = '_'.join(parts[:-3])

                if base_key in self._navtable_groups:
                    navtable_data = self._navtable_groups[base_key]
                    current_page = navtable_data['current_page']
                    rows_per_page = navtable_data['nr_rows']
                    actual_row = current_page * rows_per_page + clicked_row

                    values = self._get_values()
                    values['_clicked_row'] = actual_row
                    values['_clicked_data'] = navtable_data['data'][actual_row] if actual_row < len(
                        navtable_data['data']) else None
                    self.event_queue.put((key, values))

        image_label = tk.Label(self.root, image=photo_image)
        image_label.image = photo_image
        image_label.bind("<Button-1>", image_callback)
        image_label.config(cursor="hand2")
        image_label.place(x=x, y=y)

        return image_label

    def _navtable_navigate(self, table_key, direction):
        """Handle table navigation (direction: -1 = back, 1 = forward)"""
        if not hasattr(self, '_navtable_groups') or table_key not in self._navtable_groups:
            return

        navtable_data = self._navtable_groups[table_key]
        current_page = navtable_data['current_page']
        total_pages = navtable_data['total_pages']

        new_page = current_page + direction

        if new_page < 0 or new_page >= total_pages:
            return

        navtable_data['current_page'] = new_page
        self._navtable_update_page(table_key)

    def _navtable_update_page(self, table_key):
        """Update current page content of the table"""
        if not hasattr(self, '_navtable_groups') or table_key not in self._navtable_groups:
            return

        navtable_data = self._navtable_groups[table_key]
        current_page = navtable_data['current_page']
        data = navtable_data['data']
        conf = navtable_data['conf']
        rows_per_page = navtable_data['nr_rows']
        folder_images = navtable_data['folder_images']
        row_elements = navtable_data['row_elements']
        row_frames = navtable_data.get('row_frames', [None] * rows_per_page)
        alternate_rowcolor = navtable_data.get('alternate_rowcolor', '')

        # Calculate indices for this page
        start_idx = current_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(data))

        # First hide ALL rows, then show only necessary ones
        for i in range(rows_per_page):
            row_elements_list = row_elements[i]
            # Hide all elements of the row
            for element in row_elements_list:
                if hasattr(element, 'place_forget'):
                    try:
                        # Make sure we're not hiding navigation elements
                        if (element != navtable_data.get('btn_back') and
                            element != navtable_data.get('btn_forward') and
                            element != navtable_data.get('lbl_page')):
                            element.place_forget()
                    except:
                        pass

            # Hide row frames if they exist
            if i < len(row_frames) and row_frames[i]:
                try:
                    row_frames[i].place_forget()
                except:
                    pass

        # Now show only rows that have data for this page
        for i in range(rows_per_page):
            data_row_index = start_idx + i
            row_elements_list = row_elements[i]

            if data_row_index < len(data) and data_row_index < end_idx:
                # This row has data to show - REPOSITION all elements

                # Retrieve original positions from initial registration
                start_x = navtable_data['start_positions']['start_x']
                content_start_y = navtable_data['start_positions']['content_start_y']
                row_height = navtable_data['start_positions']['row_height']
                vgap = navtable_data.get('vgap', 0)
                row_spacing = row_height + vgap

                # Calculate row position
                row_y = content_start_y + i * row_spacing

                # Show row frame if it exists and alternating color is enabled
                if alternate_rowcolor and i % 2 == 1 and i < len(row_frames) and row_frames[i]:
                    row_frames[i].place(x=start_x, y=row_y)
                    row_frames[i].lift()  # Lift to ensure it's above any previous elements
                    # Then lower it below the content that will be placed
                    row_frames[i].lower()

                # Reposition image (first element of the list)
                if row_elements_list:
                    try:
                        image_element = row_elements_list[0]
                        # Center the image vertically in the row
                        img_width = navtable_data.get('img_width', 50)
                        img_height = navtable_data.get('img_height', 50)
                        img_y = row_y + (row_height - img_height) // 2
                        image_element.place(x=start_x, y=img_y)

                        # Update image - ALWAYS last column
                        if data[data_row_index]:
                            image_filename = data[data_row_index][-1]  # Last column = image name
                            new_image_path = os.path.join(folder_images,
                                                          image_filename) if folder_images else image_filename

                            try:
                                if os.path.exists(new_image_path):
                                    pil_image = Image.open(new_image_path)
                                    img_width = navtable_data.get('img_width', 50)
                                    img_height = navtable_data.get('img_height', 50)
                                    pil_image = pil_image.resize((img_width, img_height), Image.Resampling.LANCZOS)
                                    new_photo = ImageTk.PhotoImage(pil_image)

                                    image_element.config(image=new_photo)
                                    image_element.image = new_photo
                                else:
                                    # Create placeholder
                                    img_width = navtable_data.get('img_width', 50)
                                    img_height = navtable_data.get('img_height', 50)
                                    placeholder_image = Image.new('RGB', (img_width, img_height), color='lightgray')
                                    try:
                                        if ImageDraw:
                                            draw = ImageDraw.Draw(placeholder_image)
                                            draw.line([(0, 0), (img_width - 1, img_height - 1)], fill='gray', width=2)
                                            draw.line([(0, img_height - 1), (img_width - 1, 0)], fill='gray', width=2)
                                            draw.rectangle([(0, 0), (img_width - 1, img_height - 1)], outline='gray',
                                                           width=1)
                                    except ImportError:
                                        pass

                                    placeholder_photo = ImageTk.PhotoImage(placeholder_image)
                                    image_element.config(image=placeholder_photo)
                                    image_element.image = placeholder_photo
                            except Exception as e:
                                print(f"Image loading error {new_image_path}: {e}")
                    except:
                        pass

                    # Reposition and update text elements (from second element onwards)
                    img_width = navtable_data.get('img_width', 50)
                    current_x_text = start_x + img_width + 10  # Distance from image edge to text
                    keylist = list(conf.keys())

                    for j, text_element in enumerate(row_elements_list[1:]):
                        try:
                            # Calculate vertical center of the row for text alignment
                            text_y = row_y + (row_height - 16) // 2  # 16 is approximate height of text

                            # Update background color if needed
                            if alternate_rowcolor and i % 2 == 1:
                                text_element.config(background=alternate_rowcolor)
                            else:
                                # Reset to default system color if not an alternate row
                                text_element.config(background=self.root.cget('bg'))

                            # Reposition text element
                            text_element.place(x=current_x_text, y=text_y)

                            # Update text content
                            if j < len(keylist) and j < len(
                                    data[data_row_index]) - 1:  # -1 to exclude last column (image)
                                text_element.config(text=str(data[data_row_index][j]))
                            else:
                                text_element.config(text='')

                            # Calculate X position for next element
                            text_width = conf[keylist[j]][1] * 10 if j < len(keylist) else 100
                            current_x_text += text_width + 5
                        except:
                            pass

        # Update page label with total rows included
        try:
            total_rows = len(data)
            navtable_data['lbl_page'].config(text=f"Page {current_page + 1}/{navtable_data['total_pages']} - total rows {total_rows}")
        except:
            pass

    def _get_current_page_data_navtable(self, navtable_data):
        """Return current page data of a navigable table"""
        current_page = navtable_data['current_page']
        rows_per_page = navtable_data['nr_rows']
        data = navtable_data['data']

        start_idx = current_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(data))

        return data[start_idx:end_idx] if data else []