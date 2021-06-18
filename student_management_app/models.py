from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"),(4, "Staffs_GV_HP"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=15)



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#gv giang day
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    profile_pic = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday=models.CharField(null=True,max_length=30)
    objects = models.Manager()

class PHIEUDK_DAY(models.Model):
    MAGV=models.ForeignKey(Staffs,on_delete=models.CASCADE,primary_key=True)
    tongmonday=models.IntegerField()
    objects = models.Manager()
class Detail_phieudkday(models.Model):
    id = models.AutoField(primary_key=True)
    MAGV=models.ForeignKey(Staffs,on_delete=models.CASCADE,null=False)
    MAMODAY=models.CharField(max_length=50)
    objects = models.Manager()
#phong giao vu hoc phan
class Staffs_GV_HP(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(null=True)
    address = models.TextField()
    gender = models.CharField(max_length=50,default="Male")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.CharField(null=True, max_length=30)
    objects = models.Manager()
class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    # def __str__(self):
	#     return self.course_name


# time and details session

class Time_subject(models.Model):
    ID_time=models.AutoField(primary_key=True)
    start_day=models.DateField()
    end_day=models.DateField()
    Mahocki=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE,null=False)
    objects = models.Manager()
class THUCHANH(models.Model):
    MATH = models.CharField(primary_key=True, max_length=30)
    soTietTH=models.IntegerField()
    objects = models.Manager()
class Nhom_TH(models.Model):
    id = models.AutoField(primary_key=True)
    MATH=models.ForeignKey(THUCHANH,on_delete=models.CASCADE,null=False)
    startday_TH = models.DateField()
    endday_TH = models.DateField()
    name_nhom=models.CharField(null=False,max_length=20)
    objects = models.Manager()

class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1) #need to give defauult course
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    so_tc=models.IntegerField(null=True)
    tongsvdk=models.IntegerField(null=True)
    nienkhoa=models.CharField(max_length=50)
    ID_time=models.ForeignKey(Time_subject,on_delete=models.CASCADE)
    MATH=models.ForeignKey(THUCHANH,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#ct mon hoc -gia mon hoc

class Details_Subjects(models.Model):

    MAMH=models.ForeignKey(Subjects,on_delete=models.CASCADE,primary_key=True)
    GiaTC=models.DecimalField(max_digits=8, decimal_places=3)
    objects = models.Manager()



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_pic = models.FileField(null=True)
    gender = models.CharField(max_length=50)
    address = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.CharField(null=True, max_length=50)
    objects = models.Manager()
class PHONGHOC(models.Model):
    MAPHONG=models.AutoField(primary_key=True)
    BUOIHOC=models.CharField(max_length=20)
    Thu=models.CharField(max_length=20)
    Siso_phong=models.IntegerField()
    MAMH=models.ForeignKey(Subjects,on_delete=models.CASCADE,null=False)
    MAGVCAPPHONG=models.ForeignKey(Staffs_GV_HP,on_delete=models.CASCADE,null=False)
    objects = models.Manager()
    class Meta:
        unique_together =(("MAPHONG","BUOIHOC","Thu","MAMH"))
class PHIEUDK_HOCPHAN(models.Model):
    MASV=models.ForeignKey(Students,on_delete=models.CASCADE,null=False,primary_key=True)
    MAPHONG=models.ForeignKey(PHONGHOC,on_delete=models.CASCADE,null=False)
    objects = models.Manager()

class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
class FeedBackStaffs_GV(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs_GV_HP, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance)
        if instance.user_type == 4:
            Staffs_GV_HP.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.staffs_gv_hp.save()


