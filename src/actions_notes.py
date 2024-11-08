"""This module contains the functions to perform actions on the notes book."""

from typing import TYPE_CHECKING

from custom_console import print_to_console
from error_handlers import NotFoundWarning, input_error
from visualisation import OutputStyle

if TYPE_CHECKING:
    from commands import Commands
    from notes import NoteBook


@input_error
def edit_note(args: list[str], notes_book: "NoteBook") -> None:
    """Edits a note in the notes dictionary.

    param: args: List with 2 values: note title and new body.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """

    note_title, new_body = args
    if note_in_notebook := notes_book.find(note_title):
        notes_book.edit(note_title, new_body)
        print_to_console(f"Note edited to -{note_in_notebook.body}.", style=OutputStyle.SUCCESS)
    else:
        raise NotFoundWarning(f"Note with title '{note_title}'")


@input_error
def replace_note(args: list[str], notes_book: "NoteBook") -> None:
    """Replaces a note_body in the notes dictionary.

    param: args: List with 2 values: note title and new body.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """
    note_title, new_body = args
    note_in_notebook = notes_book.find(note_title)
    if not note_in_notebook:
        raise NotFoundWarning(f"Note with title '{note_title}'")
    notes_book.replace(note_title, new_body)
    print_to_console(f"Note replaced to -{note_in_notebook.body}.", style=OutputStyle.SUCCESS)


def show_notes(notes_book: "NoteBook") -> None:
    """Shows all notes from the notes dictionary.

    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    print_to_console(notes_book.show_all())


@input_error
def show_notes_contact(name: str, notes_book: "NoteBook") -> None:
    """Shows all notes from the notes dictionary.

    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    print_to_console(str(notes_book.show_all_for_contact(name)))


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
        raise NotFoundWarning(f"Note with title '{note_title}'")

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
        raise NotFoundWarning(f"Note with title '{note_title}'")
    notes_book.remove_tag(note_title, tag)
    print_to_console(f"Tag {tag} removed from note -{note_in_notebook.title}.", style=OutputStyle.SUCCESS)


@input_error
def attach_note(args: list[str], notes_book: "NoteBook") -> None:
    """Attaches a note to a contact in the notes dictionary.

    param: args: List with 2 values: note title and contact name.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """

    note_title, contact_name = args
    note_in_notebook = notes_book.find(note_title)
    if not note_in_notebook:
        raise NotFoundWarning(f"Note with title '{note_title}'")
    notes_book.attach_to_contact(note_title, contact_name)
    print_to_console(f"Note {note_in_notebook} attached to-{note_in_notebook.contacts}.", style=OutputStyle.SUCCESS)


def search_notes(query: str, notes_book: "NoteBook") -> None:
    """Searches for notes containing the query in their title or body.

    param: query: str: The query to search for.
    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """

    print_to_console(str(notes_book.search(query)))


def delete_note(note_title: str, notes_book: "NoteBook") -> None:
    """Deletes a note from the notes dictionary.

    param: note_title: str: The title of the note to delete.
    param: notes_book: Notes dictionary to modify.
    return: str: Result message.
    """

    if note_in_notebook := notes_book.find(note_title):
        notes_book.delete(note_title)

        print_to_console(f"Note {note_in_notebook.title} deleted.")
    raise NotFoundWarning(f"Note with title '{note_title}'")


def find_by_tag(tag: str, notes_book: "NoteBook") -> list[str]:
    """Finds all notes with a specific tag.

    param: tag: str.
    param: notes_book: Notes dictionary to read from.
    return: list: Result message.
    """

    print_to_console(notes_book.find_by_tag(tag))


def sort_by_tag(tag: str, notes_book: "NoteBook") -> str:
    """Sorts notes by tag.

    param: tag: str: The tag to sort by.
    param: notes_book: Notes dictionary to read from.
    return: str: Result message.
    """
    print_to_console(notes_book.sort_by_tag(tag))
    return notes_book.sort_by_tag(tag)


@input_error
def add_note(args: list[str], notes_book: "NoteBook") -> None:
    """Adds a note to a contact in the notes book.

    param: args: List with 2 values: name and note.
    param: notes_book: NoteBook object to modify.
    return: str: Result message.
    """

    name, note = args
    note_title: str = f"note-{len(notes_book.values()) + 1}"
    notes_book.add(note_title, note)
    notes_book.attach_to_contact(note_title, name)
    print_to_console("Note added.")