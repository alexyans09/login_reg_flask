from flask_app.config.mysqlconnection import connectToMySQL


class Record:
    """The record class"""

    DB = "vinyl_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.artist = data["artist"]
        self.genre = data["genre"]
        self.release_date = data["release_date"]
        self.comments = data["comments"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def find_all(cls):
        """This method finds all the records in the database"""
        query = (
            """SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id"""
        )
        results = connectToMySQL(Record.DB).query_db(query)
        record = []
        for each_results in results:
            record = Record(each_results)
            record.append(record)
            return record
