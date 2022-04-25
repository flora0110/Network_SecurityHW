from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, Django")


def home(request):
    text = "plain text"
    context = {'text': text}
    return render(request, 'home.html', context)


def encrypt(request):
    if 'plain_text' in request.GET:
        # ciphertext = request.GET['plain_text']+"ciphertext"
        ciphertext = Encryption(request.GET['plain_text'], request.GET['key'])
        context = {'ciphertext': ciphertext}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')


def decode(request):
    if 'cipher_text' in request.GET:
        plaintext = Decryption(request.GET['cipher_text'], request.GET['key'])
        context = {'plaintext': plaintext}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')
#generation of key


def P10(key):  # 3 5 2 7 4 10 1 9 8 6
    return key[2] + key[4] + key[1] + key[6] + key[3] + key[9] + key[0] + key[8] + key[7] + key[5]


def LS1(key):
    return key[1] + key[2] + key[3] + key[4] + key[0] + key[6] + key[7] + key[8] + key[9] + key[5]


def P8(key):  # 6 3 7 4 8 5 10 9
    return key[5] + key[2] + key[6] + key[3] + key[7] + key[4] + key[9] + key[8]


def LS2(key):
    return key[2] + key[3] + key[4] + key[0] + key[1] + key[7] + key[8] + key[9] + key[5] + key[6]

#encryption and decryption


def IP(str):  # 2 6 3 1 4 8 5 7
    return str[1] + str[5] + str[2] + str[0] + str[3] + str[7] + str[4] + str[6]


def EP(str):  # 4 1 2 3 2 3 4 1
    return str[3] + str[0] + str[1] + str[2] + str[1] + str[2] + str[3] + str[0]


def xor(str1, key):
    if(len(str1) == 4):
        output = str(int(str1[0]) ^ int(key[0])) + str(int(str1[1]) ^ int(key[1])) + \
                     str(int(str1[2]) ^ int(key[2])) + \
                         str(int(str1[3]) ^ int(key[3]))
    else:
        output = str(int(str1[0]) ^ int(key[0])) + str(int(str1[1]) ^ int(key[1])) + str(int(str1[2]) ^ int(key[2])) + str(int(str1[3]) ^ int(key[3])) + \
               str(int(str1[4]) ^ int(key[4])) + str(int(str1[5]) ^ int(key[5])) + \
                   str(int(str1[6]) ^ int(key[6])) + \
                       str(int(str1[7]) ^ int(key[7]))

    return output


def SBox(str):
    s0 = [["01", "00", "11", "10"],  # 1 0 3 2
          ["11", "10", "01", "00"],  # 3 2 1 0
          ["00", "10", "01", "11"],  # 0 2 1 3
          ["11", "01", "11", "10"]]  # 3 1 3 2

    s1 = [["00", "01", "10", "11"],  # 0 1 2 3
          ["10", "00", "01", "11"],  # 2 0 1 3
          ["11", "00", "01", "00"],  # 3 0 1 0
          ["10", "01", "00", "11"]]  # 2 1 0 3

    row0 = 2 * int(str[0]) + 1 * int(str[3])
    column0 = 2 * int(str[1]) + 1 * int(str[2])

    row1 = 2 * int(str[4]) + 1 * int(str[7])
    column1 = 2 * int(str[5]) + 1 * int(str[6])

    return s0[row0][column0] + s1[row1][column1]


def P4(str):  # 2 4 3 1
    return str[1] + str[3] + str[2] + str[0]


def IP_RE(str):  # 4 1 3 5 7 2 8 6
    return str[3] + str[0] + str[2] + str[4] + str[6] + str[1] + str[7] + str[5]


def Encryption(str, key):
    key1 = P8(LS1(P10(key)))
    key2 = P8(LS2(LS1(P10(key))))

    #first round
    str_ip = IP(str)

    temp_output1 = xor(str_ip[0:4], P4(SBox(xor(EP(str_ip[4:8]), key1))))

    temp_output2 = xor(str_ip[4:8], P4(SBox(xor(EP(temp_output1), key2))))

    #second round
    str = temp_output2 + temp_output1

    str = IP_RE(str)

    return str


def Decryption(str, key):
    key1 = P8(LS1(P10(key)))
    key2 = P8(LS2(LS1(P10(key))))

    #first round
    str_ip = IP(str)

    temp_output1 = xor(str_ip[0:4], P4(SBox(xor(EP(str_ip[4:8]), key2))))

    temp_output2 = xor(str_ip[4:8], P4(SBox(xor(EP(temp_output1), key1))))

    #second round
    str = temp_output2 + temp_output1

    str = IP_RE(str)

    return str
