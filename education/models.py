from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Users(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'Oddiy foydalanuvchi'),
        ('teacher', 'O\'qituvchi'),
        ('parent', 'Ota-Ona'),
    )
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='F.I.Sh')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='Telefon raqam')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram ID")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user', null=True, blank=True,
                            verbose_name='Foydalanuvchi roli')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'
        db_table = 'users'

    def __str__(self):
        return self.full_name


class TeacherProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name='Foydalanuvchi', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ism')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Familiya')
    birth_year = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(1970),
        MaxValueValidator(2010)
    ], verbose_name="Tug'ilgan yili")
    experience = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(30)
    ], verbose_name="Ish tajribasi")

    # other fields

    class Meta:
        db_table = 'teacher_profile'
        verbose_name = "Teacher"
        verbose_name_plural = "O'qituvchilar"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Group(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nomi')
    teacher = models.ForeignKey(TeacherProfile, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="O'qituvchi")

    # other fields

    class Meta:
        db_table = 'groups'
        verbose_name = "Group"
        verbose_name_plural = "Guruhlar"

    def __str__(self):
        return self.name


class ParentProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name='Foydalanuvchi', null=True, blank=True)
    child_first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Farzand ismi')
    child_last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Farzand familiyasi')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, verbose_name="Guruhi", null=True, blank=True)

    # other fields

    class Meta:
        db_table = 'parent_profile'
        verbose_name = "Parent"
        verbose_name_plural = "Ota-Onalar"

    def __str__(self):
        return f"{self.child_first_name} {self.child_last_name}"


class DailyMark(models.Model):
    student = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, verbose_name="O'quvchi")
    kategory1 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 1'
    )
    kategory2 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 2'
    )
    kategory3 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 3'
    )
    kategory4 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 4'
    )
    kategory5 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 5'
    )
    kategory6 = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        verbose_name='Kategory 6'
    )

    # other categories
    description = models.TextField(null=True, blank=True, verbose_name='Izoh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Time")

    class Meta:
        db_table = 'daily_mark'
        verbose_name = "Daily Mark"
        verbose_name_plural = "Kunlik baholar"

    def __str__(self):
        return f"{self.student} time: {self.created_at}"
