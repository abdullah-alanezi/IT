
from django.db import models
from django.contrib.auth.models import User

class MaintenanceRequest(models.Model):

    
    STATUS_CHOICES = [
        ('مفتوح','مفتوح' ),
        ( 'تحت الإجراء','تحت الإجراء'),
        
        ('منتهي','منتهي'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255)
    device_id = models.CharField(max_length=100)
    problem_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='مفتوح')
    request_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',default="images/default.jpg")
    
    
    def __str__(self):
        return f'{self.device_type} - {self.device_id} ({self.user.username})'
    



class PrinterRequest(models.Model):

    
    STATUS_CHOICES = [
        ('مفتوح','مفتوح' ),
        ( 'تحت الإجراء','تحت الإجراء'),
        
        ('منتهي','منتهي'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer_type = models.CharField(max_length=255)
    printer_id = models.CharField(max_length=100)
    ink_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='مفتوح')
    request_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',default="images/default.jpg")
    
    
    def __str__(self):
        return f'{self.printer_type} - {self.printer_id} ({self.user.username})'
    


class ItHelp(models.Model):

    it_employee = models.ForeignKey(User,on_delete=models.CASCADE)
    
    user_request = models.ForeignKey(MaintenanceRequest,on_delete=models.CASCADE)

    #user_request_p = models.ForeignKey(PrinterRequest,on_delete=models.CASCADE)



class PrinterHelp(models.Model):

    it_employee = models.ForeignKey(User,on_delete=models.CASCADE)
    

    user_request_p = models.ForeignKey(PrinterRequest,on_delete=models.CASCADE)





class Chat(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    content = models.TextField()