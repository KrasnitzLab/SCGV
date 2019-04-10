from PyQt5.QtWidgets import QWidget, QVBoxLayout, \
    QListWidget, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLineEdit


from scgv.qtviews.profiles_window import ShowProfilesWindow


class ProfilesActions(QWidget):

    def __init__(self, main, *args, **kwargs):
        super(ProfilesActions, self).__init__(*args, **kwargs)
        self.main = main

        self.profiles = []
        layout = QVBoxLayout(self)
        self.profiles_list = QListWidget(self)
        layout.addWidget(self.profiles_list)
        self.profiles_show_button = QPushButton("Profiles Show")
        self.profiles_show_button.clicked.connect(
            self.on_profiles_show
        )
        layout.addWidget(self.profiles_show_button)

        self.profiles_clear_button = QPushButton("Profiles Clear")
        self.profiles_clear_button.clicked.connect(
            self.on_profiles_clear
        )
        layout.addWidget(self.profiles_clear_button)

        self.profiles_add_button = QPushButton("Profiles Add")
        self.profiles_add_button.clicked.connect(
            self.on_profiles_add
        )
        layout.addWidget(self.profiles_add_button)

        self.model = None

    def set_model(self, model):
        self.model = model

    def on_profile_selected(self, profile, *args, **kwargs):
        if profile is None or profile in self.profiles:
            return
        print(profile)
        assert profile is not None

        self.profiles_list.addItem(profile)
        self.profiles.append(profile)

    def on_profiles_clear(self, *args, **kwargs):
        self.profiles_list.clear()
        self.profiles = []

    def on_profiles_show(self, *args, **kwargs):
        if not self.profiles:
            return
        profiles = self.profiles[:]
        self.profiles_list.clear()
        self.profiles = []

        show_profiles = ShowProfilesWindow(
            self.model, profiles, self.main
        )
        show_profiles.show()

    def on_profiles_add(self, *args, **kwargs):
        if self.model is None:
            return
        profile, ok_pressed = QInputDialog.getText(
            self.main, "SCGV Add Profile", "Profile:", QLineEdit.Normal, ""
        )
        if not ok_pressed or not profile:
            return
        if profile not in self.model.column_labels:
            print(
                "profile not found in current case:",
                profile, self.model.column_labels)
            return
        self.on_profile_selected(profile)
