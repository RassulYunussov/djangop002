from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from .forms import *
from .models import *
import json
from django.http import JsonResponse
import string, random
from .tasks import send_emails
from django.http import HttpResponse, HttpResponseNotFound
import requests
from bs4 import BeautifulSoup
import datetime, pytz


def noCurator(request):
    return render(request, 'web/start.html')

def getProfileName(request):
    person = Profile.objects.get(user = request.user.username)
    text = person.name
    return text


def main_page(request, id=909555):
    if id is None:
        id = 909555
    sponsor_exists = Profile.objects.filter_exists(id)
    if sponsor_exists:
        return render(request, 'web/index.html', {'id': id})
    else:
        return HttpResponseNotFound()


def videos_page(request, id=909555, video=None, start=False):
    if id is None:
        id = 909555


    sponsor_exists = Profile.objects.filter_exists(id)

    social_links = []


    if sponsor_exists:
        sponsor = Profile.objects.get(user=id)

        if sponsor.telegram_name.__len__() > 13:
            record = {}
            record['ref'] = sponsor.telegram_name
            # record['img'] = '/static/media/telegram-foot-icon.png'
            record['img'] = '/static/media/telegram-icon.png'
            social_links.append(record)


        if sponsor.instagram.__len__() > 22:
            record = {}
            record['ref'] = sponsor.instagram
            # record['img'] = '/static/media/instagram-footer-icon.png'
            record['img'] = '/static/media/instagram-apple.png'
            social_links.append(record)

        if sponsor.phone.__len__() == 12:
            record1 = {}
            record1['ref'] = 'https://api.whatsapp.com/send?phone=' + sponsor.phone[1:]
            # record1['img'] = '/static/media/whatsapp-footer.png'
            record1['img'] = '/static/media/whatsapp-apple.png'
            social_links.append(record1)

        if sponsor.youtube.__len__() > 20:
            record = {}
            record['ref'] = sponsor.youtube
            # record['img'] = '/static/media/youtube-footer-icon.png'
            record['img'] = '/static/media/youtube-logo-apple.png'
            social_links.append(record)

        if sponsor.phone.__len__() == 12:
            record = {}
            record['ref'] = 'viber://add?number=' + sponsor.phone[1:]
            # record['img'] = '/static/media/viber-footer-icon.png'
            record['img'] = '/static/media/viber-apple.png'
            social_links.append(record)

        if sponsor.vk.__len__() > 15:
            record = {}
            record['ref'] = sponsor.vk
            # record['img'] = '/static/media/vk-footer-icon.png'
            record['img'] = '/static/media/vk-apple.png'
            social_links.append(record)

        if sponsor.facebook.__len__() > 21:
            record = {}
            record['ref'] = sponsor.facebook
            # record['img'] = '/static/media/facebook-footer-icon.png'
            record['img'] = '/static/media/facebook-apple.png'
            social_links.append(record)

        if sponsor.classmate.__len__() > 14:
            record = {}
            record['ref'] = sponsor.classmate
            # record['img'] = '/static/media/odnoklassniki_footer-icon.png'
            record['img'] = '/static/media/odnoklassniki-apple.png'
            social_links.append(record)

        if sponsor.twitter.__len__() > 20:
            record = {}
            record['ref'] = sponsor.twitter
            # record['img'] = '/static/media/twitter-footer-icon.png'
            record['img'] = '/static/media/twitter-apple.png'
            social_links.append(record)



        print(social_links)
        print(social_links.__len__())
        if start:
            return render(request, 'web/start.html', {
                'id': id,
                'profile': social_links,
                'video': video,
            })
        return render(request, 'web/video.html', {
            'id': id,
            'profile': social_links,
            'video': video,
        })
    else:
        return redirect('videos_page')


def new_id(request):
    return render(request, 'web/new_id.html', {})


