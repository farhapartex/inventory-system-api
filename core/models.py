from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Permission, _user_has_module_perms, _user_has_perm
from django.utils.translation import gettext_lazy as _
from inventory.models import BaseEntity, BaseAbstractEntity
from core.enums import RoleEnum, AccessLabelEnum


class BaseUser(BaseEntity):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=150, unique=True,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator],
                                error_messages={'unique': _("A user with that username already exists."),},
                                )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    role = models.CharField(max_length=10, choices=RoleEnum.choices, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    models.EmailField()

    class Meta:
        abstract = True


class User(BaseUser, AbstractBaseUser):
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )
    is_superuser = models.BooleanField(default=False)
    access_label = models.CharField(max_length=100, choices=AccessLabelEnum.choices, default=AccessLabelEnum.READ)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class UserAuthCode(BaseAbstractEntity):
    user = models.ForeignKey(User, related_name='users', on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} code is {self.code}"

