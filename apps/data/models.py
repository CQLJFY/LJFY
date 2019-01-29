from django.db import models
from django.contrib.gis.db import models

# Create your models here.


class Surveyattribute(models.Model):
    idsurveyattribute = models.AutoField(verbose_name='ID',db_column='idSurveyAttribute', primary_key=True)  # Field name made lowercase.
    pjid = models.CharField(verbose_name='工程编号',db_column='PJID', max_length=50)  # Field name made lowercase.
    pjname = models.CharField(verbose_name='工程名称',db_column='PJName', max_length=150)  # Field name made lowercase.
    surveyperson = models.CharField(verbose_name='测量员',db_column='SurveyPerson', max_length=45)  # Field name made lowercase.
    surveytime = models.IntegerField(verbose_name='测量时间',db_column='SurveyTime')  # Field name made lowercase.
    filetype = models.CharField(verbose_name='文件类型',db_column='FileType', max_length=45)  # Field name made lowercase.
    isanalysed = models.IntegerField(verbose_name='状态',db_column='IsAnalysed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'surveyattribute'
        verbose_name = "工程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pjname[0:50]+'...'


class Surveyfile(models.Model):
    idsurveyfile = models.AutoField(verbose_name='ID',db_column='IDsurveyfile', primary_key=True)  # Field name made lowercase.
    filepath = models.CharField(verbose_name='文件路径',db_column='FilePath', max_length=300)  # Field name made lowercase.
    ctime = models.DateTimeField(verbose_name='上传时间',db_column='Ctime')  # Field name made lowercase.
    mtime = models.DateTimeField(verbose_name='建立时间',db_column='Mtime')  # Field name made lowercase.
    said = models.ForeignKey(Surveyattribute,models.DO_NOTHING, db_column='SAID')  # Field name made lowercase.
    content = models.BinaryField(verbose_name='文件内容',db_column='Content')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'surveyfile'
        verbose_name = "文件信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.said


class EfficiencyStatistic(models.Model):
    statistic_id = models.AutoField(verbose_name='ID',primary_key=True)
    source = models.ForeignKey('Surveyattribute', models.DO_NOTHING)
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    number_point = models.IntegerField(verbose_name='采集点数')
    survey_time = models.FloatField(verbose_name='时间段')
    total_time = models.FloatField(verbose_name='总时间',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'efficiency_statistic'
        verbose_name = "工作效率"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.source


class CheckInformation(models.Model):
    check_category = models.CharField(verbose_name='检查内容',max_length=30)
    log_level = models.CharField(verbose_name='等级',max_length=15)
    information = models.CharField(verbose_name='内容描述',max_length=100)
    detail = models.CharField(verbose_name='详细内容',max_length=600)
    source = models.ForeignKey('Surveyattribute', models.DO_NOTHING)
    information_id = models.AutoField(verbose_name='ID',primary_key=True)

    class Meta:
        managed = False
        db_table = 'check_information'
        verbose_name = '检查内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.source[0:50]+'...'


class Points2018(models.Model):
    source = models.ForeignKey('Surveyattribute', models.DO_NOTHING)
    wkbgeometry = models.PointField(verbose_name='坐标',srid=0, dim=3)
    code = models.CharField(verbose_name='编码',max_length=15, blank=True, null=True)
    observe_time = models.DateTimeField(verbose_name='测量时间',blank=True, null=True)
    geometry_id = models.AutoField(verbose_name='ID',primary_key=True)

    class Meta:
        managed = False
        db_table = 'points_2018'
        verbose_name = '点位数据'
        verbose_name_plural = verbose_name
