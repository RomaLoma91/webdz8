from datetime import datetime
from mongoengine import Document
from mongoengine import ReferenceField, DateTimeField, ListField, StringField, CASCADE

class Author(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

    def formatted_born_date(self):
        return self.born_date.strftime("%B %d, %Y")

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()

# if __name__ == '__main__':
#     author = Author(
#         fullname='Roman Lomachinskiy',
#         born_date=datetime(1980, 3, 14).strftime("%B %d, %Y"),
#         born_location='Ukraine, Kyiv',
#         description='Help'
#     )
#     print(author.born_date)