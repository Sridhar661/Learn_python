import time
import datetime
import pygame


def set_alarm(alarm_time):
    print(f"Alarm set at{alarm_time} ")
    Sound = "tester/Alrm.mp3"


    is_running = True
    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)   


        if (current_time == alarm_time):
            print("WAKE UP ")

            pygame.mixer.init()
            pygame.mixer.music.load(Sound)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)



            is_running = False



        time.sleep(1)

  

if __name__ == "__main__":
    tim = input("Enter the alarm Time(HH:MM:SS):")
    set_alarm(tim)