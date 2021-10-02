import threading
import tkinter as tk
from Model import Model
from Solver import Solver
from PIL import ImageTk, Image
from screeninfo import get_monitors



class GUI:
    def __init__(self):
        self.mon_width = get_monitors()[0].width
        self.mon_height = get_monitors()[0].height

        self.screen = tk.Tk()
        self.screen.wm_attributes('-fullscreen', True)
        self.screen.geometry(str(self.mon_width) + "x" + str(self.mon_height))
        self.screen.title("Python Form")

        self.number_of_clients_entry = tk.Entry(self.screen, width="30", )
        self.number_of_clients_entry.insert(0, 100)

        self.depot_x_entry = tk.Entry(self.screen, width="30", )
        self.depot_x_entry.insert(0, 50)

        self.depot_y_entry = tk.Entry(self.screen, width="30", )
        self.depot_y_entry.insert(0, 50)

        self.service_time_entry = tk.Entry(self.screen, width="30", )
        self.service_time_entry.insert(0, 0.25)

        self.first_solution_algo = tk.IntVar()
        self.first_solution_algo.set(1)
        self.screen.update()
        self.algo_text = tk.Label(self.screen, text="Minimum Iterations")
        self.algo_nn = tk.Button(self.screen, text="Nearest Neighbour", command=self.radio_clicked(2))
        self.algo_min_iter = tk.Button(self.screen, text="Minimum Iterations", command=self.radio_clicked(1))



        self.speed_entry = tk.Entry(self.screen, width="30", )
        self.speed_entry.insert(0, 35)
        self.image_label = None
        self.first_solution_label = None
        self.image = Image
        self.time_entry = tk.Entry(self.screen, width="30")
        self.time_entry.insert(0, 3.5)
        self.trucks_entry = tk.Entry(self.screen, width="30")
        self.trucks_entry.insert(0, 30)
        self.capacity_entry = tk.Entry(self.screen, width="30")
        self.capacity_entry.insert(0, 1500)

        self.improved_solutions_label = None
        self.improved_solution_label = None
        self.trajectory = None
        self.final_solution_label = None
        self.m = None
        self.s = None
        self.next_image = None
        self.prev_image = None
        self.images_index = 0
        self.init_first_screen()

        self.thread = None


        self.p = None

    def radio_clicked(self, value):
        self.algo_text.destroy()
        if value == 1:
            self.algo_text = tk.Label(self.screen, text="Minimum Iterations")
            self.algo_text.place(x=15, y=840)
        else:
            self.algo_text = tk.Label(self.screen, text="Closest Neighbour")
            self.algo_text.place(x=15, y=840)
        self.first_solution_algo.set(value)


    def submit(self):
        if self.thread is not None:
            self.s.stop_threading = True
            self.thread.join()
        if self.final_solution_label is not None:
            self.final_solution_label.destroy()
        if self.trajectory is not None:
            self.trajectory.destroy()
        if self.improved_solutions_label is not None:
            self.improved_solutions_label.destroy()
        if self.first_solution_label is not None:
            self.first_solution_label.destroy()
        if self.image_label is not None:
            self.image_label.destroy()
        n = int(self.number_of_clients_entry.get())
        depot_x = int(self.depot_x_entry.get())
        depot_y = int(self.depot_y_entry.get())
        depot = (depot_x, depot_y)
        service_time = float(self.service_time_entry.get())
        speed = int(self.speed_entry.get())
        time = float(self.time_entry.get())
        trucks = int(self.trucks_entry.get())
        capacity = int(self.capacity_entry.get())

        self.first_solution_label = tk.Button(self.screen, text="First Solution", command=self.print_first_solution_result)
        self.first_solution_label.pack(side=tk.RIGHT)

        self.m = Model(n, depot, service_time, speed)
        self.m.BuildModel()
        self.s = Solver(self.m, n, speed)
        print(self.first_solution_algo.get())
        if self.s.find_a_first_solution(self.first_solution_algo.get(), time, trucks, capacity):
            self.print_first_solution_result()

        # sol = s.solve()
        # s.report_solution()

    def init_first_screen(self):
        print(self.first_solution_algo.get())
        heading = tk.Label(text="Python Form", bg="grey", fg="black", width="500", height="3")
        heading.pack()

        number_of_clients_text = tk.Label(self.screen, text="Number of Clients* ", )
        depot_x_text = tk.Label(self.screen, text="Depot X location * ", )
        depot_y_text = tk.Label(self.screen, text="Depot Y location * ", )
        service_time_text = tk.Label(self.screen, text="Service Time * ", )
        speed_text = tk.Label(self.screen, text="Speed of Trucks in km/h * ", )
        algo_min_text = tk.Label(self.screen, text="Select the algorithm for the first Solution: (Default is Minimum Iterations)")
        time_text = tk.Label(self.screen, text="Total time available for each truck")
        trucks_number_text = tk.Label(self.screen, text="Number of trucks available")
        capacity_text = tk.Label(self.screen, text="Capacity of each Truck")

        self.algo_min_iter = tk.Button(self.screen, text="Minimum Iterations", command=lambda: self.radio_clicked(1))
        self.algo_nn = tk.Button(self.screen, text="Nearest Neighbour", command=lambda: self.radio_clicked(2))
        number_of_clients_text.place(x=15, y=70)
        depot_x_text.place(x=15, y=140)
        depot_y_text.place(x=15, y=210)
        service_time_text.place(x=15, y=280)
        speed_text.place(x=15, y=350)
        time_text.place(x=15, y=420)
        trucks_number_text.place(x=15, y= 490)
        capacity_text.place(x=15, y= 560)


        self.algo_text.place(x=15, y=840)
        self.algo_min_iter.place(x=15, y=660)
        self.algo_nn.place(x=15, y=700)
        algo_min_text.place(x=15, y=630)





        self.number_of_clients_entry.place(x=15, y=100)
        self.depot_x_entry.place(x=15, y=170)
        self.depot_y_entry.place(x=15, y=240)
        self.service_time_entry.place(x=15, y=310)
        self.speed_entry.place(x=15, y=380)
        self.time_entry.place(x=15, y= 450)
        self.trucks_entry.place(x=15, y= 520)
        self.capacity_entry.place(x=15, y= 590)


        register = tk.Button(self.screen, text="Find First Solution", width="30", height="2", command=self.submit, bg="grey")
        register.place(x=15, y=740)

        print('start')

    def print_first_solution_result(self):
        if self.improved_solution_label is not None:
            self.improved_solution_label.destroy()
        if self.next_image:
            self.next_image.destroy()
            self.prev_image.destroy()
        if self.image_label is not None:
            self.image_label.destroy()
        self.image = ImageTk.PhotoImage(Image.open('-1.png').resize((int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
        self.image_label = tk.Label(self.screen, image=self.image,  width=self.mon_width / 2, height=self.mon_width / 2)
        self.image_label.pack()
        self.improved_solution_label = tk.Button(self.screen, text="Improve Solution", width="30", height="2", command=self.improve, bg="grey")
        self.improved_solution_label.pack(side=tk.TOP)

    def print_improved_solutions_result(self):
        self.improved_solution_label.destroy()
        if self.next_image:
            self.next_image.destroy()
            self.prev_image.destroy()
        self.image_label.destroy()
        try:
            self.image = ImageTk.PhotoImage(Image.open((self.s.VND_images[self.images_index])).resize(
                (int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
            self.image_label = tk.Label(self.screen, image=self.image, width=self.mon_width / 2, height=self.mon_width / 2)
            self.image_label.pack()

            self.next_image = tk.Button(self.screen, text="Next", width="30", height="2", command=self.next_image_for, bg="grey")
            self.next_image.place(x=2000, y=450)

            self.prev_image = tk.Button(self.screen, text="Previous", width="30", height="2", command=self.prev_image_for, bg="grey")
            self.prev_image.place(x=2000, y=550)
        except:
            print("Image hasn't loaded yet")




    def print_final_solution(self):
        if self.improved_solution_label:
            self.improved_solution_label.destroy()
        self.image_label.destroy()
        if self.next_image:
            self.next_image.destroy()
            self.prev_image.destroy()
        self.image_label.destroy()

        self.image = ImageTk.PhotoImage(Image.open('final.png').resize(
            (int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
        self.image_label = tk.Label(self.screen, image=self.image, width=self.mon_width / 2, height=self.mon_width / 2)
        self.image_label.pack()


    def print_trajectort(self):
        if self.improved_solution_label:
            self.improved_solution_label.destroy()
        self.image_label.destroy()
        if self.next_image:
            self.next_image.destroy()
            self.prev_image.destroy()
        self.image = ImageTk.PhotoImage(Image.open('SearchTrajectory.png').resize(
            (int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
        self.image_label = tk.Label(self.screen, image=self.image, width=self.mon_width / 2, height=self.mon_width / 2)
        self.image_label.pack()

    def next_image_for(self):
        self.image_label.destroy()
        if self.images_index >= len(self.s.VND_images) -1:
            self.images_index = 0
        else:
            self.images_index += 1
        try:
            self.image = ImageTk.PhotoImage(Image.open((self.s.VND_images[self.images_index])).resize(
                (int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
            self.image_label = tk.Label(self.screen, image=self.image, width=self.mon_width / 2, height=self.mon_width / 2)
            self.image_label.pack()
        except:
            print("Image hasn't loaded yet")

    def prev_image_for(self):
        self.image_label.destroy()
        if self.images_index == 0:
            self.images_index = len(self.s.VND_images) - 1
        else:
            self.images_index -= 1
        try:

            self.image = ImageTk.PhotoImage(Image.open((self.s.VND_images[self.images_index])).resize(
            (int(self.mon_width / 2), int(self.mon_width / 2))), master=self.screen)
            self.image_label = tk.Label(self.screen, image=self.image, width=self.mon_width / 2, height=self.mon_width / 2)
            self.image_label.pack()
        except:
            print("Image hasn't loaded yet")



    def improve(self):
        self.images_index = 0
        self.improved_solution_label.destroy()
        self.image_label.destroy()

        self.s.VND()
        self.s.report_solution()
        self.thread = threading.Thread(target=self.s.save_sol)
        self.thread.start()

        self.improved_solutions_label = tk.Button(self.screen, text="Improved Solutions", command=self.print_improved_solutions_result)
        self.improved_solutions_label.pack(side=tk.RIGHT)

        self.final_solution_label = tk.Button(self.screen, text="Final Solution", command=self.print_final_solution)
        self.final_solution_label.pack(side=tk.RIGHT)

        self.trajectory = tk.Button(self.screen, text="Trajectory", command=self.print_trajectort)
        self.trajectory.pack(side=tk.RIGHT)



        self.print_final_solution()



    def start(self):
        if self.p is not None:
            self.p.join()
        self.screen.mainloop()


