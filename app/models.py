from app import db
from sqlalchemy.orm import validates 


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    born = db.Column(db.Date())
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone_number = db.Column(db.Integer(), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    position = db.Column(db.Enum('szef', 'pracownik', name='positions', default='pracownik'))
    tasks = db.relationship('Task', backref='em')
    news = db.relationship('News', backref='au')

    

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'born': self.born,
            'email': self.email,
            'position': self.position,
            'phone_number': self.phone_number,
            'password': self.password
        }
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()



class Horse(db.Model):
    __tablename__ = 'horse'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    father = db.Column(db.String(128), nullable=False)
    mother = db.Column(db.String(128), nullable=False)
    born = db.Column(db.Date)
    horse_coat = db.Column(db.String(64), nullable=False)
    owner = db.Column(db.String(128), nullable=False)
    image_name = db.Column(db.String(64))
    description = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'father': self.father,
            'mother': self.mother,
            'born': self.born,
            'owner': self.owner,
            'horse_coat': self.horse_coat,
            'image_name': self.image_name,
            'description': self.description
        }


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer(), primary_key=True)
    employee = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date())
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('w realizacji', 'nowe', 'odrzucone', 'zakończone', 'zaakceptowane', name='task_statuses', default='nowe'))

    def serialize(self):
        return {
            'id': self.id,
            'employee': self.employee,
            'title': self.title,
            'date': self.date,
            'description': self.description,
            'status': self.status,
        }


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text())
    author = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'description': self.description,
            'author': self.author,
        }

class EmployeesNews(db.Model):
    __tablename__ = 'employees_news'

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    title = db.Column(db.String(512), nullable=False)
    description = db.Column(db.Text())
    author = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'description': self.description,
            'author': self.author,
        }

