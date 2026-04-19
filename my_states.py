from telebot.handler_backends import State, StatesGroup



class ChoiceFilters(StatesGroup):
   waiting_filters = State()
   waiting_year_with = State()
   waiting_year_to = State()

class Pagination(StatesGroup):
   viewing = State()


