#!/usr/bin/env python3
"""Log user data"""
import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def print_d(d):
    """Prints the user data to the log"""
    f_k = ['name', 'email', 'phone', 'ssn', 'password']
    l_f = '[HOLBERTON] user_date INFO {last_login}: {data}'

    data = '; '.join(f'{k}=***' if k in f_k else f'{k}={v}'
                     for k, v in zip(['name', 'email', 'phone', 'ssn',
                                      'password', 'ip', 'last_login',
                                      'user_agent'], d))
    print(l_f.format(last_login=d[6], data=data))


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to a MySQL database"""

    return mysql.connector.connect(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"),
    )


def get_logger() -> logging.Logger:
    """Returns a logging object"""
    log_object = logging.getLogger("user_data")
    log_object.setLevel(logging.INFO)
    log_object.propagate = False

    log_temp = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log_temp.setFormatter(formatter)
    log_object.addHandler(log_temp)

    return log_object


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field_value in fields:
        sms = re.sub(f"{field_value}=.*?{separator}",
                     f"{field_value}={redaction}{separator}", message)
    return sms


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
        """"""
        format_data = logging.Formatter(self.FORMAT)
        record = format_data.format(record)
        return filter_datum(self.fields, self.REDACTION,
                            str(record), self.SEPARATOR)

    def redact(self, message: str) -> str:
        """Redacts sensitive information from a message"""
        for value in self.fields:
            message = re.sub(f"{value}=[^;]",
                             f"{value}={self.REDACTION}", message)
        return message


def main():
    """main call function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, \
                    last_login, user_agent FROM users;")

    for record in cursor:
        print_d(record)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
