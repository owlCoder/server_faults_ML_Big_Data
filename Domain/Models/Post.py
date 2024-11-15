from datetime import datetime

class Post:
    def __init__(
        self,
        id=None,
        post_type_id=None,
        accepted_answer_id=None,
        parent_id=None,
        creation_date=None,
        deletion_date=None,
        score=0,
        view_count=0,
        body="",
        owner_user_id=None,
        owner_display_name="",
        last_editor_user_id=None,
        last_editor_display_name="",
        last_edit_date=None,
        last_activity_date=None,
        title="",
        tags="",
        answer_count=0,
        comment_count=0,
        favorite_count=0,
        closed_date=None,
        community_owned_date=None,
        content_license="",
    ):
        """
        Initializes a post object with attributes matching the database schema.
        """
        self.id = id
        self.post_type_id = post_type_id
        self.accepted_answer_id = accepted_answer_id
        self.parent_id = parent_id
        self.creation_date = creation_date or datetime.now()
        self.deletion_date = deletion_date
        self.score = score
        self.view_count = view_count
        self.body = body
        self.owner_user_id = owner_user_id
        self.owner_display_name = owner_display_name
        self.last_editor_user_id = last_editor_user_id
        self.last_editor_display_name = last_editor_display_name
        self.last_edit_date = last_edit_date
        self.last_activity_date = last_activity_date
        self.title = title
        self.tags = tags
        self.answer_count = answer_count
        self.comment_count = comment_count
        self.favorite_count = favorite_count
        self.closed_date = closed_date
        self.community_owned_date = community_owned_date
        self.content_license = content_license

    def __str__(self):
        return (f"Post(Id={self.id}, PostTypeId={self.post_type_id}, AcceptedAnswerId={self.accepted_answer_id}, "
                f"ParentId={self.parent_id}, CreationDate={self.creation_date}, DeletionDate={self.deletion_date}, "
                f"Score={self.score}, ViewCount={self.view_count}, Body={self.body}, OwnerUserId={self.owner_user_id}, "
                f"OwnerDisplayName={self.owner_display_name}, LastEditorUserId={self.last_editor_user_id}, "
                f"LastEditorDisplayName={self.last_editor_display_name}, LastEditDate={self.last_edit_date}, "
                f"LastActivityDate={self.last_activity_date}, Title={self.title}, Tags={self.tags}, "
                f"AnswerCount={self.answer_count}, CommentCount={self.comment_count}, FavoriteCount={self.favorite_count}, "
                f"ClosedDate={self.closed_date}, CommunityOwnedDate={self.community_owned_date}, "
                f"ContentLicense={self.content_license})")

    def to_dict(self):
        """
        Converts the object's attributes to a dictionary.
        """
        def serialize_date(date):
            return date.isoformat() if isinstance(date, datetime) else date

        return {
            "Id": self.id,
            "PostTypeId": self.post_type_id,
            "AcceptedAnswerId": self.accepted_answer_id,
            "ParentId": self.parent_id,
            "CreationDate": serialize_date(self.creation_date),
            "DeletionDate": serialize_date(self.deletion_date),
            "Score": self.score,
            "ViewCount": self.view_count,
            "Body": self.body,
            "OwnerUserId": self.owner_user_id,
            "OwnerDisplayName": self.owner_display_name,
            "LastEditorUserId": self.last_editor_user_id,
            "LastEditorDisplayName": self.last_editor_display_name,
            "LastEditDate": serialize_date(self.last_edit_date),
            "LastActivityDate": serialize_date(self.last_activity_date),
            "Title": self.title,
            "Tags": self.tags,
            "AnswerCount": self.answer_count,
            "CommentCount": self.comment_count,
            "FavoriteCount": self.favorite_count,
            "ClosedDate": serialize_date(self.closed_date),
            "CommunityOwnedDate": serialize_date(self.community_owned_date),
            "ContentLicense": self.content_license,
        }
