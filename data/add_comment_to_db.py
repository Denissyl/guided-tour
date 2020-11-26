import datetime
from data.comment_form import CommentForm
from data.comments import Comment


def add_comment_to_db(sight, nickname, email, session):
    form = CommentForm()
    if form.validate_on_submit():
        comment_to_db = Comment(
            description=form.description.data,
            sight=sight,
            nickname=nickname,
            email=email,
            mark=form.mark.data,
            datetime=str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=0))[:19]
        )
        session.add(comment_to_db)
        session.commit()
    return form
