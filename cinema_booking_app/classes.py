from datetime import datetime as dt, time


class BookingStaff():
    def __init__(self, cinema, staffID, password):
        self.__cinema = cinema
        self.__staffID = staffID
        self.__password = password
        self.__access = "standard"

    def get_cinema(self):
        return self.__cinema

    def get_staff_id(self):
        return self.__staffID

    def get_password(self):
        return self.__password

    def get_access(self):
        return self.__access


class Admin(BookingStaff):
    def __init__(self, cinema, staffID, password):
        super().__init__(cinema, staffID, password)
        self.__access = "admin"

    def get_access(self):
        return self.__access


class Manager(Admin):
    def __init__(self, cinema, staffID, password):
        super().__init__(cinema, staffID, password)
        self.__access = "manager"

    def get_access(self):
        return self.__access



class Booking():
    def __init__(self, cinemaID, bookingID, film, date, time, ticket_type, ticket_amount, screen_number, seat_numbers, price, name, phone_number, email):
        self.__cinemaID = cinemaID
        self.__bookingID = bookingID
        self.__film = film
        self.__date = date
        self.__time = time
        self.__ticket_type = ticket_type
        self.__ticket_amount = ticket_amount
        self.__screen_number = screen_number
        self.__seat_numbers = seat_numbers
        self.__price = price
        self.__name = name
        self.__phone_number = phone_number
        self.__email = email

    def get_cinemaID(self):
        return self.__cinemaID

    def get_bookingID(self):
        return self.__bookingID

    def get_film(self):
        return self.__film

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_ticket_type(self):
        return self.__ticket_type

    def get_ticket_amount(self):
        return self.__ticket_amount

    def get_screen_number(self):
        return self.__screen_number

    def get_seat_numbers(self):
        return self.__seat_numbers

    def get_price(self):
        return self.__price

    def get_name(self):
        return self.__name

    def get_phone_number(self):
        return self.__phone_number

    def get_email(self):
        return self.__email



class Cinema():
    def __init__(self, city, cinemaID):
        self.__city = city
        self.__cinemaID = cinemaID
        self.__screens = []

    def get_city(self):
        return self.__city

    def get_cinemaID(self):
        return self.__cinemaID

    def get_screens(self):
        return self.__screens

    def get_screen_by_id(self, screen_id):
        for screen in self.__screens:
            if str(screen.get_screen_number()) == str(screen_id):
                return screen

    def check_price(self, show_time, ticket_type):
        city = self.__city
        #check location
        if city == "Birmingham" or city == "Cardiff":
            price = 5
        elif city == "Bristol":
            price = 6
        elif city == "London":
            price = 10
        else:
            print("Error: city does not match. City variable = " + str(city))

        #check time
        show_time = dt.strptime(show_time, "%H:%M").time()
        if show_time >= time(12,00) and show_time < time(17,00):
            price = price + 1
        elif show_time >= time(17,00):
            price = price + 2

        #check ticket type
        if ticket_type == "Upper Gallery":
            price = price * 1.2
        elif ticket_type == "VIP":
            price = price * 1.44

        return price

    def add_screen(self, screen):
        self.__screens.append(screen)

    def remove_screen(self, screen):
        index = self.__screens.index(screen)
        self.__screens.pop(index)

    # iterates through screens and returns all showings from all screens
    def get_film_listings(self):
        listings = []
        screens = self.__screens
        for screen in screens:
            showings = screen.get_showings()
            for showing in showings:
                listings.append(showing)
        return listings

    def get_film_names(self):
        names = []
        listings = self.get_film_listings()
        for listing in listings:
            if listing.get_name() not in names:
                names.append(listing.get_name())
        return names

    def get_film_dates(self):
        dates = []
        listings = self.get_film_listings()
        for listing in listings:
            date = listing.get_show_dates_str()
            for d in date:
                if d not in dates:
                    dates.append(d)
        return dates

    def get_film_times(self):
        times = []
        listings = self.get_film_listings()
        for listing in listings:
            time = listing.get_show_times_str()
            for t in time:
                if t not in times:
                    times.append(t)
        return times

    def check_availability(self, film, show_date, show_time, ticket_type, ticket_amount):
        show_date = dt.strptime(show_date, "%d %B").date()
        show_time = dt.strptime(show_time, "%H:%M").time()
        screens = self.__screens
        for screen in screens:
            showings = screen.get_showings()
            for showing in showings:
                if showing.get_name() == film:
                    dates = showing.get_show_dates()
                    for d in dates:
                        if d.month == show_date.month and d.day == show_date.day:
                            times = showing.get_show_times()
                            for t in times:
                                if t == show_time:
                                    if screen.check_for_seats(show_date, show_time, ticket_type, ticket_amount):
                                        return True
        return False


    def get_available_screen(self, film, show_date, show_time, ticket_type, ticket_amount):
        show_date = dt.strptime(show_date, "%d %B").date()
        show_time = dt.strptime(show_time, "%H:%M").time()
        screens = self.__screens
        for screen in screens:
            showings = screen.get_showings()
            for showing in showings:
                if showing.get_name() == film:
                    dates = showing.get_show_dates()
                    for d in dates:
                        if d.month == show_date.month and d.day == show_date.day:
                            times = showing.get_show_times()
                            for t in times:
                                if t == show_time:
                                    if screen.check_for_seats(show_date, show_time, ticket_type, ticket_amount):
                                        return screen
        print("Error: could not find available screen")
        return False



