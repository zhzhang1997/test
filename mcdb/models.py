from django.db import models

class Administrator(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='管理员ID')
    phone=models.CharField(max_length=20, verbose_name='管理员手机号')
    email=models.EmailField(verbose_name='管理员邮箱')
    password=models.CharField(max_length=30, verbose_name='管理亚密码')

    class Meta:
        verbose_name='管理员'
        verbose_name_plural=verbose_name

class Address(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='分店ID')
    address=models.CharField(max_length=200, verbose_name='分店地址')
    isDelete = models.BooleanField(default=False)
    test1 = models.CharField(max_length=10, default='DXZ', verbose_name='测试')
    class Meta:
        verbose_name='分店'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.address

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue
            data[f.name] = value

        return data

class Student(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='学生ID')
    openid=models.CharField(max_length=50, verbose_name='微信OPENID')
    name = models.CharField(max_length=20,verbose_name='微信昵称')
    real_name = models.CharField(max_length=20, default='尚未录入真实姓名', verbose_name='真实姓名')
    test1 = models.CharField(max_length=10, default='DXZ', verbose_name='测试')
    phone = models.CharField(max_length=20, default='尚未录入手机号', verbose_name='学生手机号')     # 用户账号
    password = models.CharField(max_length=100, verbose_name='学生密码')
    gender = models.CharField(max_length=5, verbose_name='性别',choices=(('0','未知'),('1','男'),('2', '女')))
    age = models.CharField(max_length=10, verbose_name='学生年龄')
    content = models.CharField(max_length=20, verbose_name='学生个人介绍')
    isDelete = models.BooleanField(default=False)
    belong=models.ForeignKey(to='Address',on_delete=models.CASCADE, verbose_name='所属分店')

    class Meta:
        verbose_name='学生'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.real_name+'('+ self.phone +')'

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, models.ForeignKey):
                if f.name == 'belong':
                    value = Address.objects.get(id=value).to_dict()
            data[f.name] = value

        return data


class Teacher(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='老师ID')
    openid = models.CharField(max_length=50, verbose_name='微信OPENID')
    name=models.CharField(max_length=20, verbose_name='老师姓名')
    gender=models.BooleanField(verbose_name='性别',choices=((0,'男'),(1,'女')))
    age = models.CharField(max_length=10, verbose_name='老师年龄')
    content = models.CharField(max_length=20, verbose_name='老师个人介绍')
    isDelete = models.BooleanField(default=False)
    belong = models.ForeignKey(to='Address',on_delete=models.CASCADE, verbose_name='老师所属分店')
    class Meta:
        verbose_name='老师'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, models.ForeignKey):
                if f.name == 'belong':
                    value = Address.objects.get(id=value).to_dict()

            data[f.name] = value

        return data

class Course(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='课程ID')
    name = models.CharField(max_length=20, verbose_name='课程名称')
    content = models.CharField(max_length=20, verbose_name='课程介绍')
    date=models.DateTimeField(verbose_name='时间')
    max_number = models.IntegerField(verbose_name='课程容纳最多人数')
    current_number = models.IntegerField(default=0, verbose_name='当前选课人数')
    isDelete = models.BooleanField(default=False)
    students = models.ManyToManyField(to='Student', through='Course2Student', through_fields=('course', 'student'), verbose_name='本课程的学生')
    teacher=models.ForeignKey(to='Teacher',on_delete=models.CASCADE, verbose_name='本课程所属老师')
    belong = models.ForeignKey(to='Address', on_delete=models.CASCADE, verbose_name='本课程所属分店')
    class Meta:
        verbose_name='课程'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, models.ForeignKey):
                if f.name=='teacher':
                    value=Teacher.objects.get(id=value).to_dict()
                elif f.name=='belong':
                    value = Address.objects.get(id=value).to_dict()

            data[f.name] = value

        return data

class Course2Student(models.Model):
    course=models.ForeignKey(to='Course',on_delete=models.CASCADE)
    student=models.ForeignKey(to='Student',on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)

    class Meta:
        unique_together=(('course','student'),)
        verbose_name = '学生课程关联表'
        verbose_name_plural = verbose_name


class VIPType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='会员种类ID')
    name = models.CharField(max_length=50, verbose_name='会员名称')
    students = models.ManyToManyField(to='Student', through='VIP2Student', through_fields=('vip', 'student'), verbose_name='本种类会员下的学生')

    class Meta:
        verbose_name='会员类别'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class VIP2Student(models.Model):
    vip = models.ForeignKey(to='VIPType', on_delete=models.CASCADE)
    student = models.ForeignKey(to='Student', on_delete=models.CASCADE)
    start_time = models.DateField(verbose_name='会员开始日期')
    end_time = models.DateField(verbose_name='会员截止日期')
    isDelete = models.BooleanField(default=False)

    class Meta:
        unique_together=(('vip','student', 'start_time'),)
        verbose_name = '学生会员'
        verbose_name_plural = verbose_name
