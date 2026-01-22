from django.shortcuts import render, redirect , get_object_or_404
from . models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
import datetime
from django.db.models import Q
from django.contrib.auth.hashers import make_password



def index(request):
    return render(request,'index.html')


def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('index')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('adminn')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('adminn')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Image = photo
        t.User_role = 'admin'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('index')
    else:
        return render(request, 'reg_admin.html')


def student_rg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('stud')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('stud')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Image = photo
        t.User_role = 'student'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as student')
        return redirect('index')
    else:
        return render(request, 'reg_student.html')


def teacher_rg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('teachr')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('teachr')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Image = photo
        t.User_role = 'teacher'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as teacher')
        return redirect('index')
    else:
        return render(request, 'reg_teacher.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, Password = password).exists():
            logs = Registration.objects.filter(user = user, Password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                teacher_email = value.user.email
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')

                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    request.session['teacher'] = teacher_email
                    cm = Registration.objects.get(id = request.session['logg'])
                    g = Enrollment.objects.filter(enrol_tea = cm)
                    count = 0
                    for i in g:
                        count += 1
                    cm.Num_of_enrolled_students = count
                    mb = Feedback.objects.filter(Feed_tea_reg = cm)
                    cnn = 0
                    avs = []
                    for t in mb:
                        cnn += 1
                        avs.append(t.Rating_score)
                    aa = avs.count(5)
                    bb = avs.count(4)
                    cc = avs.count(3)
                    dd = avs.count(2)
                    ee = avs.count(1)
                    ff = [aa,bb,cc,dd,ee]
                    gg = max(ff)
                    if int(gg) == int(aa):
                        cm.Average_review_rating = 5
                    if int(gg) == int(bb):
                        cm.Average_review_rating = 4
                    if int(gg) == int(cc):
                        cm.Average_review_rating = 3
                    if int(gg) == int(dd):
                        cm.Average_review_rating = 2
                    if int(gg) == int(ee):
                        cm.Average_review_rating = 1
                    cm.Num_of_reviews = cnn
                    cm.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id = nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('teacher_home')

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    mhp = Registration.objects.get(id = request.session['logg'])
                    dt = Enrollment.objects.filter(enrol_reg = mhp)

                    ggpp = []
                    for t in dt:
                        ksk = int(t.enrol_cou.id)
                        ggpp.append(ksk)

                    dgf = Course.objects.filter(id__in = ggpp)
                    cou_cmpltd = 0
                    for e in dgf:
                        mbt = 0
                        pas = 0
                        pas1 = 4
                        hdc = Chapter.objects.filter(cha_cou = e)
                        for t in hdc:
                            hdc1 = Content.objects.filter(cont_cha = t)
                            for c in hdc1:
                                if Learning_progress.objects.filter(Learn_p_reg = mhp, Learn_p_cnt = c, Status = 'C').exists():
                                    pas += 1
                            pas1 = Content.objects.filter(cont_cha = t).count()
                            if pas == pas1:
                                mbt += 1

                        ch_cnts = Chapter.objects.filter(cha_cou = e).count()

                        if ch_cnts == mbt:
                            cou_cmpltd += 1


                    mhp.Num_of_courses_completed = cou_cmpltd
                    enrollments = Enrollment.objects.filter(enrol_reg=mhp)
                    mhp.Num_of_courses_enrolled = enrollments.count()

                    mhp.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id=nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('student_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')


from django.shortcuts import render
from .models import Registration, Category

def admin_home(request):
    users = Registration.objects.filter(User_role__in=["teacher", "student"])  # Fetch users
    categories = Category.objects.all()
    admin_profile = Registration.objects.filter(user=request.user, User_role="admin").first()
    category_count = Category.objects.count()  # Count categories
    teacher_count = Registration.objects.filter(User_role="teacher").count()  # Count teachers
    student_count = Registration.objects.filter(User_role="student").count()  # Count students
    course_count = Course.objects.count()
    return render(request, 'admin_home.html', {
        'users': users,
        'categories': categories,
        'category_count': category_count,
        'teacher_count': teacher_count,
        'student_count': student_count,
        'course_count': course_count,
        'admin_profile': admin_profile
    })


def student_home(request):
    return render(request,'student_home.html')


def teacher_home(request):
    return render(request,'teacher_home.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def cat_admin(request):
    mkk = Category.objects.all()
    return render(request,'cat_admin.html',{'mkk':mkk})


def edit_cat_admin(request, id):
    gh = Category.objects.get(id = id)
    if request.method == 'POST':
        try:
            imgg = request.FILES['imgg']
            fs = FileSystemStorage()
            fs.save(imgg.name,imgg)
            cat = request.POST.get('cat')
            gh.Category_title = cat
            gh.Image = imgg
            gh.save()
        except:
            imgg1 = request.POST.get('imgg1')
            cat = request.POST.get('cat')
            gh.Category_title = cat
            gh.Image = imgg1
            gh.save()
        messages.success(request, 'Course category edited successfully')
        return redirect('cat_admin')
    return render(request, 'edit_cat_admin.html', {'gh': gh})


def delete_cat_admin(request, id):
    Category.objects.get(id = id).delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('cat_admin')


def add_cat_admin(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        imgg = request.FILES['imgg']
        fs = FileSystemStorage()
        fs.save(imgg.name, imgg)
        gh = Category()
        gh.Category_title = cat
        gh.Image = imgg
        gh.save()
        messages.success(request, 'Course category added successfully')
        return redirect('cat_admin')
    return render(request,'add_cat_admin.html')


def course_tr(request):
    dd = Course.objects.filter(cou_reg = request.session['logg'])
    return render(request,'course_tr.html',{'dd':dd})


def add_course_tr(request):
    hrb = Registration.objects.get(id = request.session['logg'])
    mkm = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        bbt = Category.objects.get(id = cat)
        cou_tit = request.POST.get('cou_tit')
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')

        if Course.objects.filter(cou_reg = hrb, Course_title = cou_tit).exists():
            messages.success(request, 'Course already exists')
            return redirect('course_tr')

        cdt = Course()
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Course_fee = c_f1
        cdt.Language = lang
        cdt.cou_reg = hrb
        cdt.cou_cat = bbt
        cdt.save()

        cou_st_date = request.POST.get('cou_st_date')
        cou_end_date = request.POST.get('cou_end_date')

        cmk = Course_st_stop()
        cmk.start_date = cou_st_date
        cmk.end_date = cou_end_date
        cmk.cou_st_stop_cou = cdt
        cmk.save()

        messages.success(request, 'Course added successfully')
        return redirect('course_tr')
    return render(request,'add_course_tr.html',{'mkm':mkm})


def edit_course_tr(request, id):
    mkm = Category.objects.all()
    gh = Course.objects.get(id = id)
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        yky = Category.objects.get(id = cat)
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.cou_cat = yky
        gh.save()
        messages.success(request, 'Course edited successfully')
        return redirect('course_tr')
    return render(request,'edit_course_tr.html',{'gh':gh,'mkm':mkm})


def delete_course_tr(request, id):
    Course.objects.get(id = id).delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('course_tr')


def chapter_tr(request, id):
    id = int(id)
    request.session['teacher_course'] = id
    hh = Chapter.objects.filter(cha_cou = id)
    return render(request, 'chap_tr.html', {'hh': hh})


def edit_chapter_tr(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    gh = Chapter.objects.get(id = id)
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        gh.Chapter_title = c_tt
        gh.save()
        messages.success(request, 'Chapter edited successfully')
        redd = '/chapter_tr/'+str(kkp.id)
        return redirect(redd)
    return render(request,'edit_chapter_tr.html',{'gh':gh,'kkp':kkp})


def delete_chapter(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    Chapter.objects.get(id = id).delete()
    messages.success(request, 'Chapter deleted successfully')
    redd = '/chapter_tr/' + str(kkp.id)
    return redirect(redd)


def add_chapter(request):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        if Chapter.objects.filter(cha_cou = kkp, Chapter_title = c_tt).exists():
            messages.success(request, 'Chapter already exists')
            redd = '/chapter_tr/' + str(kkp.id)
            return redirect(redd)

        cdt = Chapter()
        cdt.Chapter_title = c_tt
        cdt.cha_cou = kkp
        cdt.save()

        messages.success(request, 'Chapter added successfully')
        redd = '/chapter_tr/' + str(kkp.id)
        return redirect(redd)
    return render(request,'add_chapter.html',{'kkp':kkp})


def ch_co_tr(request, id):
    id = int(id)
    request.session['teacher_chapter'] = id
    idm = request.session['teacher_course']
    idm = int(idm)
    mm1 = Content.objects.filter(cont_cha = id)
    return render(request, 'cont_tr.html', {'mm1': mm1,'idm':idm})


def edit_content(request, id):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id = tt_chapt1)
    gh = Content.objects.get(id = id)
    if request.method == 'POST':
        try:
            c_t = request.POST.get('c_t')
            up_cont = request.FILES['up_cont']
            upp = str(up_cont)
            imm = ['.jpeg','.jpg','.png']
            vid = ['.mov','.mp4','.wmv','.avi','.avchd','.flv','.f4v','.swf','.mkv','.webm','.mpeg4']
            nbg = 0

            for i in imm:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Image'

            for i in vid:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Video'

            if nbg == 0:
                gh.Chapter_Content_type = 'File'

            fs = FileSystemStorage()
            fs.save(up_cont.name, up_cont)

            gh.Chapter_Content = up_cont
            gh.Chapter_text_content = c_t
            gh.save()
            redd = '/ch_co_tr/'+str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)

        except:
            c_t = request.POST.get('c_t')
            u_con = request.POST.get('u_con')
            u_con_typ = request.POST.get('u_con_typ')
            gh.Chapter_Content = u_con
            gh.Chapter_text_content = c_t
            gh.Chapter_Content_type = u_con_typ
            gh.save()
            redd = '/ch_co_tr/' + str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)
    return render(request, 'edit_content.html', {'gh': gh,'tt_chapt':tt_chapt})


def delete_content(request, id):
    Content.objects.get(id = id).delete()
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    redd = '/ch_co_tr/' + str(tt_chapt1)
    messages.success(request, 'Chapter content deleted successfully')
    return redirect(redd)


def add_ch_con(request):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id=tt_chapt1)
    if request.method == 'POST':
        c_t = request.POST.get('c_t')
        up_cont = request.FILES['up_cont']
        fs = FileSystemStorage()
        fs.save(up_cont.name, up_cont)

        upp = str(up_cont)
        imm = ['.jpeg', '.jpg', '.png']
        vid = ['.mov', '.mp4', '.wmv', '.avi', '.avchd', '.flv', '.f4v', '.swf', '.mkv', '.webm', '.mpeg4']

        cdt = Content()
        nbg = 0
        for i in imm:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Image'

        for i in vid:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Video'

        if nbg == 0:
            cdt.Chapter_Content_type = 'File'

        cdt.Chapter_Content = up_cont
        cdt.Chapter_text_content = c_t
        cdt.cont_cha = tt_chapt
        cdt.save()
        redd = '/ch_co_tr/' + str(tt_chapt1)
        messages.success(request, 'Chapter content added successfully')
        return redirect(redd)
    return render(request,'add_chapter_content.html',{'tt_chapt':tt_chapt})


def stu_sub_selnew(request):
    sne = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat1 = int(cat)
        request.session['st_bk_category'] = cat1
        cc = Course.objects.filter(cou_cat =cat1)
        return render(request,'st_sub_selnew2.html',{'cc':cc})
    return render(request, 'st_sub_selnew1.html',{'snew':sne})


def stu_sub_selnew1(request):
    sne = Category.objects.get(id = request.session['st_bk_category'])
    cou = request.POST.get('cou')
    cou1 = int(cou)
    request.session['st_bk_course'] = cou1
    cse = Course.objects.get(id = cou1)
    c_tit = str(cse.Course_title)
    cse = Course.objects.filter(cou_cat = sne, Course_title = c_tit)
    return render(request, 'st_sub_selnew3.html', {'cse': cse})


def stu_sub_selnew3(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.session['st_bk_course'] = course_id
    category = course.cou_cat
    cse = Course.objects.filter(cou_cat=category, Course_title=course.Course_title)
    return render(request, 'st_sub_selnew3.html', {'cse': cse, 'course': course})


def stu_buk_teacher(request, id):
    id = int(id)
    dh = Registration.objects.get(id = request.session['logg'])
    cou = Course.objects.get(id = id)
    id_tea = int(cou.cou_reg.id)
    nm = Registration.objects.get(id = id_tea)
    if Enrollment.objects.filter(enrol_reg = dh, enrol_tea = nm, enrol_cou = cou).exists():
        messages.success(request, 'You have already booked this course')
        return redirect('student_home')

    spp = Enrollment()
    spp.enrol_reg = dh
    spp.enrol_tea = nm
    spp.enrol_cou = cou
    spp.Teacher_response = 'To be expected'
    spp.notify = 'new'
    spp.save()

    messages.success(request, 'You have successfully booked a course')
    return redirect('student_home')


def stu_buk_acc(request):
    stzz = Enrollment.objects.filter(enrol_tea = request.session['logg'])
    return render(request,'stu_buk_acc.html',{'stzz':stzz})


def stu_accept(request, id):
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return redirect('stu_buk_acc')


def stu_reject(request, id):
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return redirect('stu_buk_acc')


def stu_delete(request, id):
    Enrollment.objects.get(id = id).delete()
    messages.success(request, 'Enrolled student deleted successfully')
    return redirect('stu_buk_acc')


def pay_student(request):
    ds = Enrollment.objects.filter(enrol_reg = request.session['logg'], Teacher_response = 'Accepted')
    msk = []
    for t in ds:
        c_f = float(t.enrol_cou.Course_fee)
        if c_f > 0:
            hh = int(t.id)
            msk.append(hh)
    ds = Enrollment.objects.filter(id__in = msk)
    return render(request,'pay_student.html',{'ds': ds})


def stu_buk_teacherr(request, id):
    id = int(id)
    tgt = Enrollment.objects.get(id = id)
    if tgt.Payment_status == 'paid':
        messages.success(request, 'You have already paid')
        return redirect('pay_student')
    if request.method == 'POST':
        paid = request.POST.get('paid')
        paid = float(paid)
        if float(tgt.enrol_cou.Course_fee) != paid:
            messages.success(request, 'Please pay exact amount')
            return render(request,'paid.html',{'tgt':tgt})
        tgt.Payment_status = 'paid'
        tgt.save()

        kmwe = 'You have paid for the course '+tgt.enrol_cou.cou_cat.Category_title+'('+tgt.enrol_cou.Course_title+')'
        messages.success(request, kmwe)
        return redirect('student_home')
    return render(request,'paid.html',{'tgt':tgt})


def st_book_courses(request):
    st = Registration.objects.get(id = request.session['logg'])
    buk = Enrollment.objects.filter(enrol_reg = st)
    return render(request, 'st_book_courses.html',{'buk':buk,'st':st})


def acc_chapter(request, id):
    gh = Enrollment.objects.get(id = id)
    if gh.Teacher_response == 'To be expected' or gh.Teacher_response == 'Rejected' or gh.Payment_status != 'paid':
        messages.success(request, 'Your payment is pending or wait for teacher\'s approval')
        return redirect('st_book_courses')
    request.session['acc_cha_teacher'] = t_id = int(gh.enrol_tea.id)
    nn = Registration.objects.get(id = t_id)
    request.session['tch_idd'] = nn.id
    cou_idd = int(gh.enrol_cou.id)
    thr = Course.objects.get(id = cou_idd)
    fd = Chapter.objects.filter(cha_cou = thr)
    return render(request, 'acc_chapter1.html', {'fd':fd})


def acc_chapter1(request):
    mnm = Registration.objects.get(id = request.session["logg"])
    sz1 = request.POST.get('cha')
    request.session['cou_ch_nme'] = chtw = int(sz1)
    sz = Chapter.objects.get(id = chtw)
    sz_cnt = Content.objects.filter(cont_cha = sz)
    mj = Learning_progress.objects.filter(Learn_p_reg = mnm)
    return render(request, 'acc_chapter2.html', {'sz_cnt': sz_cnt,'mj':mj})


def compp(request):
    cco = Registration.objects.get(id = request.session['acc_cha_teacher'])
    mnm = Registration.objects.get(id = request.session["logg"])
    idd = request.POST.getlist('id')
    comm = request.POST.getlist('comm')
    ggt = zip(idd,comm)
    for i,h in ggt:
        dvt = int(i)
        dvt1 = Content.objects.get(id=dvt)
        if Learning_progress.objects.filter(Learn_p_cnt = dvt1).exists():
            pk = Learning_progress.objects.filter(Learn_p_cnt = dvt1)
            for t in pk:
                t.Status = h
                t.save()
        else:
            pk = Learning_progress()
            pk.Status = h
            pk.Learn_p_reg = mnm
            pk.Learn_p_tea_reg = cco
            pk.Learn_p_cnt = dvt1
            pk.save()
    messages.success(request, 'Learning progress updated')
    return redirect('student_home')


def st_pr(request):
    vc = Registration.objects.get(id = request.session['logg'])
    dd = Learning_progress.objects.filter(Learn_p_tea_reg = vc)
    return render(request,'student_progress.html',{'dd':dd})


def m_m2(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request, 'msg2.html', {'bb': bb})


def m_m3(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request, 'msg3.html', {'bb': bb})


def message(request):
    p = Registration.objects.get(id=request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request, 'message.html', {'bb': bb})


def del_msg_student(request,id):
    Messages.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('m_m2')


def reply_msg_student(request,id):
    pa = Messages.objects.get(id = id)
    toto = int(pa.From_reg.id)
    p_to = Registration.objects.get(id=toto)
    p = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Message_content = msg_cont
        pa1.From_reg = p
        pa1.To_reg = p_to
        pa1.save()
        messages.success(request, 'Message reply successful')
        return redirect('m_m2')
    return render(request,'reply_msg_student.html',{'pa':pa})


def sent_msg_student(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = int(to_em)
        reg_to = Registration.objects.get(id=ddp)
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Message_content = msg_cont
        nm.From_reg = p
        nm.To_reg = reg_to
        nm.save()
        messages.success(request, 'Message sent successfully')
        return redirect('m_m2')
    return render(request,'sent_msg_student.html',{'kk':kk})


def m_m(request):
    p = Registration.objects.get(id = request.session['logg'])
    bb = Messages.objects.filter(To_reg = p)
    return render(request,'message.html',{'bb':bb})


def del_msg_admin(request,id):
    Messages.objects.get(id = id).delete()
    messages.success(request, 'Message deleted successfully')
    return redirect('m_m')


def reply_msg_admin(request,id):
    pa = Messages.objects.get(id = id)
    toto = int(pa.From_reg.id)
    p_to = Registration.objects.get(id = toto)
    p = Registration.objects.get(id=request.session['logg'])
    if request.method == 'POST':
        msg_cont = request.POST.get('msg_cont')
        pa1 = Messages()
        pa1.Message_content = msg_cont
        pa1.From_reg = p
        pa1.To_reg = p_to
        pa1.save()
        messages.success(request, 'Message reply successful')
        return redirect('m_m')
    return render(request,'reply_msg_admin.html',{'pa':pa})


def sent_msg_admin(request):
    kk = Registration.objects.all()
    p = Registration.objects.get(id = request.session['logg'])
    if request.method == 'POST':
        to_em = request.POST.get('to_em')
        ddp = int(to_em)
        reg_to = Registration.objects.get(id = ddp)
        msg_cont = request.POST.get('msg_cont')
        nm = Messages()
        nm.Message_content = msg_cont
        nm.From_reg = p
        nm.To_reg = reg_to
        nm.save()
        messages.success(request, 'Message sent successfully')
        return redirect('m_m')
    return render(request,'sent_msg_admin.html',{'kk':kk})


def block(request):
    t_reg = Registration.objects.filter(Q(User_role="teacher") | Q(User_role="teacher_blocked"))
    s_reg = Registration.objects.filter(Q(User_role="student") | Q(User_role="student_blocked"))
    return render(request,'block.html',{'t_reg':t_reg,'s_reg':s_reg})


def blocks(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher_blocked'
    klk.save()
    return redirect('block')


def allows(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'teacher'
    klk.save()
    return redirect('block')


def blocks1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student_blocked'
    klk.save()
    return redirect('block')


def allows1(request, id):
    klk = Registration.objects.get(id=id)
    klk.User_role = 'student'
    klk.save()
    return redirect('block')


def update_pr_tr(request):
    bb = Registration.objects.get(id = request.session['logg'])
    rfy = bb.user.pk
    um = User.objects.get(id = rfy)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('update_pr_tr')


        passwords = make_password(pasw)
        u = User.objects.get(id = rfy)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = pasw)
        auth.login(request, user)


        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('teacher_home')
    return render(request, 'update_pr_tr.html', {'bb': bb,'um':um})


def update_pr_stu(request):
    bb = Registration.objects.get(id = request.session['logg'])
    rfy = bb.user.pk
    um = User.objects.get(id = rfy)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('update_pr_stu')


        passwords = make_password(pasw)
        u = User.objects.get(id = rfy)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = pasw)
        auth.login(request, user)


        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('student_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('student_home')
    return render(request, 'update_pr_stu.html', {'bb': bb,'um':um})


def update_pr_adm(request):
    bb = Registration.objects.get(id = request.session['logg'])
    rfy = bb.user.pk
    um = User.objects.get(id = rfy)
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pasw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)

        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('update_pr_adm')


        passwords = make_password(pasw)
        u = User.objects.get(id = rfy)
        u.password = passwords
        u.username = user_name
        u.email = email
        u.first_name = f_name
        u.last_name = l_name
        u.save()

        user = auth.authenticate(username = user_name, password = pasw)
        auth.login(request, user)


        b = bb.id
        m = int(b)
        request.session['logg'] = m

        try:
            imgg1 = request.FILES['imgg1']
            fs = FileSystemStorage()
            fs.save(imgg1.name,imgg1)
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg1
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('admin_home')
        except:
            imgg2 = request.POST.get('imgg2')
            enrol = request.POST.get('enrol')
            bb.Password = pasw
            bb.Qualification = qual
            bb.Introduction_brief = intro
            bb.Image = imgg2
            bb.Num_of_enrolled_students = enrol
            bb.user = u
            bb.save()
            messages.success(request, 'Updated successfully')
            return redirect('admin_home')
    return render(request, 'update_pr_adm.html', {'bb': bb,'um':um})


def assignment(request):
    kk = Registration.objects.get(id=request.session['logg'])
    mbm = Assignment.objects.filter(teacher_reg = kk)
    return render(request,'assignment.html',{'mbm':mbm})


def edit_assignment(request, id):
    id = int(id)
    ccf = Assignment.objects.get(id = id)
    gttf = Registration.objects.get(id = request.session['logg'])
    tft = Course.objects.filter(cou_reg = gttf)
    if request.method == 'POST':
        cn = request.POST.get('cn')
        cn = int(cn)
        sds = Course.objects.get(id = cn)
        at = request.POST.get('at')
        m = request.POST.get('m')
        sd = request.POST.get('sd')
        ed = request.POST.get('ed')
        pass_perc = request.POST.get('pass_perc')
        try:
            photo = request.FILES['q']
            fs = FileSystemStorage()
            fs.save(photo.name, photo)
            ccf.assign_course = sds
            ccf.assignment_topic = at
            ccf.assignment_upload = photo
            ccf.total_marks = m
            ccf.start_date = sd
            ccf.teacher_reg = gttf
            ccf.submission_date = ed
            ccf.pass_percent = pass_perc
            ccf.save()
            messages.success(request, 'Assignment has been edited')
            return redirect('assignment')
        except:
            photo1 = request.POST.get('q1')
            ccf.assign_course = sds
            ccf.assignment_topic = at
            ccf.assignment_upload = photo1
            ccf.total_marks = m
            ccf.start_date = sd
            ccf.teacher_reg = gttf
            ccf.submission_date = ed
            ccf.pass_percent = pass_perc
            ccf.save()
            messages.success(request, 'Assignment has been edited')
            return redirect('assignment')
    return render(request,'edit_assignment.html',{'tft':tft,'ccf':ccf})


def delete_assignment(request, id):
    Assignment.objects.get(id = id).delete()
    messages.success(request, 'Assignment deleted')
    return redirect('assignment')


def add_assignment(request):
    gttf = Registration.objects.get(id = request.session['logg'])
    tft = Course.objects.filter(cou_reg = gttf)
    if request.method == 'POST':
        cn = request.POST.get('cn')
        cn = int(cn)
        cn = Course.objects.get(id = cn)
        at = request.POST.get('at')
        photo = request.FILES['q']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        m = request.POST.get('m')
        sd = request.POST.get('sd')
        ed = request.POST.get('ed')
        pass_perc = request.POST.get('pass_perc')
        cc= Assignment()
        cc.assign_course = cn
        cc.assignment_topic = at
        cc.assignment_upload = photo
        cc.total_marks = m
        cc.start_date = sd
        cc.teacher_reg = gttf
        cc.submission_date = ed
        cc.pass_percent = pass_perc
        cc.save()
        messages.success(request, 'Assignment has been added')
        return redirect('assignment')
    return render(request,'add_assignment.html',{'tft':tft})


def upload_assi_tea(request):
    kk = Registration.objects.get(id=request.session['logg'])
    gbv = Assignment.objects.filter(teacher_reg = kk)
    gg = []
    for k in gbv:
        k = int(k.id)
        gg.append(k)
    mbm = Assignment_result.objects.filter(asssi_res_assi__in = gg)
    return render(request, 'upload_assi_tea.html', {'mbm': mbm})


def add_mark_assi_tea(request, id):
    mbm = Assignment_result.objects.get(id = id)
    if request.method == 'POST':
        mrk = request.POST.get('mrk')
        mrk = float(mrk)
        tot = float(mbm.asssi_res_assi.total_marks)
        if mrk > tot:
            messages.success(request, 'Assignment mark must not be more than total marks')
            return render(request, 'add_mark_assi_tea.html',{'mbm':mbm})
        tot_acq_percent = (mrk/tot)*100
        tot_acq_percent = round(tot_acq_percent,2)
        mbm.acquired_marks = mrk
        mbm.acquired_pass_percent = tot_acq_percent
        mbm.save()
        messages.success(request, 'Assignment mark added')
        return redirect('upload_assi_tea')
    return render(request, 'add_mark_assi_tea.html',{'mbm':mbm})


def assi_st(request):
    kmk = Registration.objects.get(id = request.session['logg'])
    kmk1 = Enrollment.objects.filter(enrol_reg = kmk)
    ksdr = []
    for w in kmk1:
        dbr = int(w.enrol_cou.id)
        ksdr.append(dbr)
    kmk2 = Course.objects.filter(id__in = ksdr)
    zz2 = []
    for d in kmk2:
        d = int(d.id)
        zz2.append(d)
    a_st = Assignment.objects.filter(assign_course__in = zz2)
    if request.method == 'POST':
        ress = request.FILES['ress']
        fs = FileSystemStorage()
        fs.save(ress.name, ress)
        topp = request.POST.get('topp')
        topp = int(topp)
        sws = Assignment.objects.get(id = topp)
        today = datetime.datetime.today().date()
        if today > sws.submission_date:
            messages.success(request, 'Assignment submission date is over')
            return redirect('assi_st')
        if Assignment_result.objects.filter(asssi_res_assi = sws, asssi_res_st = kmk).exists():
            messages.success(request, 'Assignment already uploaded')
            return redirect('assi_st')
        vf = Assignment_result()
        vf.assignment_upload_ans = ress
        vf.asssi_res_assi = sws
        vf.asssi_res_st = kmk
        vf.save()
        messages.success(request, 'Assignment uploaded successfully')
        return redirect('student_home')
    return render(request, 'assi_st.html', {'a_st': a_st})


def stu_approve(request, id):
    sas = Course_st_stop.objects.get(id=id)
    ses = Enrollment.objects.get(id=id)
    today = datetime.datetime.today().date()
    if sas.end_date >= today:
        ses.Teacher_approval = 'Approved'
        ses.save()
        messages.success(request, 'Student approved to admin successfully')
    else:
        messages.error(request, 'Cannot approve student. The course has not yet ended.')
    return redirect('stu_buk_acc')


def cert(request):
    var= Enrollment.objects.filter(Teacher_approval= 'Approved')

    return render(request,'certificate.html', {'var':var})


def assign(request):
    asc = Category.objects.all()
    return render(request,'cat_admin.html',{'asc':asc})


def ex(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        selected_category = int(selected_category)
        courses = Course.objects.filter(cou_cat_id=selected_category)
    else:
        selected_category = None
        courses = Course.objects.all()

    return render(request, 'course.html', {
        'courses': courses,
        'categories': categories,
        'selected_category': selected_category
    })


def account(request):
    return render(request,'account.html')


def do_cer(request):
    sr = Enrollment.objects.filter(enrol_reg = request.session['logg']).exclude(Certificate = '')
    return render(request,'do_cer.html',{'sr':sr})


def upl_cer(request):
    bc = Enrollment.objects.filter(Teacher_approval = 'Approved')
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        stu_id = int(stu_id)
        mrt = Enrollment.objects.get(id = stu_id)
        cert = request.FILES['cert']
        fs = FileSystemStorage()
        fs.save(cert.name,cert)
        if mrt.Certificate != '':
            messages.success(request, 'Please delete old certificate of student')
            return redirect('admin_home')
        mrt.Certificate = cert
        mrt.save()
        messages.success(request, 'Certificate uploaded successfully')
        return redirect('admin_home')

    return render(request,'upload_cert.html',{'bc':bc})


def payment(request):
    return render(request,'payment.html')


def reports(request):
    teachers = Registration.objects.filter(User_role="teacher").select_related("user")
    students = Registration.objects.filter(User_role="student").select_related("user")
    categories = Category.objects.all()
    admin_profile = Registration.objects.filter(user=request.user, User_role="admin").first()
    category_count = Category.objects.count()
    teacher_count = teachers.count()
    student_count = students.count()
    course_count = Course.objects.count()
    return render(request, 'reports.html', {
        'teachers': teachers,
        'students': students,
        'categories': categories,
        'category_count': category_count,
        'teacher_count': teacher_count,
        'student_count': student_count,
        'course_count': course_count,
        'admin_profile': admin_profile
    })


def feedback(request):
    student = Registration.objects.get(id=request.session['logg'])
    enrolled_courses = Enrollment.objects.filter(enrol_reg=student)
    previous_feedbacks = Feedback.objects.filter(Feed_reg=student)

    if request.method == 'POST':
        enrollment_id = int(request.POST.get('couu'))  # From form
        enrollment = Enrollment.objects.get(id=enrollment_id)


        teacher = enrollment.enrol_tea
        course = enrollment.enrol_cou


        score = request.POST.get('scorr')
        text_feed = request.POST.get('text_feed')


        Feedback.objects.create(
            Rating_score=score,
            Feedback_text=text_feed,
            Feed_reg=student,
            Feed_tea_reg=teacher,
            Feed_cou=course
        )

        messages.success(request, 'Thank you for your valuable feedback')
        return redirect('student_home')

    return render(request, 'feedback.html', {
        'ds': enrolled_courses,
        'previous_feedbacks': previous_feedbacks
    })


def feedbak(request):
    se = Feedback.objects.all()
    return render(request,'feedbak.html',{'se':se})


def delete_feedback(request, id):
    Feedback.objects.get(id = id).delete()
    return redirect('feedbak')


def test(request):
    return render(request,'test.html')

