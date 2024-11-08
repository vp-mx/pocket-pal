"""Module for storing classes related to the address book"""

import re
from collections import UserDict
from datetime import date, datetime, timedelta
from typing import Any, Optional

from error_handlers import HelperError


class Field:
    """Base class for fields in a record"""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False
        return self.value == other.value


class Name(Field):
    """Class represents the name of a contact"""


class Phone(Field):
    """Class for storing a phone number with validation."""

    def __init__(self, value: str) -> None:
        """
        :param value: The phone number (must be 10 digits).
        :raises HelperError: If the phone number is not 10 digits.
        """
        if not re.match(r"^\d{10}$", value):
            raise HelperError("Phone number must be 10 digits")
        super().__init__(value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Phone):
            return False
        return self.value == other.value


class Birthday(Field):
    """Class for storing a birthday with validation."""

    def __init__(self, value: str) -> None:
        """Initialize the birthday field.

        :param value: The birthday in DD.MM.YYYY format.
        :raises HelperError: If the date format is invalid.
        """
        self.__value: date = self.__parse_date(value)
        super().__init__(self.__value)

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")

    @staticmethod
    def __parse_date(value: str) -> date:
        """Parse a date string in the format DD.MM.YYYY.

        :param value: The date string to parse.
        :return: The datetime object.
        :raises HelperError: If the date format is invalid.
        """
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError as e:
            raise HelperError("Invalid date format. Use DD.MM.YYYY") from e


