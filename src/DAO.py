from DTO import Vaccines, Suppliers, Clinics, Logistics
import sqlite3


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self.nextID = 1

    def insert(self, vaccines):
        if vaccines[0] == -1:
            vaccines[0] = self.nextID
        self.nextID = self.nextID + 1

        self._conn.execute("""
               INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [vaccines[0], vaccines[1], vaccines[2], vaccines[3]])

    def update(self, vaccines):
        c = self._conn.cursor()
        c.execute("""
        UPDATE vaccines SET quantity = ? WHERE date = ?      
        """, [vaccines.quantity, vaccines.date])

    def find(self, date1):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM vaccines WHERE date = ?
        """, [date1])
        return Vaccines(c.fetchall()[0])

    def findForRec(self, supp, date1):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM vaccines WHERE (date = ?) AND (supplier = ?) 
        """, [date1, supp])
        x = c.fetchall()
        if len(x) > 0:
            return Vaccines(c.fetchall()[0])
        else:
            return 0

    def sort(self):
        return (self._conn.execute("""
        SELECT * 
        FROM vaccines 
        ORDER BY date ASC """)).fetchall()

    def delete(self, date1):
        self._conn.execute("""
        DELETE FROM vaccines WHERE date = ?
        """, [date1])


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, suppliers):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [suppliers[0], suppliers[1], suppliers[2]])

    def find(self, name1):
        c = self._conn.cursor()
        c.execute("""
        SELECT * FROM suppliers WHERE name = ?
        """, [name1])
        return Suppliers(c.fetchall()[0])


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinics):
        self._conn.execute("""
               INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
           """, [clinics[0], clinics[1], clinics[2], clinics[3]])

    def find(self, location1):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE location = ?
            """, [location1])

        return Clinics(c.fetchall()[0])

    def update(self, clinics1):
        c = self._conn.cursor()
        c.execute("""
         UPDATE clinics SET demand = ? WHERE id = ?      
         """, [clinics1.demand, clinics1.id])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistics):
        self._conn.execute("""
               INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
           """, [logistics[0], logistics[1], logistics[2], logistics[3]])

    def updateSent(self, logistics):
        c = self._conn.cursor()
        c.execute("""
         UPDATE logistics SET count_sent = (?)  WHERE id = (?)      
         """, [logistics.count_sent, logistics.id])

    def updateReceived(self, logistics):
        c = self._conn.cursor()
        c.execute("""
         UPDATE logistics SET count_received = (?)  WHERE id = (?)      
         """, [logistics.count_received, logistics.id])

    def find(self, log_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ?
            """, [log_id])
        return Logistics(c.fetchall()[0])
