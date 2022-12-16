from django import forms
import psycopg2

from . import db_config


try:
    connection = psycopg2.connect(
        host=db_config.HOST,
        user=db_config.USER,
        password=db_config.PASSWORD,
        database=db_config.DB_NAME
    )
    connection.autocommit = True
except:
    print('Error while working with DB(')

with connection.cursor() as cursor:
    all_cols = []
    cursor.execute('''SELECT column_name
                      FROM information_schema.columns
                      WHERE table_name = 'users';''')
    for i in cursor.fetchall():
        all_cols.append(i[0])


with connection.cursor() as cursor:
    cursor.execute('''SELECT table_name
  FROM information_schema.tables
 WHERE table_schema='public'
   AND table_type='BASE TABLE';''')
    all_tables = []

    for i in cursor.fetchall():
        print('FETCHALL: ', cursor.fetchall())
        print('I', i)
        all_tables.append(i[0])


'''choices = (
    ('users', 'users'),
)'''


class AddBookForm(forms.Form):
    choices = (
        [(i, i) for i in all_tables]
    )
    first_name = forms.CharField(max_length=100)
    nick_name = forms.CharField(max_length=100, required=False)
    table = forms.ChoiceField(choices=choices, )


class SortBooksForm(forms.Form):
    choices = (
        [(i, i) for i in all_cols]
    )
    first_name = forms.CharField(max_length=100, required=False)
    nick_name = forms.CharField(max_length=100, required=False)
    order_by_column = forms.ChoiceField(choices=choices, )
    DESC = forms.BooleanField(required=False)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)

