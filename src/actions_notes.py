"""This module contains the functions to perform actions on the notes book."""

from typing import TYPE_CHECKING

from address_book import AddressBook
from custom_console import print_to_console
from error_handlers import NotFoundWarning, input_error
from notes import NoteBook
from visualisation import OutputStyle, create_rich_table_to_print

if TYPE_CHECKING:
    from commands import Commands


@input_error
def edit_note(args: list[str], notes_book: "NoteBook") -> None:
    """Edits a note in the notes dictionary.

    param: args: List with 2 values: note title and new body.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """

    note_title, new_body = args
    edited_note = notes_book.edit(note_title, new_body)
    note_table(edited_note)


@input_error
def replace_note(args: list[str], notes_book: "NoteBook") -> None:
    """Replaces a note_body in the notes dictionary.

    param: args: List with 2 values: note title and new body.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """
    note_title, new_body = args

    replaced = notes_book.replace(note_title, new_body)
    note_table(replaced)


def show_notes(notes_book: "NoteBook") -> None:
    """Shows all notes from the notes dictionary.

    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    notes_table(notes_book.show_all())


@input_error
def show_notes_contact(args, notes_book: "NoteBook") -> None:
    """Shows all notes from the notes dictionary.

    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    name = args[0]
    note = notes_book.show_all_for_contact(name)
    notes_table(note)


@input_error
def add_tag(args: list[str], notes_book: "NoteBook") -> None:
    """Adds a tag to a note in the notes dictionary.

    param: args: List with 2 values: note title and tag.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """
    note_title, tag = args
    note_in_notebook = notes_book.find(note_title)
    if not note_in_notebook:
        raise NotFoundWarning(f"Note with title '{note_title}' not found.")

    notes_book.add_tag(note_title, tag)
    print_to_console(f"Tag added to note -{note_in_notebook.title}.", style=OutputStyle.SUCCESS)


@input_error
def remove_tag(args: list[str], notes_book: "NoteBook") -> None:
    """Removes a tag from a note in the notes dictionary.

    param: args: List with 2 values: note title and tag.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """
    note_title, tag = args
    note_in_notebook = notes_book.find(note_title)
    if not note_in_notebook:
        raise NotFoundWarning(f"Note with title '{note_title}' not found.")
    notes_book.remove_tag(note_title, tag)
    print_to_console(f"Tag {tag} removed from note -{note_in_notebook.title}.", style=OutputStyle.SUCCESS)


@input_error
def attach_note(args: list[str], address_book: "AddressBook", notes_book: "NoteBook") -> None:
    """Attaches a note to a contact in the notes dictionary.

    param: args: List with 2 values: note title and contact name.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """

    note_title = args[0]
    contact_name = args[1]
    contact = address_book.find(contact_name)
    note = notes_book.find(note_title)
    if not contact or not note:
        raise NotFoundWarning(f"Contact with name '{contact_name}' or note with title '{note_title}' not found.")

    note_with_contact = notes_book.attach_to_contact(note_title, contact_name)
    contact.add_note(note_title)
    print_to_console(f"Note {note_with_contact.title} attached to contact {contact_name}.", style=OutputStyle.SUCCESS)


def search_notes(args: list[str], notes_book: "NoteBook") -> None:
    """Searches for notes containing the query in their title or body.

    param: query: str: The query to search for.
    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    query = args[0]
    search_results = notes_book.search(query)
    notes_table(search_results)


def delete_note(args: list[str], notes_book: "NoteBook") -> None:
    """Deletes a note from the notes dictionary.

    param: note_title: str: The title of the note to delete.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """
    note_title = args[0]

    if note_in_notebook := notes_book.find(note_title):
        notes_book.delete(note_title)
        print_to_console(f"Note {note_in_notebook.title} deleted.")


def find_by_tag(args: list[str], notes_book: "NoteBook") -> list[str]:
    """Finds all notes with a specific tag.

    param: tag: str.
    param: notes_book: Notes dictionary to read from.
    return: list: Result message.
    """
    tag = args[0]
    notes_table(notes_book.find_by_tag(tag))


def sort_by_tag(tag: str, notes_book: "NoteBook") -> str:
    """Sorts notes by tag.

    param: tag: str: The tag to sort by.
    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    sorted_notes = notes_book.sort_by_tag(tag)
    notes_table(sorted_notes)


@input_error
def add_note(args: list[str], notes_book: "NoteBook") -> None:
    """Adds a note to a contact in the notes book.

    param: args: List with 2 values: name and note. Note is a string with multiple words.
    param: notes_book: NoteBook object to modify.
    return: str: Result message.
    """

    note_title: str = args[0]
    note_body = " ".join(args[1:])

    new_note = notes_book.add(note_title, note_body)
    note_table(new_note)
    print_to_console("Note added.")


def notes_table(list_of_notes: list[str]) -> None:
    """Prints a list  with all notes.

    param: list_of_notes: List of notes to print.
    return: str: Result message.
    """
    columns = ["Title", "Body", "Tags", "Contacts", "Creation Date"]
    data = [
        [
            note.title,
            note.body,
            ",".join(note.tags) if note.tags else "No Tags",
            ", ".join(sorted(note.contacts)) if note.contacts else "No contacts",
            note.creation_date,
        ]
        for note in list_of_notes
    ]
    table = create_rich_table_to_print(columns, data)
    print_to_console(table)


def note_table(note: str) -> None:
    """Prints a table with a single note.

    param: note: Note to print.
    return: str: Result message.
    """
    columns = ["Title", "Body", "Tags", "Contacts", "Creation Date"]
    data = [
        [
            note.title,
            note.body,
            ",".join(note.tags) if note.tags else "No Tags",
            ", ".join(sorted(note.contacts)) if note.contacts else "No contacts",
            note.creation_date,
        ]
    ]
    table = create_rich_table_to_print(columns, data)
    print_to_console(table)
