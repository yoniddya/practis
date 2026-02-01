import os
# os.getcwd()
# os.listdir()
# count = 0
# for file in os.listdir():
#     if file.endswith(".py"):
#         count += 1
# print(count)

def current_folder():
    return f"{os.getcwd()}"
# print(current_folder())

def nams_of_fils_in_this_folder():
    return f"{os.listdir()}"
# print(nams_of_fils_in_this_folder())

def my_func(path):
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        print("תוכן התיקייה:")
        for item in os.listdir():
            print(item)
    except FileNotFoundError:
        print("התיקייה לא קיימת")
    finally:
        os.chdir(original_dir)
# my_func(r"C:\Users\yonid\PycharmProjects\kodkod_ex")

def print_all_files(path):
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                print(os.path.join(root, file))
    except Exception as e:
        print("שגיאה:", e)

# print_all_files(r"C:\Users\yonid\PycharmProjects\practis")


def print_all_files_end_with_py(path, extension=".py"):
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(extension):
                    print(os.path.join(root, file))
    except Exception as e:
        print("שגיאה:", e)
# print_all_files_end_with_py(r"C:\Users\yonid\PycharmProjects\practis")


