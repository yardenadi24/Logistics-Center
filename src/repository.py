
import sqlite3
from DAO import _Vaccines, _Suppliers, _Logistics, _Clinics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.logistics = _Logistics(self._conn)
        self.clinics = _Clinics(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):

        self._conn.executescript("""
            CREATE TABLE logistics(                                                    
            id INTEGER PRIMARY KEY,                                                    
            name STRING NOT NULL,                                                      
            count_sent INTEGER NOT NULL,                                               
            count_received INTEGER NOT NULL);
                                                                           
            CREATE TABLE suppliers(                                                    
            id INTEGER PRIMARY KEY,                                                    
            name STRING NOT NULL,                                                      
            logistic INTEGER REFERENCES logistics(id)           
            );
                                                                                   
            CREATE TABLE clinics(                                                      
            id INTEGER PRIMARY KEY,                                                    
            location STRING NOT NULL,                                                  
            demand INTEGER NOT NULL,                                                                                                             
            logistic INTEGER REFERENCES logistics(id)                             
            );  
            
            CREATE TABLE vaccines(                             
            id INTEGER PRIMARY KEY,                                                    
            date DATE NOT NULL,                                                        
            supplier INTEGER REFERENCES suppliers(id),                                                 
            quantity INTEGER NOT NULL); 
                                                                                  
          """)

    def totalDemand(self):
        return ((self._conn.execute("""
        SELECT SUM(clinics.demand) FROM clinics
        """)).fetchone())

    def totalInv(self):
        return ((self._conn.execute("""
        SELECT SUM(vaccines.quantity) FROM vaccines
        """)).fetchone())

    def totalSent(self):
        return ((self._conn.execute("""
        SELECT SUM(logistics.count_sent) FROM logistics
        """)).fetchone())

    def totalReceived(self):
        return ((self._conn.execute("""
        SELECT SUM(logistics.count_received) FROM logistics
        """)).fetchone())

    def sendOrder(self, temp):

        location = temp[0]

        amount = int(temp[1])

        clinic = self.clinics.find(location)
        logiObj = self.logistics.find(clinic.logistic)
        logiObj.count_sent = logiObj.count_sent + amount
        self.logistics.updateSent(logiObj)
        x = self.vaccines.sort()

        if amount > x[0][3]:
            while amount > x[0][3]:
                amount = amount - x[0][3]
                clinic.demand = clinic.demand - x[0][3]
                self.clinics.update(clinic)
                self.vaccines.delete(x[0][1])
                x = self.vaccines.sort()
        if amount == x[0][3]:
            clinic.demand = clinic.demand - x[0][3]
            self.clinics.update(clinic)
            self.vaccines.delete(x[0][1])
        if amount < x[0][3]:
            clinic.demand = clinic.demand - amount
            self.clinics.update(clinic)
            vaci = self.vaccines.find(x[0][1])
            vaci.quantity = vaci.quantity - amount
            self.vaccines.update(vaci)

        return [self.totalInv()[0], self.totalDemand()[0], self.totalReceived()[0], self.totalSent()[0]]

    def reciveOrder(self, temp):
        name = temp[0]
        amount = int(temp[1])
        date = temp[2]

        supplier1 = self.suppliers.find(name)
        logObj = self.logistics.find(supplier1.logistic)
        logObj.count_received = logObj.count_received + amount
        self.logistics.updateReceived(logObj)
        y = self.vaccines.findForRec(supplier1.id, date)
        if y == 0:
            self.vaccines.insert([-1, date, supplier1.id, amount])
        else:
            y.quantity = y.quantity + amount
            self.vaccines.update(y)

        return [self.totalInv()[0], self.totalDemand()[0], self.totalReceived()[0], self.totalSent()[0]]


repo = _Repository()
