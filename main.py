import flet as ft

from common import *

SUIT_DISPLAY = {
    'c': '♣',
    'd': '♦',
    'h': '♥',
    's': '♠',
}
SUIT_COLOR = {
    'c': '#007700',
    'd': '#000077',
    'h': '#770000',
    's': '#000000',
}

class CardDropdownOption(ft.dropdown.Option):
    def __init__(self, rank, suit):
        super().__init__(
            alignment=ft.alignment.center,
            text=rank + SUIT_DISPLAY[suit],
            key=rank + suit,
            text_style=ft.TextStyle(
                color=SUIT_COLOR[suit],
                bgcolor='#dddddd',
            ),
        )


class CardDropdown(ft.Dropdown):
    def __init__(self, *, label=None, on_change):
        options = [ ft.dropdown.Option(text=' ', key=' ') ] + [
            CardDropdownOption(rank, suit)
            for suit in SUITS
            for rank in RANKS
        ]
        super().__init__(
            border_color='transparent',
            label=label,
            width=75,
            dense=True,
            options=options,
            bgcolor='#dddddd',
            on_change=on_change,
        )

    def update_options(self, board):
        self.options = [ ft.dropdown.Option(text=' ', key=' ') ] + [
            CardDropdownOption(rank, suit)
            for suit in SUITS
            for rank in RANKS
            if rank + suit not in board or rank + suit == self.value
        ]
        self.update()


class BoardEditor(ft.Column):
    def __init__(self):
        self.cards = [None, None, None, None, None]

        def get_on_change(index):
            def on_change(e):
                self.cards[index] = e.control.value
                board = set(self.cards)
                for cc in self.card_controls:
                    if isinstance(cc, CardDropdown):
                        cc.update_options(board)

            return on_change

        self.card_controls = [
            CardDropdown(on_change=get_on_change(0)),
            CardDropdown(on_change=get_on_change(1)),
            CardDropdown(on_change=get_on_change(2)),
            ft.VerticalDivider(width=16),
            CardDropdown(on_change=get_on_change(3)),
            ft.VerticalDivider(width=16),
            CardDropdown(on_change=get_on_change(4)),
        ]

        super().__init__(
            spacing=4,
            controls=[
                ft.Text('Community cards'),
                ft.Row(controls=self.card_controls),
            ]
        )

class PreflopRangeButton(ft.Container):
    def __init__(self, starting_hand, *, is_selected=False, on_click=None):
        self._is_selected = is_selected
        self.starting_hand = starting_hand
        self._on_click = on_click

        def on_click(e):
            self.is_selected = not self.is_selected
            if self._on_click:
                self._on_click(e)

        def on_long_press(e):
            print('Long pressed {}.'.format(self.starting_hand))

        super().__init__(
            content=ft.Text(starting_hand, color=ft.colors.ON_SECONDARY_CONTAINER),
            alignment=ft.alignment.center,
            width=32,
            height=32,
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            border=ft.border.all(1, ft.colors.ON_SECONDARY_CONTAINER),
            border_radius=ft.border_radius.all(5),
            on_click=on_click,
            on_long_press=on_long_press,
        )

    def _get_is_selected(self):
        return self._is_selected

    def _set_is_selected(self, is_selected):
        self._is_selected = is_selected

        if is_selected:
            self.bgcolor = ft.colors.PRIMARY_CONTAINER
            self.content.color = ft.colors.ON_PRIMARY_CONTAINER
            self.border = ft.border.all(1, ft.colors.ON_PRIMARY_CONTAINER)

        else:
            self.bgcolor = ft.colors.SECONDARY_CONTAINER
            self.content.color = ft.colors.ON_SECONDARY_CONTAINER
            self.border = ft.border.all(1, ft.colors.ON_SECONDARY_CONTAINER)

        self.update()

    is_selected = property(_get_is_selected, _set_is_selected)

class PreflopRangeEditor(ft.Column):
    def __init__(self, *, name, pf_range=None):
        self.name = name

        if pf_range is None:
            self.range = {}
        else:
            self.range = pf_range

        def toggle_starting_hand(starting_hand):
            def handler(e):
                self.range[starting_hand] = not self.range[starting_hand]

            return handler

        column_controls = [
            ft.Text(self.name),
        ]

        for i in range(len(RANKS)):
            row_controls = []

            for j in range(len(RANKS)):
                starting_hand = (
                    RANKS[i] + RANKS[j] + 's' if i < j else
                    RANKS[j] + RANKS[i] + 'o' if i > j else
                    RANKS[i] + RANKS[i]
                )
                self.range[starting_hand] = False

                row_controls.append(PreflopRangeButton(
                    starting_hand,
                    on_click=toggle_starting_hand(starting_hand),
                ))

            column_controls.append(ft.Row(
                controls=row_controls,
                spacing=4,
            ))

        super().__init__(
            controls=column_controls,
            spacing=4,
        )

def main(page: ft.Page):
    board_editor = BoardEditor()
    hero_range_editor = PreflopRangeEditor(name='Range 1')
    villain_range_editor = PreflopRangeEditor(name='Range 2')
    page.add(board_editor)
    page.add(ft.Row(
        controls=[
            hero_range_editor,
            villain_range_editor,
        ],
        spacing=10,
    ))
    page.update()

ft.app(target=main)
