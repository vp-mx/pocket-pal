"""Module to store the commands and their information."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional, Union

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from actions import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    change_phone,
    cleanup,
    edit_email,
    print_commands_table,
    remove_contact,
    remove_email,
    search_by_partial_name,
    show_all,
    show_birthday,
    show_email,
    show_phone,
)
from actions_notes import (
    add_note,
    add_tag,
    attach_note,
    delete_note,
    edit_note,
    find_by_tag,
    remove_tag,
    replace_note,
    search_notes,
    show_notes,
    show_notes_contact,
    sort_by_tag,
)
from error_handlers import InputArgsError
from file_operations import import_csv


class Source(Enum):
    """Enum to store the source where to apply command."""

    ADDRESS_BOOK = auto()
    NOTES = auto()
    ALL = auto()
    APP = auto()


@dataclass
class Command:
    """Dataclass to store command information."""

    cli_name: str
    """The name of the command for input from CLI."""
    description: str
    """Description of the command."""
    run: Callable[..., Union[str, Table, Text, Panel, None]]
    """Function to run the command."""
    args_len: int
    """Number of arguments for command. 0, the command does not receive arguments. -1 means any number of arguments."""
    input_help: str
    """Help message for the command with the correct input format."""
    source: Source
    """Source where to apply the command."""

    def validate_args(self, args: Optional[list[str]] = None):
        """Validates the number of arguments.

        param: args: List of arguments.
        raises: InputArgsError: If the number of arguments is incorrect.
        """
        if (args is None and self.args_len == 0) or self.args_len < 0:
            return
        if args is None or len(args) != self.args_len:
            raise InputArgsError(self.input_help)


class Commands(Enum):
    """Enum to store all the commands."""

    ADD = Command(
        cli_name="add",
        description="Adds a contact to the address book.",
        run=add_contact,
        args_len=2,
        input_help="add <name> <phone>. Use _ to separate first and last names.",
        source=Source.ADDRESS_BOOK,
    )
    ADD_ADDRESS = Command(
        cli_name="add-address",
        description="Adds an address to a contact.",
        run=add_address,
        args_len=2,
        input_help="add-address <name> <address>",
        source=Source.ADDRESS_BOOK,
    )
    ADD_BIRTHDAY = Command(
        cli_name="add-birthday",
        description="Adds a birthday to a contact.",
        run=add_birthday,
        args_len=2,
        input_help="add-birthday <name> <birthday>",
        source=Source.ADDRESS_BOOK,
    )
    ADD_EMAIL = Command(
        cli_name="add-email",
        description="Adds an email to a contact.",
        run=add_email,
        args_len=2,
        input_help="add-email <name> <email>",
        source=Source.ADDRESS_BOOK,
    )
    ADD_NOTE = Command(
        cli_name="add-note",
        description="Adds a note.",
        run=add_note,
        args_len=2,
        input_help="add-note <name> <note>",
        source=Source.NOTES,
    )
    ADD_TAG = Command(
        cli_name="add-tag",
        description="Adds a tag to a note.",
        run=add_tag,
        args_len=2,
        input_help="add-tag <note_title> <tag>",
        source=Source.NOTES,
    )
    ATTACH_NOTE = Command(
        cli_name="attach-note",
        description="Attaches a note to a contact.",
        run=attach_note,
        args_len=2,
        input_help="attach-note <note_tittle> <contact_name>",
        source=Source.NOTES,
    )
    BIRTHDAYS = Command(
        cli_name="birthdays",
        description="Shows upcoming birthdays.",
        run=birthdays,
        args_len=-1,
        input_help="birthdays <days_interval>",
        source=Source.ADDRESS_BOOK,
    )
    CHANGE_PHONE = Command(
        cli_name="change",
        description="Changes contact's phone.",
        run=change_phone,
        args_len=3,
        input_help="change <name> <old_phone> <new_phone>",
        source=Source.ADDRESS_BOOK,
    )
    CLOSE = Command(
        cli_name="close",
        description="Closes the assistant bot.",
        run=lambda: "Good bye!",
        args_len=0,
        input_help="close",
        source=Source.APP,
    )
    DELETE_NOTE = Command(
        cli_name="delete-note",
        description="Deletes a note.",
        run=delete_note,
        args_len=1,
        input_help="delete-note <note>",
        source=Source.NOTES,
    )
    EDIT_EMAIL = Command(
        cli_name="edit-email",
        description="Edits the email of a contact.",
        run=edit_email,
        args_len=3,
        input_help="edit-email <name> <old_email> <new_email>",
        source=Source.ADDRESS_BOOK,
    )
    EDIT_NOTE = Command(
        cli_name="edit-note",
        description="Edits a note.",
        run=edit_note,
        args_len=2,
        input_help="edit-note <note_title> <new_body>",
        source=Source.NOTES,
    )
    EXIT = Command(
        cli_name="exit",
        description="Exits the assistant bot.",
        run=lambda: "Good bye!",
        args_len=0,
        input_help="exit",
        source=Source.APP,
    )
    FIND_BY_TAG = Command(
        cli_name="find-by-tag",
        description="Finds notes by tag.",
        run=find_by_tag,
        args_len=1,
        input_help="find-by-tag <tag>",
        source=Source.NOTES,
    )
    HELP = Command(
        cli_name="help",
        description="Shows the list of available commands.",
        run=lambda: print_commands_table(Commands),
        args_len=0,
        input_help="help",
        source=Source.APP,
    )
    REMOVE_CONTACT = Command(
        cli_name="remove",
        description="Removes a contact from the address book.",
        run=remove_contact,
        args_len=1,
        input_help="remove <name>",
        source=Source.ADDRESS_BOOK,
    )
    REMOVE_EMAIL = Command(
        cli_name="remove-email",
        description="Removes the email of a contact.",
        run=remove_email,
        args_len=2,
        input_help="remove-email <name> <email>",
        source=Source.ADDRESS_BOOK,
    )
    REMOVE_TAG = Command(
        cli_name="remove-tag",
        description="Removes a tag from a note.",
        run=remove_tag,
        args_len=2,
        input_help="remove-tag <note_title> <tag>",
        source=Source.NOTES,
    )
    REPLACE_NOTE = Command(
        cli_name="replace-note",
        description="Replaces a note.",
        run=replace_note,
        args_len=2,
        input_help="replace-note <note_title> <new_body>",
        source=Source.NOTES,
    )
    SEARCH_BY_PARTIAL_NAME = Command(
        cli_name="search",
        description="Searches for contacts by partial name.",
        run=search_by_partial_name,
        args_len=1,
        input_help="search <partial_name>",
        source=Source.ADDRESS_BOOK,
    )
    SEARCH_NOTES = Command(
        cli_name="search-notes",
        description="Searches notes.",
        run=search_notes,
        args_len=1,
        input_help="search-notes <query>",
        source=Source.NOTES,
    )
    SHOW_ALL = Command(
        cli_name="all",
        description="Shows all contacts in the address book.",
        run=show_all,
        args_len=0,
        input_help="all",
        source=Source.ADDRESS_BOOK,
    )
    SHOW_BIRTHDAY = Command(
        cli_name="show-birthday",
        description="Shows the birthday of a contact.",
        run=show_birthday,
        args_len=1,
        input_help="show-birthday <name>",
        source=Source.ADDRESS_BOOK,
    )
    SHOW_EMAIL = Command(
        cli_name="show-email",
        description="Shows the email of a contact.",
        run=show_email,
        args_len=1,
        input_help="show-email <name>",
        source=Source.ADDRESS_BOOK,
    )
    SHOW_NOTES = Command(
        cli_name="show-notes",
        description="Shows all notes.",
        run=show_notes,
        args_len=0,
        input_help="show-notes",
        source=Source.NOTES,
    )
    SHOW_NOTES_CONTACT = Command(
        cli_name="show-notes-contact",
        description="Shows all notes of a contact.",
        run=show_notes_contact,
        args_len=1,
        input_help="show-notes-contact <name>",
        source=Source.NOTES,
    )
    SHOW_PHONE = Command(
        cli_name="phone",
        description="Shows the phone number of a contact.",
        run=show_phone,
        args_len=1,
        input_help="phone <name>",
        source=Source.ADDRESS_BOOK,
    )
    SORT_BY_TAG = Command(
        cli_name="sort-by-tag",
        description="Sorts notes by tag.",
        run=sort_by_tag,
        args_len=0,
        input_help="sort-by-tag <tag>",
        source=Source.NOTES,
    )
    CLEANUP = Command(
        cli_name="cleanup",
        description="Cleans up dumps files from system.",
        run=cleanup,
        args_len=1,
        input_help="cleanup <all | address-book | notes>",
        source=Source.ALL,
    )
    IMPORT = Command(
        cli_name="import",
        description="Imports contacts and notes from a csv file.",
        run=import_csv,
        args_len=0,
        input_help="import",
        source=Source.ALL,
    )

    @classmethod
    def get_command(cls, command_name: str) -> Optional["Commands"]:
        """Returns the command based on the cli command name.

        param: command_name: The name of the command.
        return: Optional[Command]: The command object.
        """
        for command in cls:
            if command.value.cli_name == command_name:
                return command
        return None

    @classmethod
    def get_commands_list(cls) -> list[str]:
        """Returns a list of all the command names.

        return: list[str]: List of command names.
        """
        return [command.value.cli_name for command in cls]
