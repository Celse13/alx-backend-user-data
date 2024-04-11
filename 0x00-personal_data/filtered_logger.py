#!/usr/bin/env python3
"""Log user data"""
import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def print_data(user_info):
    """print user data"""
    print_values = ['name', 'email', 'phone', 'ssn', 'password']
    data = '[HOLBERTON] user_date INFO {last_login}: {data}'

    data = '; '.join(f'{key}=***' if key in print_values else f'{key}={value}'
                     for key, value in zip(['name', 'email', 'phone', 'ssn',
                                            'password', 'ip', 'last_login',
                                            'user_agent'], user_info))
    print(data.format(last_login=user_info[6], data=data))


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a MySQL database"""
    return mysql.connector.connect(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"),
    )


def get_logger() -> logging.Logger:
    """Get logger object"""
    objct = logging.getLogger("user_data")
    objct.setLevel(logging.INFO)
    objct.propagate = False

    temp = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    temp.setFormatter(formatter)
    objct.addHandler(temp)

    return objct


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for prop in fields:
        message = re.sub(f"{prop}=.*?{separator}",
                         f"{prop}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format record"""
        Formatter = logging.Formatter(self.FORMAT)
        record = Formatter.format(record)
        return filter_datum(self.fields, self.REDACTION,
                            str(record), self.SEPARATOR)

    def redact(self, message: str) -> str:
        """method to obfuscate the message"""
        for prop in self.fields:
            message = re.sub(f"{prop}=[^;]",
                             f"{prop}={self.REDACTION}", message)
        return message


def main():
    """main call function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, \
                    last_login, user_agent FROM users;")

    for record in cursor:
        print_data(record)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
