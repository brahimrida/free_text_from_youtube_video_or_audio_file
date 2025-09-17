def error_message(message: str, usage: str):
    print("-" * 40, "WHAT WENT WRONG", "-" * 40)
    print(message)
    print("-" * 40, "WHAT WENT WRONG", "-" * 40)
    print(usage)


def args_missing_count(args_length: int) -> int:
    return 3 - args_length
