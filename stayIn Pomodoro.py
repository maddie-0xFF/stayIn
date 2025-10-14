import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage
import platform
import os
from PIL import Image 

print("Initializing...")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def load_images():

    images = {}
    image_files = {
        'inicio': 'inicio.png',
        'trabajo': 'trabajo.png',
        'descanso': 'descanso.png',
        'completado': 'completado.png'
    }
    # loading images with error handling

    for key, filename in image_files.items():
        try:
            if os.path.exists(filename):
                img = Image.open(filename)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)
                images[key] = CTkImage(light_image=img, dark_image=img, size=(250, 250))
            else:
                images[key] = None
                print(f"'{filename}' not found.")
        except Exception as e:
            print(f"Yikes can not load '{filename}': {e}")
            images[key] = None
    return images


def play_sound():
# sound alert, maybe adding my own sound later
# tday Im inspired so..make it exist first xD
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except:
        print("\a")
        print("ding (sound alert hehe)")


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("stayIn - Pomodoro Timer")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#6276A5")
        self.root.overrideredirect(True)
        
        center_window(self.root)
        
        # timer variables
        self.work_time = 5
        self.break_time = 3
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
     # main frame
     title_bar = ctk.CTkFrame(self.root, fg_color="#B2CDD4", height=40)
     title_bar.pack(fill="x")

     # title text
     title_label = ctk.CTkLabel(
        title_bar,
        text="stayIn - Pomodoro Timer",
        font=("Arial", 12, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5"
     )
     title_label.pack(side="left", padx=10, pady=10)
     close_btn = ctk.CTkButton(
        title_bar,
        text="✕",
        font=("Arial", 14, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5",
        hover_color="#ACB0CA",
        cursor="hand2",
        command=self.root.destroy,
        corner_radius=15,
        width=30
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
     main_frame = ctk.CTkFrame(self.root, fg_color="#6276A5", corner_radius=25)
     main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
     self.timer_label = ctk.CTkLabel(
            main_frame,
            text="25:00",
            font=("Arial", 72, "bold"),
            fg_color="#6276A5",
            text_color="#F2D9CD"
        )
     self.timer_label.pack(pady=(20, 10))
        
     self.status_label = ctk.CTkLabel(
            main_frame,
            text="1/4 - Focus",
            font=("Arial", 18),
            fg_color="#6276A5",
            text_color="#EDEDED"
        )
     self.status_label.pack(pady=10)
        
     self.image_label = ctk.CTkLabel(
            main_frame,
            fg_color="#6276A5",
            text="inicio.jpg",
            font=("Arial", 14),
            text_color="#ACB0CA"
        )
     self.image_label.pack(pady=(10, 0), expand=True)
     
     self.message_label = ctk.CTkLabel(
            main_frame,
            text="Press start to start! :D",
            font=("Arial", 14),
            fg_color="#6276A5",
            text_color="#EDEDED"
        )
     self.message_label.pack(pady=10)
        
     self.action_button = ctk.CTkButton(
            main_frame,
            text="Start",
            font=("Arial", 20, "bold"),
            fg_color="#B2CDD4",
            text_color="#6276A5",
            hover_color="#ACB0CA",
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
            font=("Arial", 14, "bold")
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
            font=("Arial", 14)
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
    
     title_bar_label = ctk.CTkLabel(
        title_bar,
        text=title,
        font=("Arial", 12, "bold"),
        fg_color="#B2CDD4",
        text_color="#6276A5"
     )
     title_bar_label.pack(side="left", padx=10, pady=10)
    
    # close button
     close_btn = ctk.CTkButton(
        title_bar,
        text="✕",
        font=("Arial", 14, "bold"),
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
    
     message_label = ctk.CTkLabel(
        content_frame,
        text=message,
        font=("Arial", 14),
        fg_color="#7188B8",
        text_color="#EDEDED",
        wraplength=350,
        justify="center"
     )
     message_label.pack(pady=20)
    
     ok_button = ctk.CTkButton(
        content_frame,
        text="OK",
        font=("Arial", 14, "bold"),
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
     if self.images.get(image_key):
        self.image_label.configure(image=self.images[image_key], text="")
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
            font=("Arial", 14),
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
   root.geometry("500x700")  
   root.title("StayIn - Pomodoro Timer")

   root.overrideredirect(True)
   app = PomodoroTimer(root)
   root.mainloop()


if __name__ == "__main__":
    main()