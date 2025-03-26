from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from datetime import timedelta


from .models import Products
from .models import Branches
from .models import Users
from .models import Sales
from .models import Returns
from .models import Inventory

from .serializers import ProductsSerializer
from .serializers import BranchesSerializer
from .serializers import UsersSerializer
from .serializers import UsersLoginSerializer
from .serializers import SalesSerializer
from .serializers import ReturnsSerializer
from .serializers import InventorySerializer



class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow anyone to login

    def post(self, request, *args, **kwargs):
        # Step 1: Get the email and password from the request
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 2: Authenticate the user based on email and password
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Step 3: Verify the password for the user
        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Step 4: Generate tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Step 5: Serialize user data (no need for an additional request to get user details)
        user_data = UsersLoginSerializer(user).data  # Use the appropriate serializer

        # Step 6: Set the tokens as HttpOnly cookies (handled server-side)
        response = Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": user_data
        })

        return response

user_login_view = UserLoginView.as_view()



class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get the refresh token from the request data
        refresh_token = request.data.get('refresh', None)

        # If no refresh token is provided, return a bad request response
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try to create a new access token using the provided refresh token
        try:
            # Create a RefreshToken instance from the provided refresh token
            token = RefreshToken(refresh_token)
            # Generate the new access token
            access_token = str(token.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)

        except Exception as e:
            # If there's an error (e.g., the refresh token is invalid), return a bad request response
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
token_refresh_view = CustomTokenRefreshView.as_view()


class RegisterUserView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]  # Allow anyone to register

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create the user using the `add_user` method
            user = Users.add_user(serializer.validated_data)

            # If add_user returns a dictionary with a message, it's an error
            if isinstance(user, dict) and 'message' in user:
                return Response(user, status=status.HTTP_400_BAD_REQUEST)

            # Return the user data excluding the password
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Extract the error message from the ValidationError
            error_messages = e.detail  # e.detail contains the error details

            # Extract the first error message from the field's error details
            if isinstance(error_messages, dict):
                # Extract error message for the email field (or any other field)
                email_errors = error_messages.get('email', [])
                if email_errors:
                    # Extract the actual error string from the ErrorDetail object
                    error_message = email_errors[0]  # This gets the actual error string

                else:
                    error_message = 'An unknown error occurred'
            else:
                error_message = 'An unknown error occurred'

            # Return the error message in the response
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

users_register_view = RegisterUserView.as_view()



class ProductsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Call the add_product method to create the product
            validated_data = request.data
            product = Products.add_product(validated_data)
            return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Extract the error message from the ValidationError
            # The error could be inside non_field_errors or a similar structure
            error_messages = e.detail  # e.detail contains the error details
            if isinstance(error_messages, dict):  # If error details are in dictionary form
                # You can access specific error message here
                error_message = error_messages.get('non_field_errors', ['An error occurred'])[0]
            elif isinstance(error_messages, list):  # If it's in a list format
                error_message = error_messages[0]
            else:
                error_message = 'An error occurred'

            # Return the response with only the error message
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

products_list_create_view = ProductsListCreateAPIView.as_view()


class ProductsDetailAPIView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # lookup_field = 'pk'

products_detail_view = ProductsDetailAPIView.as_view()