@csrf_exempt
def filterCities(request):
    if request.method == 'POST':
        print(request.POST)
        val = request.POST.get('country')
        if val is None:
            id = request.POST.get('id')
            # check if id is not fucked up being 1 =:> 000001
            if len(id) < 6:
                id = "0"*(6-len(id)) + str(id)
            print(id)
            ##finish check
            prof = Profile.objects.get(user=id)
            return JsonResponse({'city': prof.city.name, 'country': prof.country.name})

        if (val is "") or ("---" in val):
            cities = City.objects.all().order_by("country")
            country = Country.objects.all()
        else :
            country = Country.objects.get(name=val)
            cities = City.objects.all().filter(country=country.pk)
        if cities.exists():
            result = {}
            for countr in country:
                result[countr.name] = []
            for city in cities:
                result[city.country.name].append(city.name)
            return JsonResponse(result)
        else:
            return JsonResponse({'error': 'sorry, fuckoff'})

    else:
        return JsonResponse({'error': 'sorry, fuckoff'})

@csrf_exempt
def vilaviActivity(request):
    if request.method == 'POST':
        ul = request.POST.get('ul')
        id = request.POST.get('id')
        print("UL HAVE ARRIVED")
        print(id)
        print(ul)


        # profile = get_object_or_404(Profile, user=id)
        # treeObj = Tree.objects.filter(profile = profile).filter(ul = ul)[0]
        # listWithValues = []
        # treeObj.__setattr__("active", not treeObj.active)
        # treeObj.save()
        # a = {'name': treeObj.ul}
        # if treeObj.active:
        #     if treeObj.ua == "Активность не выполнена":
        #         a['color'] = "#ff4d4d" #red
        #     else:
        #         a['color'] = "#1a8cff" #blue
        #
        # else:
        #     a['color'] = "#37474f" #grey
        #
        # listWithValues.append(a)
        # return JsonResponse( {'not_active_node': [ul]} )

        if id == ul:
            return JsonResponse({ 'node_list': [] })
        profile = get_object_or_404(Profile, user = id)
        # grandNode = dataForTreeFromTable(forD3=False, profileObject=profile, onlyActive=False)
        # targetNode = findNode(grandNode, request.POST.get('ul'))
        # children_list = findChildren(targetNode, targetNode['level'])
        # NodeAndChildren = Tree.objects.filter(profile = profile).filter(ul__in = children_list)
        NodeAndChildren = Tree.objects.filter(profile = profile).filter(ul = ul)
        # for a in NodeAndChildren:
        #     print(str(a))
        listWithValues = []


        marker =  NodeAndChildren[0].active
        for object in NodeAndChildren:
            if marker:
                object.__setattr__("active", False)
            else:
                object.__setattr__("active", True)

            object.save()
            a = {'name': object.ul}
            if marker:
                if object.ua == "Активность не выполнена":
                    a['color'] = "#ff4d4d"
                else:
                    a['color'] = "#1a8cff"
            else:
                a['color'] = "#37474f"

            listWithValues.append(a)
            # if value = 0:
        return JsonResponse({ 'node_list': listWithValues })

    else:
        return JsonResponse({ 'error': 'sorry, fuckoff' })


# def findNotActiveChildren(node):
#     marker = node['active']
#     children_list = findChildren(node, node['level'])
#
#     marker =  NodeAndChildren[0].active
#     for object in NodeAndChildren:
#         if marker:
#             object.__setattr__("active", False)
#         else:
#             object.__setattr__("active", True)
#         object.save()
#         # if value = 0:
#     return JsonResponse({ 'not_active_node': children_list })


@csrf_exempt
def vilaviQualification(request):
    if request.method == 'GET':
        query = VilaviFetch.objects.values_list("q")
        res = {"qualifications": []}
        for record in query:
            if record[0] not in res["qualifications"]:
                res["qualifications"].append(record[0])
        print(json.dumps(res))
        return JsonResponse(res)
    else:
        return JsonResponse({})


@csrf_exempt
def vilaviLevel(request):
    if request.method == 'GET':
        query = VilaviFetch.objects.values_list("g")
        res = {"levels": []}
        for record in query:
            if record[0] not in res["levels"]:
                res["levels"].append(record[0])
        res["levels"].sort()
        a = ""
        print(json.dumps(res))
        return JsonResponse(res)
    else:
        return JsonResponse({})


@csrf_exempt
def profileEmailExist(request):
    # print(request.POST.get('username'))
    # return JsonResponse({})
    if request.method == 'POST':
        print(request.POST.get('username'))
        query = Profile.objects.filter(name = request.POST.get('username'))
        print(query)
        if (query.count() == 1) and (query[0].email is not None) and (query[0].email.__len__() > 0):
            return JsonResponse( { 'exist': 1 } )

    return JsonResponse( { 'exist': 0} )


