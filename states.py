#!/usr/bin/env python3
from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    waiting_for_delegate_input = State()
    waiting_for_delegate_confirm = State()