class ProductsUpdateAPIView(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # Get the product instance to update
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Validate the data with the serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['id'] = instance.pk
        
        # Call the update_product method with validated data
        update_response = Products.update_product(serializer.validated_data)
        
        # Check if update_product returned a message (indicating no update was performed)
        if isinstance(update_response, dict) and "message" in update_response:
            return Response(update_response, status=status.HTTP_400_BAD_REQUEST)

        # If update was successful, return the updated instance data
        serializer = self.get_serializer(update_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

products_update_view = ProductsUpdateAPIView.as_view()



class ProductsDestroyAPIView(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # lookup_field = 'pk'

products_destroy_view = ProductsDestroyAPIView.as_view()


class BranchesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Call the add_product method to create the product
            validated_data = request.data
            branch = Branches.add_branch(validated_data)
            return Response(self.get_serializer(branch).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # Extract the error message from the ValidationError
            # The error could be inside non_field_errors or a similar structure
            error_messages = e.detail  # e.detail contains the error details
            if isinstance(error_messages, dict):  # If error details are in dictionary form
                # You can access specific error message here
                error_message = error_messages.get('non_field_errors', ['An error occurred'])[0]
            elif isinstance(error_messages, list):  # If it's in a list format
                error_message = error_messages[0]
            else:
                error_message = 'An error occurred'

            # Return the response with only the error message
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

branches_listcreate_view = BranchesListCreateAPIView.as_view()


class BranchesDetailAPIView(generics.RetrieveAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    lookup_field = 'id'

branches_detail_view = BranchesDetailAPIView.as_view()


class BranchesUpdateAPIView(generics.UpdateAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    # lookup_field = 'id'

branches_update_view = BranchesUpdateAPIView.as_view()


class BranchesDestroyAPIView(generics.DestroyAPIView):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    # lookup_field = 'pk'

branches_destroy_view = BranchesDestroyAPIView.as_view()



class UsersListAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # lookup_field = 'id'

users_list_view = UsersListAPIView.as_view()


class UsersDetailAPIView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # lookup_field = 'id'

users_detail_view = UsersDetailAPIView.as_view()


class UsersUpdateAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # lookup_field = 'id'

users_update_view = UsersUpdateAPIView.as_view()


class UsersDestroyAPIView(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # lookup_field = 'pk'

users_destroy_view = UsersDestroyAPIView.as_view()



class SalesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    # lookup_field = 'id'

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data, many=True) 
        serializer.is_valid(raise_exception=True) 
        self.perform_create(serializer) 
        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

sales_listcreate_view = SalesListCreateAPIView.as_view()


class SalesDetailAPIView(generics.RetrieveAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    # lookup_field = 'id'

sales_detail_view = SalesDetailAPIView.as_view()


# class SalesUpdateAPIView(generics.UpdateAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer
#     # lookup_field = 'id'

# sales_update_view = SalesUpdateAPIView.as_view()


class SalesDestroyAPIView(generics.DestroyAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    # lookup_field = 'pk'

    def delete(self, request, pk, *args, **kwargs):
        try:
            sale_instance = Sales.objects.get(pk=pk)
            serializer = SalesSerializer()
            result = serializer.delete(sale_instance)
            return Response(result, status=status.HTTP_200_OK)
        except Sales.DoesNotExist:
            return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)

sales_destroy_view = SalesDestroyAPIView.as_view()



class ReturnsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Returns.objects.all()
    serializer_class = ReturnsSerializer
    # lookup_field = 'id'

returns_listcreate_view = ReturnsListCreateAPIView.as_view()



class ReturnsDetailAPIView(generics.RetrieveAPIView):
    queryset = Returns.objects.all()
    serializer_class = ReturnsSerializer
    # lookup_field = 'id'

returns_detail_view = ReturnsDetailAPIView.as_view()


# class ReturnsUpdateAPIView(generics.UpdateAPIView):
#     queryset = Returns.objects.all()
#     serializer_class = ReturnsSerializer
#     # lookup_field = 'id'

# returns_update_view = ReturnsUpdateAPIView.as_view()


class ReturnsDestroyAPIView(generics.DestroyAPIView):
    queryset = Returns.objects.all()
    serializer_class = ReturnsSerializer
    # lookup_field = 'pk'

returns_destroy_view = ReturnsDestroyAPIView.as_view()




class InventoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # lookup_field = 'id'

inventory_listcreate_view = InventoryListCreateAPIView.as_view()


class InventoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # lookup_field = 'id'

inventory_detail_view = InventoryDetailAPIView.as_view()


class InventoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    # lookup_field = 'pk'

inventory_destroy_view = InventoryDestroyAPIView.as_view()