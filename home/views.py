from django.shortcuts import render,redirect
from .models import Fixed_routine,Needed,preferred_routine
from .classes import *
from .routine_maker import main as routine_func

# Create your views here.
def index(request):
    return render(request, "routine/index.html")

def fixed(request):
    if request.method=="POST":
        # request.session
        string=""
        title = request.POST.getlist("title")
        start = request.POST.getlist('start')
        end = request.POST.getlist('end')
        length = len(title)
        for i in range(length):
            t = title[i].replace("-","_")
            st = start[i]
            et = end[i]
            if t and st and et:
                string += f"{t} - {st} - {et}\n"
        f = Fixed_routine()
        f.data = string
        f.save()    
        request.session['fixed_id'] = f.id
        return redirect("needed")

    return render(request, "routine/fixed.html")

def needed_stuffs(request):
    if request.method=="POST":
        # request.session
        string=""
        title = request.POST.getlist("title")
        totalhour = request.POST.getlist('totalhour')
        totalminute = request.POST.getlist('totalminute')
        consistenthour = request.POST.getlist('consistenthour')
        consistentminute = request.POST.getlist('consistentminute')
        length = len(title)
        for i in range(length):
            t = title[i].replace("-","_")
            th = totalhour[i]
            if not th:
                th=0
            tm = totalminute[i]
            if not tm:
                tm=0
            ch = consistenthour[i]
            if not ch:
                ch=0
            cm = consistentminute[i]
            if not cm:
                cm=0
            if t:
                string += f"{t}_extra - {th}:{tm}:00 - {ch}:{cm}:00\n"
        f = Needed()
        f.data = string
        f.save()    
        request.session['needed_id'] = f.id
        return redirect("preferred")

    return render(request, "routine/needed.html")

def preferred(request):
    if request.method == "POST":
        # request.session
        string=""
        title = request.POST.getlist("title")
        start = request.POST.getlist('start')
        end = request.POST.getlist('end')
        length = len(title)
        for i in range(length):
            t = title[i].replace("-","_")
            st = start[i]
            et = end[i]
            if t and st and et:
                string += f"{t}_extra - {st} - {et}\n"
        f = preferred_routine()
        f.data = string
        f.save()
        print("Saved preferred data")
        request.session['preferred_id'] = f.id
        return redirect("result")

    #get the choices
    titles = set()

    #get the fixed routine with same ids
    # no = request.session.get('fixed_id',None)
    # if no == None:
        # return redirect("fixed")
    # fixed_data = Fixed_routine.objects.get(pk=no).data

    #get the needed titles
    no = request.session.get('needed_id',None)
    if no == None:
        print("From preferred: needed id is empty")
        return redirect("needed")
    needed_data = Needed.objects.get(pk=no).data

    for i in needed_data.split("\n"):
        if i:
            t = i.split("-")[0].strip().replace("_extra","")
            titles.add(t)
    titles = list(titles)
    return render(request, "routine/preferred.html" , context={
        "choices":titles
    })

def result(request):
    print("To result")
    #get the fixed data
    no = request.session.get('fixed_id',None)
    if no == None:
        return redirect("fixed")
    fixed_data = Fixed_routine.objects.get(pk=no).data

    #get the needed data
    no = request.session.get('needed_id',None)
    if no == None:
        print("From result to needed")
        return redirect("needed")
    needed_data = Needed.objects.get(pk=no).data
    no = request.session.get('preferred_id',None)
    if no == None:
        return redirect("preferred")
    preferred_data = preferred_routine.objects.get(pk=no).data

    
    rout = routine_func(fixed_data,needed_data,preferred_data)
    results = []
    for title in rout.data:
        title_updated = title.replace("_extra","").split(rout.symbol)[0]
        
        results.append(Result(title_updated,rout.data[title][0],rout.data[title][1]))
    
    
    return render(request,"routine/result.html",context = {
        "routine":results
    })