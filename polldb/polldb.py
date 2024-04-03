from enum import Enum
import os
import mariadb

config = {
    'host': os.environ.get('NEXTCLOUD_DB_HOST', ''),
    'user': os.environ.get('NEXTCLOUD_DB_USER', ''),
    'pass': os.environ.get('NEXTCLOUD_DB_PASS', ''),
    'port': os.environ.get('NEXTCLOUD_DB_PORT', 3306),
    'db': os.environ.get('NEXTCLOUD_DB', ''),
}


class Answer(Enum):
    YES = 'yes'
    NO = 'no'


class PollDB:

    def __init__(self):
        self.conn = mariadb.connect(
            user=config['user'],
            password=config['pass'],
            host=config['host'],
            port=config['port'],
            database=config['db'],
        )

    def vote_set_answer(self, vote_id: int, vote_answer: Answer):
        cur = self.conn.cursor()

        cur.execute("UPDATE oc_polls_votes SET vote_answer = ? WHERE id = ?", (vote_answer.value, vote_id))
        self.conn.commit()
