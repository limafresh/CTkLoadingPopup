import customtkinter
from CTkLoadingPopup import CTkLoadingPopup

app = customtkinter.CTk()
app.title("CTkLoadingPopup example")
app.geometry("400x300")

def show_loading_popup():
    global popup
    if not popup:
        popup = CTkLoadingPopup(app)

def close_loading_popup():
    global popup
    if popup is not None:
        popup.close()
        popup = None

popup = None

frame = customtkinter.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

customtkinter.CTkButton(frame, text="Show CTkLoadingPopup",
                        command=show_loading_popup).pack(padx=10, pady=10)

customtkinter.CTkButton(frame, text="Close CTkLoadingPopup",
                        command=close_loading_popup).pack(padx=10, pady=10)

customtkinter.CTkButton(
    frame, text="Show CTkLoadingPopup with 'Cancel' button",
    command=lambda: CTkLoadingPopup(app, cancel_button=True)
).pack(padx=10, pady=10)

app.mainloop()
