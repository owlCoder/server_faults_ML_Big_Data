from datetime import datetime

class User:
    def __init__(
        self,
        id=None,
        reputation=0,
        creation_date=None,
        display_name="",
        last_access_date=None,
        website_url="",
        location="",
        about_me="",
        views=0,
        up_votes=0,
        down_votes=0,
        profile_image_url="",
        email_hash="",
        account_id=None
    ):
        """
        Initializes a user object with attributes matching the database schema.
        """
        self.id = id
        self.reputation = reputation
        self.creation_date = creation_date or datetime.now()
        self.display_name = display_name
        self.last_access_date = last_access_date or datetime.now()
        self.website_url = website_url
        self.location = location
        self.about_me = about_me
        self.views = views
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.profile_image_url = profile_image_url
        self.email_hash = email_hash
        self.account_id = account_id

    def __str__(self):
        return (f"User(Id: {self.id}, DisplayName: {self.display_name}, Reputation: {self.reputation}, "
                f"Location: {self.location}, Views: {self.views}, UpVotes: {self.up_votes}, "
                f"DownVotes: {self.down_votes}, Website: {self.website_url})")

    def to_dict(self):
        """
        Converts the object's attributes to a dictionary.
        """
        def serialize_date(date):
            return date.isoformat() if isinstance(date, datetime) else date

        return {
            "Id": self.id,
            "Reputation": self.reputation,
            "CreationDate": serialize_date(self.creation_date),
            "DisplayName": self.display_name,
            "LastAccessDate": serialize_date(self.last_access_date),
            "WebsiteUrl": self.website_url,
            "Location": self.location,
            "AboutMe": self.about_me,
            "Views": self.views,
            "UpVotes": self.up_votes,
            "DownVotes": self.down_votes,
            "ProfileImageUrl": self.profile_image_url,
            "EmailHash": self.email_hash,
            "AccountId": self.account_id,
        }
