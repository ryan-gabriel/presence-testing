import flet as ft
from datetime import datetime
from flet_timer.flet_timer import Timer
from supabase import create_client, Client
import os
import csv


avatar_img = ft.Image(
    src="https://drive.google.com/uc?id=1J1OTH3KO9pEjp7hOIReT4-IF5ReXiLiQ", width=60, height=60, fit=ft.ImageFit.CONTAIN, border_radius=60 / 2
)


sekarang = datetime.now()
hari = sekarang.strftime("%A")
tanggal = sekarang.day
bulan = sekarang.strftime("%B")
tahun = sekarang.year
jam = sekarang.strftime("%H")
menit = sekarang.strftime("%M")
ref_opt = ft.Ref[ft.Dropdown]()
ref_keterangan = ft.Ref[ft.TextField]()
url: str = "https://gkqvcndiyyrprpndgedg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrcXZjbmRpeXlycHJwbmRnZWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDIxMDM0NjYsImV4cCI6MjAxNzY3OTQ2Nn0.FDdQRXgW-_rMqIP4g5ttRwbynr-APBIlg_oFuVoOyww"
supabase: Client = create_client(url, key)


def get_user():
    user_id = supabase.auth.get_user().user.identities[0].user_id
    return (
        supabase.table("Mahasiswa")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
        .data
    )


def get_latest_pertemuan():
    return (
        supabase.table("pertemuan")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )


def tambah_absen(file_kehadiran, data):
    header = ["Nama", "NIM", "Keterangan", "Alasan", "Tanggal", "Jam"]

    # Mengecek apakah file sudah ada
    file_exist = os.path.exists(f"data/{file_kehadiran}.csv")

    # Menulis ke file CSV
    with open(f"data/{file_kehadiran}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        # Menulis header hanya jika file baru dibuat
        if not file_exist:
            writer.writerow(header)

        # Menulis data ke dalam file CSV
        writer.writerow(data)

    return True


def data_absen(user):
    current_time = datetime.now()
    jam = current_time.strftime("%H")
    menit = current_time.strftime("%M")
    tanggal = current_time.day
    bulan = current_time.strftime("%B")
    tahun = current_time.year

    if ref_opt.current.value == "Izin" or ref_opt.current.value == "Sakit":
        return [
            user["Nama"],
            user["Nim"],
            ref_opt.current.value,
            ref_keterangan.current.value,
            f"{tanggal}-{bulan}-{tahun}",
            f"{jam}:{menit}",
        ]

    return [
        user["Nama"],
        user["Nim"],
        "Hadir",
        "-",
        f"{tanggal}-{bulan}-{tahun}",
        f"{jam}:{menit}",
    ]


def is_absen(file_kehadiran, nim):
    try:
        with open(f"data/{file_kehadiran}.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["NIM"]) == int(nim):
                    return True
        return False
    except:
        return False


def _view_(page: ft.Page):
    def handle_absen(e):
        user = get_user()
        pertemuan = get_latest_pertemuan()
        file_kehadiran = pertemuan.data[0]["file_kehadiran"]

        data = data_absen(user)

        if not is_absen(file_kehadiran, user["Nim"]):
            if tambah_absen(file_kehadiran, data):
                page.snack_bar = ft.SnackBar(
                    ft.Text(
                        "Absen berhasil",
                        color=ft.colors.WHITE,
                    ),
                    bgcolor=ft.colors.GREEN,
                    duration=2000,
                )
                page.snack_bar.open = True

                page.update()
                return
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Anda sudah absen",
                    color=ft.colors.WHITE,
                ),
                bgcolor=ft.colors.RED,
                duration=2000,
            )
            page.snack_bar.open = True

            page.update()
            return

    def upload_files(e):
        upload_list = []
        # if file_picker.result != None and file_picker.result.files != None:
        #     for f in file_picker.result.files:
        #         upload_list.append(
        #             FilePickerUploadFile(
        #                 f.name,
        #                 upload_url=page.get_upload_url(f.name, 600),
        #             )
        #         )
        #     file_picker.upload(upload_list)

