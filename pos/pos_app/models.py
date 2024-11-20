from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import datetime

def convert_to_roman(number):
    if number == str(1):
        roman = "I"
    elif number == str(2):
        roman = "II"
    elif number == str(3):
        roman = "III"
    elif number == str(4):
        roman = "IV"
    elif number == str(5):
        roman = "V"
    elif number == str(6):
        roman = "VI"
    elif number == str(7):
        roman = "VII"
    elif number == str(8):
        roman = "VIII"
    elif number == str(9):
        roman = "IX"
    elif number == str(10):
        roman = "X"
    elif number == str(11):
        roman = "XI"
    elif number == str(12):
        roman = "XII"
    return roman

def convert_to_number(roman):
    if roman == "I":
        number = int(1)
    elif roman == "II":
        number = int(2)
    elif roman == "III":
        number = int(3)
    elif roman == "III":
        number = int(4)
    elif roman == "V":
        number = int(5)
    elif roman == "VI":
        number = int(6)
    elif roman == "VII":
        number = int(7)
    elif roman == "VIII":
        number = int(8)
    elif roman == "IX":
        number = int(9)
    elif roman == "X":
        number = int(10)
    elif roman == "XI":
        number = int(11)
    elif roman == "XII":
        number = int(12)
    return number

def increment_menu_resto_code():
    last_code = MenuResto.objects.all().order_by('id').last()
    if not last_code:
        return "MN-0001"
    code = last_code.code
    code_int = int(code[3:7])
    new_code_int = code_int + 1
    return "MN-" + str(new_code_int).zfill(4)

def increment_order_menu_code():
    last_id = OrderMenu.objects.all()
    m = convert_to_roman(str(datetime.date.today().month))

    if not last_id:
        return "0001" + "-OM-" + m + "-" + str(datetime.date.today().year)
    else:
        code = last_id.code
        code_first, code_middle_1, code_middle_2, code_last = code.split('-')
        y = int(code_last[0:4])
        M = convert_to_number(code_middle_2)

        if ((M == datetime.date.today().month) & (y == datetime.date.today().year)):
            code_int = int(code_first[0:4])
            new_code_int = code_int + 1
            return str(new_code_int).zfill(4) + "-OM-" + m + "-" + str(datetime.date.today().year)
        elif ((M != datetime.date.today().month) | (y != datetime.date.today().year)):
            return "0001" + "-OM-" + m + "-" + str(datetime.date.today().year)


class User(AbstractUser):
    is_waitress = models.BooleanField(default = False)
    is_cashier = models.BooleanField(default = False)
    is_kitchen = models.BooleanField(default = False)

    def __str__(self):
        return str(self.username) + " " + str(self.first_name) + " " + str(self.last_name)
    
class StatusModel(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()

    def __str__(self):
        return self.name

class TableResto(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_table_choices = (
        ('Kosong', 'Kosong'),
        ('Terisi', 'Terisi'),
    )
    code = models.CharField(max_length = 20)
    name = models.CharField(max_length = 100)
    capacity = models.IntegerField(default = 0)
    table_status = models.CharField(max_length = 15, choices = status_table_choices, default = "Kosong")
    status = models.CharField(max_length = 15, choices = status_choices, default = "Aktif")
    user_create = models.ForeignKey(User, related_name = "user_create_table_resto", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_table_resto", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)
    
class Profile(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )
    user = models.OneToOneField(User, related_name = "user_profile", on_delete = models.PROTECT)
    avatar = models.ImageField(default = "default_images/person.jpg", upload_to = "profile_images/", blank = True, null = True)
    bio = models.TextField()
    status = models.CharField(max_length = 15, choices = status_choices, default = "Aktif")
    user_create = models.ForeignKey(User, related_name = "user_create_profile", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_profile", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)
    
    def save(self, *args, **kwargs):
        super().save()
        try:
            img = Image.open(self.avatar.path)
            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        except:
            pass

class Category(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif')
    )
    name = models.CharField(max_length = 100)
    status = models.CharField(max_length = 15, choices = status_choices, default = "Aktif")
    user_create = models.ForeignKey(User, related_name = "user_create_category", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_category", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)
    
class MenuResto(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_menu_choices = (
        ('Ada', 'Ada'),
        ('Habis', 'Habis'),
    )
    code = models.CharField(max_length = 20, default = increment_menu_resto_code, editable = False)
    name = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.CharField(max_length = 200, blank = True, null = True)
    image_menu = models.ImageField(default = 'default_images/empty.jpg', upload_to = 'menu_images/', blank = True, null = True)
    category = models.ForeignKey(Category, related_name = 'category_menu', blank = True, null = True, on_delete = models.SET_NULL)
    menu_status = models.CharField(max_length = 15, choices = status_menu_choices, default = 'Ada')
    status = models.CharField(max_length = 15, choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, related_name = "user_create_menu", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_menu", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.name)
    
class OrderMenu(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_order_status_choices = (
        ('Belum Bayar', 'Belum Bayar'),
        ('Sudah Bayar', 'Sudah Bayar'),
    )
    code = models.CharField(max_length = 20, default = increment_order_menu_code, editable = False)
    table_resto = models.ForeignKey(TableResto, related_name = 'table_resto_order_menu', blank = True, null = True, on_delete = models.SET_NULL)
    cashier = models.ForeignKey(User, related_name = 'cashier_order_menu', blank = True, null = True, on_delete = models.SET_NULL)
    waitress = models.ForeignKey(User, related_name = 'waitress_order_menu', blank = True, null = True, on_delete = models.SET_NULL)
    order_status = models.CharField(max_length = 20, choices = status_order_status_choices, default = 'Belum Bayar')
    total_order = models.DecimalField(max_digits = 10, default = 0, decimal_places = 2, blank = True, null = True)
    tax_order = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, blank = True, null = True)
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, null = True, blank = True)
    payment = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, null = True, blank = True)
    changed = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, null = True, blank = True)
    status = models.CharField(max_length = 20, choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, related_name = "user_create_order_menu", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_order_menu", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.code

class OrderMenuDetail(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_order_menu_detail_choices = (
        ('Sedang Disajikan', 'Sedang Disajikan'),
        ('Sudah Disajikan', 'Sudah Disajikan'),
    )
    order_menu = models.ForeignKey(OrderMenu, related_name = 'order_menu_order_menu_detail', blank = True, null = True, on_delete = models.SET_NULL)
    menu_resto = models.ForeignKey(MenuResto, related_name = 'menu_resto_order_menu_detail', blank = True, null = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default = 0)
    subtotal = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, blank = True, null = True)
    description = models.CharField(max_length = 200, blank = True, null = True)
    order_menu_detail_status = models.CharField(max_length = 30, choices = status_order_menu_detail_choices, default = 'Sedang Disajikan')
    status = models.CharField(max_length = 20, choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, related_name = "user_create_order_menu_detail", null = True, blank = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = "user_update_order_menu_detail", null = True, blank = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.order_menu.code) + " - " + str(self.menu_resto)
    
    def get_subtotal(self):
        return self.quantity * self.menu_resto.price