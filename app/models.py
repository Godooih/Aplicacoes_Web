from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .user_maneger import CustonUserManager

CATEGORIES = [
    ('HORROR','Terror'),
    ('COMEDY', 'Comédia'),
    ('FICCTION', 'Ficção'),
    ('DOCUMENTARY', 'Documentário'),
    ('ACTION', 'Ação'),
]

class CustonUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cfp = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    #pode acessar tela de admin do django ou não
    is_staff =  models.BooleanField(default=False)
    #se o usuario está ativo ou não
    is_active = models.BooleanField(default=True)

    #login por email
    USERNAME_FIELD = "email"
    #O que é obrigatorio além do padrão( username, email, password)
    REQUIRED_FIELDS = ["cpf"]

    objects = CustonUserManager

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model): #para definir o que terá dentro da classe vai colocando dentro dela
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=100,choices=CATEGORIES)
    published_date = models.DateField()
    photo = models.TextField()
    classification = models.IntegerField()
    directors = models.ManyToManyField(Director, null=False) #ManytoMany filds está falando que pode ter varios diretores porém tem que linkar a tabela

    def __str__(self):
        return self.title

class Plan(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    
    def __str__(self):
        return self.name

class UserPlan(models.Model):
    plan_FK = models.ForeignKey(Plan, related_name='UserPlan_plan_FK', on_delete=models.CASCADE)#ForeingKey está falando que pode ter somente um Plano porém tem que linkar a tabela
    user_FK = models.ForeignKey(User, related_name='UserPlan_user_FK', on_delete=models.CASCADE)
    #ForeingKey está falando que pode ter somente um usuario porém tem que linkar a tabela
    #on_delete está expecificando oq vai acontecer se o plano for deletado, CASCADE = 
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_FK.username}-{self.plan_FK.name}'                

class FavoriteMovie(models.Model):
    movie_FK = models.ForeignKey(Movie, related_name='FavoriteMovie_movie_FK', on_delete=models.CASCADE)
    user_FK = models.ForeignKey(User, related_name='FavoriteMovie_user_FK', on_delete=models.CASCADE)
   
    def __str__(self):
        return f'{self.user_FK.username}-{self.movie_FK.title}'