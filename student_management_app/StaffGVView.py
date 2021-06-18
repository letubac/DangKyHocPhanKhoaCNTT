from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel,  FeedBackStaffs_GV,Staffs_GV_HP,Time_subject,THUCHANH,Nhom_TH


def staff_gv_home(request):
    return render(request, "staff_gv_template/staff_home_template.html")
def staff_gv_feedback(request):
    staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs_GV.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_gv_template/staff_feedback_template.html", context)


def staff_gv_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_gv_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs_GV(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_gv_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_gv_feedback')
def staff_gv_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs_GV_HP.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_gv_template/staff_profile.html', context)
def add_room(request):

    return render(request, 'staff_gv_template/add_room_template.html')
def add_room_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_room')
    else:
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        so_tc = request.POST.get('so_tc')
        tongsvdk = request.POST.get('tongsvdk')
        nienkhoa =request.POST.get('nienkhoa')
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff,so_tc=so_tc,tongsvdk=tongsvdk,nienkhoa=nienkhoa)
            subject.save()
            messages.success(request, "Thêm Phòng Học Thành Công!")
            return redirect('add_room')
        except:
            messages.error(request, "Thêm Phòng Học Thất Bại!")
            return redirect('add_room')




def staff_gv_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_gv_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs_GV_HP.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Cập Nhật Thành Công")
            return redirect('staff_profile')
        except:
            messages.error(request, "Cập Nhật Thất Bại")
            return redirect('staff_gv_profile')
# session
def manage_session_gv(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "staff_gv_template/manage_session_template.html", context)


def add_session_gv(request):
    return render(request, "staff_gv_template/add_session_template.html")


def add_session_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session_gv")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session_gv")


def edit_session_gv(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "staff_gv_template/edit_session_template.html", context)


def edit_session_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session_gv')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session_gv/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session_gv/'+session_id)


def delete_session_gv(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session_gv')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session_gv')
#time study subject
def manage_time_study(request):
    session_years = Time_subject.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "staff_gv_template/manage_time_study_template.html", context)

def add_time_study_gv(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "staff_gv_template/add_time_study_template.html",context)
def add_time_study_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        course_id = request.POST.get('course')
        course =SessionYearModel.objects.get(id=course_id)
        try:
            tghoc = Time_subject(start_day=start_day, end_day=end_day,Mahocki=course)
            tghoc.save()
            messages.success(request, "Thêm TG Học Thành Công!")
            return redirect("add_time_study_gv")
        except:
            messages.error(request, "Thêm TG Học Thất Bại")
            return redirect("add_time_study_gv")
def edit_time_study(request, Study_id):
    tghoc = Time_subject.objects.get(ID_time=Study_id)
    session_years = SessionYearModel.objects.all()
    context = {
        "tghoc": tghoc,
        "session_years": session_years,
        "ID_time":Study_id,

    }
    return render(request, 'staff_gv_template/edit_time_study_template.html', context)


def edit_time_study_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        Study_id=request.POST.get('Study_id')
        start_day = request.POST.get('start_day')
        end_day = request.POST.get('end_day')
        course_id = request.POST.get('course')
        course = SessionYearModel.objects.get(id=course_id)
        try:
            tghoc = Time_subject.objects.get(ID_time=Study_id)

            tghoc.start_day = start_day
            tghoc.end_day = end_day
            tghoc.Mahocki = course
            tghoc.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_time_study/' + Study_id)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_time_study/' + Study_id)


def delete_time_study(request, Study_id):
    tghoc = Time_subject.objects.get(ID_time=Study_id)
    try:
        tghoc.delete()
        messages.success(request, "Xoá Môn Học Thành Công.")
        return redirect('manage_time_study')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_time_study')
#thuc hanh
def add_thuchanh_gv(request):

    return render(request, 'staff_gv_template/add_thuchanh_template.html')
def manage_thuchanh_gv(request):
    thuchanh = THUCHANH.objects.all()
    context = {
        "thuchanh": thuchanh
    }
    return render(request, "staff_gv_template/manage_thuchanh_template.html", context)

def add_thuchanh_gv_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        MATH = request.POST.get('MATH')
        soTietTH = request.POST.get('soTietTH')

        try:
            thuchanh = THUCHANH(MATH=MATH, soTietTH=soTietTH)
            thuchanh.save()
            messages.success(request, "Thêm  Thành Công!")
            return redirect("add_thuchanh_gv")
        except:
            messages.error(request, "Thêm  Thất Bại")
            return redirect("add_thuchanh_gv")
def edit_thuchanh_study(request, maTH):
    thuchanh = THUCHANH.objects.get(MATH=maTH)
    context = {
        "thuchanh": thuchanh,

    }
    return render(request, 'staff_gv_template/edit_thuchanh_template.html', context)


def edit_thuchanh_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:

        MATH = request.POST.get('MATH')
        soTietTH = request.POST.get('soTietTH')
        try:
            thuchanh = THUCHANH.objects.get(MATH=MATH)
            thuchanh.soTietTH = soTietTH
            thuchanh.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_thuchanh_study/' + MATH)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_thuchanh_study/' + MATH)


