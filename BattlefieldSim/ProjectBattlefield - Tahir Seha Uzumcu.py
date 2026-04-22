my_name = "Tahir Seha Uzumcu"
my_id = "220102002067"
my_email = "t.uzumcu2022@gtu.edu.tr"

class Transceiver():
    ide = 0
    def __init__(self, x, y ,tpower, rpower=0.001):
        self.lt = 0
        self.x = x
        self.y = y
        self.t = tpower
        self.r = rpower
        self.id = Transceiver.ide
        if type(self)==Transceiver:
            Transceiver.ide += 1
    

    def get_coordinate_x(self):
        return self.x
   
    def get_coordinate_y(self):
        return self.y
    
    def get_coordinates(self):
        return (self.x,self.y)
   
    def get_tpower(self):
        return self.t
    
    def get_rpower(self):
        return self.r
  
    def get_id(self):
        return self.id

    def get_localtime(self):
        return self.lt
    
    def set_coordinates(self, x, y):
        self.x = x
        self.y = y
        (self.x,self.y) = (x,y)
        
    def set_transmitting_power(self, tpower):
        self.t = tpower
    
    def set_receiving_power(self,rpower):
        self.r = rpower
        
    def update_local_time(self,time):
        self.lt = time
        
    def distance(self,m):
        a = abs((self.x-m.x)**2+(self.y-m.y)**2)**0.5
        return a
    
    def transmitted_power(self,a):
        try:
            b = ((self.x-a[0])**2+(self.y-a[1])**2)**0.5
            t = self.get_tpower()/b
            if b > 0 and b < 1:
                return self.get_tpower()
            return t
        except ZeroDivisionError:
            return self.get_tpower()
    
    def __eq__(self,other):
        return self.transmitted_power(other.get_coordinates()) >= other.get_rpower() and other.transmitted_power(self.get_coordinates()) >= self.get_rpower()
          
    def __lt__(self,other):
        return self.transmitted_power(other.get_coordinates()) >= other.get_rpower()
    
    def __gt__(self,other):
        return other.transmitted_power(self.get_coordinates()) >= self.get_rpower()
    
    def __str__(self):
        if self.get_tpower()>=1000 and self.get_rpower()<=1:
            return "Class: Tower\nTower number: "+str(self.id)+'\nCoordinates: <{},{}>'.format(self.x, self.y)+'\nTransmitting Power: '+str(self.get_tpower()/1000)+'kW'+'\nMin. Receiving Power: '+str(self.get_rpower()*1000)+'mW'
        elif self.get_tpower()>=1000:
            return "Class: Tower\nTower number: "+str(self.id)+'\nCoordinates: <{},{}>'.format(self.x, self.y)+'\nTransmitting Power: '+str(self.get_tpower()/1000)+'kW'+'\nMin. Receiving Power: '+str(self.get_rpower())+'W'
        elif self.get_rpower()<=1:
            return "Class: Tower\nTower number: "+str(self.id)+'\nCoordinates: <{},{}>'.format(self.x, self.y)+'\nTransmitting Power: '+str(self.get_tpower())+'W'+'\nMin. Receiving Power: '+str(self.get_rpower()*1000)+'mW'
        else:
            return "Class: Tower\nTower number: "+str(self.id)+'\nCoordinates: <{},{}>'.format(self.x, self.y)+'\nTransmitting Power: '+str(self.get_tpower())+'W'+'\nMin. Receiving Power: '+str(self.get_rpower())+'W'
        
       
    

class Robot(Transceiver):
    ide = 0
    def __init__(self, x, y, vx, vy):
        tpower= 1
        self.t = tpower
        self.dt=0
        self.st = True
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        super().__init__(x,y,tpower)
        rpower=0.01
        self.r = rpower
        self.id = Robot.ide
        Robot.ide+=1
    
    def get_velocity(self):
        return (self.vx,self.vy)
    
    def get_status(self):
        return self.st
    
    def get_disconnect_time(self):
        return self.dt
    
    def get_id(self):
        return self.id
    
    def set_velocity(self, vx,vy):
        self.vx = vx
        self.vy = vy
        
    def set_status(self,newstatus):
        self.st = newstatus
        
    def update_disconnect(self):
        self.dt +=1
    
    def set_disconnect_time(self):
        self.dt = 0
    
    def update_location(self):
        self.lt += 1
        self.x += self.vx
        self.y += self.vy    
    
    def __str__(self):
        if self.st ==True:
            return "Class: Robot\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Alive'
        else:
            return "Class: Robot\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Dead'
            

