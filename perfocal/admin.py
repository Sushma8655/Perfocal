from django.contrib import admin
from .models import AddMachine
# Register your models here.
def countX(lst, x):
    count = 0
    for ele in lst:
        if ele == x:
            count = count + 1
    return count


admin.site.register(AddMachine)