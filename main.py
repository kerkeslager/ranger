import flet as ft

from common import *
import equity

CLUB_GREEN = '#006600'
DIAMOND_BLUE = '#000099'
HEART_RED = '#880000'
SPADE_BLACK = '#000000'

SUIT_DISPLAY = {
    'c': '♣',
    'd': '♦',
    'h': '♥',
    's': '♠',
}
SUIT_COLOR = {
    'c': CLUB_GREEN,
    'd': DIAMOND_BLUE,
    'h': HEART_RED,
    's': SPADE_BLACK,
}

class CardDisplay(ft.Container):
    SMALL = (40, 64, 20)
    LARGE = (60, 96, 36)
    def __init__(self, card, size=SMALL):
        self.card = card
        super().__init__(
            alignment=ft.alignment.center,
            width=size[0],
            height=size[1],
            border_radius=5,
            bgcolor='white',
            padding=0,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    ft.Text(
                        self.card[0],
                        color=SUIT_COLOR[self.card[1]],
                        size=size[2],
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.NONE,
                            height=1,
                        ),
                    ),
                    ft.Text(
                        SUIT_DISPLAY[self.card[1]],
                        color=SUIT_COLOR[self.card[1]],
                        size=size[2],
                        style=ft.TextStyle(
                            decoration=ft.TextDecoration.NONE,
                            height=1,
                        ),
                    ),
                ],
            ),
        )

class BoardCardArea(ft.GestureDetector):
    def __init__(self, *, on_card_return):
        self._card = None

        width, height, font_size = CardDisplay.LARGE
        self._no_card_content = ft.Container(
            width=width,
            height=height,
            bgcolor='#777777',
            border_radius=5,
        )
        self.on_card_return = on_card_return

        def on_double_tap(e):
            if self.card:
                self.card = None

        super().__init__(
            content=self._no_card_content,
            on_double_tap=on_double_tap,
        )

    def _get_card(self):
        return self._card

    def _set_card(self, card):
        if self._card == card:
            return

        if card is None:
            self.on_card_return(self._card)
            self.content = self._no_card_content
        else:
            self.content = CardDisplay(card, CardDisplay.LARGE)

        self._card = card
        self.update()

    card = property(_get_card, _set_card)

class DeckCardArea(ft.GestureDetector):
    def __init__(self, *, card, try_set_card):
        self.card = card
        self._is_in_use = False
        self._in_use_content = ft.Container(
            width=40,
            height=64,
            bgcolor='#777777',
            border_radius=5,
        )

        def on_double_tap(e):
            if not self.is_in_use:
                self.is_in_use = try_set_card(self.card)

        super().__init__(
            content=CardDisplay(self.card),
            on_double_tap=on_double_tap,
        )

    def _get_is_in_use(self):
        return self._is_in_use

    def _set_is_in_use(self, is_in_use):
        if self._is_in_use == is_in_use:
            return

        self._is_in_use = is_in_use
        if is_in_use:
            self.content = self._in_use_content
        else:
            self.content = CardDisplay(self.card)

        self.update()

    is_in_use = property(_get_is_in_use, _set_is_in_use)


class BoardEditor2(ft.ExpansionTile):
    def __init__(self):
        def on_card_return(card):
            self.card_to_control_mapping[card].is_in_use = False

        self.board_card_areas = [
            BoardCardArea(on_card_return=on_card_return),
            BoardCardArea(on_card_return=on_card_return),
            BoardCardArea(on_card_return=on_card_return),
            BoardCardArea(on_card_return=on_card_return),
            BoardCardArea(on_card_return=on_card_return),
        ]

        self.board_controls = [
            self.board_card_areas[0],
            self.board_card_areas[1],
            self.board_card_areas[2],
            ft.VerticalDivider(width=16),
            self.board_card_areas[3],
            ft.VerticalDivider(width=16),
            self.board_card_areas[4],
        ]

        def try_set_card(card):
            for bca in self.board_card_areas:
                if not bca.card:
                    bca.card = card
                    return True

            return False

        self.deck_controls = []
        self.card_to_control_mapping = {}

        for suit in SUITS:
            row = []

            for rank in RANKS:
                card = rank + suit
                control = DeckCardArea(
                    card=rank + suit,
                    try_set_card=try_set_card,
                )
                row.append(control)
                self.card_to_control_mapping[card] = control

            self.deck_controls.append(ft.Row(controls=row))

        super().__init__(
            title=ft.Row(controls=self.board_controls),
            affinity=ft.TileAffinity.LEADING,
            controls=[ft.Column(controls=self.deck_controls)],
            controls_padding=ft.padding.all(18),
            initially_expanded=False,
        )

    def _get_cards(self):
        return [ bca.card for bca in self.board_card_areas ]

    cards = property(_get_cards)