class Guard(Robot):
    def __init__(self,x,y,vx,vy,period=60,localtime=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        super().__init__(x,y,vx,vy)
        self.p = period
        self.lt = localtime
        
        
    def get_period(self):
        return self.p
    
    def set_period(self,period):
        self.lt= 0
        self.p=period
        
    def update_location(self):
        self.lt+=1
        if self.lt%self.p==0:
            temp = self.vy 
            self.vy = -1*self.vx
            self.vx = temp
        self.x +=self.vx
        self.y +=self.vy
        
    def __str__(self):
        if self.st ==True:
            return "Class: Guard\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Alive'
        else:
            return "Class: Guard\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Dead' 
        
    
from random import randint
from random import uniform
class Psycho(Robot):
    
    def __init__(self,x,y,vx=uniform(-10,10),vy=uniform(-10,10)):
        super().__init__(x,y,vx,vy)
        period = randint(0,100)
        self.p = period
        self.x = x
        self.y = y



    def update_location(self):
        self.lt += 1
        if self.lt%self.p==0:
            self.p = randint(1,100)
            self.vx= uniform(-10,10)
            self.vy = uniform(-10,10)
        self.x+=self.vx
        self.y+=self.vy
    
    def __str__(self):
        if self.st ==True:
            return "Class: Psycho\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Alive'
        else:
            return "Class: Psycho\nRobot number: "+str(self.id)+'\nCurrent Coordinates: <{},{}>'.format(self.x, self.y)+'\nCurrent Velocity: <{},{}>'.format(self.vx,self.vy)+'\nTransmitting Power: '+str(self.t)+'W'+'\nMin. Receiving Power: '+str(self.r*1000)+'mW'+'\nStatus: Dead' 
            
        

class Battle_Field():
    def __init__(self):
        self.tl =[]
        self.rl =[]
        self.drl = []
        self.globt=0
    
    def add_transceiver(self,x,y,tpower,rpower=0.001):
        a=Transceiver(x,y,tpower,rpower=0.001)
        self.tl.append(a)        
    
    def add_robot(self,x,y,vx,vy):
        self.rl.append(Robot(x,y,vx,vy))
    
    def add_guard(self,x,y,vx,vy,period=60,localtime=0):
        self.rl.append(Guard(x,y,vx,vy,period=60,localtime=0))
    
    def add_psycho(self,x,y):
        self.rl.append(Psycho(x,y))
        

    def get_transceivers(self):
        #'''
        field=Battle_Field()
        field.add_transceiver(0,0,10)
        field.add_transceiver(1200,0,15)
        field.add_transceiver(500,500,12)
        
        for e in field.get_transceivers():
            e.get_id()
            e.get_coordinates()
            e.get_tpower()
        
        0
        (0, 0)
        10
        1
        (1200, 0)
        15
        2
        (500, 500)
        12
        #'''

        for i in range(len(self.tl)):
            a = self.tl[i]
            yield a
  
    def get_robots(self):
      #  '''
         field=Battle_Field()
         field.add_robot(10,25,10,0)
         field.add_robot(500,750,-10,10)
         field.add_robot(500,750,5,10)
         field.add_guard(40,58,10,10)
         field.add_guard(1000,0,10,0)
         field.add_guard(750,800,-10,0)
         field.add_psycho(-10,60)
         field.add_psycho(20,320)
         field.add_psycho(500,1020)
         field.add_psycho(750,300)
         field.add_psycho(-300,320)
         field.add_psycho(0,0)
         robotlist=[]
         for e in field.get_robots():
             e.get_id()
             e.get_coordinates()
             e.get_velocity()
             e.get_tpower()
             e.get_status()
             robotlist.append(e)
        
     

#        '''
         for i in range(len(self.rl)):
            a = self.rl[i]
            yield a
    
    def kill_robot(self,robot):
        
      #  '''
         field=Battle_Field()
         field.add_robot(10,25,10,0)
         field.add_robot(500,750,-10,10)
         field.add_robot(500,750,5,10)
         field.add_guard(40,58,10,10)
         field.add_guard(1000,0,10,0)
         field.add_guard(750,800,-10,0)
         field.add_psycho(-10,60)
         field.add_psycho(20,320)
         field.add_psycho(500,1020)
         field.add_psycho(750,300)
         field.add_psycho(-300,320)
         field.add_psycho(0,0)
         robotlist=[]
         for e in field.get_robots():
             e.get_id()
             e.get_coordinates()
             e.get_velocity()
             e.get_tpower()
             e.get_status()
             robotlist.append(e)
         field.kill_robot(robotlist[-1])
     #   '''
        
         robot.set_status(False)
         self.drl.append(robot)
         l = robot.get_id()
         p =0
         for i in range(len(self.rl)):
            if self.rl[i].get_id()==l:
                 p = i
         del self.rl[p]
        
        
    def get_deadrobots(self):
      #  '''
         field=Battle_Field()
         for e in field.get_deadrobots():
             e.get_id()
             e.get_coordinates()
             e.get_velocity()
             e.get_tpower()
             e.get_status()
        
      #  '''
         for i in range(len(self.drl)):
            a = self.drl[i]
            yield a
            
    
    def remove_robot(self,robotid):
        for i in range(len(self.rl)):
            if self.rl[i].get_id() == robotid:
                del self.rl[i]
                break
    
    
    def remove_transceiver(self,trid):
        for i in range(len(self.tl)):
            if self.tl[i].get_id() == trid:
                del self.tl[i]
                break
    
    def progress_time(self):
        self.globt+=1
        for transceiver in self.tl:
            transceiver.update_local_time(transceiver.get_localtime() + 1)
        for robot in self.rl:
            robot.update_location()
        for robot in self.rl[:]:
            is_connected = False 
            for transceiver in self.tl:
                if transceiver.transmitted_power(robot.get_coordinates()) >= robot.get_rpower():
                        is_connected = True
                        break
            if not is_connected:
                robot.update_disconnect()
            else:
                robot.set_disconnect_time()

            if robot.get_disconnect_time()>60:
                robot.st= False
                self.kill_robot(robot)
                
    def __str__(self):
        return 'Number of transceivers: '+str(len(self.tl))+'\nNumber of alive robots: '+str(len(self.rl))+'\nNumber of dead robots: '+str(len(self.drl))
    
    def create_report(self):
        print('Time: '+str(self.globt)+'\nNumber of transceivers: '+str(len(self.tl))+'\nNumber of alive robots: '+str(len(self.rl))+'\nNumber of dead robots: '+str(len(self.drl)))
        for i in self.tl:
            print(i)
        for i in self.rl:
            print(i)
        for i in self.drl:
            return (i)




