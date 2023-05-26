
from django.db import models
from user.models import User

# Create your models here.
class Company(models.Model):
    #companyId = models.IntegerField()
    companyName = models.CharField(max_length=20)
    companyInfo = models.CharField(max_length=200)

    def __str__(self):
        return self.companyName
    
    class Meta:
        db_table = 'Company'

class Sector(models.Model):
   # sectorId = models.IntegerField()
    sectorName = models.CharField(max_length=100)

    def __str__(self):
        return self.sectorName
    
    class Meta:
        db_table = 'Sector'

class Stocks(models.Model):
    stockName = models.CharField(max_length=20)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE) #foreignkey
    isActive = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) #foreignkey
    buySaleSignal = models.IntegerField()#doubt

    def __str__(self):
        return self.stockName    
    class Meta:
        db_table = 'Stocks'


class Portfolio(models.Model):
    #portfolioId = models.IntegerField()
    portfolioName = models.CharField(max_length=50)
    portfolioScore = models.IntegerField() #doubt
    user = models.ForeignKey(User, on_delete=models.CASCADE) #fk  #doubt
    createdAt = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    isDefault = models.BooleanField(default=False)

class Watchlist(models.Model):
    name = models.CharField(max_length=200)
    create = models.CharField(max_length=100)
    isActive = models.BooleanField(default=False)
    isDefault = models.BooleanField(default=False)
    
class WatchlistStock(models.Model):
    #wsid = models.IntegerField()
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE) #fk
    stocks = models.ForeignKey(Stocks, on_delete=models.CASCADE) #FK

class UserPortfolioStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #FK   #doubt
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE) #FK
    stocks = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    qty = models.IntegerField()       #DOUBTSSSSSSS
    purchaseDate = models.DateField()   #DOUBTSSSSSSS
    investPrice = models.IntegerField()  #DOUBTSSSSSSS
    currentPrice = models.IntegerField()  #DOUBTSSSSSSS

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    feedback = models.CharField(max_length=300)

# class Notification(models.Model):
#     userId = models.IntegerField()
#     type = models.CharField(max_length=20)
#     content = models.TextField(max_length=100)
#     isRead = models.BooleanField(default=False)
#     nDate = models.DateField()


# class PaymentDetails(models.Model):
#     userId = models.IntegerField()
#     transactionId = models.IntegerField()
#     amount = models.IntegerField()
#     transactionDate = models.DateField()
#     renewDate = models.DateField()
#     cardNumber = models.IntegerField(null=False)

class Alert(models.Model):
    # alert = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #doubt
    stocks = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    price = models.IntegerField()
    alertType = models.CharField(max_length=100) #doubt









