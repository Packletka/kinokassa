from screens.home.home_screen import HomeScreen
from screens.movie.movie_screen import MovieScreen
from screens.tickets.tickets_screen import TicketsScreen
from screens.profile.profile_screen import ProfileScreen
from screens.sessions.sessions_screen import SessionScreen
from screens.hall.hall_screen import HallScreen
from screens.checkout.checkout_screen import CheckoutScreen


def setup_routes(screen_manager):
    screen_manager.add_widget(HomeScreen(name="home"))
    screen_manager.add_widget(MovieScreen(name="movie"))
    screen_manager.add_widget(TicketsScreen(name="tickets"))
    screen_manager.add_widget(ProfileScreen(name="profile"))
    screen_manager.add_widget(SessionScreen(name="sessions"))
    screen_manager.add_widget(HallScreen(name="hall"))
    screen_manager.add_widget(CheckoutScreen(name="checkout"))

    screen_manager.current = "home"
