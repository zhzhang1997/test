import xadmin
from xadmin import views

from .models import *

class AdministratorAdmin(object):
    list_display = ['id', 'phone', 'email', 'password']
    search_fields =['id']
    list_editable = ['id', 'phone', 'email', 'password']
    list_filter = ['id', 'phone', 'email', 'password']


class StudentAdmin(object):
    list_display = ['id', 'openid', 'name', 'real_name', 'phone', 'password', 'gender', 'age', 'content', 'isDelete', 'belong']
    list_editable = ['phone', 'password', 'real_name', 'gender', 'age', 'content']
    list_filter = ['id']


class AddressAdmin(object):
    list_display = ['id', 'address']
    search_fields = ['id']
    list_editable = ['id']
    list_filter = ['id']


class TeacherAdmin(object):
    list_display = ['id', 'openid', 'name', 'gender', 'age', 'content', 'isDelete', 'belong']
    search_fields = ['id']
    list_editable = ['openid', 'name', 'gender', 'age', 'content', 'isDelete', 'belong']
    list_filter = ['id']


class CourseAdmin(object):
    list_display = ['id', 'name', 'content', 'date', 'current_number', 'max_number', 'teacher', 'students',  'belong']
    search_fields = ['id']
    list_editable = ['name', 'content', 'date', 'teacher', 'max_number', 'students', 'belong']
    list_filter = ['id']


class VIPTypeAdmin(object):
    list_display = ['id', 'name', 'students']
    search_fields = ['id']
    list_editable = ['name']
    list_filter = ['id']


class VIP2StudentAdmin(object):
    list_display = ['vip', 'student', 'start_time', 'end_time']
    search_fields = ['id']
    list_editable = ['vip', 'student', 'start_time', 'end_time']
    list_filter = ['id']


class Course2StudentAdmin(object):
    list_display = ['course', 'student']
    list_editable = ['course', 'student']


xadmin.site.register(Administrator, AdministratorAdmin)
xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(Address, AddressAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(VIPType, VIPTypeAdmin)
xadmin.site.register(VIP2Student, VIP2StudentAdmin)
xadmin.site.register(Course2Student, Course2StudentAdmin)
