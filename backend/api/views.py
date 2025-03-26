from rest_framework.decorators import api_view
from rest_framework.response import Response


from salestrakav2.models import Products, Branches, Users, Sales, Returns, Inventory
from salestrakav2.serializers import ProductsSerializer, BranchesSerializer, UsersSerializer, SalesSerializer, ReturnsSerializer, InventorySerializer

@api_view(["POST", "GET"])
def api_home(request, *args, **kwargs):
    if request.method == "GET":
        branch_id = request.query_params.get("id")
        if branch_id:
            try:
                branch = Users.objects.using('default').get(id=branch_id)
                serializer = UsersSerializer(branch)
                return Response(serializer.data)
            except Users.DoesNotExist:
                return Response({"error": "User not found"})
        else:
            return Response({"error": "ID parameter is required"})
    
    elif request.method == "POST":
        # serializer = BranchesSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            branch_instance = Users(**serializer.validated_data)
            branch_instance.save(using='default')  # Save using the selected database
            return Response(serializer.data)
        else:
            # Return errors if data is invalid
            return Response(serializer.errors)

        
        
    # serializer = BranchesSerializer(data=request.data)
    # if serializer.is_valid():
    #     data = serializer.save()
    #     print(data)
    #     data = serializer.data
    #     return Response(data)
    # else:
    #     return Response(serializer.errors, status=400)

    # instance = Sales.objects.using('oshodi').all().order_by("?").first()
    # data = {}
    # if instance:
    #     data = SalesSerializer(instance).data

    