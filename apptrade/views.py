from rest_framework.views import APIView, Response, status
from rest_framework.authtoken.models import Token
from .models import Market, Order, CustomUser
from .serializers import MarketSerializers, OrderSerializers, AuthSerializer

from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404
from django.db.models import Sum

# Create your views here.
class UserLogin(APIView):

  def post(self, request):
    user = get_object_or_404(CustomUser, user_name=request.data["user_name"])
    if not user.check_password(request.data["password"]):
      return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = AuthSerializer(user)
    return Response({"token": token.key, "user": serializer.data})

class UserRegister(APIView):

  def post(self, request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      user = CustomUser.objects.get(user_name=request.data["user_name"])
      user.set_password(request.data["password"])
      user.save()
      token = Token.objects.create(user=user)
      return Response({'token': token.key, "user":serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):

  authentication_classes = [TokenAuthentication]
  
  def post(self, request):
    request.user.auth_token.delete()
    return Response({ "Message": "You are logged out" })

class DisplayPortfolio(APIView):

  authentication_classes = [TokenAuthentication]

  def get(self, request):

    user = CustomUser.objects.get(pk=request.user.id)

    data = {
      "total_invested_value":Order.objects.filter(created_by=user.id).aggregate(total=Sum("total_price_order")),
      "individual_stock":OrderSerializers(Order.objects.filter(created_by=user.id), many=True).data,
    }

    return Response(data, status=status.HTTP_200_OK)

class MarketStock(APIView):

  authentication_classes = [TokenAuthentication]

  def get(self, request):

    data = {
      "stock":MarketSerializers(Market.objects.filter(created_by=request.user.id), many=True).data
    }

    return Response(data, status=status.HTTP_200_OK)
  
  def post(self, request):

    data = {
      "stock_name":request.data["stock_name"],
      "stock_price":request.data["stock_price"],
      "stock_quantity":request.data["stock_quantity"],
      "created_by":request.user.id
    }

    new_stock = MarketSerializers(data=data)

    if new_stock.is_valid():
      new_stock.save()
      return Response(new_stock.data, status=status.HTTP_200_OK)
    else:
      return Response(new_stock.errors, status=status.HTTP_400_BAD_REQUEST)

class MarketOrder(APIView):

  authentication_classes = [TokenAuthentication]

  def get(self, request):
    
    data = {
      "order":OrderSerializers(Order.objects.filter(created_by=request.user.id), many=True).data
    }

    return Response(data, status=status.HTTP_200_OK)

  def post(self, request):
    
    market_order = Market.objects.get(pk=request.data["market_order"])

    data = {
      "quantity_order":int(request.data["quantity_order"]),
      "total_price_order":market_order.stock_price * market_order.stock_quantity,
      "market_order":request.data["market_order"],
      "created_by":request.user.id
    }
    
    new_order = OrderSerializers(data=data)
    if new_order.is_valid():
      new_order.save()

      Market.objects.filter(id=request.data["market_order"]).update(stock_quantity=market_order.stock_quantity - int(request.data["quantity_order"]))

      return Response(new_order.data, status=status.HTTP_201_CREATED)
    else:
      return Response(new_order.errors, status=status.HTTP_400_BAD_REQUEST)