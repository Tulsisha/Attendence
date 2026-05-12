from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import DailyAttendance
import datetime
import calendar


# ======================================================
# Registration Page
# ======================================================
def registr(request):
    return render(request, 'registr.html')


# ======================================================
# Register New User
# ======================================================
def registeruser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "registr.html", {"msg": "⚠️ Username already taken!"})

        User.objects.create_user(username=username, email=email, password=password)
        return render(request, "registr.html", {"msg": "✅ Successfully Registered!"})

    return render(request, "registr.html")


# ======================================================
# Login Page
# ======================================================
def loginn(request):
    return render(request, 'loginn.html')


# ======================================================
# Login Form Action
# ======================================================
def loginform(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/index')
        else:
            return render(request, 'loginn.html', {"msg": "❌ Invalid username or password!"})

    return redirect('/loginn')


# ======================================================
# Index Page (Employee Dashboard)
# ======================================================
@login_required
def index(request):
    records = DailyAttendance.objects.filter(user=request.user).order_by('-date')
    return render(request, "index.html", {
        "username": request.user.username,
        "records": records
    })


# ======================================================
# Punch In / Punch Out Function
# ======================================================
@login_required
def punch(request):
    user = request.user
    today = now().date()
    current_time = now()

    try:
        # If record exists → punch-out
        record = DailyAttendance.objects.get(user=user, date=today)

        if record.punch_out is None:
            record.punch_out = current_time
            record.save()
            return JsonResponse({'status': 'punchout', 'time': current_time.strftime('%H:%M:%S')})

        else:
            return JsonResponse({'status': 'already_punched', 'message': '⚠️ You already punched in & out today!'})

    except DailyAttendance.DoesNotExist:
        # Create punch-in
        DailyAttendance.objects.create(
            user=user,
            date=today,
            punch_in=current_time
        )
        return JsonResponse({'status': 'punchin', 'time': current_time.strftime('%H:%M:%S')})


# ======================================================
# Attendance Report (Admin View)
# ======================================================
@login_required
def attendance_report(request):
    if request.user.is_staff:
        records = DailyAttendance.objects.all().order_by('-date')
    else:
        records = DailyAttendance.objects.filter(user=request.user).order_by('-date')

    return render(request, 'attendance_report.html', {
        'records': records,
        'username': request.user.username
    })


# ======================================================
# Monthly Attendance (NEW FEATURE)
# ======================================================
# ======================================================
# Monthly Attendance (with colors)
# ======================================================
@login_required
def monthly_attendance(request):
    user = request.user

    month = request.GET.get("month")
    year = request.GET.get("year")

    today = now()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    total_days = calendar.monthrange(year, month)[1]

    records = DailyAttendance.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    record_dict = {r.date: r for r in records}

    office_start = datetime.time(9, 45)   # 9:45 AM
    half_day_out = datetime.time(13, 30)  # 1:30 PM

    monthly_data = []

    for day in range(1, total_days + 1):
        date_obj = datetime.date(year, month, day)

        # Sunday Holiday
        if date_obj.weekday() == 6:
            monthly_data.append({
                "day": day,
                "date": date_obj,
                "punch_in": "-",
                "punch_out": "-",
                "status": "holiday",
                "color": "black"
            })
            continue

        rec = record_dict.get(date_obj)

        # No attendance = Absent
        if not rec:
            monthly_data.append({
                "day": day,
                "date": date_obj,
                "punch_in": "-",
                "punch_out": "-",
                "status": "absent",
                "color": "orange"
            })
            continue

        punch_in_time = rec.punch_in.time() if rec.punch_in else None
        punch_out_time = rec.punch_out.time() if rec.punch_out else None

        # No punch out
        if not punch_out_time:
            status = "in_progress"
            color = "teal"

        # Half day
        elif punch_out_time <= half_day_out:
            status = "half_day"
            color = "brown"

        # Present
        elif punch_in_time and punch_in_time <= office_start:
            status = "present"
            color = "green"

        # Late
        else:
            status = "late"
            color = "red"

        monthly_data.append({
            "day": day,
            "date": date_obj,
            "punch_in": rec.punch_in.strftime("%I:%M %p") if rec.punch_in else "-",
            "punch_out": rec.punch_out.strftime("%I:%M %p") if rec.punch_out else "-",
            "status": status,
            "color": color
        })

    return render(request, "monthly_attendance.html", {
        "monthly_data": monthly_data,
        "year": year,
        "month": month
    })