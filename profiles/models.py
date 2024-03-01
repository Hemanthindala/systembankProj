from django.db import models
import datetime


from django.contrib.auth.models import User

# Specify unique related_names for groups and user_permissions
class BasicDetails(models.Model):
    # (Name, Sex, DOB, Annual income, Email, Mobile number, Occupation)
    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basic_details')
    sex = models.CharField(max_length=1, default=None)
    annual_income = models.IntegerField(default=0)
    email = models.EmailField(default=None)
    mobile = models.IntegerField(default=0)
    occupation = models.CharField(max_length=50, default=None)
    DOB = models.DateField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

class PresentLocation(models.Model):
    # (Country, State, City, Street, Pincode)
    country = models.CharField(max_length=50, default="India")
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    pincode = models.IntegerField()
    user_name = models.CharField(max_length=150, default=None)

class Status(models.Model):
    account_number = models.IntegerField()
    balance = models.IntegerField()
    user_name = models.CharField(max_length=150, default=None)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    from_account_number = models.IntegerField()
    to_account_number = models.IntegerField()
    amount_transferred = models.DecimalField(max_digits=10, decimal_places=2)
    date_and_time = models.DateTimeField(default=datetime.datetime.now)
    def save(self, *args, **kwargs):
        # Override the save method to generate an ID before saving
        if not self.id:
            # If ID is not set, generate a new one
            last_trans = Transaction.objects.order_by('-id').first()
            new_id = 1 if not last_trans else last_trans.id + 1
            self.id = new_id
        super().save(*args, **kwargs)


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    from_account_number = models.IntegerField()
    to_account_number = models.IntegerField()
    amount_transferred = models.DecimalField(max_digits=10, decimal_places=2)
    request_resolved = models.BooleanField(default=False)  # Added a BooleanField for request resolution
    date_and_time = models.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        # Override the save method to generate an ID before saving
        if not self.id:
            # If ID is not set, generate a new one
            last_request = Request.objects.order_by('-id').first()
            new_id = 1 if not last_request else last_request.id + 1
            self.id = new_id
        super().save(*args, **kwargs)


class MoneyTransfer(models.Model):
    enter_your_user_name = models.CharField(max_length=150, default=None)
    enter_the_destination_account_number = models.IntegerField()
    enter_the_amount_to_be_transferred_in_INR = models.DecimalField(max_digits=10, decimal_places=2)



