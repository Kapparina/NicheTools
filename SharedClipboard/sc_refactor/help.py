import textwrap


def blurb():
    print(textwrap.dedent(f"""
        _________________________________________________
        This application allows for persistent storage of 
        clipboard contents, catering to various use cases.

        Upon storing a value, a 'clipboard.json' file will 
        be created in the same directory as the application
        (if such a file doesn't already exist).

        Upon quitting (via 'quit'), you will be asked
        if the 'clipboard.json' should be deleted.

        For commands, type 'help' or '?'.
        _________________________________________________
        """))


def help_text():
    print(textwrap.dedent(f"""
        _________________________________________________
        Available commands include:

        |> 'save' (ie: CTRL + V): 
        | Saves/pastes the contents of your clipboard.

        |> 'load' (ie: CTRL + C): 
        | Loads/copies the value of a specified key to your clipboard.

        |> 'all' (ie: 'see all'): 
        | Lists the currently stored items.

        |> 'delete' (ie: 'remove'): 
        | Deletes/removes the value at the specified key from storage.

        |> 'wipe' (ie: 'clear'): 
        | Clears/wipes all data previously stored.

        |> 'quit' (ie: 'exit'):
        | Exits the application after asking whether to clean up. 
        _________________________________________________
        """))