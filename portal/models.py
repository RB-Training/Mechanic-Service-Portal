from django.db import models


class Bikename(models.Model):                          #Table for bike models
    name = models.CharField(max_length=100,unique=True,null=True)
    def __str__(self):
        return self.name

class NewVehicle(models.Model):                         #new vehicle table
    Register_No = models.CharField(max_length=15, unique=True)
    Bike_Name = models.ForeignKey(Bikename,on_delete=models.CASCADE)
    Invoice_Date = models.DateField(null=False,blank=False)
    Service_Count = models.PositiveIntegerField(null=False,blank=False)
    Previous_Service_Odo = models.PositiveIntegerField(null=False,blank=False)
    Previous_Service_Date = models.DateField(null=False,blank=False)
    Current_Odo = models.PositiveIntegerField(null=False,blank=False)

    def __str__(self):
        return "Register No->"+str(self.Register_No)+" and  "+"Bike ->"+str(self.Bike_Name)


class rule_engine(models.Model):                        #rules table
    Bike_Name = models.ForeignKey(Bikename,on_delete=models.CASCADE)
    Service_Count = models.PositiveIntegerField(null=False,blank=False)
    projected_odo = models.PositiveIntegerField(null=False,blank=False)
    projected_days = models.CharField(null=False,blank=False,max_length=15)
    buffer_odo = models.PositiveIntegerField(null=False,blank=False)
    buffer_days = models.CharField(null=False,blank=False,max_length=15)

    def __str__(self):
        return " Bike ->"+str(self.Bike_Name)


class serviceCount(models.Model):
    count = models.IntegerField(max_length=1)
    def __str__(self):
        return self.count









