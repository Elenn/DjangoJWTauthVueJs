************************************************************************************************************************
                                                  Django
************************************************************************************************************************
1. Создаю папку DjangoJWTauthVueJs-MyTwo

C:\web\Django\DjangoJWTauthVueJs-My
--------------------------------------------
2. иду в папку, где я хочу создать проект
и создаю виртуальное окружение

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
python -m venv venv   
--------------------------------------
3. активирую виртуальное окружение
 
cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
.\venv\Scripts\activate  
---------------------------------------
4. Деактивирую виртуальное окружение 
deactivate  
---------------------------------------
5. Устанавливаю Django 

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
pip install Django 
---------------------------------------
6. Устанавливаю djangorestframework  

https://www.django-rest-framework.org/tutorial/quickstart/

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
pip install djangorestframework
--------------------------------------
7. Создаю проект auth

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
django-admin startproject auth
--------------------------------------
8. папку внутренную auth называют пакетом конфигурации
--------------------------------------
9. Запускаю сервер
- перехожу внутрь auth
cd auth

python manage.py runserver
--------------------------------------
10. Создаю внутри нашего auth новое апликейшен login
(то есть новую папку) - наш модуль

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
python manage.py startapp login 
--------------------------------------
11. Создаю внутри нашего auth новое апликейшен posts
(то есть новую папку) - наш модуль

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo
python manage.py startapp posts 
--------------------------------------
12. Зарегистрировать новое приложение в auth/settings.py

C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\settings.py

INSTALLED_APPS = [
     . . .
    'rest_framework',
    'login',
    'posts'
] 
-----------------------------------------
13. раню проект
python manage.py runserver
--------------------------------------------
14. Похоже, что я знаю, как сделать JWT authentication только с использованием
custome user
----------------------------------------------
15. удалила файл базы данных - пока этого не делаю
------------------------------------------------
16.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\login\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []	
 
----------------------------------------
17.
AUTH_USER_MODEL = "login.User" 

python manage.py makemigrations 
python manage.py migrate  
--------------------------------------------
18. раню миграцию

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth
python manage.py migrate 
--------------------------------------------
19. Создаю superuser

cd C:\web\Django\DjangoJWTauthVueJs-MyTwo

python manage.py createsuperuser

Username: xxx
Email: xxx
Password: xxx  
--------------------------------------------
20. Могу теперь залогинится

http://127.0.0.1:8000/admin/
---------------------------------------------
21. Создаю модель Post

C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\posts\models.py

from django.db import models 
 
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255) 
----------------------------------------------
22.  
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\posts\serializers.py

from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']  
--------------------------------------------
23.	
(venv) λ python manage.py makemigrations 
(venv) λ python manage.py migrate
--------------------------------------------
24. Чтобы увидить Post в админе добавляю

C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\posts\admin.py

from django.contrib import admin 
from .models import Post

admin.site.register(Post)
----------------------------------------
25. Добавляю Post через админ
----------------------------------------
26. 'corsheaders', 

python.exe -m pip install --upgrade pip
 
pip install django-cors-headers
pip install PyJWT==1.7.1

pip freeze > requirements.txt

asgiref==3.7.2
Django==5.0.1
django-cors-headers==4.3.1
djangorestframework==3.14.0
pytz==2023.3.post1
sqlparse==0.4.4
typing_extensions==4.9.0
tzdata==2023.4
----------------------------------------
27.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\auth\settings.py 

INSTALLED_APPS = [
    . . .
	'corsheaders',
    'rest_framework', 
    'users',
    'posts',
]
. . .
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
. . .

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'login.authentication.JWTAuthentication',
    ], 
}
. . .
CORS_ORIGIN_ALLOW_ALL = True  
--------------------------------------
28.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\users\authentication.py

import jwt 
from django.conf import settings 
from rest_framework import authentication, exceptions 
from .models import User 

class JWTAuthentication(authentication.BaseAuthentication): 

    def authenticate(self, request):
        
        request.user = None 
        
        auth_header = authentication.get_authorization_header(request).split() 

        if not auth_header:
            return None

        if len(auth_header) == 1: 
            return None

        elif len(auth_header) > 2: 
            return None
 
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8') 

        try:
            #payload = jwt.decode(token, settings.SECRET_KEY)
            payload = jwt.decode(token, 'secret', algorithm=['HS256']) 
            
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)  
--------------------------------------------
29. 
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\posts\urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowPostsViewSet 

router = DefaultRouter()
router.register(r'posts', ShowPostsViewSet, basename='post') 

urlpatterns = [
    path('', include(router.urls)), 
]
---------------------------------------------------
30.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\posts\views.py

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from .models import Post  

class ShowPostsViewSet(viewsets.ModelViewSet): 
    serializer_class = PostSerializer
    queryset = Post.objects.all()  
    permission_classes = [IsAuthenticated]	
---------------------------------------------------- 
31.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\login\views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
import jwt, datetime 


class RegisterView(APIView):
    def post(self, request):
        pass

class LoginView(APIView):
    def post(self, request):
        #email = request.data['email']
        password = request.data['password']
        username = request.data['username']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        #response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt') 

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data) 
--------------------------------------------------------------------
32.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\auth\urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('login.urls')),
    path('pages/', include('posts.urls')),
]
---------------------------------------------------------------------
33.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\users\urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserView, LogoutView, ShowUsersViewSet 

