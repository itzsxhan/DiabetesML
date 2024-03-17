import flet as ft
from flet import TextField, Checkbox, ElevatedButton,Row, Text, Column
from flet_core.control_event import ControlEvent
from flet_core.types import WEB_BROWSER


def main(page= ft.Page) -> None:
    page.title = 'Medicure'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 700
    page.window_height = 700
    page.window_resizable =True


    username: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=350)
    password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=350, password=True)
    signUp: Checkbox = Checkbox(label= "I agree to stuff", value=False)
    submitButton: ElevatedButton = ElevatedButton(text= 'Sign up', width= 200, disabled=True)


    def validate(e: ControlEvent) -> None:
        if all([username.value, password.value, signUp.value]):
            submitButton.disabled = False
        else:
            submitButton.disabled = True
        page.update()

    def submit(e: ControlEvent) -> None:
        print('Username', username.value)
        print('Password', password.value)

        page.clean()

        page.add(Row
                 (controls=[Text(value=f'Welcome: {username.value}', size=20)],
                     alignment=ft.MainAxisAlignment.CENTER
                  )
                )



    signUp.on_change = validate
    username.on_change = validate
    password.on_change = validate
    submitButton.on_click = submit

    page.add(Row(controls=[Column([username,password,signUp,submitButton])
                           ],
                 alignment=ft.MainAxisAlignment.CENTER))

if __name__ == '__main__':
    ft.app(target=main, view= WEB_BROWSER)

