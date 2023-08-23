from rest_framework.permissions import BasePermission

class BuyerUserPermission(BasePermission):

    def has_permission(self, request,view):
        if request.user.user_type == 'Buyer':
            return True

class SellerUserPermission(BasePermission):

    def has_permission(self, request,view):
        if request.user.user_type == 'Seller':
            return True