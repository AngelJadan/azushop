import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from ventas.forms import UserForm
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView
import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from ventas.models import Bilding, CarShop, CatalogProduct, Product
from ventas.recomendador.api_facebook import get_data_facebook, publish_image_facebook
from ventas.recomendador.knn import run_knn
from ventas.serializers import BildingSerializer, CarShopReadSerializer, CarShopSerializer, ProductSerialiezer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny

# Create your views here.
class RegisterUsers(APIView):
    """Clase para usuarios para registrar un nuevo usuario.
    """
    @action(detail=False, method="POST")
    def post(self, request, format=None):
        print("request ",request.data)
        register = UserForm(data=request.data)

        user_temp = User.objects.filter(email = request.data["email"])
        if len(user_temp)<=0:
            if register.is_valid():
                user = register.save()
                pw = user.password
                user.set_password(pw)
                user.save()
                return Response({"id":user.id},status=status.HTTP_201_CREATED)
            else:
                return Response(register.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Ya existe un usuario con este correo"},status=status.HTTP_400_BAD_REQUEST)

class SessionExpiredMiddleware:
    def process_request(request):
        last_activity = request.session['last_activity']
        now = datetime.now()

        if (now - last_activity).minutes > 10:
            # Do logout / expire session
            # and then...
            return Response({"code": "401", "sms": "Sessión expirada"})

        if not request.is_ajax():
            # don't set this for ajax requests or else your
            # expired session checks will keep the session from
            # expiring :)
            request.session['last_activity'] = now        

class Login(ObtainAuthToken):
    """Clase api, para realizar un login.
    """

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            username = User.objects.get(email=email)
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'pk': user.pk,
                    'user': user.username,
                    'first_name':user.first_name,
                    'last_name': user.last_name
                })
        except User.DoesNotExist:
            return Response({"Error":"El usuario no esta registrado."},status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            print("Error: ",e)
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Logout(APIView):
    '''Clase api, para elimina el token y cerrar session.
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class ListAllProduct(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class =  ProductSerialiezer

    @action(detail=False, method="GET")
    def get_queryset(self):
        return Product.objects.all()
    

class CarAPI(APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = CarShopSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Acceso no autorizado"},status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, method="PUT")
    def put(self, request, format=json): 
        if request.user.is_authenticated:
            
            car = CarShop.objects.get(id=request.data["id"])
            serializer = CarShopSerializer(car, data=request.data, context=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Acceso no autorizado"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        if request.is_authenticated:
            res = CarShop.objects.filter(id=pk)
            serializer = CarShopSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        if request.is_authenticated:
            CarShop.objects.filter(id=pk).delete()
            return Response({"sms":"Item eliminado"},status=status.HTTP_200_OK)
        else:
            return Response({"Error":"Acceso no autorizado"},status=status.HTTP_401_UNAUTHORIZED)


class ListCar(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarShopReadSerializer

    @action(detail=False, method="GET")
    def get_queryset(self):
        return CarShop.objects.filter(client=self.kwargs["client"])
    

class BildingAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BildingSerializer

    @action(detail=False, method="POST")
    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = BildingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
    

class ListBildingsClient(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  ProductSerialiezer

    @action(detail=False, method="GET")
    def get_queryset(self):
        return Bilding.objects.filter(client=self.kwargs['client'])
    
    


@api_view(["GET"])
def api_facebook_consumer(request):
    data = get_data_facebook()
    return Response({"data":data},status=status.HTTP_200_OK)


def view_list_images(request):
    products = []
    for product in Product.objects.all():
        valor_iva = (product.price * float(product.iva))/100
        total = product.price+valor_iva
        
        products.append({
            "id":product.id,
            "key":product.key,
            "price":product.price,
            "name":product.name,
            "iva":valor_iva,
            "total":total,
            "description":product.description
        })
    context = {"products":products}
    return render(request, "list_products.html", context)

@api_view(["GET"])
def publish_product(request, id_product):
    """
    Para publicar la imagen en facebook
    """
    product = Product.objects.get(id=id_product)
    catalog = CatalogProduct.objects.filter(product=product)
    path_publish = "https://mobilestore.ec/wp-content/uploads/2023/04/HONOR-Magic-5-Lite-Verde-Mobile-Store-Ecuador.jpg"
    print(path_publish)
    resp = publish_image_facebook(path_publish,product.description)
    if resp.get("id"):
        Product.objects.filter(id=id_product).update(id_publisher=resp.get("post_id"))
    return Response({"sms":resp}, status=status.HTTP_200_OK)

def image(request,id_catalog):
    """
    Para exponer la imagen en la web
    """
    catalog = CatalogProduct.objects.get(id=id_catalog)
    context={"catalog":catalog}
    return render(request, 'images.html', context)


class View_products_recomeders(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  ProductSerialiezer

    def get_queryset(self):
        data = run_knn(self.kwargs["id_product"])
        return data