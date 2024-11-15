from datetime import datetime

class Post:
    def __init__(self, post_type_id, creation_date=None, score=0, view_count=0, body="", accepted_answer_id=None):
        """
        Иницијализује објекат објаве са основним атрибутима.

        :param post_type_id: Тип објаве (нпр. "питање", "општа дискусија") (string).
        :param creation_date: Датум и време креирања објаве (datetime, подразумевано тренутни датум и време).
        :param score: Оцена корисности објаве (int, подразумевано 0).
        :param view_count: Број прегледа објаве (int, подразумевано 0).
        :param body: Опис проблема или садржај објаве (string, подразумевано празан стринг).
        :param accepted_answer_id: ID коментара који је означен као тачан одговор (int, подразумевано None).
        """
        self.post_type_id = post_type_id
        self.creation_date = creation_date or datetime.now()
        self.score = score
        self.view_count = view_count
        self.body = body
        self.accepted_answer_id = accepted_answer_id

    def __str__(self):
        """
        Враћа читљиву репрезентацију објаве.

        :return: Стринг који представља објаву.
        """
        return (f"Post(PostTypeId={self.post_type_id}, CreationDate={self.creation_date}, "
                f"Score={self.score}, ViewCount={self.view_count}, Body={self.body}, "
                f"AcceptedAnswerId={self.accepted_answer_id})")
        
    def to_dict(self):
        """
        Конвертује атрибуте објекта у речник.

        :return: Речник који представља објекат објаве.
        """
        return {
            "PostTypeId": self.post_type_id,
            "CreationDate": self.creation_date.isoformat() if isinstance(self.creation_date, datetime) else self.creation_date,
            "Score": self.score,
            "ViewCount": self.view_count,
            "Body": self.body,
            "AcceptedAnswerId": self.accepted_answer_id
        }