from django.contrib import admin
from .models import Reservation, Stock, StockMovement

admin.site.register((Stock, Reservation, StockMovement))
