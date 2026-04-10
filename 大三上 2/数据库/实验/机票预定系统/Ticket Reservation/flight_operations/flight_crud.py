from db_utils import DatabaseManager

class FlightCRUD:
    def __init__(self, db_name='airline_ticket_system.db'):
        self.db = DatabaseManager(db_name)
        self.db.connect()

    def add_flight(self, flight_data):
        sql = '''INSERT INTO Flight (FlightNo, Airline, Departure, Destination, DepartureTime, ArrivalTime, AircraftType, SeatCount, RemainingSeats, Price, Status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        return self.db.execute(sql, flight_data)

    def get_flights(self):
        sql = 'SELECT * FROM Flight'
        return self.db.fetch_all(sql)

    def update_flight(self, flight_id, update_data):
        sql = '''UPDATE Flight SET FlightNo=?, Airline=?, Departure=?, Destination=?, DepartureTime=?, ArrivalTime=?, AircraftType=?, SeatCount=?, RemainingSeats=?, Price=?, Status=? WHERE FlightID=?'''
        return self.db.execute(sql, update_data + (flight_id,))

    def delete_flight(self, flight_id):
        sql = 'DELETE FROM Flight WHERE FlightID=?'
        return self.db.execute(sql, (flight_id,))

    def get_flight_by_id(self, flight_id):
        sql = 'SELECT * FROM Flight WHERE FlightID=?'
        return self.db.fetch_one(sql, (flight_id,))

    def __del__(self):
        self.db.close()
