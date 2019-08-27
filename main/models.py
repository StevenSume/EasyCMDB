from .app import db
class Project(db.Model):
    __tablename__ =  'projects'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    project_name = db.Column(db.String(64),unique=True,index=True)

    def to_dict(self):
        mydict = {
            'id': self.id,
            'project_name': self.project_name

        }
        return mydict

    def __repr__(self):
        return '<Project %r>' % self.__name__

class Item(db.Model):
    __tablename__ = 'Items'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    project_id = db.Column(db.Integer)
    key = db.Column(db.String(64),nullable=False)
    value = db.Column(db.String(64),nullable=False)

    def to_dict(self):
        mydict = {
            'id': self.id,
            'project_id': self.project_id,
            'key': self.key,
            'value': self.value
        }
        return mydict
    def __repr__(self):
        return '<Item %r>' % self.__name__