class Email(Field):
    """Class for storing an email with validation"""

    def __init__(self, value):
        """Initialize the email field.

        :param value: The email in name@domen.domen format.
        :raises HelperError: If the email format is invalid.
        """
        self.validation(value)
        super().__init__(value)

    @staticmethod
    def validation(email):
        """Validate an email string.

        :param value: The email string to validate.
        :return: validated email.
        :raises HelperError: If the email format is invalid.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise HelperError(f"Validation for email '{email}' is declined.")


class Record:
    """Class for storing contact information, including name, phone numbers, and birthday."""

    def __init__(self, name: str) -> None:
        """Initialize the record with a name.

        :param name: The name of the contact.
        """
        self.name = Name(name.strip())
        self.phones: list[Phone] = []
        self.__birthday: Optional[Birthday] = None
        self.__address: Optional[str] = None
        self.emails = []
        self.notes: Optional[list[str]] = []

    @property
    def contact_name(self) -> str:
        """The name of the contact."""
        return str(self.name)

    @property
    def all_phones(self) -> str:
        """All phone numbers in the contact, separated by commas."""
        return ", ".join(phone.value for phone in self.phones) if self.phones else "N/A"

    @property
    def all_emails(self) -> str:
        """All emails in the contact, separated by commas."""
        return ", ".join(email.value for email in self.emails) if self.emails else "N/A"

    @property
    def all_notes(self) -> str:
        """All notes in the contact, separated by commas."""
        return ", ".join(self.notes) if self.notes else "N/A"

    @property
    def address(self) -> str:
        """All address in the contact."""
        return self.__address if self.__address else "N/A"

    @property
    def birthday(self) -> str:
        """The birthday of the contact."""
        return str(self.__birthday) if self.__birthday else "N/A"

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the contact.

        :param phone: The phone number to add.
        """
        phone_to_add = Phone(phone)
        if phone_to_add in self.phones:
            raise HelperError("Phone number already exists")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the contact.

        :param phone: The phone number to remove.
        """
        try:
            self.phones.remove(Phone(phone))
        except ValueError as e:
            raise HelperError("Phone number to remove is not found") from e

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number.

        :param old_phone: The phone number to be replaced.
        :param new_phone: The new phone number.
        :raises ValueError: If the old phone number is not found.
        """
        old_phone_obj, new_phone_obj = Phone(old_phone), Phone(new_phone)
        if old_phone_obj not in self.phones:
            raise HelperError("Phone number to update not found")
        pos = self.phones.index(old_phone_obj)
        self.phones[pos] = new_phone_obj

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone number in the contact.

        :param phone: The phone number to find.
        :return: The Phone object if found, else None.
        """
        for num in self.phones:
            if num.value == phone:
                return num
        return None

    def add_birthday(self, birthday: str) -> None:
        """Add a birthday to the contact.

        :param birthday: The birthday to add.
        """
        self.__birthday = Birthday(birthday)

    def add_address(self, address: str) -> None:
        """Add an address to the contact.
        :param address: The address to add.
        """
        self.__address = address

    def add_email(self, email):
        """Add an email to the contact.

        :param email: The email to add.
        """
        self.emails.append(Email(email))

    def edit_email(self, old_email, new_email):
        """Edit the email for a contact.

        :params: old_email, new_email.
        :return: str: Result message.
        """
        if self.emails:
            old_email_obj = Email(old_email)
            if old_email_obj in self.emails:
                self.emails[self.emails.index(old_email_obj)] = Email(new_email)
            else:
                raise HelperError(f"Email '{old_email}' doesn't exist for this contact.")
        raise HelperError("This contact doesn't have any emails to edit.")

    def remove_email(self, email):
        """Remove the email from the contact.

        :param email: The email to remove.
        """
        if self.emails:
            for i in self.emails:
                if i.value == email:
                    self.emails.remove(i)
                    return True
            raise HelperError(f"Email '{email}' doesn't exist for this contact.")
        raise HelperError("This contact doesn't have any emails to remove.")

    def add_note(self, note_title: str) -> None:
        """Add a note to the contact.

        :param note: The note to add.
        """
        self.notes.append(note_title)


class AddressBook(UserDict):
    """Class for storing contacts in an address book."""

    @property
    def all_records(self) -> str:
        """Returns all contacts in the address book.

        :return: string with all contacts separated by newlines.
        """
        return "\n".join([str(record) for record in self.values()]) or "No contacts found."

    def add_record(self, record: Record) -> None:
        """Add a record to the address book.

        :param record: The Record object to add.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Find a record by name.

        :param name: The name of the contact.
        :return: The Record object if found, else None.
        """
        return self.data.get(name.strip())

    def search_by_partial_name(self, partial_name):
        """Finds all contacts that contain the partial name.

        param: partial_name: The part of the name to search for.
        return: list[Record]: List of matching records.
        """
        return [record for name, record in self.data.items() if partial_name.lower() in name.lower()]

    def delete(self, name: str) -> None:
        """Delete a record by name.

        :param name: The name of the contact to delete.
        :raises HelperError: If the record is not found.
        """
        try:
            self.data.pop(name)
        except KeyError as e:
            raise HelperError("Record not found") from e

    def get_upcoming_birthdays(self, days_interval: int = 7) -> str:
        """Returns a list of upcoming birthdays within the next N days.

        When the birthday falls on a weekend, the congratulation date is moved to the next week.

        :return: string with upcoming birthdays separated by newlines for each contact.
        """
        today = datetime.today().date()
        contacts_with_birthdays = [record for record in self.values() if record.birthday is not None]
        upcoming_birthdays = []

        for user in contacts_with_birthdays:
            greet_date = user.birthday.value.replace(year=today.year)

            if greet_date < today:
                greet_date = greet_date.replace(year=today.year + 1)

            days_until_greet = greet_date - today
            if days_until_greet.days <= days_interval:
                if greet_date.isoweekday() in (6, 7):
                    greet_date += timedelta(days=8 - greet_date.isoweekday())
                congratulation_date = greet_date.strftime("%d.%m.%Y")
                upcoming_birthdays.append(
                    (f"Contact name: {user.name.value}, " f"congratulation date: {congratulation_date}")
                )

        return "\n".join(upcoming_birthdays) or f"No upcoming birthdays found in next {days_interval} days."


me = Record("me")
me.add_phone("1234567890")
me.add_phone("1234567891")
me.add_birthday("01.01.2000")
AddressBook().add_record(me)
