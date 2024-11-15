class Comment:
    def __init__(self, post_id, score=0, text=""):
        """
        Иницијализује објекат коментара са основним атрибутима.

        :param post_id: ID објаве са којом је коментар повезан (int).
        :param score: Оцена корисности коментара (int, подразумевано 0).
        :param text: Текст коментара (string, подразумевано празан стринг).
        """
        self.post_id = post_id
        self.score = score
        self.text = text

    def __str__(self):
        """
        Враћа читљиву репрезентацију коментара.

        :return: Стринг који представља коментар.
        """
        return f"Comment(PostId={self.post_id}, Score={self.score}, Text={self.text})"
    
    def to_dict(self):
        """
        Претвара атрибуте објекта у речник.
        """
        return {
            "PostID": self.post_id,
            "Score": self.score,
            "Text": self.text,
        }
