import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import platform
import os

print("Initializing...")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def load_images():
#it loads and resize imgs, returns None in case of error
    images = {}
    image_files = {
        'inicio': 'inicio.jpg',
        'trabajo': 'trabajo.jpg',
        'descanso': 'descanso.jpg',
        'completado': 'completado.jpg'
    }
    #named keys so I can reference them later easily :3

    for key, filename in image_files.items():
        try:
            if os.path.exists(filename):
                img = Image.open(filename)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)
                images[key] = ImageTk.PhotoImage(img)
            else:
                images[key] = None
                print(f"'{filename}' not found.")
        except Exception as e:
            print(f"Yikes can not load '{filename}': {e}")
            images[key] = None
    return images


def play_sound():
#sound alert, maybe adding my own sound later
#tday Im inspired so..make it exist first xD
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except:
        print("\a")
        print("*ding* (sound alert hehe)")


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("stayIn - Pomodoro Timer")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#FAF8F1")
        
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
        main_frame = tk.Frame(self.root, bg="#FAF8F1")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.timer_label = tk.Label(
            main_frame,
            text="25:00",
            font=("Arial", 72, "bold"),
            bg="#FAF8F1",
            fg="#D8968F"
        )
        self.timer_label.pack(pady=(20, 10))
        
        self.status_label = tk.Label(
            main_frame,
            text="1/4 - Focus",
            font=("Arial", 18),
            bg="#FAF8F1",
            fg="#535231"
        )
        self.status_label.pack(pady=10)
        
        self.image_label = tk.Label(
            main_frame,
            bg="#FAF8F1",
            text="inicio.jpg",
            font=("Arial", 14),
            fg="#726759"
        )
        self.image_label.pack(pady=30)
        
        self.message_label = tk.Label(
            main_frame,
            text="Press start to start! :D",
            font=("Arial", 14),
            bg="#FAF8F1",
            fg="#726759"
        )
        self.message_label.pack(pady=10)
        
        self.action_button = tk.Button(
            main_frame,
            text="Start",
            font=("Arial", 20, "bold"),
            bg="#A2AC80",
            fg="#FAF8F1",
            activebackground="#919869",
            activeforeground="#FAF8F1",
            cursor="hand2",
            command=self.toggle_timer,
            width=15,
            height=2,
            relief="raised",
            bd=3
        )
        self.action_button.pack(pady=20)
    
    def toggle_timer(self):
    #this is supposed to start or stop the timer
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
    #start
        self.is_running = True
        self.action_button.config(
            text="Stop", 
            bg="#D8968F", 
            activebackground="#D6AD9B"
        )
        self.message_label.config(text="")
        self.countdown()
    
    def stop_timer(self):
    #stop
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.action_button.config(
            text="Start", 
            bg="#A2AC80", 
            activebackground="#919869"
        )
    
    def countdown(self):
    #It will count down the time
        if self.time_left > 0 and self.is_running:
            mins, secs = divmod(self.time_left, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_label.config(text=time_format)
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.time_left == 0 and self.is_running:
            self.session_complete()
    
    def session_complete(self):
    #manages a session completion
        self.is_running = False
        play_sound()
        
        if self.is_working:
            self.handle_work_complete()
        else:
            self.handle_break_complete()
        
        self.update_display()
        self.action_button.config(
            text="Start", 
            bg="#A2AC80", 
            activebackground="#919869"
        )
    
    def handle_work_complete(self):
    #manages the end of a work session
        if self.current_cycle < self.total_cycles:
            self.is_working = False
            self.time_left = self.break_time
            self.message_label.config(
                text="Time to chill! Press start when ready.",
                fg="#CAD19F"
            )
            messagebox.showinfo(
                "You actually did it!", 
                f"Nice job!\ncycle {self.current_cycle} completed.\n\nTake a 5-minute break"
            )
        else:
            self.is_working = False
            self.time_left = self.break_time
            self.message_label.config(
                text="Last cycle done! Final 5-minute break.",
                fg="#CAD19F"
            )
            messagebox.showinfo(
                "What a good job!", 
                "Last cycle completed!\n\nFinal stretch!"
            )
    
    def handle_break_complete(self):
    #manages the end of a break session
        if self.current_cycle < self.total_cycles:
            self.current_cycle += 1
            self.is_working = True
            self.time_left = self.work_time
            self.message_label.config(
                text=f"Cycle {self.current_cycle} - Press start to focus!",
                fg="#D8968F"
            )
            messagebox.showinfo(
                "Back to work!", 
                f"{self.current_cycle} of {self.total_cycles}\n\n Keep going!"
            )
        else:
            self.all_cycles_complete()
    
    def all_cycles_complete(self):
     #manages the completion of all cycles
        self.show_image('completado')
        self.status_label.config(text="Yuppy!!! :D")
        self.timer_label.config(text="00:00")
        self.message_label.config(
            text="See you tomorrow! :D",
            fg="#A2AC80",
            font=("Arial", 14, "bold")
        )
        self.action_button.config(
            text="Restart",
            bg="#919869",
            activebackground="#535231",
            command=self.reset_app
        )
        messagebox.showinfo(
            ":DDDD", 
            "All cycles completed!\n\nGreat job!\n\nDrink water and rest!"
        )
    
    def reset_app(self):
    #it resets the app to initial state
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        self.current_cycle = 1
        self.is_working = True
        self.is_running = False
        self.time_left = self.work_time
        
        self.action_button.config(
            text="Start",
            bg="#A2AC80",
            activebackground="#919869",
            command=self.toggle_timer
        )
        
        self.update_display()
        self.message_label.config(
            text="press start to start! :D",
            fg="#726759",
            font=("Arial", 14)
        )
    
    def show_image(self, image_key):
    #manage the state of the images
    #never used dictionaries before, just learned and wanted to try :3
        if self.images.get(image_key):
            self.image_label.config(image=self.images[image_key], text="")
        else:
            placeholders = {
                'inicio': 'inicio.jpg',
                'trabajo': 'trabajo.jpg',
                'descanso': 'descanso.jpg',
                'completado': 'completado.jpg'
            }
            self.image_label.config(
                image='', 
                text=placeholders.get(image_key, 'Suppose to be an image'),
                font=("Arial", 14),
                fg="#726759"
            )
    
    def update_display(self):
    #updates the timer and status display
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        
        if self.is_working:
            status_text = f"Cycle {self.current_cycle}/{self.total_cycles} - Stay Focused!"
            self.timer_label.config(fg="#D8968F", bg="#FAF8F1")
            self.status_label.config(text=status_text)
            self.show_image('trabajo')
        else:
            status_text = f"Cycle {self.current_cycle}/{self.total_cycles} - Stretch"
            self.timer_label.config(fg="#CAD19F", bg="#FAF8F1")
            self.status_label.config(text=status_text)
            self.show_image('descanso')
        #the img of the very beginning
        if (self.current_cycle == 1 and self.is_working and 
            not self.is_running and self.time_left == self.work_time):
            self.show_image('inicio')


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()