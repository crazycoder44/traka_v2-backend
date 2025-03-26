from rest_framework import serializers
import uuid

from .models import Products
from .models import Branches
from .models import Users
from .models import Sales
from .models import Returns
from .models import Inventory



class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id',
            'productname',
            'desc',
            'price',
            'status',
        ]

    def create(self, validated_data):
        # Call the add_product method and capture the result
        result = Products.add_product(validated_data)

        # Check if the result is a dictionary with a message (indicating a validation issue)
        if isinstance(result, dict) and "message" in result:
            # Raise a validation error with the provided message
            raise serializers.ValidationError(result["message"])

        # If no issues, return the successfully created product instance
        return result
    
    def delete(self, instance):
        # Get the primary key (id) from the instance and pass it to delete_product
        product_id = instance.id
        result = Products.delete_product(product_id)
        
        # Print for debugging
        print(f"product_id = {product_id}, result = {result}")

        if isinstance(result, dict) and "message" in result:
            # If an error or info message was returned, raise a ValidationError
            raise serializers.ValidationError(result["message"])
        
        # Return result on successful deletion
        return result

class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            'id',
            'branchname',
            'address',
            'mobile',
            'date',
            'status',
        ]

    def create(self, validated_data):
        result = Branches.add_branch(validated_data)
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])
        return result
    
    def update(self, instance, validated_data):
        # Call the update_branch method, passing instance.id as branch_id and validated_data for updates
        result = Branches.update_branch(instance.id, validated_data)

        # If the result is a dictionary with a message, raise a ValidationError
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])

        # Return the updated instance
        return result
    
    def delete(self, instance):
        # Get the primary key (id) from the instance and pass it to delete_product
        branch_id = instance.id
        result = Branches.delete_branch(branch_id)
        
        # Print for debugging
        print(f"branch_id = {branch_id}, result = {result}")

        if isinstance(result, dict) and "message" in result:
            # If an error or info message was returned, raise a ValidationError
            raise serializers.ValidationError(result["message"])
        
        # Return result on successful deletion
        return result


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'firstname',
            'lastname',
            'gender',
            'email',
            'mobile',
            'address',
            'role',
            'datejoined',
            'branchid',
            'password',
            'status',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
        }

    def create(self, validated_data):
        # Use the add_user method from the Users model to create a new user
        result = Users.add_user(validated_data)
        
        # If result is a dictionary with a message, raise a ValidationError
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])

        return result
    
    def update(self, instance, validated_data):
        # Use the update_user method from the Users model to handle the update
        result = Users.update_user(instance.id, validated_data)
        
        # If result is a dictionary with a message, raise a ValidationError
        if isinstance(result, dict) and "message" in result:
            raise serializers.ValidationError(result["message"])

        return result
    
    def delete(self, instance):
        # Get the primary key (id) from the instance and pass it to delete_user
        user_id = instance.id
        result = Users.delete_user(user_id)
        
        # Print for debugging
        print(f"user_id = {user_id}, result = {result}")

        if isinstance(result, dict) and "message" in result:
            # If an error or info message was returned, raise a ValidationError
            raise serializers.ValidationError(result["message"])
        
        # Return result on successful deletion
        return result



class UsersLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'pk',
            'firstname',
            'lastname',
            'gender',
            'email',
            'mobile',
            'address',
            'role',
            'datejoined',
            'branchid',
            'status',
            'is_staff',
            'is_active',
            'is_salesrep', 
            'is_admin', 
            'is_superadmin',
        ]



class SalesListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print(f'validated data = {validated_data}')
        print(f'Type of validated_data: {type(validated_data)}')
        # Generate a single orderid for the entire list
        orderid = str(uuid.uuid4()).replace('-', '')[:14]
        for item in validated_data:
            item['orderid'] = orderid
            item['productid'] = item['productid'].id
            item['userid'] = item['userid'].id
            item['branchid'] = item['branchid'].id
        
        try:
            created_sales = Sales.process_sales(validated_data)
            return created_sales
        except ValueError as e:
            raise serializers.ValidationError({"error": str(e)})


class SalesSerializer(serializers.ModelSerializer):
    orderid = serializers.CharField(read_only=True)
    class Meta:
        model = Sales
        fields = [
            'id',
            'orderid',
            'ordersrc',
            'productid',
            'quantity',
            'unit_price',
            'userid',
            'branchid',
            'payment_choice',
            'date',
            'total_sale_price',
            'return_amount',
            'order_total_amount',
        ]
        list_serializer_class = SalesListSerializer
    
    def delete(self, instance):
        """Custom delete method to execute delete_sale on the model."""
        try:
            # Call the delete_sale method on the model instance
            result = instance.delete_sale()
            return {"message": result, "status": "success"}
        except Exception as e:
            # Handle exceptions and provide feedback
            raise serializers.ValidationError({"error": str(e), "status": "failure"})



class ReturnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returns
        fields = [
            'id',
            'orderid',
            'productid',
            'quantity',
            'action',
            'userid',
            'branchid',
            'date',
        ]
    

    def create(self, validated_data):
        # Create a Returns instance with the provided data
        returns_instance = Returns(**validated_data)

        # Execute the process_return method
        result = returns_instance.process_return()
        # Check the result of the return processing
        if result != 'Return processed successfully':
            # Raise a validation error if the return could not be processed
            raise serializers.ValidationError(result)
        
        # Save the instance after successful return processing
        returns_instance.save()
        return returns_instance


class InventorySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(write_only=True)
    class Meta:
        model = Inventory
        fields = [
            'id',
            'productid',
            'serialnumber',
            'userid',
            'branchid',
            'date',
            'quantity',
        ]

    def create(self, validated_data):
        # Extract the quantity value and remove it from validated_data
        quantity = validated_data.pop('quantity')
        
        # Create a list to hold multiple Inventory instances
        inventory_instances = [
            Inventory(**validated_data)
            for _ in range(quantity)
        ]
        
        # Bulk create the inventory instances
        Inventory.objects.bulk_create(inventory_instances)
        
        # Return the created instances or a success message
        return inventory_instances[-1]