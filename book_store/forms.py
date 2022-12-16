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
    with connection.cursor() as cursor:
        cursor.execute('SELECT org_name FROM publishers')
        choices_publisher = []
        for i in cursor.fetchall():
            choices_publisher.append([i[0], i[0]])

        cursor.execute('SELECT org_name FROM suppliers')
        choices_supplier = []
        for i in cursor.fetchall():
            choices_supplier.append([i[0], i[0]])

    title = forms.CharField(max_length=100)
    price = forms.FloatField()
    production_date = forms.CharField(max_length=10)    # yyyy-mm-dd
    publisher = forms.ChoiceField(choices=choices_publisher)
    supplier = forms.ChoiceField(choices=choices_supplier)


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

