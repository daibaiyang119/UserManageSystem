from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from app01.utils.pagination import PageHelper  # 自定义分页


# 登录验证
def login(request):
    message = ""
    # v = request.session
    # print(type(v))

    if request.method == "POST":
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        c = Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            return redirect('/index.html')
        else:
            message = "用户名或密码错误"

    return render(request, 'login.html', {'msg': message})


# 自定义装饰器，验证是否已经登录
def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner


# 主页
@auth
def index(request):
    current_user = request.session.get('username')
    return render(request, 'index.html', {'username': current_user})


# 退出
@auth
def logout(request):
    request.session.clear()
    return redirect("/login.html")


# 班级管理
@csrf_exempt
@auth
def handle_classes(request):
    if request.method == "GET":
        current_user = request.session.get('username')
        # 自定义分页，一页5条数据
        current_page = request.GET.get("page", 1)
        current_page = int(current_page)

        total_count = Classes.objects.all().count()

        #  创建分页对象
        page = PageHelper(total_count, current_page, "/classes.html", 10)
        html_str = page.pager_str()

        cls_list = Classes.objects.all()[page.page_start: page.page_end]

        return render(request, 'classes.html', {'username': current_user, 'cls_list': cls_list, 'page_index': html_str})
    elif request.method == "POST":
        # AJAX处理
        response_dict = {"status": True, "error": None, "data": None}

        caption = request.POST.get("caption", None)
        if caption:
            obj = Classes.objects.create(caption=caption)
            response_dict["data"] = {"id": obj.id, "caption": obj.caption}
        else:
            response_dict["status"] = False
            response_dict["error"] = "标题不能为空"
        return HttpResponse(json.dumps(response_dict))

        """
        # Form表单处理
        caption = request.POST.get("caption", None)
        if caption:
            Classes.objects.create(caption=caption)
        return redirect("/classes.html")
        """


# 通过独立页面方式添加班级信息
@auth
def handle_add_classes(request):
    message = ""
    if request.method == "GET":
        return render(request, "add_classes.html", {"msg": message})
    elif request.method == "POST":
        caption = request.POST.get("caption", None)
        if caption:
            Classes.objects.create(caption=caption)
            return redirect("/classes.html")
        else:
            message = "内容不能为空!"
            return render(request, "add_classes.html", {"msg": message})
    else:
        return redirect("/index.html")


# 通过独立页面方式编辑班级信息
@auth
def handle_edit_classes(request):
    if request.method == "GET":
        cid = request.GET.get("cid")
        obj = Classes.objects.filter(id=cid).first()
        return render(request, "edit_classes.html", {"obj": obj})
    elif request.method == "POST":
        cid = request.POST.get("cid")
        caption = request.POST.get("caption")
        if caption:
            Classes.objects.filter(id=cid).update(caption=caption)
            return redirect("/classes.html")
        else:
            # 数据为空时，将id再反传回去
            obj = {"id": cid, "caption": caption}
            message = "内容不能为空!"
            return render(request, "edit_classes.html", {"msg": message, "obj": obj})
    else:
        return redirect("/index.html")


# 通过Ajax方式编辑班级信息
@csrf_exempt
@auth
def handle_up_classes(request):
    if request.method == "POST":
        cid = request.POST.get("id")
        caption = request.POST.get("caption", None)

        response_dict = {"status": True, "error": None, "data": None}

        if caption:
            Classes.objects.filter(id=cid).update(caption=caption)
        else:
            response_dict["status"] = False
            response_dict["error"] = "标题不能为空"
        return HttpResponse(json.dumps(response_dict))


# 通过Ajax方式删除班级信息
@csrf_exempt
@auth
def handle_del_classes(request):
    if request.method == "POST":
        cid = request.POST.get("id")
        response_dict = {"status": True, "error": None, "data": None}
        Classes.objects.filter(id=cid).delete()
        return HttpResponse(json.dumps(response_dict))


# 学生管理
@auth
def handle_students(request):
    if request.method == "GET":
        current_user = request.session.get('username')

        # 获得当前页，默认为第一页
        current_page = request.GET.get("page", 1)
        current_page = int(current_page)

        total_count = Students.objects.all().count()

        # 创建分页对象，一页10条
        page = PageHelper(total_count, current_page, "/students.html")
        # 页面索引HTML
        html_str = page.pager_str()
        # 当前页数据
        stu_list = Students.objects.all()[page.page_start: page.page_end]

        return render(request, 'students.html', {'username': current_user, "students": stu_list, "page_index": html_str})
    else:
        return redirect("/index.html")


# 通过独立页面添加学生信息
@auth
def handle_add_students(request):
    if request.method == "GET":
        cls_list = Classes.objects.all()[0: 10]
        return render(request, "add_students.html", {"cls_list": cls_list})
    elif request.method == "POST":
        stu_name = request.POST.get("stu_name", None)
        stu_email = request.POST.get("stu_email", None)
        cls_id = request.POST.get("cls_id", None)
        if stu_name:
            Students.objects.create(name=stu_name, email=stu_email, cls_id=cls_id)
            return redirect("/students.html")
        else:
            message = "内容不能为空"
            return render(request, "add_students.html", {"msg": message})
    else:
        return redirect("/index.html")


