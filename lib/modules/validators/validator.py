import sys

def strEmpty(value):
    return value == '' 

def strNotEmpty(value):
    return value != ''

def validate_case_insensitive(value: str, expect: str) -> bool:
    return expect.upper() == value.upper()

def check_argument_count(n: int) -> bool:
    return len(sys.argv) >= n + 1