class Screen():
    def __init__(self, screen_number, max_seats):
        self.__screen_number = screen_number
        self.__max_seats = max_seats
        self.__seats = []
        self.__showings = []
        self.__populate_seats()

    def get_screen_number(self):
        return self.__screen_number

    def add_showing(self, showing):
        self.__showings.append(showing)

    def remove_showing(self, showing):
        index = self.__showings.index(showing)
        self.__showings.pop(index)

    def get_showings(self):
        return self.__showings
        
    def __populate_seats(self):
        max_seats = self.__max_seats
        lower_hall_seats = round(max_seats * 0.3)
        upper_gallery_seats = max_seats - lower_hall_seats
        seat_number = 1
        for i in range(lower_hall_seats):
            seat = Seat(seat_number, "Lower Hall")
            self.__seats.append(seat)
            seat_number += 1
        VIP_seats = 10
        for i in range(upper_gallery_seats):
            if VIP_seats > 0:
                seat = Seat(seat_number, "VIP")
                self.__seats.append(seat)
                VIP_seats -= 1
            else:
                seat = Seat(seat_number, "Upper Gallery")
                self.__seats.append(seat)
            seat_number += 1


    def check_for_seats(self, show_date, show_time, type, amount):
        seats = self.__seats
        unbooked_seats = 0
        for seat in seats:
            if seat.get_seat_type() == type:
                booked_times = seat.get_booked_times()
                if not booked_times or self.check_seat_times(booked_times, show_date, show_time):
                    unbooked_seats += 1
            if unbooked_seats >= amount:
                return True
        return False


    def check_seat_times(self, booked_times, ticket_date, ticket_time):
        for b in booked_times:
            if b.month == ticket_date.month and b.day == ticket_date.day:
                if not (ticket_time.hour <= (b.hour-3)) and not (ticket_time.hour >= (b.hour+3)):
                    print("time matched")
                    return False
        return True


    def get_seat_numbers(self, show_date, show_time, ticket_type, ticket_amount):
        show_date = dt.strptime(show_date, "%d %B").date()
        show_time = dt.strptime(show_time, "%H:%M").time()
        seats = self.__seats
        unbooked_seats = 0
        seat_numbers = []
        for seat in seats:
            if seat.get_seat_type() == ticket_type:
                booked_times = seat.get_booked_times()
                if not booked_times or self.check_seat_times(booked_times, show_date, show_time):
                    unbooked_seats += 1
                    seat_numbers.append(str(seat.get_seat_number()))
            if unbooked_seats >= ticket_amount:
                return seat_numbers
        print("Error: could not get seat numbers")


    def reserve_seats(self, show_date, show_time, seat_numbers):
        all_seats = self.__seats
        for seat in all_seats:
            for seat_num in seat_numbers:
                if str(seat.get_seat_number()) == str(seat_num):
                    seat.reserve_seat(show_date, show_time)


    def cancel_seats(self, show_date, show_time, seat_numbers):
        all_seats = self.__seats
        for seat in all_seats:
            for seat_num in seat_numbers:
                if str(seat.get_seat_number()) == str(seat_num):
                    seat.cancel_seat(show_date, show_time)



class Film():
    def __init__(self, name, actors, description, genre, age_rating):
        self.__name = name
        self.__actors = actors
        self.__description = description
        self.__genre = genre
        self.__age_rating = age_rating

    def get_name(self):
        return self.__name

    def get_actors(self):
        return self.__actors

    def get_description(self):
        return self.__description

    def get_genre(self):
        return self.__genre

    def get_age_rating(self):
        return self.__age_rating



class Showing():
    def __init__(self, film, show_dates, show_times):
        self.__film = film
        self.__show_dates = show_dates
        self.__show_times = show_times

    def get_name(self):
        return self.__film.get_name()

    def get_actors(self):
        return self.__film.get_actors()

    def get_description(self):
        return self.__film.get_description()

    def get_genre(self):
        return self.__film.get_genre()

    def get_age_rating(self):
        return self.__film.get_age_rating()

    def get_show_dates(self):
        return self.__show_dates

    def get_show_times(self):
        return self.__show_times

    def get_show_dates_str(self):
        str_dates = []
        dates = self.__show_dates
        for date in dates:
            d = date.strftime("%d %B")
            str_dates.append(d)
        return str_dates

    def get_show_times_str(self):
        str_times = []
        times = self.__show_times
        for time in times:
            t = time.strftime("%H:%M")
            str_times.append(t)
        return str_times


    def update_show_dates(self, dates):
        new_dates = []
        for d in dates:
            new_dates.append(dt(2023, d.month, d.day))
        self.__show_dates = new_dates


    def update_show_times(self, times):
        self.__show_times = times




class Seat():
    def __init__(self, seat_number, type):
        self.__seat_number = seat_number
        self.__booked_times = []
        self.__type = type

    def get_seat_number(self):
        return self.__seat_number

    def get_booked_times(self):
        return self.__booked_times

    def get_seat_type(self):
        return self.__type

    def reserve_seat(self, show_date, show_time):
        show_date = dt.strptime(show_date, "%d %B").date()
        show_time = dt.strptime(show_time, "%H:%M").time()
        com = dt.combine(show_date, show_time)
        self.__booked_times.append(com)

    def cancel_seat(self, show_date, show_time):
        show_date = dt.strptime(show_date, "%d %B").date()
        show_time = dt.strptime(show_time, "%H:%M").time()
        com = dt.combine(show_date, show_time)
        for b in self.__booked_times:
            if b == com:
                index = self.__booked_times.index(b)
                self.__booked_times.pop(index)
