#!/usr/intel/bin/python -w


from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class EncoderDecoderApp:
    def __init__(self, master):
        self._master = master
        self._master.title('Message Encoder/Decoder')
        self._master.geometry('500x251+300+150')
        self._master.resizable(0, 0)

        self._label_font = ('Calibri', '14')
        self._text_font = ('Calibri', '12')

        # Message fields
        ttk.Label(self._master, text='Message:', font=self._label_font)\
            .place(x=15, y=15)
        self._message_entry = ttk.Entry(self._master, width=50, font=self._text_font)
        self._message_entry.place(x=86, y=17)

        # Key fields
        ttk.Label(self._master, text='Key:', font=self._label_font)\
            .place(x=48, y=45)
        self._key_entry = ttk.Entry(self._master, width=25, font=self._text_font)
        self._key_entry.place(x=86, y=47)

        # Mode fields
        ttk.Label(self._master, text='Mode:', font=self._label_font)\
            .place(x=37, y=75)
        self._mode_combobox = ttk.Combobox(self._master, width=7, \
            values=('Encrypt', 'Decrypt'), font=self._text_font, state='readonly')
        self._mode_combobox.place(x=87, y=77)
        self._mode_combobox.current(0)
        self._mode_combobox.bind('<<ComboboxSelected>>', self.change_button_name)

        # Horizontal separator1
        ttk.Separator(self._master).place(x=10, y=116, width=479)

        # Result fields
        ttk.Label(self._master, text='Result:', font=self._label_font)\
            .place(x=31, y=135)
        self._result = StringVar()
        self._result_entry = ttk.Entry(self._master, width=50, font=self._text_font, \
            textvariable=self._result)
        self._result_entry.place(x=86, y=137)

        # Horizontal separator2
        ttk.Separator(self._master).place(x=10, y=176, width=479)

        # Encode/decode button
        self._encode_decode_button = ttk.Button(self._master, text='Encode', \
            command=self.translate_message)
        self._encode_decode_button.place(x=200, y=199, width=100, height=35)

    def change_button_name(self, event=None):
        mode = self._mode_combobox.get()

        if mode == 'Encrypt':
            self._encode_decode_button.config(text='Encode')
        elif mode == 'Decrypt':
            self._encode_decode_button.config(text='Decode')

        self._result.set('')

    def translate_message(self):
        message = self._message_entry.get()
        key = self._key_entry.get()

        if not (message and key):
            messagebox.showerror('Message Encoder/Decoder - ERROR', 'Please, provide both message and key!')
            return
        
        only_letters = self.is_only_letters(message + key)
        if not only_letters:
            messagebox.showerror('Message Encoder/Decoder - ERROR', 'Please, make sure that message and key contain only alphabetical letters!')
            return

        mode = self._mode_combobox.get()
        if mode == 'Encrypt':
            # Encodes message
            result = self.encode(message, key)
        elif mode == 'Decrypt':
            # Decodes message
            result = self.decode(message, key)

        self._result.set(result)

    def is_only_letters(self, string):
        # Checks whether entered message and key contain only alphabetical letters
        string = string.lower()
        for i in range(len(string)):
            if (ord(string[i])<ord('a') or ord('z')<ord(string[i])) and ord(' ')!=ord(string[i]):
                return False

        return True

    def encode(self, message, key):
        # Encrypts each message character in the message with key's character
        message_length = len(message)
        key_length = len(key)
        encrypted_message = ''
        for i in range(message_length):
            encrypted_char = self.get_translated_character(\
                i, message, key, key_length, '+')

            encrypted_message += encrypted_char

        return encrypted_message

    def decode(self, message, key):
        # Decrypts each message character in the message with key's character
        message_length = len(message)
        key_length = len(key)
        decrypted_message = ''

        for i in range(message_length):
            decrypted_char = self.get_translated_character(\
                i, message, key, key_length, '-')

            decrypted_message += decrypted_char

        return decrypted_message

    def get_translated_character(self, i, message, key, key_length, opperand):
        # For simplicity the encryption is done on lowercase only
        message_char = message[i]

        if message_char == ' ':
            # Skips "whitespace"
            translated_char = message_char
        else:
            uppercase = message_char.isupper()
            message_char = message_char.lower()

            key_char = key[i % key_length]
            key_char = key_char.lower()
            
            message_char_ascii = ord(message_char) - ord('a')
            key_char_ascii = ord(key_char) - ord('a')

            if opperand == '+':
                # For encryption
                translated_char_ascii = (message_char_ascii+key_char_ascii) % 26
            elif opperand == '-':
                # For decryption
                translated_char_ascii = (26+message_char_ascii-key_char_ascii) % 26

            translated_char = chr(translated_char_ascii + ord('a'))
            if uppercase:
                # Original character was uppercase
                translated_char = translated_char.upper()        

        return translated_char


def main():
    root = Tk()
    app = EncoderDecoderApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()