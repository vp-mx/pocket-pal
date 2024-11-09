"""Main module to run the assistant bot."""

from prompt_toolkit import PromptSession
from rich.panel import Panel
from rich.text import Text

from address_book import AddressBook
from autocomplete import CommandCompleter
from commands import Commands, Source
from custom_console import console
from error_handlers import ExitApp, InputArgsError, InternalError
from file_operations import ADDRESS_BOOK_FILE, NOTES_FILE, load_data, save_data
from notes import NoteBook


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parses user input and returns the command and arguments.

    param: user_input: The user input.
    return: The command in lowercase and list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    args = [arg.strip() for arg in args if arg.strip()]
    return cmd, args


def main():
    """Main function to run the assistant bot."""

    book = load_data(ADDRESS_BOOK_FILE) or AddressBook()
    notes = load_data(NOTES_FILE) or NoteBook()
    session = PromptSession(completer=CommandCompleter())
    console.print(Panel(":wave: Welcome to the assistant bot!", expand=False), style="bold green")
    while True:
        try:
            user_input = session.prompt("Enter a command: ")
            if not user_input.strip():
                continue
            command, args = parse_input(user_input)
            command_object = Commands.get_command(command)
            if not command_object:
                console.print("Invalid command.", style="bold red")
                continue
            if command_object in (Commands.EXIT, Commands.CLOSE):
                raise ExitApp
            command_object.value.validate_args(args)
            args_len = command_object.value.args_len
            if command_object.value.source == Source.ADDRESS_BOOK:
                result = command_object.value.run(args, book) if args_len else command_object.value.run(book)
            elif command_object.value.source == Source.NOTES:
                result = command_object.value.run(args, notes) if args_len else command_object.value.run(notes)
            elif command_object.value.source == Source.APP:
                result = command_object.value.run(args) if args_len else command_object.value.run()
            elif command_object.value.source == Source.ALL:
                result = (
                    command_object.value.run(args, book, notes) if args_len else command_object.value.run(book, notes)
                )
            else:
                raise InternalError
            if result:
                console.print(result)
        except (InputArgsError, InternalError) as error:
            console.print(Text(str(error), style="bold red"))
        except (KeyboardInterrupt, ExitApp):
            save_data(book, ADDRESS_BOOK_FILE)
            save_data(notes, NOTES_FILE)
            console.print("Data saved", style="bold blue")
            break


if __name__ == "__main__":
    main()
