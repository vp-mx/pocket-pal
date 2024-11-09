"""This module contains functions to save, load and delete the address book and notes book from a file."""

import csv
import os
import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Union

from address_book import AddressBook, Record
from notes import NoteBook

if TYPE_CHECKING:
    pass

FOLDER_FOR_PKL = Path().home() / "PocketPal"
ADDRESS_BOOK_FILE = "pocket-pal-book.pkl"
NOTES_FILE = "pocket-pal-notes.pkl"


def save_data(book: Union["AddressBook", "NoteBook"], file_name: str) -> None:
    """Saves the address book to a file.

    param: book: AddressBook object to save.
    param: filename: File name to save the data.
    """
    filepath = FOLDER_FOR_PKL / file_name
    os.makedirs(filepath.parent, exist_ok=True)
    with open(filepath, "wb") as pkl_file:
        pickle.dump(book, pkl_file)


def load_data(filename):
    """Loads the address book from a file.

    param: filename: File name to load the data.
    return: AddressBook object.
    """
    try:
        filepath = FOLDER_FOR_PKL / filename
        with open(filepath, "rb") as pkl_file:
            return pickle.load(pkl_file)
    except FileNotFoundError:
        return None


def delete_data(filename):
    """Deletes the address or notes book from a file.

    param: filename: File name to delete the data.
    """
    try:
        filepath = FOLDER_FOR_PKL / filename
        os.remove(filepath)
    except FileNotFoundError:
        pass


def import_csv(book: "AddressBook", notebook: "Notes") -> None:
    """Imports contacts from a csv file.

    param: file_path: Path to the csv file.
    param: book: AddressBook object to save the contacts.
    """
    try:
        contacts = FOLDER_FOR_PKL / "contacts.csv"
        if contacts.exists():
            with open(contacts, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    record = Record(row["Name"])
                    record.add_phone(row["Phones"])
                    record.add_birthday(row["Birthday"])
                    record.add_address(row["Address"])
                    record.add_email(row["Emails"])
                    record.add_note(row["Notes"])
                    book.add_record(record)
        notes = FOLDER_FOR_PKL / "notes.csv"
        if notes.exists():
            _ = notebook
    except Exception as e:
        print(f"Error importing file: {e}")
