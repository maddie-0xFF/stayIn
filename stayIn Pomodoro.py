import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage, FontManager
import platform
import os
from PIL import Image, ImageFont



def load_custom_font():
    try:
        base_dir = os.getcwd()
        font_path = os.path.join(base_dir, "stayIn", "assets", "IndieFlower-Regular.ttf")

        if os.path.exists(font_path):
        #create a PIL font to get the name
            pil_font = ImageFont.truetype(font_path, 14)
            font_name = pil_font.getname()[0]
            print(f"font: '{font_name}'")
            
        #pyglet is used by customtkinter to manage fonts
        #so we need to register the font with pyglet as well D:
            try:
                from pyglet import font as pyglet_font
                pyglet_font.add_file(font_path)
            except:
                pass
            
            return font_name
        else:
            print(f"✗ No encontrado: {font_path}")
            return "Arial"
    except Exception as e:
        print(f"✗ Error: {e}")
        return "Arial"

# it renames the default font to my custom font if available
FONT_FAMILY = load_custom_font()
DEFAULT_FONT = (FONT_FAMILY, 14)

# custom label function to use MY font hehe :D
def my_label(parent, text="", font=None, **kwargs):
    if font is None: 
        font = DEFAULT_FONT
    return ctk.CTkLabel(parent, text=text, font=font, **kwargs)
# in tears, it works T.T !!!!!!!!
print("Initializing...")
#printed this to know when it is actually running xd
def center_window(window):
    window.update_idletasks() 
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) 
    window.geometry(f'{width}x{height}+{x}+{y}')

# loads and resizes images
def load_images():

    images = {}
    image_files = {
        'inicio': 'inicio.png',
        'trabajo': 'trabajo.png',
        'descanso': 'descanso.png',
        'completado': 'completado.png'
    }

    #  error handling

    for key, filename in image_files.items():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "assets", filename)
            if os.path.exists(path):
                img = Image.open(path).convert("RGBA")
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                images[key] = CTkImage(light_image=img, dark_image=img, size=(200, 200))
            else:
                images[key] = None
                print(f"'{filename}' not found.")
        except Exception as e:
            print(f"Yikes can not load '{filename}': {e}")
            images[key] = None
    return images


def play_sound():
# sound alert, maybe adding my own sound later
# only works on windows btw
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except:
        print("\a")
        print("ding (sound alert hehe)")

