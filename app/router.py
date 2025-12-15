from screens.home.home_screen import HomeScreen
from screens.movie.movie_screen import MovieScreen
from screens.tickets.tickets_screen import TicketsScreen
from screens.profile.profile_screen import ProfileScreen


def setup_routes(screen_manager):
    screen_manager.add_widget(HomeScreen(name="home"))
    screen_manager.add_widget(MovieScreen(name="movie"))
    screen_manager.add_widget(TicketsScreen(name="tickets"))
    screen_manager.add_widget(ProfileScreen(name="profile"))

    screen_manager.current = "home"
