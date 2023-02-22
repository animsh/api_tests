from rest_framework import generics
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, ManagerListSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuser, IsManager, IsDeliveryCrew, IsCustomer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User, Group
from django.http import JsonResponse


class CategoryView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response({
            'message': 'Categories retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Category created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response({
            'message': 'Category retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Category updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response({
            'message': 'Category deleted successfully.'
        })


class SingleCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        category = self.get_queryset()
        serializer = self.get_serializer(category)
        return Response({
            'message': 'Category retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Category created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response({
            'message': 'Category retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Category updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response({
            'message': 'Category deleted successfully.'
        })


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data)
        return Response({
            'message': 'Menu item retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Menu item created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response({
            'message': 'Menu item retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Menu item updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.delete()
        return Response({
            'message': 'Menu item deleted successfully.'
        })


class CartView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'message': 'Cart created successfully.',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if self.get_object().user != request.user:
            return Response({'message': 'You do not have permission to perform this action.'}, status=403)
        return Response({
            'message': 'Cart retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Cart updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        obj = self.get_queryset()
        if obj.first().user != request.user:
            return Response({'message': 'You do not have permission to perform this action.'}, status=403)
        obj.delete()
        return Response({'message': 'Cart deleted successfully.'})


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_fields = ['user']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response({
            'message': 'Orders retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Order created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response({
            'message': 'Order retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Order updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.delete()
        return Response({
            'message': 'Order deleted successfully.'
        })


class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        serializer = self.get_serializer(data, many=True)
        return Response({
            'message': 'Orders retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Order created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response({
            'message': 'Order retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Order updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.delete()
        return Response({
            'message': 'Order deleted successfully.'
        })
# class OrderItemView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

#     def list(self, request):
#         data = self.get_queryset()
#         serializer = self.get_serializer(data, many=True)
#         return Response({
#             'message': 'Order items retrieved successfully.',
#             'data': serializer.data
#         })

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#             'message': 'Order item created successfully.',
#             'data': serializer.data
#         }, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         data = self.get_object()
#         serializer = self.get_serializer(data)
#         return Response({
#             'message': 'Order item retrieved successfully.',
#             'data': serializer.data
#         })

#     def update(self, request, pk=None):
#         data = self.get_object()
#         serializer = self.get_serializer(data, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#             'message': 'Order item updated successfully.',
#             'data': serializer.data
#         })

#     def destroy(self, request, pk=None):
#         data = self.get_object()
#         data.delete()
#         return Response({
#             'message': 'Order item deleted successfully.'
#         })


class ManagersListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsSuperuser]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Managers group'})


class ManagersRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsSuperuser]
    queryset = User.objects.filter(groups__name='Manager')

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Manager')
        managers.user_set.remove(user)
        return JsonResponse(status=200, data={'message': 'User removed Managers group'})


class DeliveryCrewListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsSuperuser]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            crew = Group.objects.get(name='Delivery Crew')
            crew.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Delivery Crew group'})


class DeliveryCrewRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsSuperuser]
    queryset = User.objects.filter(groups__name='Delivery Crew')

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name='Delivery Crew')
        managers.user_set.remove(user)
        return JsonResponse(status=201, data={'message': 'User removed from the Delivery crew group'})
