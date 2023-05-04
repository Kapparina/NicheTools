from tabulate import tabulate
import os
import shutil
import textwrap
import json

tabulate.PRESERVE_WHITESPACE = True

DIGIT_CHECKS = 0
INDEX_CHECKS = 0


class UserFilePath:
    bookmarks: dict = {}
    bookmark_flag: bool = False
    directories_file = f"{os.getcwd()}/directories.json"

    def __init__(self, directory=str(), name=str(), extension=str(), index_num=int()):
        self.directory = directory
        self.name = name
        self.extension = extension
        self.index_num = index_num

        UserFilePath.bookmarks.update({self.index_num: self.directory})

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.index_num}', {self.directory})"

    def get_directory(self):
        return self.directory

    def get_name(self):
        return self.name

    def get_extension(self):
        return self.extension

    def get_index_num(self):
        return self.index_num

    def character_removal(self):
        removed_chars = ("/", "\\", "\"", "\'")

        if self.directory.startswith(removed_chars):
            self.directory = self.directory[1:]
        if self.directory.endswith(removed_chars) and 3 >= len(self.directory):
            self.directory = self.directory[:-1]
        if self.name.startswith(removed_chars):
            self.name = self.name[1:]
        if self.name.endswith(removed_chars):
            self.name = self.name[:-1]

    @classmethod
    def instantiate_from_file(cls, _directories_file):
        if os.path.isfile(_directories_file) is False:
            open(_directories_file, "x").close()
        else:
            try:
                with open(_directories_file, "r") as f:
                    directories = json.load(f)
                    print("test")
            except json.JSONDecodeError:
                with open(_directories_file, "r") as f:
                    directories = dict(enumerate(line.strip() for line in f))
                    print("second test")

            for k, v in directories.items():
                UserFilePath(
                    index_num=k,
                    directory=v,
                )

        try:
            return directories
        except UnboundLocalError:
            return {}

    @classmethod
    def save_instances_to_file(cls, _directories_file, _data):
        with open(_directories_file, "w") as f:
            json.dump(_data, f)

    @classmethod
    def save_to_bookmarks(cls, *new_bookmark):
        UserFilePath.bookmarks.update({len(UserFilePath.bookmarks.keys()) + 1: new_bookmark})


def bookmark_check(_bookmark_index, digit_check=DIGIT_CHECKS, index_check=INDEX_CHECKS):
    if digit_check <= 0:
        print("\nYou must enter a number; I will allow 3 more attempts to do so.")
    if index_check <= 0:
        print("Likewise, you must enter an index number present in the list; again - you have 3 attempts.\n")
    while True:
        print("Please enter a bookmark's corresponding index number below.")
        _bookmark_index = input("\tBookmark number: ")

        if _bookmark_index.isdigit():
            digit_check += 1

            if int(_bookmark_index) in UserFilePath.bookmarks.keys():
                break
            else:
                print("\nNo value exists at that index...\n")
                index_check += 1
                if 1 <= index_check <= 3:
                    print(f"\t\t\t====>- Index check attempt {index_check}/3 -<====")
                elif index_check >= 3:
                    print("\nThat's 3/3 index checks completed - continuing without bookmarks.")
                    return "/"

        else:
            print("\nI require a valid integer/whole number...\n")
            digit_check += 1
            if 1 <= digit_check <= 3:
                print(f"\t\t\t___>- Integer check attempt {digit_check}/3 -<___")
            elif digit_check >= 3:
                print("\n3/3 integer checks performed - continuing without bookmarks.")
                return "/"

    return _bookmark_index


def bookmark_selection():
    UserFilePath.instantiate_from_file(UserFilePath.directories_file)
    UserFilePath.bookmark_flag = False

    if len(UserFilePath.bookmarks.items()) <= 1:
        print("There aren't any directories bookmarked.")
        return "/"
    else:
        print("These are previously bookmarked directories:")

        # for index, directory in UserFilePath.bookmarks.items():
        #     print(f"| {index} | {directory} |")

        formatted_bookmarks = {"KEY": [key for key in UserFilePath.bookmarks.keys()],
                               "VALUE": [value for value in UserFilePath.bookmarks.values()]}
        bookmark_table = tabulate(formatted_bookmarks, headers=["INDEX", "DIRECTORY"],
                                  tablefmt="grid", maxcolwidths=[1, 60], showindex=False)
        print(bookmark_table)

        bookmark_index = input("\nInput a bookmark's corresponding index number: ")

        if bookmark_index.isdigit() is False:
            bookmark_index = bookmark_check(bookmark_index)
        elif int(bookmark_index) not in UserFilePath.bookmarks.keys():
            bookmark_index = bookmark_check(bookmark_index)

    if bookmark_index == "/":
        return bookmark_index
    else:
        return UserFilePath.bookmarks.get(int(bookmark_index))


