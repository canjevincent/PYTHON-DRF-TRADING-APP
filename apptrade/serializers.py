from rest_framework import serializers
from .models import Market, Order, CustomUser

class AuthSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = "__all__"

class MarketSerializers(serializers.ModelSerializer):

  class Meta:
    model = Market
    fields = "__all__"

class OrderSerializers(serializers.ModelSerializer):

  def validate(self, data):

    raise_error = {}

    if (data["market_order"].stock_quantity - data["quantity_order"]) < 0:
      raise_error.update({"invalid_quantity":"Quantity exceeded."})

    if raise_error:
      raise serializers.ValidationError(raise_error)  
    
    return data

  class Meta:
    model = Order
    fields = "__all__"
