from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from dashboard.models import ClassSession
from poll.models import Poll
from util import SessionState, check_session, log_request

def index(request):
    log_request(request)
    return render(request, "class/index.html", {"banner_msg": ""})

# Yes, this function is nearly identical to the one in the dashboard app.
def guest_join(request):
    log_request(request)
    session = request.session
    single_jsonify = lambda key, val: f"{{\"{key}\": {val}}}"

    # Not guest.
    session_state = SessionState(from_dict=session.get(
        "state", 
        SessionState().to_dict()
    ))
    not_guest = False
    if session_state.signed_in:
        if session_state.is_instructor:
            return HttpResponse(single_jsonify("bannerMsg", "\"You are an instructor.\""))
        not_guest = True

    req_get = request.GET
    guest_username = req_get.get("username", "Anonymous")
    class_route_id = req_get.get("classID", "")
    if not_guest:
        guest_username = session["username"]
    class_session = ClassSession.objects.filter(route_id=class_route_id).first()
    if class_session is None:
        return HttpResponse(single_jsonify("bannerMsg", "\"Invalid class ID.\""))
    if not class_session.in_session:
        return HttpResponse(single_jsonify("bannerMsg", "\"Class is not in session.\""))
    if class_session.signin_required and not not_guest: # Shh, double negative.
        return HttpResponse(single_jsonify("bannerMsg", "\"Class requires sign-in.\""))
    class_session.mark_student(guest_username)
    class_session.save()
    session["username"] = guest_username
    if not not_guest: # Shh, double negative.
        session["is_guest"] = True
    return HttpResponse(single_jsonify("redir", "true"))

def instructor_class(request, route_id):
    log_request(request)
    redir, redir_name = check_session(request, instructor_only=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    class_session = ClassSession.objects.filter(route_id=route_id).first()
    if class_session is None:
        return HttpResponse(status=404)
    form = request.POST
    class_door_label = "class-door" # It's a metaphor for whether or not the literal door is open.
    if class_door_label in form:
        class_door = form.get(class_door_label)
        if class_door == "start":
            class_session.in_session = True
        elif class_door == "stop":
            class_session.in_session = False
        class_session.save()
    return render(request, "class/instructor.html", {
        "class": class_session, 
        "students": class_session.students, 
        "polls": class_session.poll_set.order_by("-creation")
    })

def student_class(request, route_id):
    log_request(request)
    redir, redir_name = check_session(request, instructor_only=False, allow_guest=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    class_session = ClassSession.objects.filter(route_id=route_id).first()
    if class_session is None:
        return HttpResponse(status=404)
    # Not a great way to get data.
    banner_msg = request.session.get("poll_msg", "")
    return render(request, "class/student.html", {
        "class": class_session, 
        "banner_msg": banner_msg, 
        "polls": class_session.poll_set.order_by("-creation")
    })