# the only class in the code :D very demure
class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("stayIn - Pomodoro Timer")

        # add trasparent color set up 
        self.root.overrideredirect(True)
        transparent_color = self.root._apply_appearance_mode(['#f2f2f2','#000001'])
        self.root.config(background = transparent_color)
        self.root.attributes("-transparentcolor", transparent_color)

        self.root.geometry("400x550")
        self.root.resizable(True, True)
        self.root.configure(fg_color = "#6276A5")
        

        # store transparent color 
        self.transparent_color = transparent_color
        
        center_window(self.root)
        
        # timer variables
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.total_cycles = 4
        self.current_cycle = 1
        self.is_working = True
        self.is_running = False
        self.time_left = self.work_time
        self.timer_id = None
        
        # img loading
        self.images = load_images()
        
        # methods that Im learning rn :3
        self.create_widgets()
        self.update_display()
        
    def create_widgets(self):
     # Title bar with rounded top corners
     title_bar = ctk.CTkFrame(
        self.root, 
        corner_radius = 10, 
        fg_color = "#B2CDD4", 
        height = 40,
        background_corner_colors=(self.transparent_color, self.transparent_color, None, None)
     )
     title_bar.pack(fill="x")
     
     # Main frame with straight top, rounded bottom corners  
     main_frame = ctk.CTkFrame(
        self.root, 
        fg_color = "#6276A5", 
        corner_radius=12,
        bg_color = self.transparent_color,
        background_corner_colors = ("#6276A5", "#6276A5", self.transparent_color, self.transparent_color)
     )
     main_frame.pack(expand = True, fill = "both", padx = 0, pady = 0)

     # title text
     title_label = my_label(
        title_bar,
        text = "stayIn - Pomodoro Timer",
        font = (FONT_FAMILY, 16, "bold"),
        fg_color = "#B2CDD4",
        text_color = "#6276A5"
     )
     title_label.pack(side="left", padx = 10, pady = 10)
     close_btn = ctk.CTkButton(
        title_bar,
        text = "✕",
        font = (FONT_FAMILY, 14, "bold"),
        fg_color = "#B2CDD4",
        text_color = "#6276A5",
        hover_color = "#ACB0CA",
        cursor ="hand2",
        command = self.root.destroy,
        corner_radius = 15,
        width = 30
     )
     close_btn.pack(side="right", padx=10)

     # this makes the window draggable
     def start_move(event):
        self.x = event.x
        self.y = event.y

     def stop_move(event):
        self.x = None
        self.y = None

     def on_motion(event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")


     title_bar.bind("<Button-1>", start_move)
     title_bar.bind("<ButtonRelease-1>", stop_move)
     title_bar.bind("<B1-Motion>", on_motion)
        
     self.timer_label = my_label(
            main_frame,
            text = "25:00",
            font = (FONT_FAMILY, 72, "bold"),
            fg_color = "#6276A5",
            text_color = "#F2D9CD"
        )
     self.timer_label.pack(pady=(20, 10))
        
     self.status_label = my_label(
            main_frame,
            text = "1/4 - Focus",
            font = (FONT_FAMILY, 18),
            fg_color = "#6276A5",
            text_color = "#EDEDED"
        )
     self.status_label.pack(pady=10)
        
     self.image_label = my_label(
            main_frame,
            fg_color = "#6276A5",
            text = "",
            font = (FONT_FAMILY, 14),
            text_color = "#ACB0CA",
            anchor = "center"
        )
     self.image_label.pack(pady = (10, 0), expand=True)
     if self.images.get('inicio'):
            self.current_image = self.images['inicio']
            self.image_label.configure(image=self.current_image, text="")
     
     self.message_label = my_label(
            main_frame,
            text = "Press start to start! :D",
            font = (FONT_FAMILY, 16),
            fg_color = "#6276A5",
            text_color = "#EDEDED"
        )
     self.message_label.pack(pady=10)
        
     self.action_button = ctk.CTkButton(
            main_frame,
            text = "Start",
            font = (FONT_FAMILY, 20, "bold"),
            fg_color = "#B2CDD4",
            text_color ="#6276A5",
            hover_color = "#ACB0CA",
            cursor="hand2",
            command=self.toggle_timer,
            width=200,
            height=60,
            corner_radius=15
        )
     self.action_button.pack(pady=20)
    
    def toggle_timer(self):
    # this is supposed to start or stop the timer
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
    # start
        self.is_running = True
        self.action_button.configure(
            text="Stop", 
            fg_color="#F2D9CD", 
            hover_color="#EBC7BA"
        )
        self.message_label.configure(text="")
        self.show_image('trabajo')
        self.countdown()
    
    def stop_timer(self):
    # stop
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.action_button.configure(
            text="Start", 
            fg_color="#B2CDD4", 
            hover_color="#ACB0CA"
        )
    
    def countdown(self):
    # it will count down the time
        if self.time_left > 0 and self.is_running:
            mins, secs = divmod(self.time_left, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_label.configure(text=time_format)
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.time_left == 0 and self.is_running:
            self.session_complete()
    
    def session_complete(self):
    # manages a session completion
        self.is_running = False
        play_sound()
        
        if self.is_working:
            self.handle_work_complete()
        else:
            self.handle_break_complete()
        
        self.update_display()
        self.action_button.configure(
            text="Start", 
            fg_color="#B2CDD4", 
            hover_color="#ACB0CA"
        )
    
    def handle_work_complete(self):
    # manages the end of a work session
        if self.current_cycle < self.total_cycles:
            self.is_working = False
            self.time_left = self.break_time
            self.message_label.configure(
                text="Time to chill! Press start when ready.",
                text_color="#EDEDED"
            )
           
        else:
            self.is_working = False
            self.time_left = self.break_time
            self.message_label.configure(
                text="Last cycle done! Final 5-minute break.",
                text_color="#EDEDED"
            )
            
    
    def handle_break_complete(self):
    # manages the end of a break session
        if self.current_cycle < self.total_cycles:
            self.current_cycle += 1
            self.is_working = True
            self.time_left = self.work_time
            self.message_label.configure(
                text=f"Cycle {self.current_cycle} - Press start to focus!",
                text_color="#F2D9CD"
            )
            
        else:
            self.all_cycles_complete()
    
    def all_cycles_complete(self):
    # manages the completion of all cycles
        self.show_image('completado')
        self.status_label.configure(text="Yuppy!!! :D")
        self.timer_label.configure(text="00:00")
        self.message_label.configure(
            text="See you tomorrow! :D",
            text_color="#EDEDED",
            font=(FONT_FAMILY, 14, "bold")
        )
        self.action_button.configure(
            text="Restart",
            fg_color="#B2CDD4",
            hover_color="#ACB0CA",
            command=self.reset_app
        )
        self.root.update() 
        self.root.after(5000)
        self.show_custom_message(
            ":DDDD", 
            "All cycles completed!\n\nGreat job!\n\nDrink some water and rest!"
        )
    
    def reset_app(self):
    # it resets the app to initial state
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        self.current_cycle = 1
        self.is_working = True
        self.is_running = False
        self.time_left = self.work_time
        
        self.action_button.configure(
            text="Start",
            fg_color="#B2CDD4",
            hover_color="#ACB0CA",
            command=self.toggle_timer
        )
        
        self.update_display()
        self.message_label.configure(
            text="press start to start! :D",
            text_color="#EDEDED",
            font=(FONT_FAMILY, 14)
        )
    
    def show_custom_message(self, title, message):
    # custom popup message
     popup = ctk.CTkToplevel(self.root)
     popup.overrideredirect(True)  
     popup.geometry("400x280")
     popup.configure(fg_color="#7188B8")
    
     popup.update_idletasks()
     x = (popup.winfo_screenwidth() // 2) - (200)
     y = (popup.winfo_screenheight() // 2) - (140)
     popup.geometry(f'400x280+{x}+{y}')
    
     title_bar = ctk.CTkFrame(popup, fg_color="#B2CDD4", height=40, corner_radius=0)
     title_bar.pack(fill="x")
    
     title_bar_label = my_label(
        title_bar,
        text=title,
        font=(FONT_FAMILY, 12, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5"
     )
     title_bar_label.pack(side="left", padx=10, pady=10)
    
    # close button
     close_btn = ctk.CTkButton(
        title_bar,
        text="✕",
        font=(FONT_FAMILY, 14, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5",
        hover_color="#ACB0CA",
        cursor="hand2",
        command=popup.destroy,
        corner_radius=0,
        width=30
     )
     close_btn.pack(side="right", padx=10)
    
    # content
     content_frame = ctk.CTkFrame(popup, fg_color="#7188B8", corner_radius=0)
     content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
     message_label = my_label(
        content_frame,
        text=message,
        font=(FONT_FAMILY, 14),
        fg_color="#7188B8",
        text_color="#EDEDED",
        wraplength=350,
        justify="center"
     )
     message_label.pack(pady=20)
    
     ok_button = ctk.CTkButton(
        content_frame,
        text="OK",
        font=(FONT_FAMILY, 14, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5",
        hover_color="#ACB0CA",
        command=popup.destroy,
        width=100,
        cursor="hand2",
        corner_radius=15
     )
     ok_button.pack(pady=10)
    
     popup.transient(self.root)
     popup.grab_set()

    def show_image(self, image_key):
     img = self.images.get(image_key)
     if img:
         self.current_image = img
         self.image_label.configure(image=self.current_image, text="")
     else:
      placeholders = {
            'inicio': 'inicio.png',
            'trabajo': 'trabajo.png',
            'descanso': 'descanso.png',
            'completado': 'completado.png'
        }
      self.image_label.configure(
            image=None,  # Use None, not ''
            text=placeholders.get(image_key, 'Suppose to be an image'),
            font=(FONT_FAMILY, 14),
            text_color="#ACB0CA"
        )
    def update_display(self):
    # updates the timer and status display
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        
        if self.is_working:
            status_text = f"Cycle {self.current_cycle}/{self.total_cycles} - Stay Focused!"
            self.timer_label.configure(text_color="#F2D9CD", fg_color="#6276A5")
            self.status_label.configure(text=status_text)
            self.show_image('trabajo')
        else:
            status_text = f"Cycle {self.current_cycle}/{self.total_cycles} - Stretch"
            self.timer_label.configure(text_color="#B2CDD4", fg_color="#6276A5")
            self.status_label.configure(text=status_text)
            self.show_image('descanso')
        # the img of the very beginning
        if (self.current_cycle == 1 and self.is_working and 
            not self.is_running and self.time_left == self.work_time):
            self.show_image('inicio')


def main():
   ctk.set_appearance_mode("dark")  
   ctk.set_default_color_theme("blue")  

   root = ctk.CTk() 
   root.geometry("400x550")  
   root.title("StayIn - Pomodoro Timer")
   app = PomodoroTimer(root)
   root.mainloop()


if __name__ == "__main__":
    main()