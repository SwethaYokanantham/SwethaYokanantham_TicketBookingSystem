from enum import Enum
from datetime import datetime


class EventType(Enum):
    MOVIE = "Movie"
    SPORT = "Sport"
    CONCERT = "Concert"


class EventNotFoundException(Exception):
    def __init__(self, event_name):
        super().__init__(f"Event '{event_name}' not found.")


class InvalidBookingIDException(Exception):
    def __init__(self, booking_id):
        super().__init__(f"Invalid booking ID: {booking_id}")


class Venue:
    def __init__(self, venue_name, address):
        self.venue_name = venue_name
        self.address = address

    def display_venue_details(self):
        print(f"Venue Name: {self.venue_name}")
        print(f"Address: {self.address}")


class Event:
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, event_type):
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.venue = venue
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.ticket_price = ticket_price
        self.event_type = event_type

    def calculate_total_revenue(self, num_tickets):
        return self.ticket_price * num_tickets

    def getBookedNoOfTickets(self):
        return self.total_seats - self.available_seats

    def book_tickets(self, num_tickets):
        if num_tickets > self.available_seats:
            raise ValueError(f"Only {self.available_seats} tickets available for {self.event_name}.")

        self.available_seats -= num_tickets
        print(f"{num_tickets} tickets booked for {self.event_name}. Available seats: {self.available_seats}")

    def cancel_booking(self, num_tickets):
        self.available_seats += num_tickets
        print(f"{num_tickets} tickets cancelled for {self.event_name}. Available seats: {self.available_seats}")

    def display_event_details(self):
        print(f"Event: {self.event_name}")
        print(f"Date: {self.event_date} Time: {self.event_time}")
        self.venue.display_venue_details()
        print(f"Total Seats: {self.total_seats} | Available Seats: {self.available_seats}")
        print(f"Ticket Price: ${self.ticket_price}")
        print(f"Event Type: {self.event_type.value}")


class Movie(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, genre, actor_name,
                 actress_name):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, EventType.MOVIE)
        self.genre = genre
        self.actor_name = actor_name
        self.actress_name = actress_name


class Concert(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, artist):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, EventType.CONCERT)
        self.artist = artist


class Sport(Event):
    def __init__(self, event_name, event_date, event_time, venue, total_seats, ticket_price, sport_name, teams_name):
        super().__init__(event_name, event_date, event_time, venue, total_seats, ticket_price, EventType.SPORT)
        self.sport_name = sport_name
        self.teams_name = teams_name


class Customer:
    def __init__(self, customer_name, email, phone_number):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number

    def display_customer_details(self):
        print(f"Customer Name: {self.customer_name}")
        print(f"Email: {self.email}")
        print(f"Phone Number: {self.phone_number}")


class Booking:
    booking_id = 0

    def __init__(self, customers, event, num_tickets):
        self.booking_id = Booking.booking_id
        Booking.booking_id += 1
        self.customers = customers
        self.event = event
        self.num_tickets = num_tickets
        self.total_cost = event.calculate_total_revenue(num_tickets)
        self.booking_date = datetime.now()

    def display_booking_details(self):
        print(f"Booking ID: {self.booking_id}")
        print("Customers:")
        for customer in self.customers:
            customer.display_customer_details()
        self.event.display_event_details()
        print(f"Number of Tickets: {self.num_tickets}")
        print(f"Total Cost: ${self.total_cost}")
        print(f"Booking Date: {self.booking_date}")


