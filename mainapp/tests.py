from django.test import TestCase
from .models import Unit,Profile,Booking, UserManager,User
from django.contrib.auth import get_user_model
User = get_user_model()



# Create your tests here.

# class TestUnit(TestCase):
#   def  setUp(self): 
#    self.unit =Unit.objects.create(id=1, name='1A', width="10", length="15", height="15" ,size="small", occupied=True , daily_charge="400", weekly_charge="2400" ,monthly_charge="8400" , access_code="123", suitable_property="clothes" , average_temperature="30")   

#   def test_instance(self):
#     self.assertTrue(isinstance(self.unit , Unit))

#   def test_save_unit(self):
#     self.unit.save_unit()
#     unit = Unit.objects.all()
#     self.assertTrue(len(unit) > 0) 

  # def test_get_units(self):
  #       self.unit.save()
  #       units = Unit.view_all()
  #       self.assertTrue(len(units) > 0)

  # def test_search_unit(self):
  #       self.unit.save()
  #       unit = Unit.search('test')
  #       self.assertTrue(len(unit) != 1)

  # def test_delete_unit(self):
  #   self.unit.delete_unit('unit_name')
  #   unit = Unit.search('test')
  #   self.assertTrue(len(unit)<1)



# class TestUser(TestCase):
#   def  setUp(self):
#       self.user = User.objects.create(username='sia', email="tajeusanta@gmail.com",name="siantayo", user_type="client", is_staff=True, is_superuser=True,is_active=False,last_login="",date_joined="" ,USERNAME_FIELD="email" ,EMAIL_FIELD = 'email',	REQUIRED_FIELDS = []
# )
#       self.user.save()

# class TestProfile(TestCase):
#   def setUp(self):
#     self.user = User.objects.create(username='sia', email="tajeusanta@gmail.com",name="siantayo", user_type="client", is_staff=True, is_superuser=True,is_active=False,last_login="",date_joined="" )
#     self.user.save()
#      self.profile = Profile.objects.create(id=1, user=self.user, pic='https://res-console.cloudinary.com/instagram-santa/thumbnails/transform/v1/image/upload//v1627631217/ZnJ3b203aXFuYTBlcXdwOWNydGc=/drilldown?0.37747607967659147', phone_number='0987654', location="kahawa", address='West',nok_fullname="Sian",nok_email="sian@gmail.com",nok_number="0981234",nok_relationship="sister")

#   def test_instance(self):
#       self.assertTrue(isinstance(self.profile, Profile))

#   def test_save_user(self):
#       self.profile.save_user()
#       after = Profile.objects.all()
#       self.assertTrue(len(after) > 0)





class TestBooking(TestCase):
  def  setUp(self):
    self.new_user = User.objects.create(username='sia', email="tajeusanta@gmail.com",name="siantayo", user_type="client", is_staff=True, is_superuser=True,is_active=False,last_login="2001-11-12",date_joined="2001-11-12")
    self.profile = Profile.objects.create( id=2 ,user=self.new_user, pic='https://www.shutterstock.com/image-photo/home-office-dress-code-girl-strict-1719984745', phone_number='09249654', location="buru", address='buru',nok_fullname="Sia",nok_email="sia@gmail.com",nok_number="15681234",nok_relationship="brother")
    self.unit =Unit.objects.create( name='1A', width="10", length="15", height="15" ,size="small", occupied=True , daily_charge="400", weekly_charge="2400" ,monthly_charge="8400" , access_code="123", suitable_property="clothes" , average_temperature="30") 
    self.booking =Booking.objects.create( profile=self.profile, unit=self.unit ,description="Foods", start_date="2001-11-12" ,end_date="2001-11-12", address ="1234" , pickup=False, delivery=True, delivery_address="southB", billing_Cycle="monthly" ,payment_mode="mpesa", account_number="1234", cost="5000", total_cost = "6000")   

  def test_instance(self):
    self.assertTrue(isinstance(self.booking , Booking))

  def test_save_booking(self):
    self.booking.save_booking()
    booking = Booking.objects.all()
    self.assertTrue(len(booking) > 0)            

  def test_delete_booking(self):
    self.booking.delete_booking(id)
    booking = Unit.search('test')
    self.assertTrue(len(booking)<1)

  def test_get_bookings(self):
        self.booking.save()
        bookings = Booking.view_all()
        self.assertTrue(len(bookings) > 0)


