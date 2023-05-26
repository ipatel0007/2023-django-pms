from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Company)
admin.site.register(Sector)
admin.site.register(Stocks)
admin.site.register(Portfolio)
admin.site.register(Watchlist)
admin.site.register(WatchlistStock)
admin.site.register(UserPortfolioStock)


