
from urna.forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'login/register.html', {'form': form})