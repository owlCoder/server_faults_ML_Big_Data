from datetime import datetime

class Comment:
    def __init__(
        self,
        id=None,
        post_id=None,
        score=0,
        text="",
        creation_date=None,
        user_display_name="",
        user_id=None,
        content_license=""
    ):
        """
        Initializes a comment object with attributes matching the database schema.
        """
        self.id = id
        self.post_id = post_id
        self.score = score
        self.text = text
        self.creation_date = creation_date or datetime.now()
        self.user_display_name = user_display_name
        self.user_id = user_id
        self.content_license = content_license

    def __str__(self):
        return (f"Comment(Id={self.id}, PostId={self.post_id}, Score={self.score}, Text={self.text}, "
                f"CreationDate={self.creation_date}, UserDisplayName={self.user_display_name}, "
                f"UserId={self.user_id}, ContentLicense={self.content_license})")

    def to_dict(self):
        """
        Converts the object's attributes to a dictionary.
        """
        def serialize_date(date):
            return date.isoformat() if isinstance(date, datetime) else date

        return {
            "Id": self.id,
            "PostId": self.post_id,
            "Score": self.score,
            "Text": self.text,
            "CreationDate": serialize_date(self.creation_date),
            "UserDisplayName": self.user_display_name,
            "UserId": self.user_id,
            "ContentLicense": self.content_license,
        }
