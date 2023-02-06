import tkinter as tk
from tkinter import ttk
import tkcalendar as tkcal
from tktimepicker import SpinTimePickerOld, constants
import tkinter.font as tkfont
import random as rand
from datetime import datetime as dt, time

from classes import *

films = []
users = []
cinemas = []
bookings = []

avatar2 = Film("Avatar: the Way of Water", ["Sam Worthington", "Zoe Saldana", "Sigourney Weaver"], "Jake Sully and Ney'tiri have formed a family and are doing everything to stay together."+ \
                " However, they must leave their home and explore the regions of Pandora. When an ancient threat resurfaces, Jake must fight a difficult war against the humans.", \
                    ["Sci-fi", "Action"], "12A")
films.append(avatar2)

tmywud = Film("The Minute You Wake Up Dead", ["Cole Hauser", "Russ Potter", "Jaimie Alexander"], "When a shady small-town stockbroker begins dating a shy waitress, a shocking murder "\
                + "takes place -- and one of them may be responsible. As word leaks out that there's money behind the killing, every criminal in town wants their share of the cash.", \
                    ["Mystery"], "15")
films.append(tmywud)

blackpanther2 = Film("Black Panther: Wakanda Forever", ["Letitia Wright", "Lupita Nyong'o", "Danai Gurira"], "Queen Ramonda, Shuri, M'Baku, Okoye and the Dora Milaje fight to " +\
                "protect their nation from intervening world powers in the wake of King T'Challa's death. As the Wakandans strive to embrace their next chapter, the heroes must band together "+ \
                    "with Nakia and Everett Ross to forge a new path for their beloved kingdom.", ["Action", "Adventure"], "12A")
films.append(blackpanther2)

empireoflight = Film("Empire of Light", ["Olivia Colman", "Micheal Ward", "Colin Firth"], "A romance develops in a beautiful old cinema on the south coast of England in the 1980s.", \
                ["Romance", "Drama"], "15")
films.append(empireoflight)

amancalledotto = Film("A Man Called Otto", ["Tom Hanks", "Mariana Trevino", "John Higgins"], "When a lively young family moves in next door, grumpy widower Otto Anderson meets his match "+\
                "in a quick-witted, pregnant woman named Marisol, leading to an unlikely friendship that turns his world upside down.", ["Comedy"], "15")
films.append(amancalledotto)

cities = ["Birmingham", "Bristol", "Cardiff", "London"]

for city in cities:
    for c in range(1, 3):
        cinema = Cinema(city, city + str(c))
        cinemas.append(cinema)
        for s in range(1, 7):
            screen = Screen(s, rand.randint(50, 120))
            cinema.add_screen(screen)      
            times = []  
            for t in range(1, 5):                
                times.append(time(rand.randint(8, 22), rand.randrange(0, 45, 15)))
            now = dt.now()
            dates = []
            for d in range(0, 8):
                dates.append(dt(now.year, now.month, now.day+d))
            showing = Showing(films[rand.randint(0, len(films)-1)], dates, times)
            screen.add_showing(showing)


bookingstaff = BookingStaff(cinemas[rand.randint(0, len(cinemas)-1)], "bookingstaff", "bookingstaff")
admin = Admin(cinemas[rand.randint(0, len(cinemas)-1)], "admin", "admin")
manager = Manager(cinemas[rand.randint(0, len(cinemas)-1)], "manager", "manager")
users.append(bookingstaff)
users.append(admin)
users.append(manager)


def get_all_films():
    return films


def get_list_of_cinemas_id():
    list = []
    for cinema in cinemas:
        str = f"{cinema.get_cinemaID()}"
        list.append(str)
    return list


def get_list_of_screen_numbers(cinema):
    list = []
    for screen in cinema.get_screens():
        list.append(screen.get_screen_number())
    return list


def find_cinema(id):
    for cinema in cinemas:
        if id == cinema.get_cinemaID():
            return cinema
    else:
        print("Couldnt find cinema")


def check_id(id):
    for user in users:
        if id == user.get_staff_id():
            return user
    return False


def check_password(user, password):
    if user.get_password() == password:
        return True
    return False


def login(id, password):
    user = check_id(id)
    if user is not False:
        if check_password(user, password):
            print("Logged in successfully")
            return user
        else:
            print("Invalid credentials")
            return False
    else:
        print("No matched id")
        return False


def book_film(cinemaid, bookingid, film, date, time, ticket_type, ticket_amount, screen, seat_numbers, price, name, phone, email):
    print(screen)
    screen_number = screen.get_screen_number()
    booking = Booking(cinemaid, bookingid, film, date, time, ticket_type, ticket_amount, screen_number, seat_numbers, price, name, phone, email)
    screen.reserve_seats(date, time, seat_numbers)
    bookings.append(booking)


def get_booking(bookingid):
    for booking in bookings:
        if str(booking.get_bookingID()) == str(bookingid):
            return booking
    print("Could not find booking")
    return False


def cancel_booking(bookingid):
    for booking in bookings:
        if str(booking.get_bookingID()) == str(bookingid):
            cinemaid = booking.get_cinemaID()
            screen_number = booking.get_screen_number()
            for cinema in cinemas:
                if cinema.get_cinemaID() == cinemaid:
                    screen = cinema.get_screen_by_id(screen_number)
            date = booking.get_date()
            time = booking.get_time()
            seat_numbers = booking.get_seat_numbers()
            screen.cancel_seats(date, time, seat_numbers)
            index = bookings.index(booking)
            cancelled_booking = bookings.pop(index)
            return cancelled_booking
    return False


def add_film(dic):
    actors = dic["actors"]
    genre = dic["genre"]
    t_actors = []
    t_genre = []
    for a in actors:
        if a.get() != "":
            t_actors.append(a.get())
    for g in genre:
        if g.get() != "":
            t_genre.append(g.get())
    new_film = Film(dic["name"].get(), t_actors, dic["description"].get(), t_genre, dic["age_rating"].get())
    films.append(new_film)


def remove_film(film):
    index = films.index(film)
    films.pop(index)


def create_cinema(city, cinema_id, screen_amount, screen_seats):
    cinema = Cinema(city, cinema_id)
    for i in range(1, int(screen_amount)+1):
        screen = Screen(int(i), int(screen_seats[i-1].get()))
        cinema.add_screen(screen)
    cinemas.append(cinema)