# 通过独立页面方式编辑学生信息
@auth
def handle_edit_students(request):
    if request.method == "GET":
        stu_id = request.GET.get("stu_id", None)
        student = Students.objects.get(id=stu_id)
        cls_list = Classes.objects.all()[0:10]
        return render(request, "edit_students.html", {"student": student, "cls_list": cls_list})
    elif request.method == "POST":
        stu_id = request.POST.get("stu_id", None)
        stu_name = request.POST.get("stu_name", None)
        stu_email = request.POST.get("stu_email", None)
        cls_id = request.POST.get("cls_id", None)
        Students.objects.filter(id=stu_id).update(name=stu_name, email=stu_email, cls_id=cls_id)
        return redirect("/students.html")
    else:
        return redirect("/index.html")


# 通过Ajax方式删除学生信息
@csrf_exempt
@auth
def handle_del_students(request):
    if request.method == "POST":
        stu_id = request.POST.get("id")
        response_dict = {"status": True, "error": None, "data": None}
        Students.objects.filter(id=stu_id).delete()
        return HttpResponse(json.dumps(response_dict))


# 老师管理
@auth
def handle_teachers(request):
    current_user = request.session.get('username')

    # 获得当前页，默认为第一页
    current_page = request.GET.get("page", 1)
    current_page = int(current_page)

    total_count = Teacher.objects.all().count()

    # 创建分页对象，一页5条
    page = PageHelper(total_count, current_page, "/teachers.html", 5)
    # 页面索引HTML
    html_str = page.pager_str()
    teacher_list = Teacher.objects.all()[page.page_start: page.page_end].values_list("id")
    # 取得当前页要显示的教师ID列表
    teacher_list = list(zip(*teacher_list))[0]
    # 获取当前页教师ID，教师姓名，班级ID，班级名称
    # 因为一个教师不止教一个班级，所以要先取得当前页要显示的教师ID列表，例如一页5个教师
    teachers = Teacher.objects.filter(id__in=teacher_list).values("id", "name", "cls__id", "cls__caption")
    teacher_dic = {}
    for teacher in teachers:
        if teacher["id"] in teacher_dic:
            teacher_dic[teacher["id"]]["cls_list"].append({"id": teacher["cls__id"], "caption": teacher["cls__caption"]})
        else:
            if teacher["cls__id"]:
                temp = [{"id": teacher["cls__id"], "caption": teacher["cls__caption"]},]
            else:
                temp = []
            teacher_dic[teacher["id"]] = {
                "tid": teacher["id"],
                "name": teacher["name"],
                "cls_list": temp,
            }
    return render(request, 'teachers.html', {'username': current_user, "teacher_dic": teacher_dic, "page_index": html_str})


# 通过独立页面方式添加教师
@auth
def handle_add_teachers(request):
    if request.method == "GET":
        cls_list = Classes.objects.all()
        return render(request, "add_teachers.html", {"cls_list": cls_list})
    elif request.method == "POST":
        tch_name = request.POST.get("tch_name", None)
        cls_list = request.POST.getlist("cls_id")
        if tch_name:
            teacher = Teacher.objects.create(name=tch_name)
            teacher.cls.add(*cls_list)
            return redirect("/teachers.html")
        else:
            message = "内容不能为空"
            return render(request, "add_teachers.html", {"msg": message})
    else:
        return redirect("/index.html")


# 通过独立页面编辑教师信息
@auth
def handle_edit_teachers(request):
    if request.method == "GET":
        tch_id = request.GET.get("tch_id", None)
        teacher = Teacher.objects.get(id=tch_id)
        cls_list = Classes.objects.all()
        # 获取当前教师任课的班级ID列表
        tch_cls_list = teacher.cls.all().values_list("id")
        id_list = list(zip(*tch_cls_list))[0]
        return render(request, "edit_teachers.html", {"teacher": teacher, "cls_list": cls_list, "id_list": id_list})
    elif request.method == "POST":
        tch_id = request.POST.get("tch_id", None)
        tch_name = request.POST.get("tch_name", None)
        cls_list = request.POST.getlist("cls_id")
        print(cls_list)
        if tch_name:
            teacher = Teacher.objects.get(id=tch_id)
            teacher.name = tch_name
            teacher.save()
            teacher.cls.add(*cls_list)
        else:
            message = "内容不能为空"
            teacher = Teacher.objects.get(id=tch_id)
            cls = Classes.objects.all()
            id_list = []
            for cls_id in cls_list:
                id_list.append(int(cls_id))
            return render(request, "edit_teachers.html", {"teacher": teacher, "cls_list": cls, "id_list": id_list, "msg": message})
    else:
        return redirect("/index.html")


# 通过Ajax删除教师信息
@csrf_exempt
@auth
def handle_del_teachers(request):
    if request.method == "POST":
        tch_id = request.POST.get("id", None)
        Teacher.objects.filter(id=tch_id).delete()
        response_dict = {"status": True, "error": None, "data": None}
        return HttpResponse(json.dumps(response_dict))