class ClockTimmer(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.timenow = ft.Text(size=30,weight=ft.FontWeight.BOLD,color="white")
        self.timer = Timer(name='youtime1',
                            interval_s=1,
                            callback=self.myrefresh)

    def myrefresh(self):
        self.timenow.value = datetime.now().strftime("%H:%M")
        self.update()

    def build(self):
        return ft.Container(
            content=ft.Column([
                self.timenow,
                self.timer,
            ])
        )      


def _view_(page:ft.Page):

    opt = ft.Ref[ft.Dropdown]() # option dropdown izin
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        print(e.files)

        # selected_files.value = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else None
        # )
        # selected_files.update()

    def dropdown_changed(e):
        if ref_opt.current.value == "Izin" or ref_opt.current.value == "Sakit":
            fileDispen.visible = False
            box_area.visible = True
            t.value = "Keterangan"
            page.update()
        elif ref_opt.current.value == "Dispen":
            box_area.visible = False
            fileDispen.visible = True
            t.value = "File"
            page.update()

    # option dropdown izin

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()
    page.overlay.append(pick_files_dialog)

    t = ft.Text(color="black")

    konfirmasi_btn = ft.ElevatedButton("Konfirmasi", on_click=handle_absen)

    box_area = ft.TextField(
        ref=ref_keterangan,
        height=100,
        visible=False,
        width=page.width,
        min_lines=3,
        max_lines=3,
        max_length=50,
    )

    fileDispen = ft.Row(
        [
            ft.ElevatedButton(
                "Upload",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
            ),
            selected_files,
        ],
        visible=False,

    def konfirmasi_izin(e):
        pass

    konfirmasi_btn = ft.ElevatedButton("Konfirmasi",on_click=konfirmasi_izin)
    box_area = ft.TextField(
      height=100,
      visible=False,
      width=page.width,
      min_lines=3,
      max_lines=3,
      max_length=50
    )
    fileDispen = ft.Row([
        ft.ElevatedButton(
                        "Upload",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True
                        ),
                    ),selected_files
    ],visible=False)
    
    status_dropdown=ft.Text(color="black")

    absent_tab = ft.Tabs(
        selected_index=0,
        animation_duration=100,
        tabs=[
            ft.Tab(
                tab_content=ft.Text("Hadir", color="blue"),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Absensi sekarang: ", color="#00BAE9"),
                            ],
                            alignment="center",

    def dropdown_changed(e):
        if opt.current.value == "Izin" or opt.current.value == "Sakit":
            fileDispen.visible = False
            box_area.visible = True
            status_dropdown.value = "Keterangan"
            page.update()
        elif opt.current.value == "Dispen":
            box_area.visible = False
            fileDispen.visible = True
            status_dropdown.value = "File"
            page.update()

  
    def totalAttendance(count):
        panel = []
        
        for i in range(count):
            tanggal_sekarang = datetime.now().date()
            tanggal_absen = datetime.strptime("2024-1-1", "%Y-%m-%d").date() # tanggal dibuatnya absen (ambil dari supabase), tipe datanya harus date, ini contoh aja
            absent_status = 'belum absen' # status absen kalau izin, dispen, belum absen atau sudah absen
            batas_absen = datetime.strptime("20:30:00", "%H:%M:%S").time() # batas absen
            
            if absent_status == 'belum absen' and (datetime.now().time() >= batas_absen or datetime.now().date() > tanggal_absen):
                absent_status = 'alpa' #ini diubah lagi status absennya di supabase

            if tanggal_sekarang == tanggal_absen:
                
                matkul = "Rekayasa Perangkat Lunak" # matkul absen dalam bentuk string
                jam_absen = "12:05"  # jam absen user
                jam_matkul = "02:30" # lama jam matkul


                absent_tab = ft.Tabs(
                    selected_index=0,
                    animation_duration=100,
                    tabs=[
                        ft.Tab(
                            tab_content=ft.Text("Hadir",color="blue"),
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Absensi sekarang: ",color="#00BAE9"),
                                ],alignment="center"),
                                ft.Row([
                                    ft.Text(matkul,color="#00BAE9"),
                                ],alignment = "center"),
                                ft.Row([
                                    ft.Text("Batas Absen",color="#00BAE9"),
                                ],alignment = "center"),
                                ft.Row([
                                    ft.Text("12:15 ",color="#00BAE9"), #place holder
                                ],alignment = "center",),
                                ft.Row([
                                    ft.ElevatedButton(
                                        content= ft.Icon(name=ft.icons.FINGERPRINT,color="white",size=125),
                                        bgcolor="#00BAE9",
                                        style=ft.ButtonStyle(
                                            padding=0
                                        )
                                    ),
                                ],alignment="center"),
                                ft.Row([
                                    ft.Text("Absen kehadiranmu",color="#00BAE9")
                                ],alignment="center")
                            ],width=1000)

                        ),
                        ft.Tab(
                            tab_content=ft.Text("Izin",color="blue"),
                            content=ft.Column([
                                ft.Text("Keterangan: ",weight=ft.FontWeight.BOLD,color="black"),
                                ft.Dropdown(
                                    ref = opt,
                                    width = page.width,
                                    options=[
                                        ft.dropdown.Option("Dispen"),
                                        ft.dropdown.Option("Sakit"),
                                        ft.dropdown.Option("Izin"),
                                    ],
                                    color="#00BAE9",
                                    focused_bgcolor="94D3E4",
                                    hint_text="Pilih Keterangan Anda",
                                    border_radius=10,
                                    on_change=dropdown_changed
                                ),
                                status_dropdown,
                                box_area,
                                fileDispen,
                                ft.Stack([
                                    ft.Container(
                                        content= konfirmasi_btn, #belum ditambahin fungsionalitas
                                        bottom=10,
                                        right=10
                                    )
                                ],
                                expand=True,
                                width=page.width,
                                )
                            ]),
                        ),
                    ],
                    width=1000,
                ),
            ),
            ft.Tab(
                tab_content=ft.Text("Izin", color="blue"),
                content=ft.Column(
                    [
                        ft.Text(
                            "Keterangan: ", weight=ft.FontWeight.BOLD, color="black"
                        ),
                        ft.Dropdown(
                            ref=ref_opt,
                            width=page.width,
                            options=[
                                ft.dropdown.Option("Dispen"),
                                ft.dropdown.Option("Sakit"),
                                ft.dropdown.Option("Izin"),
                            ],
                            color="#00BAE9",
                            focused_bgcolor="94D3E4",
                            hint_text="Pilih Keterangan Anda",
                            border_radius=10,
                            on_change=dropdown_changed,
                        ),
                        t,
                        box_area,
                        fileDispen,
                        ft.Stack(
                            [
                    scrollable=True,
                    expand=True,
                    width=page.width,
                    divider_color=ft.colors.TRANSPARENT,
                )


                izin_tab =ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row([
                                                ft.Text(absent_status.capitalize(),size=20,color="#00BAE9",weight=ft.FontWeight.BOLD)
                                            ],alignment="center"),
                                            ft.Column([
                                                ft.Row([
                                                    ft.Text("Absensi:",color="#00BAE9")
                                                ],alignment="center"),
                                                ft.Row([
                                                    ft.Text(matkul,color="#00BAE9")
                                                ],alignment="center"),
                                                ft.Row([
                                                    ft.Text("Batas Absen:",color="#00BAE9")
                                                ],alignment="center"),
                                                ft.Row([
                                                    ft.Text(str(batas_absen),color="#00BAE9")
                                                ],alignment="center"),
                                            ],spacing=5),
                                            ft.Row([
                                                ft.ElevatedButton(
                                                    content= ft.Icon(name=ft.icons.FINGERPRINT,color="white",size=125),
                                                    style=ft.ButtonStyle(
                                                        padding=0
                                                    ),
                                                    disabled=True
                                                ),
                                            ],alignment="center"),
                                            ft.Row([
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                ft.Icon(name=ft.icons.ACCOUNT_CIRCLE,color="#00BAE9"),
                                                                ft.Text(absent_status.capitalize(),size=12),
                                                                ft.Text(jam_absen,size=12), #place holder buat waktu absen
                                                            ],
                                                            spacing=0
                                                        ),
                                                        border=ft.border.only(right=ft.border.BorderSide(1,"#00BAE9"),top=ft.border.BorderSide(2,"#00BAE9")),
                                                        padding=ft.padding.only(left=55,right=70,top=10,bottom=10)
                                                    ),
                                                    ft.Container(
                                                        content=ft.Column(
                                                            [
                                                                ft.Icon(name=ft.icons.ACCESS_TIME_SHARP,color="#00BAE9"),
                                                                ft.Text("Waktu",size=12),
                                                                ft.Text(jam_matkul,size=12), #place holder buat waktu absen
                                                            ],
                                                            spacing=0
                                                        ),
                                                        border=ft.border.only(left=ft.border.BorderSide(1,"#00BAE9"),top=ft.border.BorderSide(2,"#00BAE9")),
                                                        padding=ft.padding.symmetric(horizontal=70,vertical=10)
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                                height=100,
                                            )
                                        ],
                                        width=page.width,
                                        spacing=20
                                    ),
                                    height=400,
                                    width=page.width
                                )
                            ]),
                            width=page.width,
                            bgcolor="white",
                            border_radius=25,
                            padding=10,
                            height=400
                        )



                if absent_status == 'belum absen':
                    panel.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Pilih Kehadiran",weight=ft.FontWeight.BOLD,size=20,color="black",text_align="center")
                                ],alignment="center"),
                                ft.Container(
                                    content=absent_tab,
                                    height=400,
                                    width=page.width
                                )
                            ],),
                            width=700,
                            bgcolor="white",
                            border_radius=25,
                            padding=10,
                            height=450
                        )
                    )
                elif absent_status == 'izin' or absent_status == 'sakit' or absent_status=='dispen' or absent_status=='alpa':
                    panel.append(izin_tab)
            else:
                pass

        return panel


    homepage = ft.Stack(
                [
                    ft.Container(
                        content=ft.Text(f"{hari}, {tanggal} {bulan} {tahun}",text_align="center",size=16,color="white"),
                        right=50,
                        left=50,
                        top=70
                    ),
                    ft.Container(
                        content=ft.Row(
                                [
                                    ClockTimmer()
                                ],alignment="center"),
                        width= page.width,
                        right=50,
                        left=50,
                        top=105
                    ),
                    ft.Container(
                        content=ft.Column(totalAttendance(3),alignment=ft.MainAxisAlignment.CENTER,scroll=ft.ScrollMode.ALWAYS,spacing=5),
                        width=page.width,
                        top=160,
                        left = 20,
                        right = 20,
                        height = 700,
                        bottom=60
                    )
                ],
                expand=True,
                width=page.width,
                right=50,
                left=50,
                top=105,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Pilih Kehadiran",
                                    weight=ft.FontWeight.BOLD,
                                    size=20,
                                    color="black",
                                    text_align="center",
                                )
                            ],
                            alignment="center",
                        ),
                        ft.Container(content=absent_tab, height=400, width=page.width),
                    ],
                ),
                width=700,
                left=50,
                right=50,
                top=200,
                bgcolor="white",
                border_radius=25,
                padding=10,
            ),
        ],
        expand=True,
        width=page.width,
    )

    return homepage