@csrf_exempt
def profileDeactivate(request):
    if request.method == 'POST':
        result = {}
        parent_name = request.POST.get('parent')
        parent = get_object_or_404(Profile, name = parent_name)
        child = request.POST.get('user')
        grandNode = dataForTreeFromTable(forD3 = False, profileObject = parent, onlyActive = False)
        node = findNode(grandNode, parent.user)
        childList = findChildren(node, node['level'])

        if int(child) in childList:
            result['isChild'] = 1
            prof = Profile.objects.get(user = int(child))
            prof.active = not prof.active
            prof.save()
            print(prof.active)
            result['active'] = prof.active
        else:
            result['isChild'] = 0

        return JsonResponse(result)

@csrf_exempt
def profileInfo(request):
    if request.method == "POST":
        result = {}
        attribute = request.POST.get('by')
        if attribute == 'id':
            id = request.POST.get('id')
            obj = get_object_or_404(Profile, user = id)
            result['id'] = obj.user
            result['name'] = obj.name
            result['isAdmin'] = 0
            result['active'] = obj.active
            if int(obj.user) == 909555:
                result['isAdmin'] = 1

        elif attribute == 'name':
            name = request.POST.get('name')
            obj = get_object_or_404(Profile, name = name)
            result['id'] = obj.user
            result['name'] = obj.name
            result['isAdmin'] = 0
            result['active'] = obj.active
            if int(obj.user) == 909555:
                result['isAdmin'] = 1
    return JsonResponse(result)


class ForgetPasswordView(View):
    form_class = ForgetPasswordForm
    template_name = 'web/forget_password.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        forget_form = self.form_class(request.POST)
        email = request.POST.get('email')
        try:
            user = Profile.objects.get(email = email).user
            password = ''.join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(12))
            user.set_password(password)
            user.save()
            send_emails(email, password, user)
            return HttpResponse("Сообщение отправленно на вашу электронную почту")
        except Profile.DoesNotExist:
            return render(request, self.template_name, {'form': forget_form})


def findChildren(node, baseLevel):
    children = []
    children.append(node['name'])

    # print("LLLLLLLLLLLLLEEEEEEEEEEEEEEEEEVVVVVVVVVVVVVVEEEEEEEEEEEEELLLLLLLLLLLLL")
    # print(node["level"])
    if node["level"] == 0:
        node["level"] = node["level"] - (1+baseLevel)
    else:
        node["level"] = node["level"] - baseLevel
    # print(node["level"])

    if 'children' in node:
        if node['children'].__len__() > 0:
            for child in node['children']:
                chilist = findChildren(child, baseLevel)
                for a in chilist:
                    if a not in children:
                        children.append(a)
    return children

def findNode(node, target):
    # print(node['name'])
    # print(type(node['name']))
    # print(target)
    # print(type(target))
    if str(node['name']) == target:
        print("here")
        return node
    if ('children' in node) and (node['children'].__len__() > 0):
        for child in node['children']:
            n = findNode(child, target)
            if n:
                print("there")
                return n
    print("over there")
    return None





