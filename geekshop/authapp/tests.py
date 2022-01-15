from django.conf import settings
from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from authapp.models import User

#TestCase
class UserManagementTestCase(TestCase):
    username = 'django'
    email = 'djano@mail.ru'
    password = 'geekshop'

    new_user_data = {
        'username':'django1',
        'first_name':'Django1',
        'last_name':'Django2',
        'password1': 'Isponec_2',
        'password2': 'ISponec_2',
        'email': 'geekshop@mail.ru',
        'age':31

    }
    # Описали 1 пункт из 3х  предустановпрека параметров
    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    #Описываем 2тий пункт
    # 1 test авторизация
    # 1.Нужно првоерить что пользователь не авторизован
    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        #Проверяем что пользователь не авторизованный и является анонимным
        self.assertTrue(response.context['user'].is_anonymous)
        #пробуем авторизоваться
        self.client.login(username=self.username,password=self.password)
        #отправляем на авторизацию
        response =self.client.get('/users/login/')
        #Проверяем что вы авторизовались
        self.assertEqual(response.status_code, 302)

        # нужно допилить код для редиректа
        # def get(self, request, *args, **kwargs):
        #     get = super(LoginListView, self).get(request, *args, **kwargs)
        #     if request.user.is_authenticated:
        #         return HttpResponseRedirect(reverse_lazy(self.success_url))
        #     return get
        # self.assertEqual(response.status_code, 302)

    # 2.Делае регистрацию протестриуем
    def test_register(self):
        # new_user_data = {
        #     'username': 'django1',
        #     'first_name': 'Django',
        #     'last_name': 'Django',
        #     'password1': 'geekshop',
        #     'password2': 'geekshop',
        #     'email': 'geekshop@mail.ru',
        #
        # }
        #начинаем регистрироваться
        response  = self.client.post('/users/register/',data=self.new_user_data)
        #должен быть редирект
        print(response.status_code)

        # print(response.)
        self.assertEqual(response.status_code,302)
        #Вспомним логику у нас есть пользователь не активированные
        # его нужно активировать с помошью ссылки которая отправляется на емайл
        # что нам нужно сделать? давайте ее соберем сами

        #Получаем пользователя
        new_user = User.objects.get(username=self.new_user_data['username'])

        #готовим ссылку
        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)


        #обновляем пользователя в базе данных
        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    #Описываем 3тий пункт
    def tearDown(self):
        # определяется для очистки после
        # работы теста исполяется после setUP
        # (базу удалять не нужно она автоматом удалится)
        # но данные чистим допустим когда мы выкачивали
        # аватар на первом уроке ее можно почистить
        # но очень редко сам использую и коллеги тоже
        pass
