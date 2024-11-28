from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from dashboard.models import ClassSession
from login.models import User, get_user
from util import SessionState, check_session

def index(request):
    session_state = SessionState(from_dict=request.session.get(
        "state", 
        SessionState().to_dict()
    ))
    if not session_state.signed_in:
        return HttpResponseRedirect(reverse("login_index"))
    if session_state.is_instructor:
        return HttpResponseRedirect(reverse("instructor_dashboard"))
    return HttpResponseRedirect(reverse("student_dashboard"))

def instructor_dashboard(request):
    redir, redir_name = check_session(request, instructor_only=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    user = get_user(request)
    return render(request, "dashboard/instructor.html", {
        "classes": user.classsession_set.order_by("-creation")
    })

def student_dashboard(request):
    redir, redir_name = check_session(request, instructor_only=False)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    return render(request, "dashboard/student.html")

def create_class(request):
    redir, redir_name = check_session(request, instructor_only=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    form = request.POST
    class_name = form.get("class-name")
    signin_required = form.get("signin-required")
    if len(class_name) == 0:
        return render(request, "dashboard/instructor.html", {
            "banner_msg": "Invalid parameters."
        })
    new_class = ClassSession(
        name=class_name, 
        signin_required=bool(signin_required), 
        owner=get_user(request)
    )
    new_class.save()
    return HttpResponseRedirect(reverse("instructor_class", args=[new_class.route_id]))

def join_class(request):
    redir, redir_name = check_session(request, instructor_only=False)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    class_route_id = request.POST.get("route-id")
    class_session = ClassSession.objects.filter(route_id=class_route_id).first()
    if class_session is None:
        return render(request, "dashboard/student.html", {
            "banner_msg": "Invalid class ID."
        })
    if not class_session.in_session:
        return render(request, "dashboard/student.html", {
            "banner_msg": "Class is not in session."
        })
    class_session.mark_student(request.session.get("username"))
    class_session.save()
    return HttpResponseRedirect(reverse("student_class", args=[class_route_id]))