# TODO: Complete bookmark functionality.
# TODO: Fix bookmark index validation.
def src_file_path():
    src_file = UserFilePath()

    if UserFilePath.bookmark_flag:
        src_file.directory = bookmark_selection()
    elif UserFilePath.bookmark_flag is False:
        print("Tell me where the source file lives...")
        src_file.directory = input("\tSource directory: ")
    elif len(bookmark_selection()) <= 1:
        print("I need you to tell me where the source file lives...")
        src_file.directory = input("\tSource directory: ")

    src_file.character_removal()

    while os.path.isdir(src_file.directory.casefold()) is False:
        print("\nPlease, tell me where the source file lives: ")
        src_file.directory = input("\tSource directory: ")
        src_file.character_removal()

    return src_file


def src_file_name(src_file):
    print("\nTell me the name of the source file...")
    src_file.name = input("\tSource file name: ")

    while os.path.isfile(f"{src_file.directory}/{src_file.name}".casefold()) is False:
        print("\nNo such file exists in this directory. Tell me the name of the source file:")
        src_file.name = input("\tSource file name: ")
        src_file.character_removal()

    src_file.name, src_file.extension = os.path.splitext(src_file.name)
    UserFilePath.bookmark_flag = False
    return src_file


def dest_file_path(src_file):
    dest_path = UserFilePath()

    if UserFilePath.bookmark_flag:
        dest_path.directory = bookmark_selection()
    elif UserFilePath.bookmark_flag is False:
        print("Give the file a new home...")
        dest_path.directory = input("\tDestination directory: ")
    elif len(bookmark_selection()) <= 1:
        print("I need you to tell me the destination directory...")
        dest_path.directory = input("\tDestination directory: ")

    dest_path.character_removal()

    dest_path.character_removal()

    while os.path.isdir(dest_path.directory.casefold()) is False:
        print("\nPlease, give me a valid destination:")
        dest_path.directory = input("\tNew destination: ")
        dest_path.character_removal()

    print("\nWould you like to rename the resulting file?")

    if (rename_file := input("\tY/N: ").casefold()) == "y":
        print("Give the resulting file a new name...")
        rename_file = input("\tNew file name: ")
        dest_path.name = rename_file
        dest_path.name, dest_path.extension = os.path.splitext(dest_path.name)
        dest_path.character_removal()
    elif rename_file.casefold() == "n":
        dest_path.name = src_file.name
        dest_path.extension = src_file.extension
    else:
        print("...Opting not to rename file...\n")

    return dest_path


def move_file(src_file, dest_path):
    print(textwrap.dedent(f"""
        Confirm whether I should move:
        | {src_file.name}{src_file.extension} | 
        from: 
        | {src_file.directory} |
        to: 
        | {dest_path.directory} | 
        with the resulting name: 
        | {dest_path.name}{dest_path.extension} |
        
        NOTE: 
        If a file named {dest_path.name}{dest_path.extension} exists in {dest_path.directory}, it will be replaced.
                        """))

    if (confirm_move := input("Y/N: ").casefold()) == "y":
        final_src_path = f"{src_file.directory}/{src_file.name}{src_file.extension}"
        final_dest_path = f"{dest_path.directory}/{dest_path.name}{dest_path.extension}"
        shutil.move(final_src_path, final_dest_path)
        print("File moved successfully!")
    elif confirm_move.casefold() == "n":
        print("Aborting as directed.")
    else:
        print("Indecisiveness detected! Aborting operation.")


# noinspection PyUnusedLocal
def main():
    print("Would you like to use a bookmark as a source directory?")

    if (bookmark_choice := input("\tY/N: ").casefold()) == "y":
        UserFilePath.bookmark_flag = True
    else:
        print("Continuing to choose custom source directory...\n")

    src_file_name(source_file := src_file_path())
    print("Would you like to use a bookmark as a destination directory?")

    if (bookmark_choice := input("\tY/N: ").casefold()) == "y":
        UserFilePath.bookmark_flag = True
    else:
        print("Continuing to choose custom destination directory...\n")

    destination_file = dest_file_path(source_file)
    move_file(source_file, destination_file)

    print("Would you like to save the source directory, the destination directory, or both, as a bookmark?")

    if bm_add := "source" in input(f"\t'Source'/'Dest'/'Both' or 'N': ").casefold():
        UserFilePath.save_to_bookmarks(source_file.directory)
    elif bm_add == "dest":
        UserFilePath.save_to_bookmarks(destination_file.directory)
    elif bm_add == "both":
        UserFilePath.save_to_bookmarks(source_file.directory)
        UserFilePath.save_to_bookmarks(destination_file.directory)
    elif bm_add == "n":
        print("No changes made to bookmarks...")

    print("Pleased to have been of service!")

    UserFilePath.save_instances_to_file(UserFilePath.directories_file, UserFilePath.bookmarks)


main()
