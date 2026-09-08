from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from tkinter import Entry, Checkbutton, BooleanVar, Frame
from PIL import Image, ImageTk, ImageDraw, ImageFont

window = Tk()
window.title("Sproutly")
window.geometry("960x682")
window.configure(bg="#689046")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_and_resize(file_name: str, width: int, height: int) -> ImageTk.PhotoImage:
    img_path = relative_to_assets(file_name)
    raw_img = Image.open(img_path)
    resized_img = raw_img.resize((int(width), int(height)), Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(resized_img)


FONT_DIR = relative_to_assets("fonts/Iosevka_Charon_Mono")

def load_custom_font(font_filename: str, size: int):
    font_path = FONT_DIR / font_filename
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError:
        fallback_path = FONT_DIR / "IosevkaCharonMono-Bold.ttf"
        try:
            return ImageFont.truetype(str(fallback_path), size)
        except OSError:
            return ImageFont.load_default()


FONTS = {
    "regular_s": load_custom_font("IosevkaCharonMono-Regular.ttf", 12),
    "regular_m": load_custom_font("IosevkaCharonMono-Regular.ttf", 16),
    "medium_m": load_custom_font("IosevkaCharonMono-Medium.ttf", 26),
    "bold_s": load_custom_font("IosevkaCharonMono-Bold.ttf", 12),
    "bold_m": load_custom_font("IosevkaCharonMono-Bold.ttf", 16),
    "bold_l": load_custom_font("IosevkaCharonMono-Bold.ttf", 24),
    "italic_s": load_custom_font("IosevkaCharonMono-Italic.ttf", 12),
    "bold_italic_s": load_custom_font("IosevkaCharonMono-BoldItalic.ttf", 12)
}


def make_button_image(text: str, width: int = 140, height: int = 35, font_style: str = "bold_l") -> ImageTk.PhotoImage:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],
        radius=10,
        fill="#EFF5E6",
        outline="#4A6125",
        width=1
    )

    draw.text(
        (width / 2, height / 2),
        text,
        fill="#243D0A",
        font=FONTS.get(font_style, FONTS["bold_l"]),
        anchor="mm"
    )
    return ImageTk.PhotoImage(img)


def make_text_image(text: str, fill="#FFFFFF", size: int = 24, bold: bool = True) -> ImageTk.PhotoImage:
    font_filename = "IosevkaCharonMono-Bold.ttf" if bold else "IosevkaCharonMono-Regular.ttf"
    font = load_custom_font(font_filename, size)


    if not hasattr(font, "getbbox"):
        font = ImageFont.load_default()


    bbox = font.getbbox(text)
    w = (bbox[2] - bbox[0]) + 10
    h = (bbox[3] - bbox[1]) + 10

    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((w / 2, h / 2), text, fill=fill, font=font, anchor="mm")
    return ImageTk.PhotoImage(img)



def make_panel_image(width: int, height: int, radius: int = 20) -> ImageTk.PhotoImage:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],
        radius=radius,
        fill="#B1DE77",
        outline="#D0FF8C",
        width=2
    )
    return ImageTk.PhotoImage(img)


def make_input_box_image(width: int, height: int, radius: int = 10) -> ImageTk.PhotoImage:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)


    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],
        radius=radius,
        fill="#A1D45D",
        outline="#286B00",
        width=1
    )
    return ImageTk.PhotoImage(img)


def make_timer_text_image(text: str, size: int = 64) -> ImageTk.PhotoImage:

    font_path = ASSETS_PATH.parent / "fonts" / "Jersey_20" / "Jersey20-Regular.ttf"

    try:
        font = ImageFont.truetype(str(font_path), size)
    except OSError:

        font_path = relative_to_assets("fonts/Jersey_20/Jersey20-Regular.ttf")
        try:
            font = ImageFont.truetype(str(font_path), size)
        except OSError:
            font = ImageFont.load_default()


    bbox = font.getbbox(text)
    w = (bbox[2] - bbox[0]) + 20
    h = (bbox[3] - bbox[1]) + 20

    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((w / 2, h / 2), text, fill="#EFF5E6", font=font, anchor="mm")
    return ImageTk.PhotoImage(img)


def format_time(seconds: int) -> str:
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

