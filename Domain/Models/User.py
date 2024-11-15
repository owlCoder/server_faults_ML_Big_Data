from datetime import datetime

class User:
    def __init__(self, reputation=0, creation_date=None, display_name="", last_access_date=None, 
                 website_url="", location="", about_me=""):
        """
        Иницијализација атрибута корисника.
        :param reputation: Кредибилитет корисника (int).
        :param creation_date: Датум креирања налога (datetime).
        :param display_name: Име и презиме корисника (str).
        :param last_access_date: Датум и време последњег приступа (datetime).
        :param website_url: Веб страница корисника (str).
        :param location: Место становања корисника (str).
        :param about_me: Биографски подаци о кориснику (str).
        """
        self.reputation = reputation
        self.creation_date = creation_date or datetime.now()
        self.display_name = display_name
        self.last_access_date = last_access_date or datetime.now()
        self.website_url = website_url
        self.location = location
        self.about_me = about_me

    def __str__(self):
        """
        Представљање објекта као стринг.
        """
        return (f"User(DisplayName: {self.display_name}, Reputation: {self.reputation}, "
                f"Location: {self.location}, Website: {self.website_url})")

    def to_dict(self):
        """
        Претвара атрибуте објекта у речник.
        """
        return {
            "Reputation": self.reputation,
            "CreationDate": self.creation_date,
            "DisplayName": self.display_name,
            "LastAccessDate": self.last_access_date,
            "WebsiteUrl": self.website_url,
            "Location": self.location,
            "AboutMe": self.about_me,
        }
