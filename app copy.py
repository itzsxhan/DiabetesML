import flet as ft
from flet import *
from flet import TextField, Checkbox, ElevatedButton, Row, Text, Column
from flet_core import Page, Container
from flet_core.control_event import ControlEvent
from flet_core.types import WEB_BROWSER
from checkBox import CustomCheckBox


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
        height= 430,
        scroll= 'auto',
        #controls=[Container(height= 100, width= 700, bgcolor= mediumBlue, border_radius= 45)]
    )
    for i in range(10):
        tasks.controls.append(
            Container(height=98,
                      width=700,
                      bgcolor=mediumBlue,
                      border_radius=45, padding= padding.only( left= 20, top= 25),
                      content=CustomCheckBox(blue, size= 50, stroke_width= 7),
                      )
                )
    def shrink(e):
        page_2.controls[0].width = 470
        page_2.controls[0].scale = transform.Scale(0.8,alignment= alignment.center_right)
        page_2.update()

    def restore(e):
        page_2.controls[0].width = 650
        page_2.controls[0].scale = transform.Scale(1,alignment= alignment.center_right)
        page_2.update()


    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )

    categories = Row()

    contact = FloatingActionButton(width= 190, bgcolor= blue, height= 130, text="Contact a Doctor", on_click= lambda _: page.go('/create_task'))

    meal_plan = FloatingActionButton(width= 190, bgcolor= blue, height= 130, text="Meal Plan", on_click= lambda _: page.go('/create_task'))

    selfDiagnosis = FloatingActionButton(width=190, height=130, bgcolor= blue, text="Self Diabetes Check",on_click=lambda _: page.go('/create_task'))

    categorical_List = [contact,meal_plan,selfDiagnosis]

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
                        content=Icon(icons.MENU, size= 35)),
                    Row(controls=[
                        Icon(icons.SEARCH,size=35),
                        Icon(icons.NOTIFICATIONS_OUTLINED,size=35)
                    ])
                ]),
                Text(value='What\'s up !!!', font_family='PD', weight=ft.FontWeight.BOLD,
                     color=blue, size= 25),
                Text(
                    value='CATEGORIES', font_family='PD', weight=ft.FontWeight.BOLD, color= blue
                ),
                Container(
                    padding= padding.only(top=10, bottom=20),
                    content= categories
                ),
                Container(height=20),
                Text("FITNESS GOALS",font_family='PD', weight=ft.FontWeight.BOLD, color= blue),
                Stack(
                    controls=[
                        tasks,
                        FloatingActionButton( bottom= 2, right=20,
                            icon = icons.ADD, bgcolor= coral, on_click= lambda _: page.go('/create_task')
                        )
                    ]
                )


            ]
        )
    )

    page.on_route_change = route_change
    page_1 = Container(content=Column( alignment= MainAxisAlignment.SPACE_EVENLY, controls= [Container(content= Text("x"),
                                                                                                       width= 480,
                                                                                                       height= 800,
                                                                                                       bgcolor= mediumBlue,
                                                                                                       border_radius= 35,
                                                                                                       alignment= alignment.center)]))
    page_2 = Row( alignment= 'end',
        controls=[Container(
            width=650,
            height=900,
            bgcolor=lightBlue,
            border_radius=35,
            animate= animation.Animation(600, AnimationCurve.DECELERATE),
            animate_scale= animation.Animation(400, curve='decelerate'),
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
        border_radius=35,
        content=Stack(
            controls=[page_1, page_2])

    )

    create_task_view = Container(
        content= Container( on_click= lambda _: page.go('/'),
            height= 40, width= 40,
            content=Text('x'))
    )

    pages = {
        '/': View(
            "/",
            [
                container
            ],

        ),
        '/create_task':View(
            "/create_task",
            [
                create_task_view
            ]
        )
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
