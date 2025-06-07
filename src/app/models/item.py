from app import db
import datetime

class Item(db.Model):
    __tablename__ = 'item'
    
    id = db.Column(db.Integer, primary_key=True)
    item_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    item_encontrado_time = db.Column(db.Time, nullable=False)
    funcionario = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(200), nullable=False)
    item_description = db.Column(db.Text, nullable=False)
    imagem_path = db.Column(db.String(300), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Item {self.id} - {self.item_description}>'