from django.contrib.auth.models import BaseUserManager

class CustonUserManager(BaseUserManager):
    def create_user(self, email, password=None, cpf=None, **extra_field):
        #se faltar algum campo, gera um erro
        if None in(email,password,cpf):
            raise ValueError("Campo email, senha ou de CPF não foi informado.")
        
        email_ok = self.normalize_email(email)

        extra_field.setdefault("is_active", True)
        #prepara para salvar no banco (construção do objeto)
        user = self.model(email=email_ok, cpf=cpf, **extra_field)
        #seta a senha e criptografa
        user.set_password(password)
        #salva no banco de dados
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, cpf=None, **extra_field):
        return self.create_user(email,password,cpf,**extra_field)