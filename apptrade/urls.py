from django.urls import path
from .views import DisplayPortfolio, MarketStock, MarketOrder, UserLogin, UserRegister, UserLogout

urlpatterns = [
  path("user-login", UserLogin.as_view(), name="app-user-login"),
  path("user-register", UserRegister.as_view(), name="app-user-register"),
  path("user-logout", UserLogout.as_view(), name="app-user-logout"),
  path("portfolio", DisplayPortfolio.as_view(), name="app-portfolio"),
  path("market-stock", MarketStock.as_view(), name="app-market-stock"),
  path("market-order", MarketOrder.as_view(), name="app-market-order")
]