class RangeButton(ft.Container):
    def __init__(self, starting_hand, *, is_selected=False, on_click=None, on_long_press=None):
        self._is_selected = is_selected
        self.starting_hand = starting_hand
        self._on_click = on_click
        self._on_long_press = on_long_press

        def on_click(e):
            self.is_selected = not self.is_selected
            if self._on_click:
                self._on_click(e)

        def on_long_press(e):
            if self._on_long_press:
                self._on_long_press(e)


        self.text = ft.Text(
            starting_hand,
            color=ft.colors.ON_SECONDARY_CONTAINER,
        )

        super().__init__(
            content=self.text,
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
            self.text.color = ft.colors.ON_PRIMARY_CONTAINER
            self.border = ft.border.all(1, ft.colors.ON_PRIMARY_CONTAINER)

        else:
            self.bgcolor = ft.colors.SECONDARY_CONTAINER
            self.text.color = ft.colors.ON_SECONDARY_CONTAINER
            self.border = ft.border.all(1, ft.colors.ON_SECONDARY_CONTAINER)

        self.update()

    is_selected = property(_get_is_selected, _set_is_selected)

class RangeEditor(ft.Stack):
    def __init__(self, *, name, pf_range=None):
        self.name = name

        if pf_range is None:
            self.range = {}
        else:
            self.range = pf_range

        def toggle_starting_hand(starting_hand):
            def handler(e):
                for combo in starting_hand_to_combos(starting_hand):
                    self.range[combo] = not self.range[combo]

            return handler

        def edit_combos(starting_hand):
            def handler(e):
                self.controls.append(
                    ft.Container(
                        content=ft.Text('Long press {}'.format(starting_hand)),
                        alignment=ft.alignment.center,
                        width=100,
                        height=100,
                        bgcolor=ft.colors.PRIMARY,
                        border=ft.border.all(1, ft.colors.ON_PRIMARY),
                        border_radius=ft.border_radius.all(5),
                    )
                )
                self.update()
                print('Long pressed {}'.format(starting_hand))

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

                for combo in starting_hand_to_combos(starting_hand):
                    self.range[combo] = False

                row_controls.append(RangeButton(
                    starting_hand,
                    on_click=toggle_starting_hand(starting_hand),
                    on_long_press=edit_combos(starting_hand),
                ))

            column_controls.append(ft.Row(
                controls=row_controls,
                spacing=4,
            ))

        super().__init__(
            controls=[
                ft.Column(
                    controls=column_controls,
                    spacing=4,
                ),
            ],
            alignment=ft.alignment.center,
        )

class EquityForm(ft.Column):
    def __init__(self, *, board_editor, range_editors):
        self.board_editor = board_editor
        self.range_editors = range_editors

        self.error_message = ft.Text(color='#dd0000')
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text('Range')),
                ft.DataColumn(ft.Text('Equity')),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text('--')),
                        ft.DataCell(ft.Text('--%')),
                    ],
                ),
            ],
        )

        def run_equity_calc(e):
            board = frozenset(
                card
                for card in self.board_editor.cards
                if card and card.strip()
            )

            if len(board) not in {0,3,4,5}:
                self.error_message.value = 'Invalid number of board cards'
                self.update()
                return

            ranges = [re.range for re in self.range_editors]

            if any(is_range_empty(r) for r in ranges):
                self.error_message.value = 'One or more ranges contain(s) no combos'
                self.update()
                return

            self.error_message.value = ''
            self.controls = [
                ft.ProgressRing(width=50, height=50, stroke_width=2)
            ]
            self.update()

            equities = equity.get_equity(board, ranges)

            self.data_table.rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(range_editor.name)),
                    ft.DataCell(ft.Text(fraction_to_percent(eq))),
                ])
                for range_editor, eq in zip(self.range_editors, equities)
            ]

            self.controls = self.cached_controls
            self.update()

        self.cached_controls = [
            ft.FilledButton(
                text='Run Equity Calc',
                style=ft.ButtonStyle(
                    shape=ft.ContinuousRectangleBorder(radius=15),
                    side=ft.BorderSide(width=0, color='transparent'),
                ),
                on_click=run_equity_calc,
            ),
            self.error_message,
            self.data_table,
        ]

        super().__init__(
            spacing=8,
            width=200,
            controls=self.cached_controls,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

def main(page: ft.Page):
    board_editor = BoardEditor2()
    hero_range_editor = RangeEditor(name='Hero')
    villain_range_editor = RangeEditor(name='Villain')
    equity_form = EquityForm(
        board_editor=board_editor,
        range_editors=[
            hero_range_editor,
            villain_range_editor,
        ],
    )
    page.add(board_editor)
    page.add(ft.Row(
        controls=[
            hero_range_editor,
            villain_range_editor,
            equity_form,
        ],
        spacing=10,
    ))

    page.window.top = 0
    page.window.left = 0
    page.window.maximized = True
    page.update()

ft.app(target=main)
