import flet as ft

def _view_ (page:ft.Page):


    profile_img = ft.Image(
        src=f"testing.jpg",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
        border_radius= 150/2
    )

    profile_name = "Syahdan Alfiansyah"
    profile_nim = 2305929
    
    
    help_menu = ft.Column(
        [
            ft.Row(
                [
                    ft.Icon(name=ft.icons.QUESTION_MARK,size=100,color="#58C9E6")
                ],
                alignment="center"
            ),
            ft.Row(
                [
                    ft.Text("Memiliki pertanyaan terkait aplikasi ini",size=20,color="#58C9E6")
                ],
                alignment="center"
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Kirim Pertanyaan",
                        color="white",
                        bgcolor="#58C9E6",
                        style=ft.ButtonStyle(
                            padding=5,
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5)
                            }
                        )
                    )
                ],
                alignment="center"
            )
        ],
        spacing=15
    )

    help_menus = ft.Container(
            content=help_menu,
            top=330,
            left=15,
            right=15,
            bottom=15,
            width=page.width,
            expand=True,
            bgcolor="white",
            border_radius=20,
            padding=15
        )

    help_page = ft.Stack(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Profile",size=20,color="white",weight=ft.FontWeight.BOLD)
                                ],alignment="center"
                            ),
                            ft.Row(
                                [
                                    profile_img
                                ], alignment="center"
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(profile_name,size=25,weight=ft.FontWeight.BOLD,color="white")
                                        ],alignment="center"
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(profile_nim,size=23,color="white")
                                        ],alignment="center"
                                    )
                                ],
                                spacing=5
                            )
                        ],
                        spacing=8
                    ),
                    top=40,
                    width=page.width,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                            content=ft.Icon(name = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,color="white",size=30),
                            on_click= lambda e:e.page.go('/app'),
                            bgcolor = "#58C9E6",
                            width=45,
                            height=45,
                            style = ft.ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=15),
                                },
                                padding=0
                            ),
                        ),
                    top=15,
                    left=15,
                ),
                help_menus
            ],
            expand=True,
            width=page.width,
        )
    

    return ft.View(
        '/help',
        controls=[
            ft.Container(
                content=help_page,
                expand = True,
                width= page.width,
                gradient=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=['#00A7D2', "#94D3E4"],
                        ),
                margin=-10
                )
            ]
    ) 