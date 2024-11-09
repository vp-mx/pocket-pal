"""This module contains the functions to perform actions on the address book."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from address_book import AddressBook, Record
from custom_console import console, print_to_console
from error_handlers import NotFoundWarning, input_error
from file_operations import ADDRESS_BOOK_FILE, NOTES_FILE, delete_data
from visualisation import OutputStyle, create_rich_table_to_print

if TYPE_CHECKING:
    from commands import Commands


@input_error
def add_contact(args: list[str], book: "AddressBook") -> None:
    """Adds a contact to the address book.

    param: args: List with 2 values: name and phone.
    param: book: AddressBook object to modify.
    return: str: Result message.
    """
    name, phone = args
    if record := book.find(name):
        record.add_phone(phone)
        print_to_console(
            f"Phone number '{phone}' added to contact '{name.replace('_', ' ')}'.", style=OutputStyle.SUCCESS
        )
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print_to_console(
            f"Contact '{name.replace('_', ' ')}' created with phone number '{phone}'.", style=OutputStyle.SUCCESS
        )


@input_error
def remove_contact(args: list[str], book: "AddressBook") -> None:
    """Removes a contact from the address book.

    param: args: List with 1 value: name.
    param: book: AddressBook object to modify.
    return: str: Result message.
    """
    name = args[0]
    if not book.find(name):
        raise NotFoundWarning(f"Contact '{name}' not found")

    book.delete(name)
    print_to_console(f"Contact '{name}' deleted.", style=OutputStyle.SUCCESS)


@input_error
def change_phone(args: list[str], book: "AddressBook") -> None:
    """Changes the phone number of a contact in the address book.

    param: args: List with 3 values: name, old phone, new phone.
    param: book: AddressBook object to modify.
    return: str: Result message.
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found.")

    record.edit_phone(old_phone, new_phone)
    print_to_console(f"Phone number updated from {old_phone} on {new_phone} .", style=OutputStyle.SUCCESS)


@input_error
def show_phone(args: list[str], book: "AddressBook") -> None:
    """Shows the phone number of a contact from the address book.

    param: args: List with 1 value: name.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name = args[0]
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    print_to_console(f"{name}'s phones: {record.all_phones}", style=OutputStyle.SUCCESS)


def show_all(book: "AddressBook", filtered_data: Optional[list[Record]] = None) -> None:
    """Shows all contacts from the contacts dictionary.

    param: contacts: Contacts dictionary to read from.
    return: str: Result message.
    """
    columns = ["Name", "Phones", "Birthday", "Address", "Emails", "Notes"]
    records = filtered_data or book.data.values()
    data = [
        [
            record.contact_name.replace("_", " "),
            record.all_phones,
            record.birthday,
            record.address,
            record.all_emails,
            record.all_notes,
        ]
        for record in records
    ]
    data = sorted(data, key=lambda x: x[0])
    table = create_rich_table_to_print(columns, data)
    table.title = "Contacts:" if not filtered_data else "Search Results:"
    table.title_style = "bold blue"
    console.print(table)


@input_error
def add_birthday(args: list[str], book: "AddressBook") -> None:
    """Adds a birthday to a contact in the address book.

    param: args: List with 2 values: name and birthday.
    param: book: AddressBook object to modify.
    return: str: Result message.
    """
    name, birthday = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    record.add_birthday(birthday)
    print_to_console("Birthday added.")


@input_error
def show_birthday(args: list[str], book: "AddressBook") -> None:
    """Shows the birthday of a contact from the address book.

    param: args: List with 1 value: name.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name = args[0]
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    if record.birthday:
        print_to_console(f"{name}'s birthday is in {record.birthday}", style=OutputStyle.SUCCESS)
    else:
        print_to_console(f"{name}'s birthday not set", style=OutputStyle.WARNING)