def update_timer_display():
    time_str = format_time(time_left)
    images["txt_cronometro"] = make_timer_text_image(time_str, size=166)
    canvas.itemconfig(cronometro_id, image=images["txt_cronometro"])


canvas = Canvas(
    window,
    bg="#689046",
    height=682,
    width=960,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

images = {}
buttons = {}

timer_running = False
time_left = 0
timer_after_id = None
timer_mode = "livre"
current_tab = "tab_timer"
total_active_seconds = 0
elapsed_seconds = -1


def update_flowers():
    canvas.itemconfigure("flower", state="hidden")

    if elapsed_seconds < 0:
        return

    m25 = 25 * 60
    m50 = 50 * 60
    m60 = 60 * 60
    m85 = 85 * 60
    m110 = 110 * 60
    m120 = 120 * 60
    m145 = 145 * 60
    m170 = 170 * 60

    if elapsed_seconds >= m50:
        canvas.itemconfigure("flower_1.3", state="normal")
    elif elapsed_seconds >= m25:
        canvas.itemconfigure("flower_1.2", state="normal")
    else:
        canvas.itemconfigure("flower_1.1", state="normal")

    if elapsed_seconds >= m110:
        canvas.itemconfigure("flower_2.3", state="normal")
    elif elapsed_seconds >= m85:
        canvas.itemconfigure("flower_2.2", state="normal")
    elif elapsed_seconds >= m60:
        canvas.itemconfigure("flower_2.1", state="normal")

    if elapsed_seconds >= m170:
        canvas.itemconfigure("flower_3.3", state="normal")
    elif elapsed_seconds >= m145:
        canvas.itemconfigure("flower_3.2", state="normal")
    elif elapsed_seconds >= m120:
        canvas.itemconfigure("flower_3.1", state="normal")

def update_insights():
    formatted_time = format_time(total_active_seconds)
    canvas.itemconfigure(insights_time_text_id, text=f"Tempo Ativo: {formatted_time}")


def run_timer():
    global time_left, timer_running, timer_after_id, elapsed_seconds, total_active_seconds
    if timer_running:
        total_active_seconds += 1
        elapsed_seconds += 1

        update_flowers()
        update_insights()

        if timer_mode == "livre":
            time_left += 1
            update_timer_display()
            timer_after_id = window.after(1000, run_timer)
        elif timer_mode == "pomodoro":
            if time_left > 0:
                time_left -= 1
                update_timer_display()
                timer_after_id = window.after(1000, run_timer)
            else:
                timer_running = False


def start_timer():
    global timer_running, elapsed_seconds
    if elapsed_seconds < 0:
        elapsed_seconds = 0
        update_flowers()

    if not timer_running:
        if timer_mode == "pomodoro" and time_left == 0:
            return
        timer_running = True
        run_timer()

def pause_timer():
    global timer_running, timer_after_id
    timer_running = False
    if timer_after_id:
        window.after_cancel(timer_after_id)

def reset_timer():
    pause_timer()
    global time_left, elapsed_seconds
    time_left = 25 * 60 if timer_mode == "pomodoro" else 0
    elapsed_seconds = -1
    update_flowers()
    update_timer_display()

def set_preset_time(minutes: int):
    pause_timer()
    global time_left, elapsed_seconds
    time_left = minutes * 60
    elapsed_seconds = -1
    update_flowers()
    update_timer_display()

def show_pomodoro_mode():
    global timer_mode, time_left, elapsed_seconds
    pause_timer()
    timer_mode = "pomodoro"
    time_left = 25 * 60
    elapsed_seconds = -1
    update_flowers()
    update_timer_display()
    canvas.itemconfigure("pomodoro_presets", state="normal")

def show_livre_mode():
    global timer_mode, time_left, elapsed_seconds
    pause_timer()
    timer_mode = "livre"
    time_left = 0
    elapsed_seconds = -1
    update_flowers()
    update_timer_display()
    canvas.itemconfigure("pomodoro_presets", state="hidden")

def show_tab(tab_name: str):
    global current_tab
    current_tab = tab_name
    canvas.itemconfigure("tab_timer", state="hidden")
    canvas.itemconfigure("tab_tasks", state="hidden")
    canvas.itemconfigure("tab_insights", state="hidden")
    canvas.itemconfigure("pomodoro_presets", state="hidden")

    canvas.itemconfigure(tab_name, state="normal")

images["sidebar_bg"] = make_panel_image(280, 547, radius=20)
canvas.create_image(40, 93.34, image=images["sidebar_bg"], anchor="nw")

raw_img = Image.open(relative_to_assets("Sproutly (1).png"))
target_width = 216
target_height = int(target_width * raw_img.height / raw_img.width)

resized_img = raw_img.resize((target_width, target_height), Image.Resampling.NEAREST)
images["sproutly"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(72, 20, image=images["sproutly"], anchor="nw")


raw_img = Image.open(relative_to_assets("Image_prateleira (1).png"))
resized_img = raw_img.resize((534, 112))
images["prateleira"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(374.02, 548.69, image=images["prateleira"], anchor="nw")

raw_img = Image.open(relative_to_assets("Image_vaso1 (1).png"))
resized_img = raw_img.resize((102, 107))
images["vaso1"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(481.02, 474.02, image=images["vaso1"], anchor="nw")

raw_img = Image.open(relative_to_assets("Image_vaso2 (1).png"))
resized_img = raw_img.resize((102, 107))
images["vaso2"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(591.7, 474.02, image=images["vaso2"], anchor="nw")

raw_img = Image.open(relative_to_assets("Image_vaso3 (1).png"))
resized_img = raw_img.resize((102, 107))
images["vaso3"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(699.7, 474.02, image=images["vaso3"], anchor="nw")

#raw_img = Image.open(relative_to_assets("Image_vaso4 (1).png"))
#resized_img = raw_img.resize((102, 107))  # (Largura, Altura)
#images["vaso4"] = ImageTk.PhotoImage(resized_img)
#canvas.create_image(746.7, 474.02, image=images["vaso4"], anchor="nw")

def load_sprite(filename: str, fallback_file: str):
    file_path = relative_to_assets(filename)
    if file_path.exists():
        return Image.open(file_path)
    return Image.open(relative_to_assets(fallback_file))

#flor 1
raw_img = Image.open(relative_to_assets("pixil-frame-0 1.png"))
resized_img = raw_img.resize((55, 62))
images["flor1.1"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(503.69, 440.35, image=images["flor1.1"], anchor="nw", state="hidden", tags=("flower", "flower_1.1"))

raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 1.png"))
resized_img = raw_img.resize((71, 91))
images["flor1.2"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(491.69, 411.35, image=images["flor1.2"], anchor="nw", state="hidden", tags=("flower", "flower_1.2"))

raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (1) 1.png"))
resized_img = raw_img.resize((91, 118))
images["flor1.3"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(487.69, 384.35, image=images["flor1.3"], anchor="nw", state="hidden", tags=("flower", "flower_1.3"))

#flor2
raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (2) 1.png"))
resized_img = raw_img.resize((53, 60))
images["flor2.1"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(615.69, 442.35, image=images["flor2.1"], anchor="nw", state="hidden", tags=("flower", "flower_2.1"))

raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (3) 1.png"))
resized_img = raw_img.resize((56, 88))
images["flor2.2"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(612.69, 416.35, image=images["flor2.2"], anchor="nw", state="hidden", tags=("flower", "flower_2.2"))

raw_img = Image.open(relative_to_assets("pixil-frame-1 1.png"))
resized_img = raw_img.resize((74, 104))
images["flor2.3"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(604.69, 398.35, image=images["flor2.3"], anchor="nw", state="hidden", tags=("flower", "flower_2.3"))

#flor 3
raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (4) 1.png"))
resized_img = raw_img.resize((39, 66))
images["flor3.1"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(733.69, 438.35, image=images["flor3.1"], anchor="nw", state="hidden", tags=("flower", "flower_3.1"))

raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (5) 1.png"))
resized_img = raw_img.resize((52, 79))
images["flor3.2"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(722.69, 425.35, image=images["flor3.2"], anchor="nw", state="hidden", tags=("flower", "flower_3.2"))

raw_img = Image.open(relative_to_assets("pixil-layer-Layer 1 (7) 1.png"))
resized_img = raw_img.resize((63, 102))
images["flor3.3"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(721.69, 402.35, image=images["flor3.3"], anchor="nw", state="hidden", tags=("flower", "flower_3.3"))


#joaninhas
raw_img = Image.open(relative_to_assets("Image_joaninha (1).png"))
resized_img = raw_img.resize((18, 10))
images["joaninha_1"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(284.68, 83.34, image=images["joaninha_1"], anchor="nw")

raw_img = Image.open(relative_to_assets("Image_joaninha.png"))
resized_img = raw_img.resize((18, 10))
images["joaninha_base"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(669.37, 292.01, image=images["joaninha_base"], anchor="nw")

raw_img = Image.open(relative_to_assets("Image_joaninha (2).png"))
resized_img = raw_img.resize((18, 10))
images["joaninha_2"] = ImageTk.PhotoImage(resized_img)
canvas.create_image(865.38, 571.36, image=images["joaninha_2"], anchor="nw")

#botoes
raw_img = Image.open(relative_to_assets("Button_TabTimer (1).png"))
resized_img = raw_img.resize((73, 33))
images["btn_timer"] = ImageTk.PhotoImage(resized_img)
btn_timer_id = canvas.create_image(56.67, 106.67, image=images["btn_timer"], anchor="nw")
canvas.tag_bind(btn_timer_id, "<Button-1>", lambda event: show_tab("tab_timer"))

raw_img = Image.open(relative_to_assets("Button_TabTask (1).png"))
resized_img = raw_img.resize((73, 33))
images["btn_task"] = ImageTk.PhotoImage(resized_img)
btn_task_id = canvas.create_image(143.34, 106.67, image=images["btn_task"], anchor="nw")
canvas.tag_bind(btn_task_id, "<Button-1>", lambda event: show_tab("tab_tasks"))

raw_img = Image.open(relative_to_assets("Button_TabInsights (2).png"))
resized_img = raw_img.resize((73, 33))
images["btn_insights"] = ImageTk.PhotoImage(resized_img)
btn_insights_id = canvas.create_image(230.02, 106.67, image=images["btn_insights"], anchor="nw")
canvas.tag_bind(btn_insights_id, "<Button-1>", lambda event: show_tab("tab_insights"))


images["txt_cronometro"] = make_timer_text_image(format_time(time_left), size=166)
cronometro_id = canvas.create_image(635.0, 180.0, image=images["txt_cronometro"], anchor="center")

images["btn_start"] = load_and_resize("Button (10).png", 120, 40)
btn_start_id = canvas.create_image(582.03, 253.35, image=images["btn_start"], anchor="nw")
canvas.tag_bind(btn_start_id, "<Button-1>", lambda event: start_timer())

images["btn_pause"] = load_and_resize("Button (20).png", 120, 40)
btn_pause_id = canvas.create_image(708.04, 253.35, image=images["btn_pause"], anchor="nw")
canvas.tag_bind(btn_pause_id, "<Button-1>", lambda event: pause_timer())

images["btn_reset"] = load_and_resize("Button (8).png", 120, 40)
btn_reset_id = canvas.create_image(454.69, 253.35, image=images["btn_reset"], anchor="nw")
canvas.tag_bind(btn_reset_id, "<Button-1>", lambda event: reset_timer())

raw_img = Image.open(relative_to_assets("Button (15).png"))
resized_img = raw_img.resize((211, 33))
images["btn_pomodoro"] = ImageTk.PhotoImage(resized_img)
btn_pomodoro_id = canvas.create_image(70.67, 396.02, image=images["btn_pomodoro"], anchor="nw", tags="tab_timer")
canvas.tag_bind(btn_pomodoro_id, "<Button-1>", lambda event: show_pomodoro_mode())

raw_img = Image.open(relative_to_assets("Button (16).png"))
resized_img = raw_img.resize((211, 33))
images["btn_livre"] = ImageTk.PhotoImage(resized_img)
btn_livre_id = canvas.create_image(70.67, 334.68, image=images["btn_livre"], anchor="nw", tags="tab_timer")
canvas.tag_bind(btn_livre_id, "<Button-1>", lambda event: show_livre_mode())


images["btn_50min"] = load_and_resize("Button (11).png", 101, 27)
btn_50min_id = canvas.create_image(180.01, 440.02, image=images["btn_50min"], anchor="nw", tags="pomodoro_presets")
canvas.tag_bind(btn_50min_id, "<Button-1>", lambda event: set_preset_time(50))

images["btn_25min"] = load_and_resize("Button (12).png", 101, 27)
btn_25min_id = canvas.create_image(70.67, 440.02, image=images["btn_25min"], anchor="nw", tags="pomodoro_presets")
canvas.tag_bind(btn_25min_id, "<Button-1>", lambda event: set_preset_time(25))


images["btn_add"] = load_and_resize("Button (19).png", 27, 32)
btn_add_id = canvas.create_image(277, 179, image=images["btn_add"], anchor="nw", tags="tab_tasks")
canvas.tag_bind(btn_add_id, "<Button-1>", lambda event: print("add Clicado!"))

images["input_box_bg"] = make_input_box_image(205, 50, radius=7)
canvas.create_image(64.67, 170.68, image=images["input_box_bg"], anchor="nw", tags="tab_tasks")

desc_pomodoro = (
    "Modo Pomodoro: Estudo focado por\n"
    "blocos de tempo com pausas curtas\n"
    "garantidas. Ideal para manter a\n"
    "concentração sem cansar a mente."
)
canvas.create_text(
    74.67, 160.0,
    text=desc_pomodoro,
    fill="#1C3805",
    font=("Menlo", 10),
    anchor="nw",
    width=240,
    tags="tab_timer"
)

desc_livre = (
    "Modo Livre: Cronômetro progressivo\n"
    "sem limite de tempo. Perfeito para\n"
    "quando você quer entrar em estado\n"
    "de fluxo e estudar no seu ritmo."
)
canvas.create_text(
    74.67, 245.0,
    text=desc_livre,
    fill="#1C3805",
    font=("Menlo", 10),
    anchor="nw",
    width=240,
    tags="tab_timer"
)

task_entry = Entry(
    window,
    font=("Iosevka Charon Mono", 12),
    bg="#A1D45D",
    fg="#286B00",
    bd=0,
    highlightthickness=0,
    insertbackground="#286B00"
)

entry_window = canvas.create_window(
    74.67, 180.68,
    anchor="nw",
    window=task_entry,
    width=185,
    height=30,
    tags="tab_tasks"
)


canvas.create_text(
    64.67, 235.0,
    text="tasks:",
    fill="#1C3805",
    font=("Menlo", 18, "bold"),
    anchor="nw",
    tags="tab_tasks"
)



tasks_container = Frame(window, bg="#B1DE77")
canvas.create_window(64.67, 275.0, anchor="nw", window=tasks_container, tags="tab_tasks")

task_vars = []


def add_task():
    text = task_entry.get().strip()
    if text:
        var = BooleanVar()
        task_vars.append(var)

        cb = Checkbutton(
            tasks_container,
            text=text,
            variable=var,
            font=("Menlo", 12),
            bg="#A3D977",
            fg="#1C3805",
            activebackground="#A3D977",
            selectcolor="#94CF68",
            anchor="w"
        )
        cb.pack(fill="x", pady=2, anchor="w")
        task_entry.delete(0, "end")


canvas.tag_bind(btn_add_id, "<Button-1>", lambda e: add_task())

insights_time_text_id = canvas.create_text(
    64.67, 180.0,
    text="Tempo Ativo Total:\n00:00:00",
    fill="#1C3805",
    font=("Menlo", 14, "bold"),
    anchor="nw",
    tags="tab_insights"
)


def force_stage(target_seconds: int):
    global elapsed_seconds, time_left
    elapsed_seconds = target_seconds

    if timer_mode == "livre":
        time_left = target_seconds
    else:
        time_left = max(0, (25 * 60) - target_seconds)

    update_flowers()
    update_timer_display()


window.bind("1", lambda e: force_stage(0))
window.bind("2", lambda e: force_stage((25 * 60) - 5))
window.bind("3", lambda e: force_stage((50 * 60) - 5))
window.bind("4", lambda e: force_stage((60 * 60) - 5))
window.bind("5", lambda e: force_stage((85 * 60) - 5))
window.bind("6", lambda e: force_stage((110 * 60) - 5))
window.bind("7", lambda e: force_stage((120 * 60) - 5))
window.bind("8", lambda e: force_stage((145 * 60) - 5))
window.bind("9", lambda e: force_stage((170 * 60) - 5))

show_tab("tab_timer")
window.resizable(False, False)

if __name__ == "__main__":
    window.mainloop()

