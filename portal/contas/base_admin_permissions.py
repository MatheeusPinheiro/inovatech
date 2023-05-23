from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import View 

class BaseAdminUsers(LoginRequiredMixin, UserPassesTestMixin, View):
    
    authorized_admin_access = []
    
    def test_func(self):
        
        if self.request.user.type_user in self.authorized_admin_access:
            return True   
        else: 
            return self.request.user == self.get_object()
        
    def handle_no_permission(self):
        
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('post-list')
        return redirect('login')       


class BaseAdminUserAd(BaseAdminUsers):
    authorized_admin_access = ['ad']  

class BaseAdminUserCo(BaseAdminUsers):
    authorized_admin_access = ['ad', 'co']   

class BaseAdminUserall(BaseAdminUsers):
    authorized_admin_access = ['ad', 'co', 'us']  