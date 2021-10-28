import dataclasses
import sqlite3
import os

from contextlib import closing

DB_PATH = "./db.sqlite3"


@dataclasses.dataclass
class PhoneBookEntry:
    id: int
    nickname: str
    phone_number: str


class DB:
    def __init__(self, custom_path=None) -> None:
        self.db_path = custom_path if custom_path else DB_PATH
        need_init = False
        if not os.path.exists(self.db_path):
            need_init = True
            print('INIT')
        # FIXME : Use a good thread strategy instead of bypassing
        self.db = sqlite3.connect(self.db_path, check_same_thread=False)
        if need_init:
            self.init_db()

    def init_db(self) -> None:
        with open("sql/init.sql") as f:
            with closing(self.db.cursor()) as cursor:
                cursor.executescript(f.read())

    def commit_and_close(self):
        self.db.commit()
        self.db.close()

    def add_entry(self, phone_number: str, nickname: str) -> PhoneBookEntry:
        with closing(self.db.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO phonebook (nickname, phone_number) VALUES (?, ?)",
                (nickname, phone_number),
            )
            return PhoneBookEntry(cursor.lastrowid, nickname, phone_number)

    def get_entries(self) -> list[PhoneBookEntry]:
        with closing(self.db.cursor()) as cursor:
            cursor.execute(
                "SELECT * FROM phonebook",
            )
            tuples = cursor.fetchall()
            return [PhoneBookEntry(*tuple) for tuple in tuples]

    def delete_entry(self, id: int) -> int:
        with closing(self.db.cursor()) as cursor:
            cursor.execute("DELETE FROM phonebook WHERE id = ?", (id,))
            return cursor.rowcount

    def update_entry(self, id: int, phone_number: str, nickname: str) -> int:
        with closing(self.db.cursor()) as cursor:
            cursor.execute(
                "UPDATE phonebook SET phone_number = ?, nickname = ? WHERE id = ?",
                (phone_number, nickname, id),
            )
            return PhoneBookEntry(id, nickname, phone_number)