def delete_thuchanh_study(request, maTH):
    tghoc = THUCHANH.objects.get(MATH=maTH)
    try:
        tghoc.delete()
        messages.success(request, "Xoá Thực Hành Thành Công.")
        return redirect('manage_thuchanh_gv')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_thuchanh_gv')
#nhom thuc hanh
def add_nhom_TH(request):
    tghoc = THUCHANH.objects.all()
    context = {
        "tghoc": tghoc
    }
    return render(request, 'staff_gv_template/add_nhomTH_template.html',context)
def manage_nhomTH_gv(request):
    nhomth = Nhom_TH.objects.all()
    context = {
        "nhomth": nhomth,
    }
    return render(request, "staff_gv_template/manage_nhomTH_template.html", context)

def add_nhomTH_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:

        math_id = request.POST.get('course')
        MATH = THUCHANH.objects.get(MATH=math_id)
        startday_TH = request.POST.get('startday_TH')
        end_day = request.POST.get('end_day')
        name_nhom = request.POST.get('name_nhom')
        try:
            thuchanh = Nhom_TH(MATH=MATH, startday_TH=startday_TH,endday_TH=end_day,name_nhom=name_nhom)
            thuchanh.save()
            messages.success(request, "Thêm  Thành Công!")
            return redirect("add_nhom_TH")
        except:
            messages.error(request, "Thêm  Thất Bại")
            return redirect("add_nhom_TH")
def edit_nhomTH_study(request, maTH):
    tghoc = Nhom_TH.objects.get(MATH=maTH)
    context = {
        "tghoc": tghoc,


    }
    return render(request, 'staff_gv_template/edit_nhomTH_template.html', context)


def edit_nhomTH_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:


        MATH = request.POST.get('MATH')
        startday_TH = request.POST.get('startday_TH')
        endday_TH = request.POST.get('endday_TH')
        name_nhom = request.POST.get('name_nhom')
        try:
            thuchanh = Nhom_TH.objects.get(MATH=MATH,startday_TH=startday_TH,endday_TH=endday_TH,name_nhom=name_nhom)

            thuchanh.save()
            messages.success(request, "Cập Nhật Thành Công.")
            return redirect('/edit_nhomTH_study/' + MATH)
        except:
            messages.error(request, "Cập Nhật Thất Bại.")
            return redirect('/edit_nhomTH_study/' + MATH)


def delete_nhomTH_study(request, id):
    tghoc = Nhom_TH.objects.get(id=id)
    try:
        tghoc.delete()
        messages.success(request, "Xoá  Thành Công.")
        return redirect('manage_nhomTH_gv')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_nhomTH_gv')
#manage subject
def add_subject_gv(request):

    staffs = CustomUser.objects.filter(user_type='2')
    time_subject=Time_subject.objects.get.all()
    thuchanhs=THUCHANH.objects.get.all()
    context = {
        "time_subject":time_subject,
        "staffs": staffs,
        "thuchanhs":thuchanhs,
    }
    return render(request, 'hod_template/add_subject_template.html', context)

def manage_subject_gv(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'staff_gv_template/manage_subject_template.html', context)
def add_subject_gv(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    time_subjects = Time_subject.objects.all()
    thuchanhs = THUCHANH.objects.all()
    context = {
        "courses": courses,
        "staffs": staffs,
        "time_subjects":time_subjects,
        "thuchanhs":thuchanhs,
    }
    return render(request, 'staff_gv_template/add_subject_template.html', context)



def add_subject_save_gv(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject_gv')
    else:
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        so_tc = request.POST.get('so_tc')
        tongsvdk = request.POST.get('tongsvdk')
        nienkhoa =request.POST.get('nienkhoa')
        i_time= request.POST.get('ID_time')
        id_time=Time_subject.objects.get(ID_time=i_time)
        th_id=request.POST.get('MATH')
        math=THUCHANH.objects.get(MATH=th_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff,so_tc=so_tc,tongsvdk=tongsvdk,nienkhoa=nienkhoa,
                               ID_time=i_time,MATH= th_id)

            subject.save()
            messages.success(request, "Thêm Môn Học Thành Công!")
            return redirect('add_subject_gv')
        except:
            messages.error(request, "Thêm Môn Học Thất Bại!")
            return redirect('add_subject_gv')


def edit_subject_gv(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id,

    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save_gv(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        so_tc = request.POST.get('so_tc')
        tongsvdk = request.POST.get('tongsvdk')
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.so_tc = so_tc
            subject.tongsvdk = tongsvdk
            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff

            subject.save()

            messages.success(request, "Cập Nhật Môn Học Thành Công.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))

        except:
            messages.error(request, "Cập Nhật Môn Học Thất Bại.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
            # return redirect('/edit_subject/'+subject_id)


def delete_subject_gv(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Xoá Môn Học Thành Công.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Xoá Thất Bại ! Thử Lại.")
        return redirect('manage_subject')