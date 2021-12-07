from django.shortcuts import render, redirect
import random
from time import localtime, strftime

def process_money(request):
    limit = request.session['limit']
    target = request.session['target']
    if limit == 0 or target == 0:
        return redirect('/play/')
    location = request.POST['location']
    gold = 0
    message = ''
    time = strftime("%Y-%m-%d %H:%M %p", localtime())

    if location == 'farm':
        gold = random.randint(10,20)
    elif location == 'cave':
        gold = random.randint(5,10)
    elif location == 'house':
        gold = random.randint(2,5)
    else:  
        gold = random.randint(-50,50)

    if gold >= 0:
        message = f'Earned {gold} golds from the {location}! ({time})'
    else:
        message = f'Entered a {location} and lost {gold} golds... Ouch.. ({time})'

    request.session['money'] += gold
    request.session['message'].append(message)
    if request.session['target'] - gold < 0:
        request.session['target'] = 0
        request.session['message'].append('Congratulations, target Gold has been achieved! You WIN!')
    else:
        request.session['target'] -= gold
    if limit-1 == 0:
        request.session['message'].append('Number of moves has reached its limit! You LOSE!')
        request.session['limit'] = 0
    else:
        request.session['limit'] -= 1
    return redirect('/play/')

def set_limit(request):
    request.session['money'] = 0
    request.session['message'] = []
    request.session['limit'] = 0
    request.session['target'] = 0
    return render(request, 'start.html')

def index(request):
    if request.session['message'] == []:
        request.session['limit'] = int(request.POST['move_limit'])
        request.session['target'] = int(request.POST['gold_target'])
    return render(request, 'index.html')

def reset(request):
    request.session['money'] = 0
    request.session['message'] = []
    request.session['limit'] = 0
    request.session['target'] = 0
    return redirect('/')
