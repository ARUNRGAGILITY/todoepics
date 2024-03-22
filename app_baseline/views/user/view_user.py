# all imports
from ..all_view_imports import *

# config
from ..._common.config.config import *

# specific imports
from ...forms.user.form_user import *
from ...models.user.model_user import *

# which app is being referred
app_base_ref = base_app_ref

class CustomPasswordChangeView(PasswordChangeView):
    template_name = '001.password_change.html'
    success_url = reverse_lazy('user-home')

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('user-home')

    if request.method == 'POST':
        user = None
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        #print(f"EMAIL: {email}")
        try:
            user = User.objects.get(email=email)
            #print(f"EMAIL1: {user.email}")
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User does not exist 1')
        #print(f"EMAIL2: {email}")        

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url != None:                
                return redirect(next_url)
            return redirect('user-home')
            
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    template_url = f"{app_base_ref}/user/login_register.html"
    return render(request, template_url, context)

def user_home(request):
    context = {'page': 'home'}
    template_url = f"{app_base_ref}/user/home.html"
    return render(request, template_url, context)

def logoutPage(request):
    logout(request)
    return redirect('/')
@login_required
def home(request):
    context = {'page': 'home'}
    template_url = f"{app_base_ref}/base/visitor_page.html"
    return render(request, template_url, context)

def registerPage(request):
    template_url = f"{app_base_ref}/user/login_register.html"
    if request.user.is_authenticated:
        return redirect('user-home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        reg_code = None
        # chk_reg_code = None
        if form.is_valid():
            new_user = form.save(commit=False)
            # check the registration code           
            reg_code = form.cleaned_data.get('RegistrationCode')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            # password1 = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password2')
            context = {'form':form}
            if RegCode.objects.filter(reg_code=reg_code).exists():
                chk_reg_code = RegCode.objects.filter(reg_code=reg_code)
                #print(f"USERNAME: {username} EMAIL: {email}")
                email = form.cleaned_data.get('email').lower()
                new_user.username = username
                form.save()
                context = {'form':form}
                messages.success(request, f"Your account {email} has been created! You may log in now.")
                return redirect('login')
            else:
                print(f">>> Error in the creation of the user: regcode not working")
                form.add_error('RegistrationCode', 'Invalid registration code provided.')
                messages.error(request, f"Contact Administrator or utilize the correct Regn. Code/Information.")
                return render(request, template_url, context)
        else:
                print(f">>> REG form NOT VALID {form.errors}")
                context = {'form':form}
                return render(request, template_url, context)
    else:
        form = UserRegisterForm()
    context = {'form':form}
    
    return render(request, template_url, context)

@login_required
def profile(request):
    
    # check if user has profile or create one
    user_profile = None 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        print(f"UserProfile does not exists")
        user_profile = Profile(user=request.user, bio='Enter Bio')
        user_profile.save()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-home')
        else:
            print(f"error in the profile updation {u_form} {p_form}")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    template_url = f"{app_base_ref}/user/profile.html"
    return render(request, template_url, context)