class TicketBookingSystem:
    def __init__(self):
        self.events = []

    def create_event(self, event_name, event_date, event_time, venue, total_seats, ticket_price, event_type, **kwargs):
        if event_type == EventType.MOVIE:
            event = Movie(event_name, event_date, event_time, venue, total_seats, ticket_price, **kwargs)
        elif event_type == EventType.CONCERT:
            event = Concert(event_name, event_date, event_time, venue, total_seats, ticket_price, **kwargs)
        elif event_type == EventType.SPORT:
            event = Sport(event_name, event_date, event_time, venue, total_seats, ticket_price, **kwargs)
        else:
            raise ValueError("Invalid event type.")

        self.events.append(event)
        return event

    def calculate_booking_cost(self, num_tickets, ticket_price):
        return num_tickets * ticket_price

    def book_tickets(self, event_name, num_tickets, customers):
        event_found = False
        for event in self.events:
            if event.event_name == event_name:
                event_found = True
                try:
                    event.book_tickets(num_tickets)
                    booking = Booking(customers, event, num_tickets)
                    return booking
                except ValueError as e:
                    print(e)
                    return None

        if not event_found:
            raise EventNotFoundException(event_name)

    def cancel_booking(self, booking_id):
        booking_found = False
        for event in self.events:
            if event.event_name == booking.event.event_name:
                event.cancel_booking(booking.num_tickets)
                booking_found = True
                print(f"Booking ID {booking_id} cancelled successfully.")
                break

        if not booking_found:
            raise InvalidBookingIDException(booking_id)

    def getAvailableNoOfTickets(self):
        available_tickets = 0
        for event in self.events:
            available_tickets += event.available_seats
        return available_tickets

    def getEventDetails(self):
        for event in self.events:
            event.display_event_details()

    def main(self):
        while True:
            print("\n=== Ticket Booking System Menu ===")
            print("1. Create Event")
            print("2. Display Event Details")
            print("3. Book Tickets")
            print("4. Cancel Booking")
            print("5. View Available Tickets")
            print("6. View All Events")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                event_name = input("Enter event name: ")
                event_date = input("Enter event date (YYYY-MM-DD): ")
                event_time = input("Enter event time (HH:MM): ")
                venue_name = input("Enter venue name: ")
                address = input("Enter venue address: ")
                total_seats = int(input("Enter total seats: "))
                ticket_price = float(input("Enter ticket price: "))
                event_type = input("Enter event type (Movie/Sport/Concert): ").capitalize()

                if event_type not in ["Movie", "Sport", "Concert"]:
                    print("Invalid event type. Please try again.")
                    continue

                if event_type == "Movie":
                    genre = input("Enter movie genre: ")
                    actor_name = input("Enter actor name: ")
                    actress_name = input("Enter actress name: ")
                    venue = Venue(venue_name, address)
                    event = self.create_event(event_name, event_date, event_time, venue, total_seats, ticket_price,
                                              EventType.MOVIE, genre=genre, actor_name=actor_name,
                                              actress_name=actress_name)
                elif event_type == "Concert":
                    artist = input("Enter artist name: ")
                    venue = Venue(venue_name, address)
                    event = self.create_event(event_name, event_date, event_time, venue, total_seats, ticket_price,
                                              EventType.CONCERT, artist=artist)
                elif event_type == "Sport":
                    sport_name = input("Enter sport name: ")
                    teams_name = input("Enter teams name: ")
                    venue = Venue(venue_name, address)
                    event = self.create_event(event_name, event_date, event_time, venue, total_seats, ticket_price,
                                              EventType.SPORT, sport_name=sport_name, teams_name=teams_name)

                print(f"Event '{event_name}' created successfully.")

            elif choice == "2":
                if not self.events:
                    print("No events available.")
                    continue
                print("\n=== Available Events ===")
                for idx, event in enumerate(self.events):
                    print(f"{idx + 1}. {event.event_name}")

                event_idx = int(input("Enter event index to display details: ")) - 1
                if 0 <= event_idx < len(self.events):
                    self.events[event_idx].display_event_details()
                else:
                    print("Invalid event index.")

            elif choice == "3":
                if not self.events:
                    print("No events available for booking.")
                    continue
                event_name = input("Enter event name to book tickets: ")
                num_tickets = int(input("Enter number of tickets to book: "))
                if num_tickets <= 0:
                    print("Invalid number of tickets.")
                    continue
                customers = []
                for _ in range(num_tickets):
                    customer_name = input("Enter customer name: ")
                    email = input("Enter customer email: ")
                    phone_number = input("Enter customer phone number: ")
                    customer = Customer(customer_name, email, phone_number)
                    customers.append(customer)

                try:
                    booking = self.book_tickets(event_name, num_tickets, customers)
                    if booking:
                        print("Booking Successful!")
                        booking.display_booking_details()
                except EventNotFoundException as e:
                    print(e)

            elif choice == "4":
                booking_id = int(input("Enter Booking ID to cancel: "))
                try:
                    self.cancel_booking(booking_id)
                except InvalidBookingIDException as e:
                    print(e)

            elif choice == "5":
                available_tickets = self.getAvailableNoOfTickets()
                print(f"Total Available Tickets: {available_tickets}")

            elif choice == "6":
                self.getEventDetails()

            elif choice == "7":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    ticket_booking_system = TicketBookingSystem()
    ticket_booking_system.main()
