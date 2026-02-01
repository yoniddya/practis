import os
# כתבו תוכנה שמקבלת מהמשתמש שורות טקסט ושומרת אותן לקובץ.
# התוכנה תמשיך לקבל קלט עד שהמשתמש יקליד 'quit'

def write_into_file():
    try:
        with open('notes.txt', 'w') as file:
            line_num = 1
            while True:
                text = input("type your text or quit:")

                if text == 'quit':
                   break

                file.write(f'{line_num}. {text}\n')
                line_num += 1
    except Exception as e:
            print(f"error: {e}")
write_into_file()

