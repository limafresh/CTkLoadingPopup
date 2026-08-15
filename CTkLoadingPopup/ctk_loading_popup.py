import customtkinter

class CTkLoadingPopup(customtkinter.CTkFrame):
    def __init__(
        self,
        parent,
        text: str="Loading...",
        progress: float=0.0,
        start_angle: int=90,
        indeterminate_speed: int=10,
        spinner_size: int=50,
        spinner_width: int=4,
        corner_radius: int=15,
        border_width: int=2,
        border_color=None,
        font=None,
        bg_color=("gray28", "gray21"),
        text_color="gray99",
        spinner_color=None,
        progress_color=None,
        mode: str="indeterminate",
        padx: int=20,
        pady: int=30,
        cancel_button: bool=False,
        cancel_button_text: str="Cancel",
        cancel_button_text_color="white",
        cancel_button_hover_color=("gray39", "gray33"),
        cancel_button_state: str="normal",
        compound: str="left",
        close_command=None,
    ):
        super().__init__(parent, border_width=border_width, border_color=border_color,
                         corner_radius=corner_radius, fg_color=bg_color)
        self.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        self.progress = progress
        self.angle = start_angle
        self.indeterminate_speed = indeterminate_speed
        self.spinner_size = spinner_size
        self.spinner_width = spinner_width
        self.bg_color = bg_color
        self.spinner_color = spinner_color if spinner_color else customtkinter.ThemeManager.theme["CTkProgressBar"]["fg_color"]
        self.progress_color = progress_color if progress_color else customtkinter.ThemeManager.theme["CTkProgressBar"]["progress_color"]
        self.mode = mode
        self.close_command = close_command

        self.is_stop = False

        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=padx, pady=pady)

        self.canvas = customtkinter.CTkCanvas(frame, width=spinner_size, height=spinner_size, highlightthickness=0)

        self.label = customtkinter.CTkLabel(frame, text=text, font=font, text_color=text_color,
                                            width=150)

        if compound == "left":
            self.canvas.pack(side=customtkinter.LEFT)
            self.label.configure(anchor=customtkinter.W)
            self.label.pack(side=customtkinter.LEFT, padx=(padx, 0))
        elif compound == "right":
            self.label.configure(anchor=customtkinter.W)
            self.label.pack(side=customtkinter.LEFT)
            self.canvas.pack(side=customtkinter.LEFT, padx=(padx, 0))
        elif compound == "top":
            self.label.pack()
            self.canvas.pack(pady=(pady, 0))

        if cancel_button:
            self.cancel_button = customtkinter.CTkButton(
                self,
                fg_color=self.bg_color,
                text_color=cancel_button_text_color,
                hover_color=cancel_button_hover_color,
                text=cancel_button_text.upper(),
                width=0,
                height=35,
                state=cancel_button_state,
                corner_radius=20,
                cursor="hand2",
                command=self.close,
            )
            self.cancel_button.pack(padx=(0, 10), pady=(0, 10), anchor=customtkinter.E)
        else:
            self.cancel_button = None

        self.animate()

    def animate(self):
        self.canvas.delete("all")

        if customtkinter.get_appearance_mode() == "Light":
            theme_index = 0
        else:
            theme_index = 1
        bg_color, spinner_color, progress_color = self.bg_color, self.spinner_color, self.progress_color
        if isinstance(self.bg_color, (list, tuple)):
            bg_color = self.bg_color[theme_index]
        if isinstance(self.spinner_color, (list, tuple)):
            spinner_color = self.spinner_color[theme_index]
        if isinstance(self.progress_color, (list, tuple)):
            progress_color = self.progress_color[theme_index]
        self.canvas.configure(background=bg_color)

        scaling = customtkinter.ScalingTracker.widget_scaling
        spinner_size = int(self.spinner_size * scaling)
        spinner_width = int(self.spinner_width * scaling)
        if self.canvas.winfo_width() != spinner_size:
            self.canvas.configure(width=spinner_size, height=spinner_size)

        center = spinner_size // 2

        # Draw anti-aliased circle using CustomTkinter method

        # outline
        self.canvas.create_aa_circle(
            center, center,
            center,
            fill=spinner_color
        )

        # fill
        self.canvas.create_aa_circle(
            center, center,
            center - spinner_width,
            fill=bg_color
        )

        if self.mode == "indeterminate":
            extent = -90
        elif self.mode == "determinate":
            extent = -self.progress * 360
        else:
            print(f"Invalid mode: {self.mode}. Please use 'indeterminate' or 'determinate'")
            return

        start = spinner_width // 2

        self.canvas.create_arc(
            start, start,
            spinner_size - start,
            spinner_size - start,
            start=self.angle,
            extent=extent,
            outline=progress_color,
            style="arc",
            width=spinner_width,
        )

        if self.mode == "indeterminate":
            self.angle = (self.angle - self.indeterminate_speed) % 360

        if not self.is_stop:
            self.after(50, self.animate)

    def configure(self, text: str=None, progress: float=None, progress_color=None,
                  cancel_button_state: str=None):
        if text:
            self.label.configure(text=text)
        if progress is not None:
            self.progress = progress
        if progress_color:
            self.progress_color = progress_color
        if cancel_button_state and self.cancel_button:
            self.cancel_button.configure(state=cancel_button_state)

    def close(self):
        if self.close_command:
            self.close_command()

        self.destroy()

    def stop(self, value: bool):
        self.is_stop = value
        if not self.is_stop:
            self.animate()

    def get(self):
        if self.mode == "determinate":
            return self.progress
        else:
            return None