def get_number_of_bookings(showing):
    num = 0
    for booking in bookings:
        date = dt.strptime(booking.get_date(), "%d %B").date()
        time = dt.strptime(booking.get_time(), "%H:%M").time()
        if booking.get_film() == showing.get_name():
            print("name same")
            match = False
            for d in showing.get_show_dates():                
                if d.month == date.month and d.day == date.day:
                    match = True
            if match:
                for t in showing.get_show_times():
                    print(t)
                    print(booking.get_time())
                    if t.hour == time.hour and t.minute == time.minute:
                        print("time match")
                        num += 1
    return num
                


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500+500+200")
        self.resizable(0, 0)
        self.user = None
        self.access = None
        self.columnconfigure(0, weight=1)
        self.current_page = LoginPage(self)


    def nav_bar(self):
        # create navigation bar
        ttk.Style().configure("nav.TFrame")
        nav = ttk.Frame(self, borderwidth=5)
        # nav buttons
        buttons = {}
        buttons["home_button"] = ttk.Button(nav, text="Home", command=lambda: self.page_change(HomePage(self, self.user)))
        buttons["film_listings_button"] = ttk.Button(nav, text="Film Listings", command=lambda: self.page_change(FilmListingsPage(self, self.user)))
        buttons["booking_button"] = ttk.Button(nav, text="Booking", command=lambda: self.page_change(BookingPage(self, self.user)))
        buttons["cancellation_button"] = ttk.Button(nav, text="Cancellation", command=lambda: self.page_change(CancellationPage(self, self.user)))
        if self.access == "admin":
            buttons["admin_button"] = ttk.Button(nav, text="Admin", command=lambda: self.page_change(AdminPage(self, self.user)))
        if self.access == "manager":
            buttons["manager_button"] = ttk.Button(nav, text="Manager", command=lambda: self.page_change(ManagerPage(self, self.user)))
        buttons["logout_button"] = ttk.Button(nav, text="Logout", command=lambda: self.logout())

        ttk.Style().configure("nav.TButton", font=("Helvetica", 12))

        c = 0
        for button in buttons.values():
            button.config(style="nav.TButton")
            if self.access == "standard":
                button.grid(row=0, column=c, sticky=tk.N, padx=10, pady=10, ipadx=5, ipady=5)
            else:
                button.grid(row=0, column=c, sticky=tk.N, padx=5, pady=10, ipadx=5, ipady=5)
            c = c + 1
        nav.grid(row=0, column=0)
        return nav


    def page_change(self, new_page):
        self.current_page.grid_forget()
        self.current_page = new_page
        

    # called from login page if login succeeded
    def logged_in(self, user):
        # set user to be used and access
        self.user = user
        self.access = user.get_access()
        print(self.access)
        # display nav bar and move to home page
        self.navigation = self.nav_bar()
        self.page_change(HomePage(self, self.user))


    # called when logout button pressed
    def logout(self):
        # reset user and access to none
        self.user = None
        self.access = None
        # remove nav bar and return to login
        self.navigation.grid_forget()
        self.page_change(LoginPage(self))



class HomePage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Home")
        self.user = user
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text=f"Logged in as {main.user.get_staff_id()}", font=("Arial", 16)).grid(row=0, column=0, padx=70, pady=70)
        self.grid(row=1, column=0)



class FilmListingsPage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Film listings")
        self.user = user
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky=tk.W)
        self.create_top()
        self.create_listings_canvas()


    # create canvas needed for making a scrolling page
    def create_listings_canvas(self):
        self.canvas = tk.Canvas(self, width="800", height="400")
        self.listings_frame = self.load_listings()
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky=tk.NS)
        self.canvas.grid(row=1, column=0, columnspan=2)
        self.canvas_id = self.canvas.create_window(0, 0, window=self.listings_frame, anchor=tk.NW)
        self.listings_frame.bind("<Configure>", self.scroll_config)
        self.canvas.bind("<Configure>", self.resize_canvas)


    # for making the canvas scroll
    def scroll_config(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # makes canvas expand to sceen
    def resize_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_id, width=canvas_width)


    # makes drop down for changing cinema if admin or manager
    def create_top(self):
        user = self.user
        if user.get_access() == "admin" or user.get_access() == "manager":
            cinema_id = tk.StringVar()
            cinema_options = ttk.OptionMenu(self, cinema_id, "Change cinema", *get_list_of_cinemas_id(), command=lambda cinema_id: self.change_cinema(cinema_id))
            cinema_options.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)
            self.cinema = user.get_cinema()
        else:
            self.cinema = user.get_cinema()


    # display all listings for current cinema
    def load_listings(self):
        ttk.Style().configure("listings.TFrame", background="#BDE6E6")
        self.frame_listings = ttk.Frame(self)
        self.frame_listings.columnconfigure(0, weight=1)
        r = 0
        self.current_listings = []
        for listing in self.cinema.get_film_listings():
            current_listings = ttk.Frame(self.frame_listings, borderwidth=5, relief="groove")
            ttk.Label(current_listings, text=listing.get_name(), font=("Arial", 16), background="#BDE6E6", wraplength=650, justify="left").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(current_listings, text="Starring: " + ", ".join(listing.get_actors()), font=("Arial", 12), background="#BDE6E6", wraplength=650, justify="left").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(current_listings, text=listing.get_description(), font=("Arial", 10), background="#BDE6E6", wraplength=650, justify="left").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(current_listings, text=", ".join(listing.get_genre()), font=("Arial", 12), background="#BDE6E6", wraplength=650, justify="left").grid(row=3, column=0, sticky=tk.W)
            ttk.Label(current_listings, text=listing.get_age_rating(), font=("Arial", 12), background="#BDE6E6", wraplength=650, justify="left").grid(row=4, column=0, sticky=tk.W)
            ttk.Label(current_listings, text="Film showing on: " + str(", ".join(listing.get_show_dates_str())), font=("Arial", 12), background="#BDE6E6", wraplength=650, justify="left").grid(row=5, column=0, sticky=tk.W)
            ttk.Label(current_listings, text="Showing times are: " + str(", ".join(listing.get_show_times_str())), font=("Arial", 12), background="#BDE6E6", wraplength=650, justify="left").grid(row=6, column=0, sticky=tk.W)
            current_listings.config(style="listings.TFrame")
            current_listings.grid(row=r, column=0, padx=50, pady=10, sticky=tk.EW)
            r = r + 1
            self.current_listings.append(current_listings)
        self.frame_listings.grid(row=1, column=0)
        print("Loaded listings")
        return self.frame_listings


    # called if new cinema is chosen, reloads the page with listings from chosen cinema
    def change_cinema(self, id):
        print("Reloading listings for cinema: " + str(id))
        self.cinema = find_cinema(id)
        self.frame_listings.grid_forget()
        self.create_listings_canvas()



