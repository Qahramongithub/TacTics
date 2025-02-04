from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, ImageField, ManyToManyField, DateTimeField, \
    PositiveSmallIntegerField, DecimalField, TextField, ForeignKey, CASCADE, FileField, BooleanField,TextChoices
from django.db.models import Model


# Create your models here.
class CustomUser(UserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone number must be set")
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        phone_number = GlobalUserModel.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class Position(Model):
    title = CharField(max_length=255)


class User(AbstractUser):
    phone_number = CharField(max_length=9, unique=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    position = ManyToManyField('apps.Position', related_name='users')
    image = ImageField(upload_to="user/%y/%m/%d/", null=True, blank=True)
    USERNAME_FIELD = "phone_number"
    birthday_data = DateTimeField(null=True, blank=True)
    username = None
    objects = CustomUser()


class Trainer(User):
    experience = PositiveSmallIntegerField()
    price = DecimalField(max_digits=9, decimal_places=2)
    description = TextField(null=True, blank=True)
    online = BooleanField(default=False)


class City(Model):
    name = CharField(max_length=255)


class Club(Model):
    name = CharField(max_length=255)
    country = PositiveSmallIntegerField()


class Comment(Model):
    trainer = ForeignKey('apps.Trainer', on_delete=CASCADE)
    student = ForeignKey('apps.Student', on_delete=CASCADE)
    description = TextField(null=True, blank=True)
    video = FileField(upload_to="comment/%Y/%m/%d/", null=True, blank=True)


class Student(User):
    trainer = ManyToManyField('apps.Trainer', related_name='students')
    city = ForeignKey('apps.City', on_delete=CASCADE, related_name='profiles')
    club = ForeignKey('apps.Club', on_delete=CASCADE, related_name='profiles')


class Lesson(Model):
    class VideoRole(TextChoices):
        VIDEO_SOROV = 'video sorov', 'Video Sorov'
        SAVOL_JAVOB = 'savol javob', 'Savol Javob'
        INDIVIDUAL_TAKTIKA = 'individual taktika', 'Individual Taktika'
    trainer = ForeignKey('apps.Trainer', on_delete=CASCADE, related_name='lessons')
    video = FileField(upload_to="video/%y/%m/%d/", null=True, blank=True)
    title = CharField(max_length=255)
    represenative = CharField(max_length=255, null=True, blank=True)
    student = ForeignKey('apps.Student', on_delete=CASCADE, related_name='lessons')
    role = CharField(max_length=255, choices=VideoRole.choices)  # noqa
