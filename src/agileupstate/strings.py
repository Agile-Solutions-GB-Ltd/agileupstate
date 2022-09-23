def indent(message) -> str:
    return f'  {message}'


def truncate(text, length=-50) -> str:
    """ Right truncate string with message.

    :param text: string to truncate
    :param length: negative length
    :return:
    """
    return f'...{text[length:]}'