class BookingPage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Booking")
        self.user = user
        self.film_is_available = False
        self.columnconfigure(0, weight=1)
        # put functions in a list, they return their frame for iteration later
        self.booking_main = []
        self.booking_main.append(self.create_top())
        self.booking_main.append(self.check_for_film_form())
        self.booking_main.append(self.seperator())
        self.booking_main.append(self.book_ticket_form())
        self.grid(row=1, column=0, sticky=tk.W)


    # creates dropdown for changing cinema is admin or manager
    def create_top(self):
        user = self.user
        if user.get_access() == "admin" or user.get_access() == "manager":
            top_frame = ttk.Frame(self)
            cinema_id = tk.StringVar()
            self.cinema = user.get_cinema()
            ttk.Label(top_frame, text="Change cinema: ").grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)
            cinema_options = ttk.OptionMenu(top_frame, cinema_id, self.cinema.get_cinemaID(), *get_list_of_cinemas_id(), command=lambda cinema_id: self.change_cinema(cinema_id))
            cinema_options.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)
            top_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)
            return top_frame
        else:
            self.cinema = user.get_cinema()     


    # called if new cinema is chosen and reloads page with showings from that cinema
    def change_cinema(self, id):
        print("Reloading listings for cinema: " + str(id))
        self.cinema = find_cinema(id)
        self.top_frame.grid_forget()
        self.make_top_frame()


    # creates form for filling in the film, dates, times, and tickets
    def make_top_frame(self):
        label_font = ("Arial", 12)
        self.top_frame = ttk.Frame(self.film_checking_form)
        # make labels
        labels_top = {}
        labels_top["film"] = ttk.Label(self.top_frame, text="Select film:")
        labels_top["date"] = ttk.Label(self.top_frame, text="Select date:")
        labels_top["showing"] = ttk.Label(self.top_frame, text="Select showing:")
        labels_top["ticket_type"] = ttk.Label(self.top_frame, text="Select ticket type:")
        labels_top["ticket_number"] = ttk.Label(self.top_frame, text="Select number of tickets:")

        # make inputs
        self.booking_form_input = {}
        self.booking_form_input["selected_film"] = tk.StringVar()
        self.booking_form_input["selected_date"] = tk.StringVar()
        self.booking_form_input["selected_showing"] = tk.StringVar()
        self.booking_form_input["selected_ticket_type"] = tk.StringVar()
        self.booking_form_input["selected_ticket_number"] = tk.IntVar()

        # add trace to vars, will prevent booking if user has changed input before checking availability
        for val in self.booking_form_input.values():
            val.trace_add("write", lambda a, b, c: self.set_unchecked())

        style = ttk.Style()
        style.configure("booking_drop_downs.TMenubutton", background="#d8d8d8")
        entries_top = {}
        entries_top["film"] = ttk.OptionMenu(self.top_frame, self.booking_form_input["selected_film"], self.film_def, *self.cinema.get_film_names(), \
                    command=lambda event: self.set_date_and_time(), style="booking_drop_downs.TMenubutton")
        entries_top["date"] = ttk.OptionMenu(self.top_frame, self.booking_form_input["selected_date"], None, *self.film_dates, style="booking_drop_downs.TMenubutton")
        entries_top["showing"] = ttk.OptionMenu(self.top_frame, self.booking_form_input["selected_showing"], None, *self.film_times, style="booking_drop_downs.TMenubutton")
        entries_top["ticket_type1"] = ttk.Radiobutton(self.top_frame, text="Lower hall", value="Lower Hall", variable=self.booking_form_input["selected_ticket_type"])
        entries_top["ticket_type2"] = ttk.Radiobutton(self.top_frame, text="Upper hall", value="Upper Gallery", variable=self.booking_form_input["selected_ticket_type"])
        entries_top["ticket_type3"] = ttk.Radiobutton(self.top_frame, text="VIP", value="VIP", variable=self.booking_form_input["selected_ticket_type"])
        entries_top["ticket_number"] = ttk.Entry(self.top_frame, textvariable=self.booking_form_input["selected_ticket_number"])

        # grid labels and entries
        r = 0
        for label in labels_top.values():
            label.config(font=label_font)
            label.grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
            r = r + 1
        r = 0
        c = 1
        for name, value in entries_top.items():
            if name == "ticket_type1" or name == "ticket_type2" or name == "ticket_type3":
                value.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)
                c = c + 1
                if name == "ticket_type3":
                    r = r + 1
            else:
                value.config()
                value.grid(row=r, column=1, sticky=tk.EW, padx=5, pady=5, columnspan=2)
                r = r + 1
        self.top_frame.grid(row=0, column=0)


    # creates button for checking if film is available and shows price if it is
    def check_for_film_form(self):
        self.cinema = self.user.get_cinema()

        self.film_checking_form = ttk.Frame(self)
        # create form for checking if a film is available
        label_font = ("Arial", 12)
        self.film_dates = self.cinema.get_film_dates()
        self.film_times = self.cinema.get_film_times()
        self.film_def = None
        
        self.make_top_frame()

        # make frame with button and output for checking film price and availability
        checking_frame = ttk.Frame(self.film_checking_form, borderwidth=5, border=1)
        check_button = tk.Button(checking_frame, text="Check price and seating availability", font=tkfont.Font(family="Arial", size=12), \
                            command=lambda: self.check_availability_and_price(self.booking_form_input["selected_film"].get(), self.booking_form_input["selected_date"].get(), \
                                self.booking_form_input["selected_showing"].get(), self.booking_form_input["selected_ticket_type"].get(), \
                                    self.booking_form_input["selected_ticket_number"].get(), self.cinema))
        check_button.grid(row=0, column=0, padx=15, pady=10, ipadx=5, ipady=5, columnspan=2, sticky=tk.EW)

        self.form_error_message = tk.Label(checking_frame, text="", fg="red", font=("Arial", 10))
        self.form_error_message.grid(row=1, column=0, sticky=tk.N, padx=5, pady=5, columnspan=2)

        labels_checking = {}
        labels_checking["availability_label"] = ttk.Label(checking_frame, text="Availability:")
        labels_checking["price_label"] = ttk.Label(checking_frame, text="Total price:")

        self.output_checking = {}
        self.output_checking["availability"] = ttk.Label(checking_frame)
        self.output_checking["price"] = ttk.Label(checking_frame)

        r = 2
        for label in labels_checking.values():
            label.config(font=label_font)
            label.grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
            r = r + 1
        r = 2
        for label in self.output_checking.values():
            label.config(font=label_font)
            label.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5, columnspan=2)
            r = r + 1
        checking_frame.grid(row=2, column=0, sticky=tk.W)

        self.film_checking_form.grid(row=1, column=0, padx=10, pady=0, sticky=tk.NW)
        return self.film_checking_form


    # callback for when input is changed
    def set_unchecked(self):
        self.film_is_available = False


    # called when film is selected and reloads date and time dropdowns to show only times that are available for the chosen film
    def set_date_and_time(self):
        film = self.booking_form_input["selected_film"].get()
        cinema = self.cinema
        listings = cinema.get_film_listings()
        for listing in listings:
            if listing.get_name() == film:
                # get list of times and dates for listing in string format
                self.film_times = listing.get_show_times_str()
                self.film_dates = listing.get_show_dates_str()
        self.top_frame.grid_forget()
        self.film_def = film
        self.make_top_frame()


    # called when check button is clicked
    def check_availability_and_price(self, film, date, time, type, amount, cinema):
        self.form_error_message.config(text="")
        for input in self.booking_form_input.values():
            # check inputs are filled
            if input.get() == "":
                self.form_error_message.config(text="Please fill in all fields")
                return
        # check availability
        if cinema.check_availability(film, date, time, type, amount):
            self.film_is_available = True
            self.output_checking["availability"].config(text="Film available")
            # display price
            price = "{:0.2f}".format(round((cinema.check_price(time, type) * amount), 2))
            self.output_checking["price"].config(text="£" + str(price))
        else:
            self.output_checking["availability"].config(text="Film not available for the selected date or time")
            self.output_checking["price"].config(text="")


    # creates horazontal line as a seperator
    def seperator(self):
        canvas_frame = ttk.Frame(self)
        canvas = tk.Canvas(canvas_frame, width=5, height=500)
        canvas.grid(row=0, column=0, sticky=tk.NW)
        canvas.create_line(0, 0, 0, 400, fill="#3EAFD1", width=5)
        canvas_frame.grid(row=0, column=1, rowspan=5)
        return canvas_frame
        

    # creates right side of page, form for users details
    def book_ticket_form(self):
        booking_ticket_form = ttk.Frame(self)
        # create labels
        label_font = ("Arial", 12)
        labels_frame = ttk.Frame(booking_ticket_form)
        labels = {}
        labels["name"] = ttk.Label(labels_frame, text="Name:")
        labels["phone"] = ttk.Label(labels_frame, text="Phone number:")
        labels["email"] = ttk.Label(labels_frame, text="Email address:")
        labels["card_number"] = ttk.Label(labels_frame, text="Card number:")
        labels["card_expiry"] = ttk.Label(labels_frame, text="Card expiry:")
        labels["card_cvv"] = ttk.Label(labels_frame, text="Card CVV:")

        r = 0
        for label in labels.values():
            label.config(font=label_font)
            label.grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
            r = r + 1
        labels_frame.grid(row=0, column=0, sticky=tk.W)

        inputs_frame = ttk.Frame(booking_ticket_form)

        # create variables
        self.saved_inputs = {}
        self.saved_inputs["saved_name"] = tk.StringVar()
        self.saved_inputs["saved_phone"] = tk.StringVar()
        self.saved_inputs["saved_email"] = tk.StringVar()
        self.saved_inputs["saved_card_number"] = tk.StringVar()
        self.saved_inputs["saved_card_expiry"] = tk.StringVar()
        self.saved_inputs["saved_card_cvv"] = tk.StringVar()

        # create entries
        inputs = {}
        inputs["name"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_name"])
        inputs["phone"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_phone"])
        inputs["email"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_email"])
        inputs["card_number"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_card_number"])
        inputs["card_expiry"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_card_expiry"])
        inputs["card_cvv"] = ttk.Entry(inputs_frame, textvariable=self.saved_inputs["saved_card_cvv"])

        r = 0
        for input in inputs.values():
            input.grid(row=r, column=0, padx=5, pady=5, sticky=tk.W)
            r = r + 1
        inputs_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # book button
        book_frame = ttk.Frame(booking_ticket_form)
        book_button = tk.Button(book_frame, text="Book now", font=tkfont.Font(family="Arial", size=12), command=lambda: self.book(self.booking_form_input["selected_film"].get(), \
                self.booking_form_input["selected_date"].get(), self.booking_form_input["selected_showing"].get(), self.booking_form_input["selected_ticket_type"].get(), \
                    self.booking_form_input["selected_ticket_number"].get(), self.saved_inputs["saved_name"].get(), self.saved_inputs["saved_phone"].get(), \
                        self.saved_inputs["saved_email"].get()))
        book_button.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10, ipadx=5, ipady=5)

        self.booking_error_message = tk.Label(book_frame, fg="red", font=("Arial", 10))
        self.booking_error_message.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)

        book_frame.grid(row=1, column=0, columnspan=2)

        booking_ticket_form.grid(row=0, column=2, padx=10, pady=10, sticky=tk.N, rowspan=5)
        return booking_ticket_form


    # called when form is properly filled in and book button is clicked
    def book(self, film, date, time, ticket_type, ticket_amount, name, phone, email):
        bookingid = len(bookings) + 1      # temp booking id
        if self.vailidate_booking():
            screen = self.cinema.get_available_screen(film, date, time, ticket_type, ticket_amount)
            seat_numbers = screen.get_seat_numbers(date, time, ticket_type, ticket_amount)
            price = "{:0.2f}".format(round((self.cinema.check_price(time, ticket_type) * ticket_amount), 2))
            screen_number = screen.get_screen_number()
            book_film(self.cinema.get_cinemaID(), bookingid, film, date, time, ticket_type, ticket_amount, screen, seat_numbers, price, name, phone, email)            
            self.receipt_page(self.cinema, bookingid, film, date, time, ticket_type, ticket_amount, screen_number, seat_numbers, price, name)


    # after booked, display receipt
    def receipt_page(self, cinema, bookingid, film, date, time, ticket_type, ticket_amount, screen_number, seat_numbers, price, name):
        if not self.vailidate_booking():
            return False
        for frame in self.booking_main:
            try:
                frame.grid_forget()
            except:
                pass
        receipt_frame = ttk.Frame(self)
        receipt_frame.columnconfigure(0, weight=1)
        # labels
        labels = {}
        labels["cinemaid"] = ttk.Label(receipt_frame, text="Cinema:")
        labels["bookingid"] = ttk.Label(receipt_frame, text="Booking ID:")
        labels["name"] = ttk.Label(receipt_frame, text="Name:")
        labels["film"] = ttk.Label(receipt_frame, text="Film:")
        labels["date"] = ttk.Label(receipt_frame, text="Date:")
        labels["time"] = ttk.Label(receipt_frame, text="Time:")
        labels["ticket_type"] = ttk.Label(receipt_frame, text="Ticket type:")
        labels["ticket_amount"] = ttk.Label(receipt_frame, text="Ticket amount:")
        labels["price"] = ttk.Label(receipt_frame, text="Price:")
        labels["screen_number"] = ttk.Label(receipt_frame, text="Screen:")
        labels["seat_numbers"] = ttk.Label(receipt_frame, text="Seats:")

        r = 0
        for value in labels.values():
            value.config(font=("Arial", 12))
            value.grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
            r = r + 1

        info = {}
        # booking info
        info["cinemaid"] = ttk.Label(receipt_frame, text=cinema.get_cinemaID())
        info["bookingid"] = ttk.Label(receipt_frame, text=bookingid)
        info["name"] = ttk.Label(receipt_frame, text=name)
        info["film"] = ttk.Label(receipt_frame, text=film)
        info["date"] = ttk.Label(receipt_frame, text=date)
        info["time"] = ttk.Label(receipt_frame, text=time)
        info["ticket_type"] = ttk.Label(receipt_frame, text=ticket_type)
        info["ticket_amount"] = ttk.Label(receipt_frame, text=ticket_amount)
        info["price"] = ttk.Label(receipt_frame, text="£" + str(price))
        info["screen_number"] = ttk.Label(receipt_frame, text=screen_number)

        info["seat_numbers"] = ttk.Label(receipt_frame, text=", ".join(seat_numbers), wraplength=200, justify="left")

        r = 0
        for info in info.values():
            info.config(font=("Arial", 12))
            info.grid(row=r, column=1, sticky=tk.W, padx=5, pady=5)
            r = r + 1

        receipt_frame.grid(row=0, column=0, padx=220, pady=20)


    # called in book when booking button is pressed, checks for any input fields not filled in and that the film is available
    def vailidate_booking(self):
        for input in self.saved_inputs.values():
            if input.get() == "":
                self.booking_error_message.config(text="Please fill in all input fields")
                return False
        if self.film_is_available:
            return True
        self.booking_error_message.config(text="Please verify selected booking is available")
        return False



class CancellationPage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Cancellation")
        self.user = user
        self.columnconfigure(0, weight=1)
        self.make_search()
        self.grid(row=1, column=0, padx=10, pady=10)


    # creates search bar and button
    def make_search(self):
        search_frame = ttk.Frame(self)
        search_frame.columnconfigure(0, weight=1)
        bookingid_var = tk.StringVar()
        bookingid_label = ttk.Label(search_frame, text="Enter booking ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        bookingid_input = ttk.Entry(search_frame, textvariable=bookingid_var).grid(row=0, column=1, padx=5, pady=5)
        search_button = ttk.Button(search_frame, text="Search", command=lambda: self.get_booking(bookingid_var.get())).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        search_frame.grid(row=0, column=0)
        self.cancelled_message = ttk.Label(self, text="", font=("Arial", 10))
        self.cancelled_message.grid(row=2, column=0, padx=5, pady=10)


    # displays booking correlating to booking id
    def get_booking(self, bookingid):
        self.cancelled_message.config(text="")
        booking_info = get_booking(bookingid)
        # if no booking with that booking id, display error message
        if not booking_info:
            tk.Label(self, text="No booking found with that ID", fg="red").grid(row=1, column=0, padx=5, pady=5)
            return
        # frame for the booking
        booking_frame = ttk.Frame(self, borderwidth=5, relief="groove")
        booking_frame.columnconfigure(0, weight=1)
        # labels
        labels = {}
        labels["name"] = ttk.Label(booking_frame, text="Name:")
        labels["film"] = ttk.Label(booking_frame, text="Film:")
        labels["date"] = ttk.Label(booking_frame, text="Date:")
        labels["time"] = ttk.Label(booking_frame, text="Time:")
        labels["ticket_type"] = ttk.Label(booking_frame, text="Ticket type:")
        labels["ticket_amount"] = ttk.Label(booking_frame, text="Ticket amount:")
        r = 0
        for label in labels.values():
            label.config(font=("Arial", 12))
            label.grid(row=r, column=0, sticky=tk.W, padx=5, pady=2)
            r = r + 1

        # booking info
        info = {}
        info["name"] = ttk.Label(booking_frame, text=booking_info.get_name())
        info["film"] = ttk.Label(booking_frame, text=booking_info.get_film())
        info["date"] = ttk.Label(booking_frame, text=booking_info.get_date())
        info["time"] = ttk.Label(booking_frame, text=booking_info.get_time())
        info["ticket_type"] = ttk.Label(booking_frame, text=booking_info.get_ticket_type())
        info["ticket_amount"] = ttk.Label(booking_frame, text=booking_info.get_ticket_amount())
        r = 0
        for info in info.values():
            info.config(font=("Arial", 12))
            info.grid(row=r, column=1, sticky=tk.W, padx=5, pady=2)
            r = r + 1
        # cancel booking button inside frame
        if self.check_booking_date(booking_info.get_date()):
            cancellation_button = ttk.Button(booking_frame, text="Cancel booking", command=lambda: self.cancel_booking(bookingid, booking_frame))
            cancellation_button.grid(row=r, column=0, columnspan=2, ipadx=5, ipady=2)
        else:
            cancellation_message = ttk.Label(booking_frame, text="Cannot cancel bookings later than one day before show")
            cancellation_message.grid(row=r, column=0, columnspan=2, ipadx=5, ipady=2)
        booking_frame.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=10)
            

    # called to cancel booking
    def cancel_booking(self, bookingid, booking_frame):
        booking = cancel_booking(bookingid)     # returns false if booking not found, otherwise the cancelled booking info
        if booking is not False:
            booking_frame.grid_forget()
            self.cancelled_message.config(text="Ticket cancelled, 50% refunded at £{:0.2f}".format(float(booking.get_price()) / 2))
            print("Booking cancelled")
        else:
            print("Booking failed to cancel")


    def check_booking_date(self, date):
        date = dt.strptime(date, "%d %B").date()
        print(date)
        now = dt.now()
        print(now)
        if not (now.day < date.day) and not (now.month <= date.month):
            return False
        return True



class LoginPage(ttk.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main.title("Login")
        self.main = main
        self.create_login()
        self.grid(row=1, column=0)


    # creates login page
    def create_login(self):
        login_frame = ttk.Frame(self)
        login_frame.columnconfigure(0, weight=1)
        login_frame.rowconfigure(0, weight=1)
        # login variables
        id = tk.StringVar()
        password = tk.StringVar()

        # all labels and entries
        fields = {}
        fields["id_label"] = ttk.Label(login_frame, text="Staff ID:", font=("Arial", 14)).grid(row=0, column=0)
        fields["id_value"] = ttk.Entry(login_frame, textvariable=id).grid(row=1, column=0, padx=5, pady=5, ipadx=15, ipady=1)
        fields["password_label"] = ttk.Label(login_frame, text="Password:", font=("Arial", 14)).grid(row=3, column=0)
        fields["password_value"] = ttk.Entry(login_frame, textvariable=password, show="*").grid(row=4, column=0, padx=5, pady=5, ipadx=15, ipady=1)
        login_button = ttk.Button(login_frame, text="Login", command=lambda: self.login(id.get(), password.get())).grid(row=6, column=0, padx=5, pady=5, ipadx=20, ipady=2)

        # create error message incase of failed login but dont display any text
        self.login_error = tk.Label(login_frame, text="", fg="red", font=("Arial", 10))
        self.login_error.grid(row=7, column=0, padx=5, pady=5)

        login_frame.grid(row=0, column=0, pady=20)


    # called when login button is pressed
    def login(self, id, password):
        user = login(id, password)      # returns false if credentials dont match, otherwise returns the user object
        if user is not False:
            self.main.logged_in(user)
        else:
            # display text for error message
            self.login_error.config(text="Invalid credentials")



class AdminPage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Admin view")
        self.user = user
        self.main = main
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.create_left()
        self.seperator()
        self.create_right()
        self.grid(row=1, column=0, sticky=tk.NSEW)


    # called when any button on admin page is pressed, hides the main page so another page can display and displays the back button
    def new_page(self):
        self.screenings_frame.grid_forget()
        self.canvas_frame.grid_forget()
        try:
            self.canvas.grid_forget()
            try: 
                self.canvas2.grid_forget()
            except:
                pass
        except:
            pass
        self.reports_frame.grid_forget()
        back_button = ttk.Button(self, text="Back", command=self.main_page)
        back_button.grid(row=0, column=0, padx=20, pady=10, ipadx=5, ipady=2, sticky=tk.NW)


    # called when back button is pressed, returns to main admin page
    def main_page(self):
        self.main.page_change(AdminPage(self.main, self.user))


    def create_top(self):
        self.cinema = self.user.get_cinema()
        screens = self.cinema.get_screens()
        if screens:
            self.screen = screens[0]
        self.top_frame = ttk.Frame(self)
        self.cinema_id_var = tk.StringVar()
        self.screen_number_var = tk.StringVar()
        ttk.Label(self.top_frame, text="Select cinema:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.NW)
        cinema_options = ttk.OptionMenu(self.top_frame, self.cinema_id_var, self.cinema.get_cinemaID(), *get_list_of_cinemas_id(), command=lambda cinema_id: self.change_cinema(cinema_id))
        cinema_options.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)
        ttk.Label(self.top_frame, text="Select screen:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.NW)
        self.screen_menu()
        self.top_frame.grid(row=1, column=0, sticky=tk.W)


    def screen_menu(self):
        self.screen_options = ttk.OptionMenu(self.top_frame, self.screen_number_var, self.screen.get_screen_number(), *get_list_of_screen_numbers(self.cinema), command=lambda screen_number: self.change_screen(screen_number))
        self.screen_options.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=2, sticky=tk.NW)


    def change_cinema(self, id):
        print("Reloading listings for cinema: " + str(id))
        self.cinema = find_cinema(id)
        screens = self.cinema.get_screens()
        if screens:
            self.screen = screens[0]
        self.screen_options.grid_forget()
        self.temp_frame.grid_forget()
        self.canvas.grid_forget()
        self.screen_menu()
        self.manage_shows_page()


    def change_screen(self, id):
        print("Reloading listings for screen: " + str(id))
        self.screen = self.cinema.get_screen_by_id(id)
        self.temp_frame.grid_forget()
        self.canvas.grid_forget()
        self.manage_shows_page()
        

    # create canvas needed for making a scrolling page
    def create_listings_canvas(self, row, col, func, width="350", height="300"):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(2, weight=0)
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.listing_frame = func()
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=row, column=col+1, sticky="nsw")
        self.canvas.grid(row=row, column=col, sticky=tk.W, padx=10)
        self.canvas_id = self.canvas.create_window(0, 0, window=self.listing_frame, anchor=tk.NW)
        self.listing_frame.bind("<Configure>", self.scroll_config)
        self.canvas.bind("<Configure>", self.resize_canvas)


    def create_listings_canvas2(self, row, col, func):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(2, weight=0)
        self.canvas2 = tk.Canvas(self, width="350", height="300")
        self.listing_frame2 = func()
        self.scrollbar2 = ttk.Scrollbar(self, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.grid(row=row, column=col+1, sticky="nsw", rowspan=3)
        self.canvas2.grid(row=row, column=col, sticky=tk.W, padx=10, rowspan=3)
        self.canvas_id2 = self.canvas2.create_window(0, 0, window=self.listing_frame2, anchor=tk.NW)
        self.listing_frame2.bind("<Configure>", self.scroll_config2)
        self.canvas2.bind("<Configure>", self.resize_canvas2)


    # for making the canvas scroll
    def scroll_config(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # makes canvas expand
    def resize_canvas(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_id, width=canvas_width)


    # for making the canvas scroll
    def scroll_config2(self, event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))


    # makes canvas expand
    def resize_canvas2(self, event):
        canvas_width = event.width
        self.canvas2.itemconfig(self.canvas_id2, width=canvas_width)


    def manage_shows_page(self):
        self.current_page = self.manage_shows_page
        self.new_page()
        self.create_listings_canvas(2, 0, self.manage_showing_page)
        self.create_listings_canvas2(0, 2, self.add_films_to_screen_page)


    def manage_showing_page(self):
        self.temp_frame = ttk.Frame(self)
        self.temp_frame.columnconfigure(0, weight=1)

        ttk.Style().configure("listings.TFrame", background="#BDE6E6")
        r = 0
        self.current_listings = []
        for listing in self.screen.get_showings():
            current_listing = ttk.Frame(self.temp_frame, borderwidth=5, relief="groove")
            ttk.Label(current_listing, text=listing.get_name(), font=("Arial", 16), background="#BDE6E6", wraplength=320, justify="left").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(current_listing, text="Show dates: " + str(", ".join(listing.get_show_dates_str())), font=("Arial", 12), background="#BDE6E6", \
                        wraplength=320, justify="left").grid(row=5, column=0, sticky=tk.W)
            ttk.Label(current_listing, text="Show times: " + str(", ".join(listing.get_show_times_str())), font=("Arial", 12), background="#BDE6E6", \
                        wraplength=320, justify="left").grid(row=6, column=0, sticky=tk.W)
            current_listing.config(style="listings.TFrame")
            current_listing.grid(row=r, column=0, padx=0, pady=10, sticky=tk.EW)
            r = r + 1
            b_frame = ttk.Frame(current_listing, style="listings.TFrame")
            manage_show_buttons = {}
            manage_show_buttons["remove"] = ttk.Button(b_frame, text="Remove from screen", command=lambda listing=listing: self.remove_listing(listing))
            manage_show_buttons["remove"].grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
            manage_show_buttons["update"] = ttk.Button(b_frame, text="Update dates/times", command=lambda listing=listing, frame=b_frame, dic=manage_show_buttons: self.update_dates_times(listing, frame, dic))
            manage_show_buttons["update"].grid(row=0, column=1, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.E)
            b_frame.grid(row=7, column=0, sticky=tk.EW)
            self.current_listings.append(current_listing)

        self.temp_frame.grid(row=0, column=0)
        return self.temp_frame


    def add_films_to_screen_page(self):
        temp_frame = ttk.Frame(self)
        temp_frame.columnconfigure(0, weight=1)

        ttk.Style().configure("listings.TFrame", background="#BDE6E6")
        r = 0
        films = []
        for film in get_all_films():
            current_listing = ttk.Frame(temp_frame, borderwidth=5, relief="groove")
            ttk.Label(current_listing, text=film.get_name(), font=("Arial", 16), background="#BDE6E6", wraplength=320, justify="left").grid(row=0, column=0, sticky=tk.W)
            current_listing.config(style="listings.TFrame")
            current_listing.grid(row=r, column=0, padx=0, pady=10, sticky=tk.EW)
            r = r + 1
            b_frame = ttk.Frame(current_listing, style="listings.TFrame")
            manage_show_buttons = {}
            manage_show_buttons["add"] = ttk.Button(b_frame, text="Add to screen", command=lambda film=film, frame=b_frame, dic=manage_show_buttons: self.add_film_to_screen(film, frame, dic))
            manage_show_buttons["add"].grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
            b_frame.grid(row=7, column=0, sticky=tk.EW)
            films.append(current_listing)

        temp_frame.grid(row=0, column=0)
        return temp_frame


    def add_film_to_screen(self, film, frame, dic):
        s = ttk.Style()
        s.configure("bg.TFrame", background="#BDE6E6")
        for b in dic.values():
            b.grid_forget()
        self.film_dates_frame = ttk.Frame(frame, style="bg.TFrame")
        self.film_date_entries = []
        ttk.Label(self.film_dates_frame, text="Enter show date:", background="#BDE6E6").grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        ttk.Button(self.film_dates_frame, text="New date", command=lambda: self.new_film_date()).grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.film_date_entries.append(tkcal.DateEntry(self.film_dates_frame, selectmode="day"))
        self.film_date_entries[0].grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.film_dates_frame.grid(row=0, column=0, sticky=tk.W)
        self.film_times_frame = ttk.Frame(frame, style="bg.TFrame")
        self.film_time_entries = []
        ttk.Label(self.film_times_frame, text="Enter show time:", background="#BDE6E6").grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        ttk.Button(self.film_times_frame, text="New time", command=lambda: self.new_film_time()).grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.film_time_entries.append(SpinTimePickerOld(self.film_times_frame))
        self.film_time_entries[0].addAll(constants.HOURS24)
        self.film_time_entries[0].grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.film_times_frame.grid(row=1, column=0, sticky=tk.W)
        confirm_button = ttk.Button(frame, text="Confirm", command=lambda film=film: self.confirm_add_film_to_screen(film))
        confirm_button.grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def confirm_add_film_to_screen(self, film):
        show_dates = []
        show_times = []
        for d in self.film_date_entries:
            date = d.get_date()
            show_dates.append(dt(2023, date.month, date.day))
        for t in self.film_time_entries:
            show_times.append(time(t.hours(), t.minutes()))
        self.screen.add_showing(Showing(film, show_dates, show_times))
        self.change_screen(self.screen.get_screen_number())


    def new_film_date(self):
        self.film_date_entries.append(tkcal.DateEntry(self.film_dates_frame, selectmode="day"))
        self.film_date_entries[len(self.film_date_entries)-1].grid(row=len(self.film_date_entries)+1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def new_film_time(self):
        self.film_time_entries.append(SpinTimePickerOld(self.film_times_frame))
        self.film_time_entries[len(self.film_time_entries)-1].addAll(constants.HOURS24)
        self.film_time_entries[len(self.film_time_entries)-1].grid(row=len(self.film_time_entries)+1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def remove_listing(self, listing):
        self.screen.remove_showing(listing)
        self.change_screen(self.screen.get_screen_number())


    def update_dates_times(self, listing, frame, dic):
        s = ttk.Style()
        s.configure("bg.TFrame", background="#BDE6E6")
        for b in dic.values():
            b.grid_forget()
        self.dates_frame = ttk.Frame(frame, style="bg.TFrame")
        self.date_entries = []
        ttk.Label(self.dates_frame, text="Enter date:", background="#BDE6E6").grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        ttk.Button(self.dates_frame, text="New date", command=lambda: self.new_date()).grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.date_entries.append(tkcal.DateEntry(self.dates_frame, selectmode="day"))
        self.date_entries[0].grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.dates_frame.grid(row=0, column=0, sticky=tk.W)
        self.times_frame = ttk.Frame(frame, style="bg.TFrame")
        self.time_entries = []
        ttk.Label(self.times_frame, text="Enter time:", background="#BDE6E6").grid(row=0, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        ttk.Button(self.times_frame, text="New time", command=lambda: self.new_time()).grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.time_entries.append(SpinTimePickerOld(self.times_frame))
        self.time_entries[0].addAll(constants.HOURS24)
        self.time_entries[0].grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)
        self.times_frame.grid(row=1, column=0, sticky=tk.W)
        confirm_button = ttk.Button(frame, text="Confirm", command=lambda listing=listing: self.confirm_update_dates_times(listing))
        confirm_button.grid(row=2, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def new_date(self):
        self.date_entries.append(tkcal.DateEntry(self.dates_frame, selectmode="day"))
        self.date_entries[len(self.date_entries)-1].grid(row=len(self.date_entries)+1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def new_time(self):
        self.time_entries.append(SpinTimePickerOld(self.times_frame))
        self.time_entries[len(self.time_entries)-1].addAll(constants.HOURS24)
        self.time_entries[len(self.time_entries)-1].grid(row=len(self.time_entries)+1, column=0, padx=5, pady=2, ipadx=5, ipady=2, sticky=tk.W)


    def confirm_update_dates_times(self, listing):
        dates = []
        times = []
        for d in self.date_entries:
            dates.append(d.get_date())
        for t in self.time_entries:
            times.append(time(t.hours(), t.minutes()))
        listing.update_show_dates(dates)
        listing.update_show_times(times)
        self.change_screen(self.screen.get_screen_number())


    def add_film_page(self):
        self.current_page = self.add_film_page
        self.new_page()
        self.temp_frame = ttk.Frame(self)
        self.temp_frame.columnconfigure(0, weight=1)

        # labels
        film_labels = {}
        film_labels["name"] = ttk.Label(self.temp_frame, text="Film name:")
        film_labels["actors"] = ttk.Label(self.temp_frame, text="Actors:")
        film_labels["description"] = ttk.Label(self.temp_frame, text="Description:")
        film_labels["genre"] = ttk.Label(self.temp_frame, text="Genre:")
        film_labels["age_rating"] = ttk.Label(self.temp_frame, text="Age rating:")

        r = 0
        for val in film_labels.values():
            val.grid(row=r, column=0, padx=5, pady=5, sticky=tk.W)
            r += 1


        self.add_film_entry_vars = {}
        self.add_film_entry_vars["name"] = tk.StringVar()
        self.add_film_entry_vars["actors"] = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.add_film_entry_vars["description"] = tk.StringVar()
        self.add_film_entry_vars["genre"] = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.add_film_entry_vars["age_rating"] = tk.StringVar()

        # entries
        film_entries = {}
        film_entries["name"] = ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["name"])
        film_entries["actors"] = [ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["actors"][0]), ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["actors"][1]), \
                                    ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["actors"][2]), ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["actors"][3])]
        film_entries["description"] = ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["description"])
        film_entries["genre"] = [ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["genre"][0]), ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["genre"][1]), \
                                    ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["genre"][2]), ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["genre"][3])]
        film_entries["age_rating"] = ttk.Entry(self.temp_frame, textvariable=self.add_film_entry_vars["age_rating"])


        r = 0
        for name, value in film_entries.items():
            c = 1
            if name == "actors" or name == "genre":
                for v in value:
                    v.grid(row=r, column=c, padx=5, pady=5, sticky=tk.W)
                    c += 1
            else:
                value.grid(row=r, column=1, padx=5, pady=5, sticky=tk.W)
            r += 1

        ttk.Button(self.temp_frame, text="Add film", command=lambda: self.add_film()).grid(row=r, column=0, columnspan=5, padx=10, pady=10, ipadx=5, ipady=2)
        self.add_film_message = tk.Label(self.temp_frame, text="")
        self.add_film_message.grid(row=r+1, column=0, columnspan=5, padx=10, pady=10)

        self.temp_frame.grid(row=1, column=0, padx=50, pady=20)


    def add_film(self):
        self.add_film_message.config(text="")
        if self.validate_entries():
            add_film(self.add_film_entry_vars)
            self.add_film_message.config(text=str(self.add_film_entry_vars["name"].get()) + " successfully added", fg="black")
            self.new_page()
        else:
            self.add_film_message.config(text="Please fill in more inputs", fg="red")


    def validate_entries(self):
        for name, val in self.add_film_entry_vars.items():
            if name == "actors" or name == "genre":
                empty = 0
                for v in val:
                    if not v.get():
                        empty += 1
                    if empty >= 4:
                        return False  
            else:
                if val.get() == "":
                    return False
        return True


    def remove_film_page(self):
        self.current_page = lambda: self.create_listings_canvas(2, 0, self.remove_film_page, "760", "370")
        self.new_page()
        self.temp_frame = ttk.Frame(self)
        self.temp_frame.columnconfigure(0, weight=1)

        ttk.Style().configure("listings.TFrame", background="#BDE6E6")
        film_list = []
        r = 0
        for film in get_all_films():
            film_frame = ttk.Frame(self.temp_frame, borderwidth=5, relief="groove", style="listings.TFrame")
            film_frame.columnconfigure(0, weight=1)
            ttk.Label(film_frame, text=film.get_name(), font=("Arial", 16), background="#BDE6E6").grid(row=0, column=0, sticky=tk.W) 
            ttk.Label(film_frame, text="Starring: " + ", ".join(film.get_actors()), font=("Arial", 12), background="#BDE6E6").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(film_frame, text=film.get_description(), font=("Arial", 10), background="#BDE6E6").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(film_frame, text=", ".join(film.get_genre()), font=("Arial", 12), background="#BDE6E6").grid(row=3, column=0, sticky=tk.W)
            ttk.Label(film_frame, text=film.get_age_rating(), font=("Arial", 12), background="#BDE6E6").grid(row=4, column=0, sticky=tk.W)
            ttk.Button(film_frame, text="Remove film", command=lambda film=film: self.remove_film(film)).grid(row=5, column=0)
            film_frame.grid(row=r, column=0, padx=50, pady=10, sticky=tk.EW)
            r = r + 1
            film_list.append(film_frame)
        self.temp_frame.grid(row=1, column=0)
        return self.temp_frame

    
    def remove_film(self, film):
        remove_film(film)
        self.temp_frame.grid_forget()
        self.current_page()


    # make left side of main page, for screening management
    def create_left(self):
        self.screenings_frame = ttk.Frame(self)
        self.screenings_frame.columnconfigure(0, weight=1)
        ttk.Label(self.screenings_frame, text="Manage screenings", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.N)

        # make buttons
        buttons_frame = ttk.Frame(self.screenings_frame)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.rowconfigure(0, weight=1)

        manage_showings_button = ttk.Button(buttons_frame, text="Manage showings")
        manage_showings_button.bind("<Button>", lambda e: self.create_top())
        manage_showings_button.bind("<Button>", lambda e: self.manage_shows_page(), "+")
        manage_showings_button.grid(row=0, column=0, padx=5, pady=5, ipadx=10, ipady=5)

        manage_films_buttons = {}
        manage_films_buttons["add_film"] = ttk.Button(buttons_frame, text="Add film", command=self.add_film_page)      
        manage_films_buttons["remove_film"] = ttk.Button(buttons_frame, text="Remove film", command=lambda: self.create_listings_canvas(2, 0, self.remove_film_page, "760", "370"))

        r = 1
        for button in manage_films_buttons.values():
            button.grid(row=r, column=0, padx=5, pady=5, ipadx=10, ipady=5)
            r += 1        


        buttons_frame.grid(row=1, column=0, pady=50)
        self.screenings_frame.grid(row=0, column=0, sticky=tk.NSEW)


    # make seperator in middle of screen
    def seperator(self):
        self.canvas_frame = ttk.Frame(self)
        canvas = tk.Canvas(self.canvas_frame, width=5, height=500)
        canvas.grid(row=0, column=1, sticky=tk.N)
        canvas.create_line(0, 0, 0, 400, fill="#3EAFD1", width=5)
        self.canvas_frame.grid(row=0, column=1)


    # make right side of main page, for report generating
    def create_right(self):
        self.reports_frame = ttk.Frame(self)
        self.reports_frame.columnconfigure(0, weight=1)
        ttk.Label(self.reports_frame, text="Generate a report", font=("Arial", 12)).grid(row=0, column=0)

        # make buttons
        buttons_frame = ttk.Frame(self.reports_frame)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.rowconfigure(0, weight=1)

        ttk.Button(buttons_frame, text="Number of booking for listings", command=lambda: self.create_listings_canvas(2, 0, self.bookings_report, "760", "370")).grid(row=0, column=0, padx=5, pady=5, ipadx=10, ipady=5)


        buttons_frame.grid(row=1, column=0, pady=50)

        self.reports_frame.grid(row=0, column=2, sticky=tk.NSEW)


    def bookings_report(self):
        self.current_page = lambda: self.create_listings_canvas(2, 0, self.bookings_report, "760", "370")
        self.new_page()
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("l.TFrame", background="#BDE6E6")
        r = 0
        for cinema in cinemas:
            for showing in cinema.get_film_listings():
                current_listings = ttk.Frame(frame, borderwidth=5, relief="groove", style="l.TFrame")
                ttk.Label(current_listings, text=showing.get_name(), font=("Arial", 16), background="#BDE6E6").grid(row=0, column=0, sticky=tk.W)
                ttk.Label(current_listings, text="Cinema: " + str(cinema.get_cinemaID()), font=("Arial", 15), background="#BDE6E6").grid(row=1, column=0, sticky=tk.W)
                ttk.Label(current_listings, text="Show dates: " + str(", ".join(showing.get_show_dates_str())), font=("Arial", 12), background="#BDE6E6").grid(row=2, column=0, sticky=tk.W)
                ttk.Label(current_listings, text="Show times: " + str(", ".join(showing.get_show_times_str())), font=("Arial", 12), background="#BDE6E6").grid(row=3, column=0, sticky=tk.W)
                ttk.Label(current_listings, text="Number of bookings: " + str(get_number_of_bookings(showing)), font=("Arial", 12), background="#BDE6E6").grid(row=4, column=0, sticky=tk.W)
                current_listings.grid(row=r, column=0, padx=50, pady=10, sticky=tk.EW)
                r = r + 1
        frame.grid(row=1, column=0)
        return frame



