from hashlib import sha256
import inspect
import os
from random import randint

from django.http import HttpResponseRedirect
from django.urls import reverse
from dotenv import load_dotenv

load_dotenv()
logging = os.environ.get("LOGGING", "OFF") == "ON"

def stringify_attrs(*kargs):
    items = [str(item) for item in kargs]
    return " | ".join(items)

def sha256_hash(s):
    return sha256(s.encode("utf-8")).hexdigest()

class SessionState:
    def __init__(self, signed_in=False, is_instructor=False, from_dict=None):
        self.signed_in = signed_in
        self.is_instructor = is_instructor
        if from_dict is not None:
            self.signed_in = from_dict["signed_in"]
            self.is_instructor = from_dict["is_instructor"]
    
    def to_dict(self):
        return {"signed_in": self.signed_in, "is_instructor": self.is_instructor}

def check_session(request, instructor_only=True, allow_guest=False):
    session_state = SessionState(from_dict=request.session.get(
        "state", 
        SessionState().to_dict()
    ))
    if not session_state.is_instructor and allow_guest:
        return False, None
    if not session_state.signed_in:
        return True, "login_index"
    # Instructor
    if session_state.is_instructor:
        if instructor_only:
            return False, None
        return True, "instructor_dashboard"
    # Student
    if instructor_only:
        return True, "student_dashboard"
    return False, None

def generate_route_id():
    seed = hex(randint(0x0, 0xFFFFFF))[2:]
    route_id = sha256_hash(seed)[0:6]
    return route_id

def log_request(request):
    if not logging:
        return
    print(f"Request: Func: {inspect.stack()[1].function}, Session: {request.session.session_key} {[i for i in request.session.items()]}, GET: {list(request.GET.items())}, POST: {list(request.POST.items())}")
