"""Module for storing classes related to the notes"""

from collections import UserDict
from datetime import datetime
from typing import List, Optional


class Note:
    """Class representing a note."""

    def __init__(
        self, title: str, body: str, tags: Optional[List[str]] = None, contacts: Optional[List[str]] = None
    ) -> None:
        """Initialize the note.
        :param title: The title of the note.
        :param body: The body of the note.
        :param tags: A list of tags for the note.
        :param contacts: A list of contacts if the note is attached to a contact.
        """

        self.title = title
        self.body = body
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        if len(tag) < 0 and len(tag) > 20:
            raise ValueError("Tag must be between 1 and 20 characters")
        self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the note."""
        if tag not in self.tags:
            raise ValueError(f"Tag {tag} not found")
        self.tags.remove(tag)

    def __repr__(self):
        return f"{self.title}, {self.body}, {self.tags}, {self.contacts}"


class NoteBook(UserDict):
    """Class representing a collection of notes."""

    def add(
        self, title: str, body: str, tags: Optional[List[str]] = None, contacts: Optional[List[str]] = None
    ) -> None:
        """Add a new note to the notebook."""
        self.data[title] = Note(title, body, tags, contacts)

    def delete(self, title: str) -> None:
        """Delete a note from the notebook by title."""
        if not title in self.data:
            raise KeyError(f"Note with title {title} not found")
        del self.data[title]

    def edit(self, title: str, new_body: str) -> None:
        """Edit the body of an existing note."""
        if not title in self.data:
            return KeyError(f"Note with title {title} not found")
        return self.data[title].edit(new_body)

    def replace(self, title: str, new_body: str) -> None:
        """Edit the body of an existing note."""
        if not title in self.data:
            return KeyError(f"Note with title {title} not found")
        return self.data[title].replace(new_body)

    def attach_to_contact(self, title: str, contact_name: str) -> None:
        """Attach a note to a contact."""
        if not title in self.data:
            raise KeyError(f"Note with title {title} not found")

        return self.data[title].attach_to_contact(contact_name)

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
        return list(self.data.values())

    def find(self, title: str) -> Optional[Note]:
        """Find a note in the notebook."""
        return self.data.get(title)

    def show_all_for_contact(self, contact_name: str) -> List[Note]:
        """Find all notes attached to a contact."""
        if not any(contact_name in note.contacts for note in self.data.values()):
            raise ValueError(f"No notes found for contact {contact_name}")
        return [note for note in self.data.values() if contact_name in note.contacts]

    def find_by_tag(self, tag: str) -> List[Note]:
        """Find all notes with a specific tag."""
        notes = [note for note in self.data.values() if tag in note.tags]
        return notes

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"
