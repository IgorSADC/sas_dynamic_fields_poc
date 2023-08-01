    
import typing
import strawberry


book = strawberry.type(
    type(
        'Book',
        (),
        {
            '__annotations__': {
                'title': 'str',
                'author': 'str'
            }
        }
                            
        ))

query = strawberry.type(
    type(
        'Query',
        (),
        {
            'books': strawberry.field(lambda : [book(title='oi', author='igor')]),
            '__annotations__': {
                'books' : typing.List[book]
            }
           
        }
    )
)

@strawberry.type
class Query:
    books: typing.List[book]
    
def get_books():
    return [
        book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
        book(
            title= 'Thing',
            author= 'Igor'
        )
    ]
    
@strawberry.type
class Query:
    books: typing.List[book] = strawberry.field(resolver=get_books)
    
    
print("creating schema")
schema = strawberry.Schema(query=Query)
print("schema created")