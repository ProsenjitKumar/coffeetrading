from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.utils.translation import gettext as _
from django.templatetags.static import static
# from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.


# ----------------------------
#
#          Networker
#
# ----------------------------
class Networker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        qs = Networker.objects.all()
        # my_recs = [p for p in qs if p.recommended_by==self.user]
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)

        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


# ----------------------------
#
#          Profile
#
# ----------------------------
class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')

    def __str__(self):
        return self.user.username


# ----------------------------
#
#          Deposit Payment Method
#
# ----------------------------


class DepositPaymentMethod(models.Model):
    currency_name = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="currency/logo/", null=True, blank=True)
    currency_address = models.CharField(max_length=455, null=True, blank=True)
    qr_code_image = models.ImageField(upload_to="currency/qrcode/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.currency_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.currency_name


CURRENCY_SELECTED = (
    ('1', 'Bitcoin'),
    ('2', 'Litecoin'),
    ('3', 'Ethereum'),
)


class DepositConfirmation(models.Model):
    investor_user_name = models.ForeignKey(User, related_name="deposit_confirmation", on_delete=models.CASCADE)
    amount_deposited = models.FloatField()
    currency_selected = models.CharField(max_length=25, choices=CURRENCY_SELECTED, null=True, blank=True)
    transaction_id = models.CharField(max_length=450, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.investor_user_name.username}-{self.amount_deposited}"


class WithdrawalRequest(models.Model):
    investor_user_name = models.ForeignKey(User, related_name="withdrawal_request", on_delete=models.CASCADE)
    amount = models.FloatField()
    currency_selected = models.CharField(max_length=25, choices=CURRENCY_SELECTED, null=True, blank=True)
    currency_address = models.CharField(max_length=455, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.investor_user_name.username}-{self.amount}"







