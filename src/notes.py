"""Module for storing classes related to the notes"""

from collections import UserDict
from datetime import datetime
from typing import List, Optional

from error_handlers import HelperError


class Note:
    """Class representing a note."""

    def __init__(
        self, title: str, body: str, tags: Optional[List[str]] = None, contacts: Optional[List[str]] = None
    ) -> None:
        """Initialize the note.
        :param title: The title of the note.
        :param body: The body of the note.
        :param tags: A list of tags for the note.
        :param contacts: A set of contacts if the note is attached to a contact.
        """

        self.title = title
        self.body = body
        self.creation_date = datetime.now().date().strftime("%Y-%m-%d")
        self.tags = tags if tags else []
        self.contacts = contacts if contacts else set()

    def edit(self, new_body: str) -> None:
        """Edit the note by adding something to the body."""
        self.body = self.body + " " + new_body

    def replace(self, new_body: str) -> None:
        """Edit the note by replacing the body."""

        self.body = new_body

    def attach_to_contact(self, contact_name: str) -> None:
        """Attach the note to a contact."""
        self.contacts.add(contact_name)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the note."""
        if len(tag) < 1 or len(tag) > 20:
            raise ValueError("Tag must be between 1 and 20 characters")
        self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        if tag not in self.tags:
            raise HelperError(f"Tag {tag} not found")
        self.tags.remove(tag)

    def __repr__(self):
        tags_str = ", ".join(self.tags) if self.tags else "No tags"
        contacts_str = ", ".join(sorted(self.contacts)) if self.contacts else "No contacts"
        return (
            f"Note: {self.title}\n"
            f"Created: {self.creation_date}\n"
            f"Tags: {tags_str}\n"
            f"Attached to Contacts: {contacts_str}\n"
            f"Body: {self.body}\n"
        )


class NoteBook(UserDict):
    """Class representing a collection of notes."""

    def add(
        self, title: str, body: str, tags: Optional[List[str]] = None, contacts: Optional[List[str]] = None
    ) -> None:
        """Add a new note to the notebook."""
        self.data[title] = Note(title, body, tags, contacts)
        return self.data[title]

    def delete(self, title: str) -> None:
        """Delete a note from the notebook by title."""
        if not title in self.data:
            raise KeyError(f"Note with title {title} not found")
        del self.data[title]
        return f"Note with title {title} deleted"

    def edit(self, title: str, new_body: str) -> None:
        """Edit the body of an existing note by adding new text to existing one."""
        if not title in self.data:
            raise HelperError(f"Note with title {title} not found")
        self.data[title].edit(new_body)
        return self.data[title]

    def replace(self, title: str, new_body: str) -> None:
        """Edit the body of an existing note."""
        if not title in self.data:
            raise KeyError(f"Note with title {title} not found")
        self.data[title].replace(new_body)
        return self.data[title]

    def attach_to_contact(self, title: str, contact_name: str) -> None:
        """Attach a note to a contact."""
        if not title in self.data:
            raise KeyError(f"Note with title {title} not found")
        self.data[title].attach_to_contact(contact_name)
        return self.data[title]

    def search(self, query: str) -> List[Note]:
        """Search for notes containing the query in their title or body."""
        if query == "":
            return list(self.data.values())
        return [
            note
            for note in self.data.values()
            if query in note.title or query in note.body or query in note.tags or query in note.contacts
        ]

    def add_tag(self, title: str, tag: str) -> None:
        """Add a tag to a note."""
        self.data[title].add_tag(tag)

    def remove_tag(self, title: str, tag: str) -> None:
        """Remove a tag from a note."""
        self.data[title].remove_tag(tag)

    def show_all(self) -> List[Note]:
        """Show all notes."""
        return self.data.values()

    def find(self, title: str) -> Optional[Note]:
        """Find a note in the notebook."""
        return self.data.get(title) or f"Note with title {title} not found"

    def show_all_for_contact(self, contact_name: str) -> List[Note]:
        """Find all notes attached to a contact."""
        notes = []
        for note in self.data.values():
            if contact_name in note.contacts:
                notes.append(note)
            return notes

    def find_by_tag(self, tag: str) -> List[Note]:
        """Find all notes with a specific tag."""
        if not any(tag in note.tags for note in self.data.values()):
            raise ValueError(f"No notes found with tag {tag}")
        return [note for note in self.data.values() if tag in note.tags]

    def sort_by_tag(self, tag: str) -> List[Note]:
        """Sort all notes by a specific tag."""
        if not any(tag in note.tags for note in self.data.values()):
            raise ValueError(f"No notes found with tag {tag}")
        with_tag = sorted([note for note in self.data.values() if tag in note.tags], key=lambda x: x.creation_date)
        without_tag = sorted(
            [note for note in self.data.values() if tag not in note.tags], key=lambda x: x.creation_date
        )
        return with_tag + without_tag

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"
