import psycopg2
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from book_store import db_config
from . import forms

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


def index(request):
    with connection.cursor() as cursor:
        SQL_query = f'''SELECT * FROM books'''
        cursor.execute("select * from users")

    return HttpResponse('Main page')


def login(request):
    form = forms.LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        with connection.cursor() as cursor:
            SQL_query = f'''SELECT email FROM users'''
            cursor.execute(SQL_query)
            all_user_ids = []

            for raw_tp in cursor.fetchall():
                all_user_ids.append(raw_tp[0])

            print('ALL_USER_IDS', all_user_ids)

            if email in all_user_ids:
                cursor.execute(f'SELECT user_id FROM users WHERE email=\'{email}\'')
                id_of_current_user = cursor.fetchone()[0]
                cursor.execute('SELECT user_id FROM employees')
                all_user_ids_employees =[i[0] for i in cursor.fetchall()]

                if id_of_current_user in all_user_ids_employees:
                    return HttpResponseRedirect('employee_main_page')
                else:
                    return HttpResponseRedirect('customer_main_page')
            else:
                return HttpResponseRedirect('.')

    context = {
        'form': form,
    }

    return render(request, 'book_store/login.html', context=context)


def customer_main_page(request):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT title, price, production_date, org_name FROM books
                            JOIN publishers USING(publisher_id)''')
        all_rows = cursor.fetchall()
        for i in range(len(all_rows)):
            all_rows[i] = list(all_rows[i])
        for i in range(len(all_rows)):
            all_rows[i][1] = float(all_rows[i][1])
        print('ALL ROWS: ', all_rows)

    context = {
        'all_books': all_rows
    }
    return render(request, 'book_store/customer_main_page.html', context)


def employee_main_page(request):
        return render(request, 'book_store/employee_main_page.html')


def add_book(request):
    form = forms.AddBookForm(request.POST or None)
    all_columns = []
    context = {
        'form': form
    }
    with connection.cursor() as cursor:
        cursor.execute('''SELECT column_name
                                  FROM information_schema.columns
                                  WHERE table_name = 'books';''')
        for i in cursor.fetchall():
            all_columns.append(i[0])
    print('CHOICES PUBLISHERS: ', forms.AddBookForm.choices_publisher)

    if form.is_valid():
        data = (
            form.cleaned_data['title'],
            form.cleaned_data['price'],
            form.cleaned_data['production_date'],
        )
        with connection.cursor() as cursor:
            cursor.execute(f'''SELECT publisher_id FROM publishers
                                WHERE org_name=\'{form.cleaned_data['publisher']}\'''')
            publisher_id = cursor.fetchone()
            print(f'PUBLISHER_ID: {publisher_id}')

            cursor.execute(f'''SELECT supplier_id FROM suppliers
                                            WHERE org_name=\'{form.cleaned_data['supplier']}\'''')
            supplier_id = cursor.fetchone()
            print(f'SUPPLIER_ID: {supplier_id}')

            data += publisher_id[0], supplier_id[0]
            print('DATA: ', data)

        with connection.cursor() as cursor:
            SQL_query = f'INSERT INTO books(title, price, production_date, publisher_id, supplier_id) VALUES ' + f'\n{data}'
            print(SQL_query)
            cursor.execute(SQL_query)

        return HttpResponseRedirect('.')    # это чтобы после обновления страницы или отправки формы, данные
                                            # полей формы очищались
    return render(request, 'book_store/add_book.html', context)


def all_books_employee(request):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM books''')
        all_rows = cursor.fetchall()
        for i in range(len(all_rows)):
            all_rows[i] = list(all_rows[i])
        for i in range(len(all_rows)):
            all_rows[i][3] = float(all_rows[i][3])
        print('ALL ROWS: ', all_rows)
        cursor.execute('SELECT book_id FROM books')
        book_ids = [i[0] for i in cursor.fetchall()]
        print('BOOK_IDS', book_ids)

    context = {
        'all_books': zip(all_rows, book_ids),
    }
    return render(request, 'book_store/all_books_employee.html', context)


def delete_book(request, book_id):
    with connection.cursor() as cursor:
        SQL_query = f'''DELETE FROM books
                        WHERE book_id={book_id}'''
        cursor.execute(SQL_query)
    return HttpResponseRedirect('/all_books_employee/')