@input_error
def birthdays(args, book: "AddressBook") -> None:
    """Shows all birthdays in next 7 days.

    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    days_interval = int(args[0]) if args else 7
    upcoming_birthdays = book.get_upcoming_birthdays(days_interval)
    if not upcoming_birthdays:
        print_to_console(f"No birthdays in the next {days_interval} days.")
        return
    upcoming_birthdays = sorted(upcoming_birthdays, key=lambda x: datetime.strptime(x[1], "%d.%m.%Y").date())
    upcoming_birthdays = [[name.replace("_", " "), birthday] for name, birthday in upcoming_birthdays]
    console.print(f"Upcoming birthdays in next {days_interval} days:")
    console.print(create_rich_table_to_print(["Contact name", "Congratulation day"], upcoming_birthdays))


@input_error
def add_address(args: list[str], book: "AddressBook") -> None:
    """Adds an address to a contact in the address book.
    param: args: List with 2 values: name and address.
    param: book: AddressBook object to modify.
    return: str: Result message.
    """
    name, address = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    record.add_address(address)
    print_to_console("Address added.", style=OutputStyle.SUCCESS)


@input_error
def add_email(args, book) -> None:
    """Add an email to a contact.

    param: args: List with 2 values - name and email.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name, email = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    record.add_email(email)
    print_to_console(f"Email '{email}' was successfully added for contact '{name}'.", style=OutputStyle.SUCCESS)


@input_error
def edit_email(args, book) -> None:
    """Edit an email for a contact.

    param: args: List with 3 values - name, old_email and new_email.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name, old_email, new_email = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")
    record.edit_email(old_email, new_email)
    print_to_console(
        f"Email '{old_email}' was successfully changed to '{new_email}' for contact '{name}'.",
        style=OutputStyle.SUCCESS,
    )


@input_error
def remove_email(args, book) -> None:
    """Remove an email for a contact.

    param: args: List with 2 values - name and email.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name, email = args
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")

    record.remove_email(email)
    print_to_console(f"Email '{email}' was successfully removed from contact '{name}'.", style=OutputStyle.SUCCESS)


@input_error
def show_email(args, book) -> None:
    """Show contact email/emails.

    param: args: List with 1 value - name.
    param: book: AddressBook object to read from.
    return: str: Result message.
    """
    name = args[0]
    record = book.find(name)
    if not record:
        raise NotFoundWarning(f"Contact '{name}' not found")
    text = "Contact doesn't have any emails" if not record.emails else "; ".join(email.value for email in record.emails)
    print_to_console(text, style=OutputStyle.SUCCESS)


@input_error
def search_by_partial_name(args, book) -> None:
    """Searches for contacts by partial name.

    param: args: 1 value: the partial name to search.
    param: book: AddressBook object to search in.
    return: str: Result message.
    """
    partial_name = args[0]
    records = book.search_by_partial_name(partial_name)
    if not records:
        raise NotFoundWarning(f"Contacts with '{partial_name}' in name not found.")
    show_all(book, records)


def print_commands_table(cmds: type["Commands"]) -> None:
    """Returns a table with all the commands and their descriptions.

    Note: For helper it stores into ths module due to circular imports. For Notes and AddressBook
    similar helper functions should be stored in their respective modules.

    return: Table: The table with the commands.
    """
    cmds = list(cmds)
    cmds = sorted(cmds, key=lambda x: x.value.cli_name)
    cmds = sorted(cmds, key=lambda x: x.value.source.value)
    columns = ["Command Name", "Description", "Input Help"]
    data = [[command.value.cli_name, command.value.description, command.value.input_help] for command in cmds]
    console.print(create_rich_table_to_print(columns, data))


@input_error
def cleanup(args: list[str], book, notebook) -> None:
    """Cleans up dumps files from system.

    return: str: Result message.
    """
    config = args[0]
    files_to_delete = {
        "all": [ADDRESS_BOOK_FILE, NOTES_FILE],
        "address-book": [ADDRESS_BOOK_FILE],
        "notes": [NOTES_FILE],
    }
    if files_to_delete.get(config) is None:
        raise NotFoundWarning("Choose from 'all', 'address-book', or 'notes'.")

    for file in files_to_delete[config]:
        print(f"Deleting {file}...")
        delete_data(file)
    if config in ("all", "address-book"):
        book.clear()
    if config in ("all", "notes"):
        notebook.clear()
    print_to_console("Dumps cleaned up.")
