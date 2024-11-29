from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from dashboard.models import ClassSession
from poll.models import Poll
from util import check_session

def create_poll(request, class_route_id):
    redir, redir_name = check_session(request, instructor_only=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    class_session = ClassSession.objects.filter(route_id=class_route_id).first()
    if class_session is None:
        return HttpResponse(status=404)
    new_poll = Poll(name="", owner=class_session)
    poll_name = request.POST.get("poll-name")
    if poll_name is None or len(poll_name) == 0:
        poll_name = f"Poll {new_poll.route_id}"
    new_poll.name = poll_name
    new_poll.save()
    return HttpResponseRedirect(
        reverse("poll_detail", args=[class_session.route_id, new_poll.route_id])
    )

def poll_detail(request, class_route_id, poll_route_id):
    redir, redir_name = check_session(request, instructor_only=True)
    if redir:
        return HttpResponseRedirect(reverse(redir_name))
    class_session = ClassSession.objects.filter(route_id=class_route_id).first()
    if class_session is None:
        return HttpResponse(status=404)
    poll = Poll.objects.filter(route_id=poll_route_id).first()
    if poll is None:
        return HttpResponse(status=404)
    form = request.POST
    poll_open_label = "poll-window" # Now it's a window.
    if poll_open_label in form:
        poll_open = form.get(poll_open_label)
        if poll_open == "open":
            poll.is_open = True
        elif poll_open == "close":
            poll.is_open = False
        poll.save()
    return render(request, "poll/detail.html", {
        "class_route_id": class_route_id, 
        "poll_route_id": poll_route_id, 
        "poll": poll,
        "answers": poll.answers
    })

def answer_poll(request, class_route_id):
    session = request.session
    form = request.POST
    if "username" not in session or "answer" not in form or "active-poll" not in form:
        return HttpResponse(status=403)
    answer = form.get("answer")
    active_poll = form.get("active-poll")
    poll = Poll.objects.filter(route_id=active_poll).first()
    back = HttpResponseRedirect(reverse("student_class", args=[class_route_id]))
    if poll is None:
        session["poll_msg"] = "Invalid poll ID." # Not a great way to send data.
        return back
    if not poll.is_open:
        session["poll_msg"] = "Poll expired."
        return back
    poll.add_answer(request.session["username"], answer)
    poll.save()
    session["poll_msg"] = "Submitted answer to poll." # Not a great way to send data.
    return back