router = DefaultRouter()
router.register(r'users', ShowUsersViewSet, basename='user') 

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
]
----------------------------------------
34.
C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\login\serializers.py

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance	
------------------------------------------------------		
35. хеширование пароля

C:\web\Django\DjangoJWTauthVueJs-MyTwo\auth\login\serializers.py

- так как мы создали модель User, которая наследуется от AbstractUser
- мы используем set_password(password) для хеширования пароля  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        . . . 

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
		
- используем user.check_password(password)
для сравнения пароля из формы и пароля из базы данных	 
----------------------------------------
***********************************************************************************************************************
                                      VueJs
***********************************************************************************************************************
1. Создала папку jwt-auth-vuejs

C:\web\Django\DjangoJWTauthVueJs-MyTwo\jwt-auth-vuejs
----------------------------
2. Скопировала содержимое папки 
из 
C:\web\Django\DjangoJWTauthVueJs\auth-JWT-vue-my
в
C:\web\Django\DjangoJWTauthVueJs-MyTwo\jwt-auth-vuejs   
-----------------
3. login

C:\web\Django\DjangoJWTauthVueJs-MyTwo\jwt-auth-vuejs\src\pages\LoginView.vue

<script> 
import axios from 'axios';  
export default {
    name: "LoginView",
    data() {
        return {  
            inputUserName: '',
            inputPassword: '',
        }
    },
    methods: {
        login() {  
            axios.post('http://localhost:8000/api/login/', {
                username: this.inputUserName,
                password: this.inputPassword 
            })
                .then(response => {  
                    this.$store.dispatch('setAuth', true);
                    this.$store.dispatch('setToken', response.data.jwt);
                    console.log(response.data); 

                    this.$router.push('posts')   
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.$store.dispatch('setAuth', false);

                });
        }, 
    } 
 }
</script>
----------------------------------------
4. axios.get

C:\web\Django\DjangoJWTauthVueJs-MyTwo\jwt-auth-vuejs\src\pages\PostView.vue

 computed: {
        tokenStr() {
            return this.$store.state.token;
        },
    },
    methods: {
        showPosts() {
            this.errorMessage = ''
            axios.get('http://localhost:8000/pages/posts/', { headers: { "Authorization": `Bearer ${this.tokenStr}`}})
                .then(response => {
                    this.posts = response.data
                    console.log(response.data);
                })
                .catch(error => {
                    this.errorMessage = ''
                    if (error.message == 'Request failed with status code 403')
                        this.errorMessage = 'You do not have access to see this data. Please login.'
                    console.error('Error:', error);
                });
        }, 
        createPost() {
            this.errorMessage = ''
            axios.post('http://localhost:8000/pages/posts/', { title: 'aaa', content: 'bbb'}, { headers: { "Authorization": `Bearer ${this.tokenStr}` } })
                .then(response => {
                    this.posts = response.data
                    console.log(response.data);
                })
                .catch(error => {
                    this.errorMessage = ''
                    if (error.message == 'Request failed with status code 403')
                        this.errorMessage = 'You do not have access to see this data. Please login.'
                    console.error('Error:', error);
                });
        }, 
    }
------------------------------------------
5. logout()

C:\web\Django\DjangoJWTauthVueJs-MyTwo\jwt-auth-vuejs\src\components\topNav.vue

<script> 
export default {
    name: "topNav",
    computed: {
        auth() {
            return this.$store.state.authenticated;
        },
    },
    methods: {
        logout() { 
            this.$store.dispatch('setAuth', false);
            this.$store.dispatch('setToken', '');
            this.$router.push('login') 
        }
    }
}
</script>
-----------------------------------------------
6. Store

import { createStore } from 'vuex' 
const store = createStore({ 
    state: {
        authenticated: false,
        token: ''
    }, 
    getters: {},
    mutations: {
        SET_AUTH(state, payload) {
            state.authenticated = payload
        },
        set_token(state, payload) {
            state.token = payload
        }
    },
    actions: {
        setAuth(context, payload) {
            context.commit('SET_AUTH', payload)
        },
        setToken(context, payload) {
            context.commit('set_token', payload)
        } 
    }, 
})

export default store;
---------------------------------------------
7. TODO: Register 
**********************************************************************************************************************
                                           Выставляю на git
**********************************************************************************************************************
1. https://github.com/login

GitDjangoJWTauthVueJs 
-----------------------------------
2. https://github.com -> New
 
DjangoJWTauthVueJs 
-----------------------------------
3. Clone
 
Visual Studio  
-> Clone Repository ->

https://github.com/Elenn/DjangoJWTauthVueJs.git 
в папку C:\web\Django\GitDjangoJWTauthVueJs
---------------------------
4. Скопировала сначала requirements.txt
----------------------------------
5. требует пароль ->
login with brauser
---------------------------------
6. 	Cкопировала папку (без db.sqlite3, venv и node_modules)

с
C:\web\Django\DjangoJWTauthVueJs-MyTwo
в
C:\web\Django\GitDjangoJWTauthVueJs 
-----------------------------------
 

 

 







