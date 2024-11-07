"""This module implements autocomplete functionality for the application."""

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from commands import Commands

commands = [
    "hello",
    "menu",
    "phone",
    "change",
    "all",
    # Email-related commands
    "add-email",
    "edit-email",
    "remove-email",
    "show-email",
    # Birthday-related commands
    "add-birthday",
    "show-birthday",
    "birthdays",
] + Commands.get_commands_list()


class CommandCompleter(Completer):
    """
    Class for handling autocompletion using the prompt_toolkit library.
    """

    def get_completions(self, document: Document, complete_event) -> iter:
        """Provide command suggestions based on user input.

        Ignores completions after the first space and suggests commands starting with the input.

        :param document: The current input text.
        :param complete_event: Event passed by the prompt_toolkit (ignored here but must remain).
        """
        _ = complete_event  # Ignored because it's not used in this method, but cannot be removed
        # because it's part of the required interface for the `Completer` class.

        if len(document.text.split()) > 1:
            return

        for command in commands:
            if command.startswith(document.text):
                yield Completion(command, start_position=-len(document.text))