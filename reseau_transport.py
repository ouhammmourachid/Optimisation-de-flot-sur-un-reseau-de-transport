import numpy as np
class City:
    # the Constructor of the city 
    def __init__(self ,id : int ,name : str ):
        self.id = id
        self.name = name
        self.m = []
    # seter methode
    def SetCityName(self ,new_name):
        self.name = new_name
    # geter methode
    def GetId(self):
        return self.id

    def GetName(self):
        return self.name
    # to change self lock as string
    def __str__(self):
        return str(self.id)+":"+self.name
    
class Road:
    # the Constructor of the road.
    def __init__(self ,start_city : City ,end_city : City ,capacity : int):
        self.start_city = start_city
        self.end_city = end_city
        self.capacity = capacity
        self.flow = 0
    # seter methode
    def SetStart_city(self ,new_start_city):
        self.start_city = new_start_city

    def SetEnd_city(self ,new_end_city):
        self.end_city = new_end_city

    def SetCapacity(self ,new_capacity):
        self.capacity = new_capacity
    # geter methode
    def GetStart_city(self):
        return self.start_city

    def GetEnd_city(self):
        return self.end_city

    def GetCapacity(self):
        return self.capacity
    # to change self lock as string
    def __str__(self):
        return str(self.start_city)+"------"+str(self.capacity)+"/"+str(self.flow)+"------>"+str(self.end_city)


class TransportNetwork:

    total_city = 0
    total_Road = 0
    def __init__(self):
        self.all_cities = dict()
        self.all_road = dict()

    def AddCity(self ,id ,name):
        if id not in self.all_cities:
            city = City(id ,name)
            self.all_cities[id] = city
            self.total_city += 1
        else :
            print(f'this id {id} allready associated with the city \
                {self.all_cities[id]} please try an other one .')
    
    def AddRoad(self ,id_start_city ,id_end_city ,capacity = 0):
        if (id_start_city in self.all_cities) and (id_end_city in self.all_cities) \
        and ( (id_start_city,id_end_city) not in self.all_road):
            start_city = self.all_cities[id_start_city]
            end_city = self.all_cities[id_end_city]
            road = Road(start_city ,end_city ,capacity)
            self.all_road[(id_start_city,id_end_city)] = road
            self.total_Road += 1
        else:
            print("one of the city id doesn't exist yet .")
    
    def isNeighbour(self ,u ,v):
        if ((u,v) in self.all_road) or ((v,u) in self.all_road):
            return True
        return False

    def print_road(self):
        for road in self.all_road.values():
            print(road)

    def GetCity(self ,id):
        try :
            return self.all_cities[id]
        except:
            return None
    def GetRoad(self ,id_start_city ,id_end_city):
        try:
            return self.all_road[(id_start_city,id_end_city)]
        except:
            return None
    
    def GetFlow(self ,id_start_city ,id_end_city):
        try:
            return self.all_road[(id_start_city,id_end_city)].flow
        except:
            return None

    def SetFlow(self,id_start_city ,id_end_city,new_flow):
        try:
            self.all_road[(id_start_city,id_end_city)].flow += new_flow
        except:
            print("this road doesn't exist yet !!")

    def GetInfo(self,id):
        try :
            return self.all_cities[id].m
        except:
            return None

    def SetInfo(self,id,new_info):
        self.all_cities[id].m = new_info
    
    def IsFull(self ,id_start_city ,id_end_city):
        return self.GetFlow(id_start_city ,id_end_city) == \
            self.GetRoad(id_start_city ,id_end_city).capacity
        
    def GetAllCitiesIds(self):
        return self.all_cities.keys()

class Optimisation(TransportNetwork):
    def __init__(self ,source :int ,sink :int):
        super().__init__()
        self.source = source
        self.sink = sink
        self.Vf = 0

    def exist_j(self ,S):
        global exist_i
        global exist_j
        X_S = (i for i in self.GetAllCitiesIds() if i not in S)
        for j in X_S:
            for i in S:
                if (self.GetRoad(i ,j)!=None) and \
                    (self.GetRoad(i ,j).capacity - self.GetFlow(i,j) > 0\
                        or self.GetFlow(i,j) > 0) and not (self.IsFull(i,j)) :
                    exist_i = i
                    exist_j = j
                    return True
        return False

    def optimisation_de_flot(self):
        self.SetInfo(self.source ,[np.inf ,np.inf ,+1])
        S = [self.source]
        while self.exist_j(S):
            i = exist_i
            j = exist_j
            if self.GetRoad(i ,j).capacity - self.GetFlow(i ,j) > 0:
                self.SetInfo(j, [i ,min(self.GetInfo(i)[1],\
                    self.GetRoad(i ,j).capacity - self.GetFlow(i,j)),+1])
            else:
                print(self.GetFlow(j,i))
                self.SetInfo(j ,[i ,min(self.GetInfo(i)[1],self.GetFlow(j ,i)),-1])
            S.append(j)
            if j == self.sink:
                self.Vf += self.GetInfo(j)[1]
                break
        if self.sink in S:
            while j != self.source:
                if self.GetInfo(j)[2]>0:
                    self.SetFlow(self.GetInfo(j)[0] ,j,self.GetInfo(self.sink)[1])
                else:
                    self.SetFlow(j,self.GetInfo(j)[0],-1*self.GetInfo(self.sink)[1])
                j = self.GetInfo(j)[0]
            self.optimisation_de_flot()
        
T = Optimisation(1,7)
T.AddCity(1,"Casablanca")
T.AddCity(7,"Agadir")
for i in range(2,7):
    T.AddCity(i,"city:"+str(i))
G = [[0,5,8,0,0,0,0],[0,0,0,4,2,0,0],[0,0,0,0,5,2,0],\
    [0,0,0,0,0,0,7],[0,0,0,0,0,0,3],[0,0,0,0,0,0,3],[0,0,0,0,0,0,0]]
for i in range(7):
    for j in range(7):
        if G[i][j]!=0:
            T.AddRoad(i+1,j+1,G[i][j])
print("--------------------------------------\n")
T.print_road()
print("the number of the car on the road is :",T.Vf,"\n")
T.optimisation_de_flot()
print("--------------------------------------\n")
T.print_road()
print("the number of the car on the road is :",T.Vf,"\n")


