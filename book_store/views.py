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
    return HttpResponse('Customer main page')


def employee_main_page(request):
    return HttpResponse('Employee main page')
