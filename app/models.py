from app import db
from typing import List
from sqlalchemy.dialects.postgresql import insert


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False, unique=True)
    questions = db.relationship("Questions", backref="quest", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.category_name)

    @staticmethod
    def add(category_name: str) -> None:
        category = Categories(category_name=category_name)
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def get_categories() -> List[list]:
        categories = db.session.query(Categories).all()
        return [[item.category_id, item.category_name] for item in
                categories]

    @staticmethod
    def delete_note(category_id: int) -> None:
        delete = db.session.query(Categories).filter_by \
            (category_id=category_id).one()
        db.session.delete(delete)
        db.session.commit()

    def to_json(self):
        json_category = {"Category_id": self.category_id,
                         "Category_name": self.category_name}
        return json_category

    @staticmethod
    def check_exist_category(category_name: str) -> bool:
        categories = db.session.query(Categories).all()
        categories_names = [item.category_name for item in categories]
        if category_name in categories_names:
            return True
        return False

    @staticmethod
    def edit(category_name: str, id: int) -> bool:
        if category_name in [item.category_name for item in
                             db.session.query(Categories).all()]:
            check_id = Categories.query.filter_by(category_name=category_name).first()
            if check_id.category_id == id:
                return False
            return True
        insert_stmt = insert(Categories).values(
            category_id=id,
            category_name=category_name)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint='category_name',
            set_=dict(category_name='updated value'))
        db.session.execute(do_update_stmt)
        db.session.commit()
        return False




class Questions(db.Model):
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'))
    question = db.Column(db.String(140), nullable=False, unique=True)
    question_id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship("Answers", backref="questions", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.question)

    def __eq__(self, other):
        return self.question == other.question and self.category_id == \
               other.category_id and self.question_id == other.question_id


class Answers(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer = db.Column(db.String, nullable=False)
    answer_id = db.Column(db.Integer, primary_key=True)
    right_answer = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return '{}'.format(self.answer)

    def __eq__(self, other):
        return self.answer == other.answer and self.answer_id == \
               other.answer_id and self.question_id == other.question_id and \
               self.right_answer == other.right_answer
