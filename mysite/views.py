from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.views.generic.edit import FormView

# Create your views here.
def home(request):	
	return render(request, 'mysite/home.html')

# Custom form for updating profile information
class ProfileForm(forms.ModelForm):
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w3-input w3-border w3-round'}))
	class Meta:
		model = User
		fields = ['first_name','last_name','email']
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round', 'placeholder' : 'Enter first name'}),            
			'last_name': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round', 'placeholder' : 'Enter last name'}),
			'email': forms.TextInput(attrs={'class': 'w3-input w3-border w3-round'}),
        }

def user_profile_view(request):
    user = request.user
    profile_form = ProfileForm(instance=user)
    # password_form = PasswordChangeForm(user=user)
    # groups = user.groups.all()  # Retrieve user's groups

    if request.method == 'POST':
        # Process profile update form
        profile_form = ProfileForm(request.POST, instance=user)
        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
    
    context = {
        'profile_form': profile_form,
        # 'password_form': password_form,
        # 'groups': groups,
    }
    return render(request, 'user_profile.html', context)


#Process password change form
class PasswordChangeView(LoginRequiredMixin, FormView):
        model = User
        form_class = PasswordChangeForm
        template_name = './account/password_change.html'

        def get_form_kwargs(self):
            kwargs = super(PasswordChangeView, self).get_form_kwargs()
            kwargs['user'] = self.request.user
            if self.request.method == 'POST':
                kwargs['data'] = self.request.POST
            return kwargs

        def form_valid(self, form):
            form.save()
            update_session_auth_hash(self.request, form.user)        
            return super(PasswordChangeView, self).form_valid(form)
        

class GroupMembershipView(LoginRequiredMixin, TemplateView):
    template_name = "account/group_membership.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user.username)
        context['groups'] = user.groups.all()  # Accessing the user's groups
        return context
    

class InviteView(LoginRequiredMixin, TemplateView):
    template_name = "account/invites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user.username)
        context['groups'] = user.groups.all()  # Accessing the user's groups
        return context

    
class BillingView(LoginRequiredMixin, TemplateView):
    template_name = "account/billing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user.username)
        context['groups'] = user.groups.all()  # Accessing the user's groups
        return context