def dataForTreeFromTable(forD3, profileObject, onlyActive):
    data = []
    # rows = VilaviFetch.objects.all()
    print("MYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYPROFILE")
    rows = Tree.objects.filter(profile = profileObject).order_by("g")

    print(rows)

    if onlyActive:
        rows = rows.filter(active = True)

    print(rows.count())


    for row in rows:
        active = row.active

        list_over = Tree.objects.filter_activity(0).filter(profile=profileObject)
        list_norm = Tree.objects.filter_activity(1).filter(profile=profileObject)
        list_under = Tree.objects.filter_activity(2).filter(profile=profileObject)
        if row in list_over:
            activity = 0
        elif row in list_norm:
            activity = 1
        if row in list_under:
            activity = 2

        if active:
            if activity == 0:
                ncolor = "#1a8cff"
                color = "#1a8cff"
            elif activity == 1:
                ncolor = "#53ff1a"
                color = "#53ff1a"
            else:
                ncolor = "#ff4d4d"
                color = "#ff4d4d"


        else:
            ncolor = "#37474f"
            color = "#37474f"


        a = {

            "id": row.uid,
            "pid": row.sid,
            "name": row.ul,
            "level": int(row.g),
            "number_of_show": row.numberOfShow,
            "last_time_show": str(row.lastTimeShow)[:19],
            "belong_to": profileObject.user,

        }
        if forD3:
            a['color'] = color # color of parent connection and text
            a['ncolor'] = ncolor # color of node
            a['fullName'] = row.un
            a['gpv'] = row.gpv
            a['phone'] = row.up
            a['qual'] = row.q
        else:
            a['active'] = row.active # added if tree is not used for d3 diagram construction
        data.append(a)
    # return data

    if data.__len__() != 0:
        data[0]['pid'] = ''  # import if not 909555, will crush otherwise

    print(data)



    out = {
    }

    for p in data:
        pid = p['pid'] or 'root'
        out.setdefault(pid, {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[pid]['children'].append(out[p['id']])
    # print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTT')
    # print(json.dumps(out, indent=4))

    # print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUTTTTTTTTTTTTTTTTT')
    # tree = out[data['pid']]['children'][0]
    tree = {}
    if out.__len__() != 0:
        tree = out['root']['children'][0]


    def lookForNull(something):
        if something.__len__() == 0:
            return
        if isinstance(something, dict):
            if bool(something['children']) is False:
                del something['children']
            else:
                lookForNull(something['children'])
        else:
            for a in something:
                lookForNull(a)

    lookForNull(tree)
    if 'children' not in tree:
        tree['children'] = []

    return tree


def dataForTreeFromVilavi():
    data = []
    rows = VilaviFetch.objects.all()
    for row in rows:

        a = {

            "id": row.uid,
            "pid": row.sid,
            "name": row.ul,
            "level": int(row.g),
        }

        data.append(a)
    out = {
    }

    for p in data:
        pid = p['pid'] or 'root'
        out.setdefault(pid, {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[pid]['children'].append(out[p['id']])
    tree = out['root']['children'][0]

    def lookForNull(something):
        if isinstance(something, dict):
            if bool(something['children']) is False:
                del something['children']
            else:
                lookForNull(something['children'])
        else:
            for a in something:
                lookForNull(a)

    lookForNull(tree)
    return tree



def traverseTree(node):

    # print('------------------------------------------')
    if node['active'] is True:
        if "children" in node:
            if node['children'].__len__() > 0:
                if node['children'].__len__() == 1:
                    if foundOneNodeWithOneChildren(node):
                        return node
                # node['children'].sort(key=lambda x: (findHeight, countChildren))
                # node['children'].sort(key=lambda item: item['last_time_show'], reverse=True)
                if node['children'].__len__() >= 2:
                    print("UNSOOOOOORTED")
                    for a in node['children']:
                        print(a['name'])
                    print("UNSOOOOOORTED")
                    res = []
                    print("SOOOOOORTED")
                    for a in node['children']:
                        if a['active']:
                            res.append(a)
                    node['children'] = res  # get rid of not active nodes
                    node['children'].sort(key=findHeight)
                    node['children'].sort(key=countChildren)
                    for b in node['children']:
                        print(b['name'])
                    print("SOOOOOORTED")

                    # node['children'].sort(key=lambda item: item['number_of_show'])

                    for child in node['children']:
                        record = traverseTree(child)
                        if record is not None:
                            return record

                # return toShow(node)
            else:
                return toShow(node)

        else:
            return toShow(node)
    else:
        return None

def compareLastTimeShow(lastTimeShow):
    #TRUE IF 10 minutes have passed
    sets = SuperAdminSettings.objects.all()[0]
    now = timezone.now()
    year = int(lastTimeShow[:4])
    month = int(lastTimeShow[5:7])
    day = int(lastTimeShow[8:10])
    hour = int(lastTimeShow[11:13])
    minute = int(lastTimeShow[14:16])
    second = int(lastTimeShow[17:19])
    lts = datetime.datetime(year, month, day, hour, minute, second, tzinfo=pytz.UTC)
    print("NOW: " + str(now))
    print("THEN: " + str(lts))
    difference = now - lts
    print("DIF: " + str(difference.seconds))
    differenceInMin = difference.seconds / 60
    if (differenceInMin > sets.registrationTime):
        return True
    else:
        return False


def toShow(node):
    profile = Profile.objects.get(user = node['belong_to'])
    obj = Tree.objects.filter(profile = profile).get(ul=node['name'])
    print(node['name'])
    print(node['number_of_show'])
    print(node['last_time_show'])



    if node['name'] == int(node['belong_to']):
        if node['children'].__len__() >= 2:
            return None



    if node['number_of_show'] < 2:
        node['number_of_show'] += 1
        obj.numberOfShow = node['number_of_show']
        obj.save()
        if node['number_of_show'] == 2:
            node['last_time_show'] = str(timezone.now())[:19]
            obj.lastTimeShow = timezone.now()
            obj.save()
        return node

    else:
        if compareLastTimeShow(node['last_time_show']):
            node['number_of_show'] = 1
            obj.numberOfShow = node['number_of_show']
            obj.save()
            return node
        else:
            return None


def foundOneNodeWithOneChildren(node):
    if compareLastTimeShow(node['last_time_show']):
        profile = Profile.objects.get(user=node['belong_to'])
        obj = Tree.objects.filter(profile=profile).get(ul=node['name'])
        obj.numberOfShow = 2
        obj.lastTimeShow = timezone.now()
        obj.save()
        return True
    return False

def countChildren(node):
    childrenNum = 0
    if "children" in node:
        res = []
        for a in node['children']:
            if a['active']:
                res.append(a)
        node['children'] = res
        if node['children'].__len__() > 0:
            for child in node['children']:
                childrenNum += 1
                childrenNum += countChildren(child)
    # print(node['name'] + ' has    '+ str(childrenNum) + '    children')
    return childrenNum



def findHeight(node):
    height = 0
    if 'children' in node:
        res = []
        for a in node['children']:
            if a['active']:
                res.append(a)
        node['children'] = res
        if node['children'].__len__() > 0:
            for child in node['children']:
                height = max(height, findHeight(child))
    # print(node['name'] + ' is    '+ str(height+1) + '    level high')
    return height + 1



@csrf_exempt
def vilaviSponsorId(request):
    if request.method == "POST":

        allChildrenDeactivated = False
        profile = get_object_or_404(Profile, user=request.POST.get('id'))
        data = dataForTreeFromTable(forD3=False, profileObject=profile, onlyActive=False)
        if data['children'].__len__() == 0 or data['children'].__len__() == 1:
            output = data
        else:
            if not atLeastOneChildrenIsActive(data):
                return JsonResponse(data['name'], safe=False)
            output = traverseTree(data)
        print("MYMHYMYNYMYMHMHs")
        print(output)
        if output is None:
            output = {'name': ''}

        return JsonResponse(output['name'], safe=False)

def atLeastOneChildrenIsActive(node):
    for a in node['children']:
        if a['active']:
            return True
    return False

@csrf_exempt
def timeRemaining(request):
    if request.method == "POST":

        profile = get_object_or_404(Profile, user=request.POST.get('id'))
        data = Tree.objects.filter(profile=profile)
        sets = SuperAdminSettings.objects.all()[0]
        result = sets.inactiveTime*60 # 10 minutes in seconds
        cur_time = timezone.now()
        for record in data:
            dif = leastTimeLeft(record.lastTimeShow, cur_time)
            if dif < result and dif > 0:
                result = dif
        return JsonResponse({'result': result})

def leastTimeLeft(lastTimeShow, currentTime):
    difference = currentTime - lastTimeShow; sets = SuperAdminSettings.objects.all()[0]
    print("DIIIIIIIIIIIIIIIIIIIIIIIFFFFFFFFFFFFFFFFFF")
    print(sets.inactiveTime*60)
    print(difference.seconds)
    return (sets.inactiveTime*60) - difference.seconds



@csrf_exempt
def getTimerValues(request):
    sets = SuperAdminSettings.objects.all()[0]
    res = {}
    res['registration_time'] = sets.registrationTime
    res['inactive_time'] = sets.inactiveTime
    return JsonResponse(res)
