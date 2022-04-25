from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, Django")


def home(request):
    text = "plain text"
    context = {'text': text}
    return render(request, 'home.html', context)

#
# def decode(request):
#     text = "string"
#     ciphertext = ""
#     context = {'text': text}
#     return render(request, 'home.html', context)


def encrypt(request):
    if 'plain_text' in request.GET:
        ciphertext = request.GET['plain_text']+"ciphertext"
        context = {'ciphertext': ciphertext}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


def decode(request):
    if 'cipher_text' in request.GET:
        plaintext = request.GET['cipher_text']+"plaintext"
        context = {'plaintext': plaintext}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
