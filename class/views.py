from django.http import HttpResponse
from django.shortcuts import render

from dashboard.models import ClassSession

def index(request):
    return render(request, "class/index.html", {"banner_msg": ""})

def guest_join(request):
    single_jsonify = lambda key, val: f"{{\"{key}\": {val}}}"
    req_get = request.GET
    guest_username = req_get.get("username", "Anonymous")
    class_route_id = req_get.get("classID", "")
    class_session = ClassSession.objects.filter(route_id=class_route_id).first()
    if class_session is None:
        return HttpResponse(single_jsonify("bannerMsg", "\"Invalid class ID.\""))
    if not class_session.in_session:
        return HttpResponse(single_jsonify("bannerMsg", "\"Class is not in session.\""))
    if class_session.signin_required:
        return HttpResponse(single_jsonify("bannerMsg", "\"Class requires sign-in.\""))
    class_session.mark_student(guest_username)
    class_session.save()
    request.session["username"] = guest_username
    request.session["is_guest"] = True
    return HttpResponse(single_jsonify("redir", "true"))

def instructor_class(request, route_id):
    return HttpResponse("IC")

def student_class(request, route_id):
    return HttpResponse("SC")
