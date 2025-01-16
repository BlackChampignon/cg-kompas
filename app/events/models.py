from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REGISTRATION_CHOICES = [
        ('email', 'Email and Password'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email',
        help_text='Specifies how the user registered.',
    )

    is_email_password_enabled = models.BooleanField(
        default=True,
        help_text="Indicates whether the user can log in using email and password.",
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='events_user_set',  # Avoids clash with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='events_user_permissions_set',  # Avoids clash with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    username = models.CharField(
        max_length=150,
        unique=False,
    )
    email = models.CharField(
        max_length=150,
        unique=True
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    region = models.CharField(max_length=100)
    precise_place = models.CharField(max_length=255)
    date = models.DateTimeField()
    repetition = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="events")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Many-to-Many relationship for likes
    liked_by = models.ManyToManyField('User', related_name='liked_events', blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.event.name}"