class ManagerPage(ttk.Frame):
    def __init__(self, main, user):
        super().__init__(main)
        main.title("Manager view")
        self.main = main
        self.user = user
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.make_page()
        self.grid(row=1, column=0)


    def make_page(self):
        button_frame = ttk.Frame(self)
        button_frame.columnconfigure(0, weight=1)
        button_frame.rowconfigure(0, weight=1)

        admin_button = ttk.Button(button_frame, text="Admin features", command=self.admin_page)
        admin_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=5)

        new_cinema_button = ttk.Button(button_frame, text="Add new cinema", command=lambda frame=button_frame: self.new_cinema_page(frame))
        new_cinema_button.grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5)

        button_frame.grid(row=0, column=0, padx=80, pady=80)


    def admin_page(self):
        self.main.page_change(AdminPage(self.main, self.user))


    def new_cinema_page(self, f):
        f.grid_forget()

        title = ttk.Label(self, text="Add new cinema", font=("Arial", 16))
        title.grid(row=0, column=0, padx=5, pady=5)

        main_frame = ttk.Frame(self)

        input_labels = {}
        input_labels["city"] = ttk.Label(main_frame, text="Choose city:")
        input_labels["cinema_id"] = ttk.Label(main_frame, text="Enter city ID:")
        input_labels["screen_amount"] = ttk.Label(main_frame, text="Select amount of screens:")

        r = 0
        for val in input_labels.values():
            val.grid(row=r, column=0, padx=5, pady=5, sticky=tk.W)
            r += 1

        self.entry_vars = {}
        self.entry_vars["city"] = tk.StringVar()
        self.entry_vars["cinema_id"] = tk.StringVar()
        self.entry_vars["screen_amount"] = tk.StringVar()

        cities = ["Birmingham", "Bristol", "Cardiff", "London"]

        input_entries = {}
        input_entries["city"] = ttk.OptionMenu(main_frame, self.entry_vars["city"], None, *cities)
        input_entries["cinema_id"] = ttk.Entry(main_frame, textvariable=self.entry_vars["cinema_id"])
        input_entries["screen_amount"] = ttk.Entry(main_frame, textvariable=self.entry_vars["screen_amount"])

        r = 0
        for val in input_entries.values():
            val.grid(row=r, column=1, padx=5, pady=5, sticky=tk.W)
            r += 1

        ttk.Button(main_frame, text="Continue", command=lambda: self.check_screens(title, main_frame)).grid(row=r, column=0, columnspan=2, padx=10, pady=10, ipadx=5, ipady=5)

        self.message = tk.Label(main_frame, text="")
        self.message.grid(row=r+1, column=0, columnspan=2)

        main_frame.grid(row=1, column=0, padx=20, pady=20)


    def check_screens(self, t, f):
        self.message.config(text="", fg="black")
        if self.validate_form(self.entry_vars):
            t.grid_forget()
            f.grid_forget()

            num_of_screens = int(self.entry_vars["screen_amount"].get())
            title = ttk.Label(self, text="Enter amount of seats for each screen", font=("Arial", 12))
            title.grid(row=1, column=0, padx=10, pady=10)
            entry_frame = ttk.Frame(self)
            screen_seats = []
            for i in range(0, num_of_screens):
                screen_seats.append(tk.StringVar())
            for i in range(1, num_of_screens+1):
                ttk.Label(entry_frame, text="Screen " + str(i) + ":").grid(row=i-1, column=0, padx=5, pady=5, sticky=tk.W)
                ttk.Entry(entry_frame, textvariable=screen_seats[i-1]).grid(row=i-1, column=1, padx=5, pady=5, sticky=tk.W)
            ttk.Button(entry_frame, text="Confirm", command=lambda: self.confirm_seats(title, entry_frame, screen_seats)).grid(row=i+1, column=0, columnspan=2, padx=10, pady=10, ipadx=5, ipady=2)
            self.check_message = tk.Label(entry_frame, text="")
            self.check_message.grid(row=i+2, column=0, columnspan=2, padx=5, pady=5)

            entry_frame.grid(row=2, column=0, padx=20, pady=20)


    def validate_form(self, entries):
        for name, val in entries.items():
            if val.get() == "":
                self.message.config(text="Please fill in all entries", fg="red")
                return False
            if name == "screen_amount":
                print("screen_amount")
                try:
                    num = int(val.get())
                    if num > 6 or num < 1:
                        self.message.config(text="Amount of screens must be between 1 and 6", fg="red")
                        return False
                except:
                    self.message.config(text="Amount of screens must be an integer", fg="red")        
                    return False        
        return True


    def confirm_seats(self, t, f, vars):
        self.check_message.config(text="", fg="black")
        if self.validate_seating_form(vars):
            t.grid_forget()
            f.grid_forget()
            create_cinema(self.entry_vars["city"].get(), self.entry_vars["cinema_id"].get(), self.entry_vars["screen_amount"].get(), vars)
            ttk.Label(self, text="Successfully created cinema " + self.entry_vars["cinema_id"].get() + " in " + self.entry_vars["city"].get() + " with "\
                        + self.entry_vars["screen_amount"].get() + " screens", font=("Arial", 16)).grid(row=1, column=0, padx=50, pady=50)


    def validate_seating_form(self, vars):
        for var in vars:
            var = var.get()
            if var == "":
                self.check_message.config(text="Please fill in all entries", fg="red")
                return False
            try:
                num = int(var)
                if num > 120 or num < 50:
                    self.check_message.config(text="Seat amount must be between 50 and 120", fg="red")
                    return False
            except:
                self.check_message.config(text="Entires must be an integer", fg="red")
                return False
        return True



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()