import flet as ft
from flet import *
from flet import TextField, Checkbox, ElevatedButton, Row, Text, Column
from flet_core import Page, Container
from flet_core.control_event import ControlEvent
from flet_core.types import WEB_BROWSER
from checkBox import CustomCheckBox

from chatBot import ChatMessage, Message

from chatBot import *


def main(page=ft.Page) -> None:
    blue = '#2d3140'
    lightBlue = '#e9fafc'
    mediumBlue = "#a7bfd7"
    coral = '#d17255'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=350)
    password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=350, password=True)
    signUp: Checkbox = Checkbox(label="I agree to stuff", value=False)
    submitButton: ElevatedButton = ElevatedButton(text='Sign up', width=200, disabled=True)

    page.title = 'Medicure'
    page.fonts = {
        'PD': 'Playfair Display'
    }
    page.add(Text("MEDI", size=70, font_family='PD', weight=ft.FontWeight.BOLD, color='yellow',

                  spans=[ft.TextSpan("CURE", ft.TextStyle(font_family='Arial', size=70, weight=ft.FontWeight.BOLD))],
                  text_align=ft.TextAlign.CENTER))

    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 725
    page.window_height = 1000
    page.window_resizable = True

    def validate(e: ControlEvent) -> None:
        if all([username.value, password.value, signUp.value]):
            submitButton.disabled = False
        else:
            submitButton.disabled = True
        page.update()

    signUp.on_change = validate
    username.on_change = validate
    password.on_change = validate

    tasks = Column(
        height=430,
        scroll='auto',
        # controls=[Container(height= 100, width= 700, bgcolor= mediumBlue, border_radius= 45)]
    )
    for i in range(10):
        tasks.controls.append(
            Container(height=98,
                      width=700,
                      bgcolor=mediumBlue,
                      border_radius=45, padding=padding.only(left=20, top=25),
                      content=CustomCheckBox(blue, size=50, stroke_width=7),
                      )
        )

    def shrink(e):
        page_2.controls[0].width = 450
        page_2.controls[0].scale = transform.Scale(0.8, alignment=alignment.center_right)
        page_2.controls[0].border_radius = border_radius.only(top_left=35, top_right=0, bottom_left=35, bottom_right=0)
        page_2.update()

    def restore(e):
        page_2.controls[0].width = 650
        page_2.controls[0].scale = transform.Scale(1, alignment=alignment.center_right)
        page_2.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )

    def chat(chatPage: ft.Page):
        chatPage.horizontal_alignment = "stretch"
        chatPage.title = "Flet Chat"

        def join_chat_click(e):
            if not join_user_name.value:
                join_user_name.error_text = "Name cannot be blank!"
                join_user_name.update()
            else:
                chatPage.session.set("user_name", join_user_name.value)
                chatPage.dialog.open = False
                new_message.prefix = ft.Text(f"{join_user_name.value}: ")
                chatPage.pubsub.send_all(
                    Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.",
                            message_type="login_message"))
                chatPage.update()

        def send_message_click(e):
            if new_message.value != "":
                chatPage.pubsub.send_all(
                    Message(chatPage.session.get("user_name"), new_message.value, message_type="chat_message"))
                new_message.value = ""
                new_message.focus()
                chatPage.update()

        def on_message(message: Message):
            if message.message_type == "chat_message":
                m = ChatMessage(message)
            elif message.message_type == "login_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            chat.controls.append(m)
            chatPage.update()

        chatPage.pubsub.subscribe(on_message)

        # A dialog asking for a user display name
        join_user_name = ft.TextField(
            label="Enter your name to join the chat",
            autofocus=True,
            on_submit=join_chat_click,
        )
        chatPage.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([join_user_name], width=300, height=70, tight=True),
            actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
            actions_alignment="end",
        )

        # Chat messages
        chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        # A new message entry form
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=send_message_click,
        )

        # Add everything to the page
        chatPage.add(
            ft.Container(
                content=chat,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    new_message,
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=send_message_click,
                    ),
                ]
            ),
        )

    circle = Stack(
        controls=[
            Container(
                width=100,
                height=100,
                border_radius=50,
                bgcolor='white12'
            ),
            Container(
                gradient=SweepGradient(
                    center=alignment.center,
                    start_angle=0.0,
                    end_angle=3,
                    stops=[0.5, 0.5],
                    colors=['#00000000', coral],
                ),
                width=100,
                height=100,
                border_radius=50,
                content=Row(alignment='center',
                            controls=[
                                Container(padding=padding.all(5),
                                          bgcolor=blue,
                                          width=90, height=90,
                                          border_radius=50,
                                          content=Container(bgcolor=lightBlue,
                                                            height=80, width=80,
                                                            border_radius=40,
                                                            content=CircleAvatar(opacity=0.8,
                                                                                 foreground_image_url="https://api.wallpapers.ai/static/downloads/4fb6a17634b74186850e9e3bf9fae995/upscaled/000000_98188236_kdpmpp2m15_PS7.5_Obito_uchiha_sad_sitting_on_a_cliff._digital_art_concept_art_[upscaled].jpg"
                                                                                 )
                                                            )
                                          )
                            ],
                            ),
            ),

        ]
    )

    categories = Row()

    contact = FloatingActionButton(width=190, bgcolor=blue, height=130, text="Get Help",
                                   on_click=lambda _: page.go('/message'))

    meal_plan = FloatingActionButton(width=190, bgcolor=blue, height=130, text="Meal Plan",
                                     on_click=lambda _: page.go('/create_task'))

    selfDiagnosis = FloatingActionButton(width=190, height=130, bgcolor=blue, text="Self Diabetes Check",
                                         on_click=lambda _: page.go('/create_task'))

    categorical_List = [contact, meal_plan, selfDiagnosis]

    for category in categorical_List:
        categories.controls.append(
            category
        )

    first_page_contents = Container(
        content=Column(
            controls=[
                Row(alignment='spaceBetween', controls=[
                    Container(
                        on_click=lambda e: shrink(e),
                        content=Icon(icons.MENU, size=35)),
                    Row(controls=[
                        Icon(icons.SEARCH, size=35),
                        Icon(icons.NOTIFICATIONS_OUTLINED, size=35)
                    ])
                ]),
                Text(value='What\'s up !!!', font_family='PD', weight=ft.FontWeight.BOLD,
                     color=blue, size=25),
                Text(
                    value='CATEGORIES', font_family='PD', weight=ft.FontWeight.BOLD, color=blue
                ),
                Container(
                    padding=padding.only(top=10, bottom=20),
                    content=categories
                ),
                Container(height=20),
                Text("FITNESS GOALS", font_family='PD', weight=ft.FontWeight.BOLD, color=blue),
                Stack(
                    controls=[
                        tasks,
                        FloatingActionButton(bottom=2, right=20,
                                             icon=icons.ADD, bgcolor=coral, on_click=lambda _: page.go('/create_task')
                                             )
                    ]
                )

            ]
        )
    )

    vitals = Column(height=350, scroll='auto')

    features = ['HighBP', 'High Cholesterol', 'Stroke', ' Risk of Heart Disease or Attack',
                'Physical Activity', 'Fruit Consumption', 'Calorie Intake', 'Heavy Alcohol Consumption']

    for j in features:
        vitals.controls.append(
            Container(
                border_radius=20,
                bgcolor=blue,
                width=270,
                height=110,
                padding=15,
                content=Column(
                    controls=[
                        Text('vital'),
                        Text(j),
                        Container(
                            width=160,
                            height=5,
                            bgcolor= coral,
                            border_radius=20,
                            padding=padding.only(right=i * 30),
                            content=Container(
                                bgcolor=coral,
                            ),

                        )
                    ]

                )
            )
        )

    page.on_route_change = route_change
    page_1 = Container(content=Column(alignment=MainAxisAlignment.SPACE_EVENLY, controls=
    [Row(controls=[Container(content=Column(alignment=MainAxisAlignment.SPACE_EVENLY, controls=[
        Container(content=Column(controls=[Icon(icons.ARROW_BACK_IOS_NEW, color=blue),
                                           Row(controls=[Text(" Sehan", size=52, weight='bold', color=blue),
                                                         Container(height=15), circle]),
                                           Text('  Vitals:', size=32, weight='bold', color=blue), vitals])
                  , width=435, height=570, alignment=alignment.top_left)]),
                             padding=padding.only(bottom=20, right=20),
                             on_click=lambda e: restore(e),
                             width=480,
                             height=800,
                             bgcolor=mediumBlue,
                             border_radius=25,
                             alignment=alignment.top_left)]
         )]
                                      ))
    page_2 = Row(alignment='end',
                 controls=[Container(
                     width=650,
                     height=900,
                     bgcolor=lightBlue,
                     border_radius=30,
                     animate=animation.Animation(600, AnimationCurve.DECELERATE),
                     animate_scale=animation.Animation(400, curve='decelerate'),
                     padding=padding.only(
                         top=50, left=20,
                         right=20, bottom=5
                     ),
                     content=Column(
                         controls=[first_page_contents]
                     )
                 )]
                 )

    container = Container(
        width=650,
        height=900,
        bgcolor=blue,
        border_radius=30,
        content=Stack(
            controls=[page_1, page_2])

    )

    create_task_view = Container(
        content=Container(on_click=lambda _: page.go('/'),
                          height=40, width=40,
                          content=Icon(icons.FULLSCREEN_EXIT_SHARP))
    )

    pages = {
        '/': View(
            "/",
            [
                container
            ],

        ),
        '/create_task': View(
            "/create_task",
            [
                create_task_view
            ]
        ),
        '/message': View('/message', [chat(page)])

    }

    def submit(e: ControlEvent) -> None:
        print('Username', username.value)
        print('Password', password.value)

        page.clean()

        page.add(container)

    def firstPage(page: Page) -> None:
        container = Container(
            width=300
        )

    submitButton.on_click = submit

    page.add(Row(controls=[Column([username, password, signUp, submitButton])
                           ],
                 alignment=ft.MainAxisAlignment.CENTER))


if __name__ == '__main__':
    ft.app(target=main)


