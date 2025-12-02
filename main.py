# quiz_app.py
import json
import os
import random
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results.json"
MIN_QUESTIONS = 10
MAX_QUESTIONS = 30

PRELOADED_QUESTIONS = [
    {"question": "What is the SI unit of force?", "options": ["Pascal", "Joule", "Newton", "Watt"], "answer_index": 2, "subject": "physics", "level": "easy"},
    {"question": "Which of the following is a non-renewable resource?", "options": ["Coal", "Solar energy", "Biomass", "Wind energy"], "answer_index": 0, "subject": "science", "level": "easy"},
    {"question": "What is the primary function of the human digestive system?", "options": ["To regulate temperature", "To circulate blood", "To break down food and absorb nutrients", "To provide oxygen to the body"], "answer_index": 2, "subject": "biology", "level": "easy"},
    {"question": "Which part of the plant is responsible for photosynthesis?", "options": ["Roots", "Leaves", "Stem", "Flowers"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "What is the chemical formula of water?", "options": ["H2O", "CO2", "NaCl", "O2"], "answer_index": 0, "subject": "chemistry", "level": "easy"},
    {"question": "What is the atomic number of an element?", "options": ["Number of neutrons", "Protons+Neutrons", "Number of protons", "Number of electrons"], "answer_index": 2, "subject": "chemistry", "level": "easy"},
    {"question": "What is the purpose of a fuse in a circuit?", "options": ["To store energy", "To regulate voltage", "To increase current", "To protect the circuit"], "answer_index": 3, "subject": "physics", "level": "easy"},
    {"question": "Which part of the brain controls balance?", "options": ["Medulla", "Thalamus", "Cerebellum", "Cerebrum"], "answer_index": 2, "subject": "biology", "level": "easy"},
    {"question": "Which is asexual reproduction?", "options": ["Needs organs", "Two parents", "Only in plants", "Genetically identical"], "answer_index": 3, "subject": "biology", "level": "easy"},
    {"question": "Which gas causes greenhouse effect?", "options": ["Carbon dioxide", "Oxygen", "Hydrogen", "Nitrogen"], "answer_index": 0, "subject": "science", "level": "easy"},
    {"question": "What is pH of pure water?", "options": ["7", "5", "9", "11"], "answer_index": 0, "subject": "chemistry", "level": "easy"},
    {"question": "Lens used for myopia?", "options": ["Cylindrical", "Concave", "Convex", "Bifocal"], "answer_index": 1, "subject": "physics", "level": "easy"},
    {"question": "Hemoglobin function?", "options": ["Fight infections", "Clot blood", "Carry oxygen", "Digest glucose"], "answer_index": 2, "subject": "biology", "level": "easy"},
    {"question": "Purpose of vaccines?", "options": ["Heal wounds", "Provide nutrition", "Prevent infections", "Relieve pain"], "answer_index": 2, "subject": "biology", "level": "easy"},
    {"question": "Which vitamin is ascorbic acid?", "options": ["Vitamin C", "Vitamin D", "Vitamin A", "Vitamin B"], "answer_index": 0, "subject": "biology", "level": "easy"},
    {"question": "Which is a chemical reaction?", "options": ["Melting ice", "Boiling water", "Dissolving sugar", "Burning wood"], "answer_index": 3, "subject": "chemistry", "level": "easy"},
    {"question": "A + B → AB is?", "options": ["Double displacement", "Displacement", "Combination", "Decomposition"], "answer_index": 2, "subject": "chemistry", "level": "easy"},
    {"question": "HCl + NaOH gives?", "options": ["Sodium sulfate", "Sodium chloride", "Sodium carbonate", "Sodium nitrate"], "answer_index": 1, "subject": "chemistry", "level": "easy"},
    {"question": "Gas evolved when acid reacts with metal?", "options": ["CO2", "Oxygen", "Nitrogen", "Hydrogen"], "answer_index": 3, "subject": "chemistry", "level": "easy"},
    {"question": "Iron with moist air forms?", "options": ["Rust", "Aluminum oxide", "Copper", "Zinc"], "answer_index": 0, "subject": "chemistry", "level": "easy"},
    {"question": "Metal used in wiring?", "options": ["Zinc", "Copper", "Lead", "Iron"], "answer_index": 1, "subject": "physics", "level": "easy"},
    {"question": "Which is an alcohol?", "options": ["Propane", "Butane", "Methane", "Ethanol"], "answer_index": 3, "subject": "chemistry", "level": "easy"},
    {"question": "Organ that filters blood?", "options": ["Heart", "Kidney", "Lungs", "Liver"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "Water transport in plants?", "options": ["Xylem", "Phloem", "Root hairs", "Leaves"], "answer_index": 0, "subject": "biology", "level": "easy"},
    {"question": "Fusion of gametes is called?", "options": ["Regeneration", "Fertilization", "Pollination", "Fragmentation"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "Fertilizer production uses?", "options": ["Sulphur", "Phosphorus", "Nitrogen", "All"], "answer_index": 3, "subject": "chemistry", "level": "easy"},
    {"question": "Purpose of meiosis?", "options": ["Identical cells", "Reduce chromosomes", "New offspring", "Produce energy"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "Sex of baby determined by?", "options": ["Father", "Environment", "Mother", "Genes"], "answer_index": 0, "subject": "biology", "level": "easy"},
    {"question": "Law of reflection?", "options": ["i = r(refraction)", "i = r(reflection)", "i > r", "None"], "answer_index": 1, "subject": "physics", "level": "easy"},
    {"question": "Air to water light bends?", "options": ["Towards normal", "Straight", "Away from normal", "Reflects"], "answer_index": 0, "subject": "physics", "level": "easy"},
    {"question": "Focal length of lens?", "options": ["Object-lens", "Lens-focus", "Image-lens", "Lens-retina"], "answer_index": 1, "subject": "physics", "level": "easy"},
    {"question": "Dispersion through prism due to?", "options": ["Refraction", "Reflection", "Interference", "Scattering"], "answer_index": 0, "subject": "physics", "level": "easy"},
    {"question": "SI unit of current?", "options": ["Volt", "Ohm", "Ampere", "Coulomb"], "answer_index": 2, "subject": "physics", "level": "easy"},
    {"question": "Measures current?", "options": ["Voltmeter", "Ohmmeter", "Galvanometer", "Ammeter"], "answer_index": 3, "subject": "physics", "level": "easy"},
    {"question": "Solenoid produces?", "options": ["Gravity", "Magnetic field", "Electric field", "Sound"], "answer_index": 1, "subject": "physics", "level": "easy"},
    {"question": "Main component of smog?", "options": ["CO", "SO2", "NO2", "Water vapor"], "answer_index": 0, "subject": "science", "level": "easy"},
    {"question": "Cause of acid rain?", "options": ["CO2", "Ozone depletion", "NOx and SO2", "Pesticides"], "answer_index": 2, "subject": "science", "level": "easy"},
    {"question": "Decomposers?", "options": ["Plants", "Animals", "Herbivores", "Microorganisms"], "answer_index": 3, "subject": "biology", "level": "easy"},
    {"question": "Blue litmus in acid turns?", "options": ["Blue to red", "Red to blue", "No change", "Red to yellow"], "answer_index": 0, "subject": "chemistry", "level": "easy"},
    {"question": "Function of stomata?", "options": ["Absorb water", "Release oxygen", "Take CO2", "Produce food"], "answer_index": 2, "subject": "biology", "level": "easy"},
    {"question": "Not part of circulatory system?", "options": ["Kidneys", "Heart", "Blood", "Lungs"], "answer_index": 0, "subject": "biology", "level": "easy"},
    {"question": "Plants make food by?", "options": ["Respiration", "Photosynthesis", "Digestion", "Transpiration"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "Ore of aluminum?", "options": ["Bauxite", "Hematite", "Galena", "Magnetite"], "answer_index": 0, "subject": "chemistry", "level": "easy"},
    {"question": "Longest cell?", "options": ["Nerve cell", "RBC", "WBC", "Muscle cell"], "answer_index": 0, "subject": "biology", "level": "easy"},
    {"question": "Master gland?", "options": ["Thyroid", "Pituitary", "Pancreas", "Adrenal"], "answer_index": 1, "subject": "biology", "level": "easy"},
    {"question": "Speed of light?", "options": ["4e8", "2e8", "1e8", "3e8"], "answer_index": 3, "subject": "physics", "level": "easy"},
    {"question": "Controls amount of light in eye?", "options": ["Retina", "Cornea", "Iris", "Optic nerve"], "answer_index": 2, "subject": "biology", "level": "easy"},

    # HARD JEE QUESTIONS
    {"question": "Force needed for same extension if area becomes 4A?", "options": ["3F", "5F", "9F", "16F"], "answer_index": 3, "subject": "physics", "level": "hard"},
    {"question": "Temp when A+C mixed?", "options": ["130/11", "140/11", "121/12", "90/12"], "answer_index": 1, "subject": "physics", "level": "hard"},
    {"question": "Work done on soap bubble increase radius 4cm to 7cm?", "options": ["4pi", "0.2pi", "2pi", "0.8pi"], "answer_index": 3, "subject": "physics", "level": "hard"},
    {"question": "Height where g becomes g/9?", "options": ["2R", "R/sqrt2", "R/2", "sqrt2 R"], "answer_index": 0, "subject": "physics", "level": "hard"},
    {"question": "MOI relation of discs?", "options": ["32X", "16X", "X", "64X"], "answer_index": 3, "subject": "physics", "level": "hard"},
    {"question": "Incorrect gas mixture statement?", "options": ["KE equal", "RMS 4x", "Pressure 4x", "Molecules 8x"], "answer_index": 2, "subject": "physics", "level": "hard"},
    {"question": "Rod-ball angular speed?", "options": ["22", "13.5", "4.4", "2.3"], "answer_index": 2, "subject": "physics", "level": "hard"},
    {"question": "Dimensional formula of diffusivity?", "options": ["L2T-1", "LT-1", "L2T2", "LT-3"], "answer_index": 0, "subject": "physics", "level": "hard"},
    {"question": "Dielectric constant of liquid?", "options": ["3", "7", "1.5", "2"], "answer_index": 3, "subject": "physics", "level": "hard"}
]



# ---------------- FILE HELPERS ----------------
def save_questions(questions):
    try:
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error saving questions:", e)

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        save_questions(PRELOADED_QUESTIONS)
        return PRELOADED_QUESTIONS[:]
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        fixed = []
        for q in data:
            if "subject" not in q:
                q["subject"] = "general"
            if "level" not in q:
                q["level"] = "easy"
            fixed.append(q)
        # ensure file normalized
        save_questions(fixed)
        return fixed
    except Exception as e:
        print("Error loading questions:", e)
        return PRELOADED_QUESTIONS[:]

def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []

def save_results(results):
    try:
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error saving results:", e)

def append_result(result_record):
    results = load_results()
    results.append(result_record)
    save_results(results)

# ---------------- KIVY KV ----------------
KV = """
#:import dp kivy.metrics.dp

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.05,0.05,0.08,1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "Quiz App"
            font_size: "28sp"
            bold: True
            color: 1,1,1,1
            size_hint_y: None
            height: dp(40)

        Label:
            text: "Practice · Analyse · Improve"
            font_size: "16sp"
            color: 0.8,0.8,0.8,1
            size_hint_y: None
            height: dp(30)

        Widget:

        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(200)
            spacing: dp(12)

            Button:
                text: "Start Quiz"
                font_size: "18sp"
                background_normal: ""
                background_color: 0.27,0.34,0.8,1
                on_release: app.go_settings()

            Button:
                text: "View Past Results"
                font_size: "18sp"
                background_normal: ""
                background_color: 0.18,0.18,0.25,1
                on_release: app.go_history()

            Button:
                text: "Exit"
                font_size: "18sp"
                background_normal: ""
                background_color: 0.4,0.1,0.1,1
                on_release: app.stop()

        Widget:

<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.05,0.05,0.08,1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Button:
                text: "< Back"
                size_hint_x: None
                width: dp(100)
                background_normal: ""
                background_color: 0.18,0.18,0.25,1
                on_release: app.go_home()
            Label:
                text: "Quiz Settings"
                font_size: "20sp"
                color: 1,1,1,1

        Label:
            text: "Name:"
            color: 1,1,1,1
            size_hint_y: None
            height: dp(20)
        TextInput:
            id: name_field
            size_hint_y: None
            height: dp(40)
            multiline: False
            foreground_color: 1,1,1,1
            background_color: 0.15,0.15,0.2,1
            cursor_color: 1,1,1,1

        Label:
            text: "Subject filter (physics / chemistry / biology / science) – empty = ALL"
            text_size: self.width, None
            size_hint_y: None
            height: dp(40)
            color: 0.8,0.8,0.8,1
        TextInput:
            id: subject_field
            size_hint_y: None
            height: dp(40)
            multiline: False
            foreground_color: 1,1,1,1
            background_color: 0.15,0.15,0.2,1
            cursor_color: 1,1,1,1

        Label:
            text: "Level filter (easy / hard) – empty = ALL"
            size_hint_y: None
            height: dp(20)
            color: 0.8,0.8,0.8,1
        TextInput:
            id: level_field
            size_hint_y: None
            height: dp(40)
            multiline: False
            foreground_color: 1,1,1,1
            background_color: 0.15,0.15,0.2,1
            cursor_color: 1,1,1,1

        Label:
            text: "Number of questions (10–30)"
            size_hint_y: None
            height: dp(20)
            color: 0.8,0.8,0.8,1
        TextInput:
            id: num_field
            text: "10"
            size_hint_y: None
            height: dp(40)
            multiline: False
            input_filter: "int"
            foreground_color: 1,1,1,1
            background_color: 0.15,0.15,0.2,1
            cursor_color: 1,1,1,1

        Label:
            text: "Negative marks per wrong (e.g. 0.25, 0.33, 0)"
            size_hint_y: None
            height: dp(20)
            color: 0.8,0.8,0.8,1
        TextInput:
            id: neg_field
            text: "0"
            size_hint_y: None
            height: dp(40)
            multiline: False
            foreground_color: 1,1,1,1
            background_color: 0.15,0.15,0.2,1
            cursor_color: 1,1,1,1

        Label:
            id: info_label
            text: ""
            size_hint_y: None
            height: dp(20)
            color: 1,0.4,0.4,1

        Button:
            text: "Start Quiz"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: 0.27,0.34,0.8,1
            on_release: app.start_quiz()

<QuizScreen>:
    name: "quiz"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.05,0.05,0.08,1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Button:
                text: "< Cancel"
                size_hint_x: None
                width: dp(100)
                background_normal: ""
                background_color: 0.18,0.18,0.25,1
                on_release: app.cancel_quiz()
            Label:
                id: progress_label
                text: "Question 1/1"
                color: 1,1,1,1

        ScrollView:
            do_scroll_x: False
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(40)
                row_force_default: False

                Label:
                    id: question_label
                    text: "Question text here"
                    color: 1,1,1,1
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(20)

                Button:
                    id: opt1
                    text: "Option 1"
                    background_normal: ""
                    background_color: 0.18,0.18,0.25,1
                    on_release: app.select_option(0)
                Button:
                    id: opt2
                    text: "Option 2"
                    background_normal: ""
                    background_color: 0.18,0.18,0.25,1
                    on_release: app.select_option(1)
                Button:
                    id: opt3
                    text: "Option 3"
                    background_normal: ""
                    background_color: 0.18,0.18,0.25,1
                    on_release: app.select_option(2)
                Button:
                    id: opt4
                    text: "Option 4"
                    background_normal: ""
                    background_color: 0.18,0.18,0.25,1
                    on_release: app.select_option(3)

                Button:
                    text: "Next"
                    size_hint_y: None
                    height: dp(50)
                    background_normal: ""
                    background_color: 0.27,0.34,0.8,1
                    on_release: app.next_question()

<ResultScreen>:
    name: "result"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.05,0.05,0.08,1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Button:
                text: "< Home"
                size_hint_x: None
                width: dp(100)
                background_normal: ""
                background_color: 0.18,0.18,0.25,1
                on_release: app.go_home()
            Label:
                text: "Result"
                color: 1,1,1,1

        Label:
            id: result_label
            text: "Result summary..."
            color: 1,1,1,1
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1] + dp(20)

        Button:
            text: "View Past Results"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: 0.18,0.18,0.25,1
            on_release: app.go_history()

        Button:
            text: "Back to Home"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: 0.27,0.34,0.8,1
            on_release: app.go_home()

<HistoryScreen>:
    name: "history"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.05,0.05,0.08,1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            Button:
                text: "< Home"
                size_hint_x: None
                width: dp(100)
                background_normal: ""
                background_color: 0.18,0.18,0.25,1
                on_release: app.go_home()
            Label:
                text: "Past Results"
                color: 1,1,1,1

        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: history_box
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                row_default_height: dp(30)
                row_force_default: True
"""

# ---------------- Screens (empty classes) ----------------
class HomeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class QuizScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

# ---------------- Main App ----------------
class QuizApp(App):
    def build(self):
        self.title = "Quiz App"
        Builder.load_string(KV)
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(QuizScreen(name="quiz"))
        self.sm.add_widget(ResultScreen(name="result"))
        self.sm.add_widget(HistoryScreen(name="history"))

        self.quiz_state = None
        self.selected_option_index = None
        return self.sm

    # Navigation
    def go_home(self):
        self.sm.current = "home"

    def go_settings(self):
        self.sm.current = "settings"

    def go_history(self):
        self.refresh_history()
        self.sm.current = "history"

    def cancel_quiz(self):
        self.quiz_state = None
        self.selected_option_index = None
        self.sm.current = "home"

    # Start quiz
    def start_quiz(self):
        settings = self.sm.get_screen("settings")
        name = settings.ids.name_field.text.strip()
        subject = settings.ids.subject_field.text.strip().lower()
        level = settings.ids.level_field.text.strip().lower()
        num_text = settings.ids.num_field.text.strip()
        neg_text = settings.ids.neg_field.text.strip()
        info_label = settings.ids.info_label

        if not name:
            info_label.text = "Name is required."
            return

        questions = load_questions()
        filtered = []
        for q in questions:
            q_sub = q.get("subject", "").strip().lower()
            q_lvl = q.get("level", "").strip().lower()
            if subject and q_sub != subject:
                continue
            if level and q_lvl != level:
                continue
            filtered.append(q)

        if not filtered:
            info_label.text = "No questions for this filter."
            return

        available = len(filtered)
        try:
            n = int(num_text) if num_text else MIN_QUESTIONS
        except ValueError:
            n = MIN_QUESTIONS

        min_allowed = MIN_QUESTIONS if available >= MIN_QUESTIONS else 1
        max_allowed = MAX_QUESTIONS if available >= MAX_QUESTIONS else available

        if n < min_allowed:
            n = min_allowed
        if n > max_allowed:
            n = max_allowed

        try:
            neg_mark = float(neg_text) if neg_text else 0.0
            if neg_mark < 0:
                neg_mark = 0.0
        except ValueError:
            neg_mark = 0.0

        random.shuffle(filtered)
        selected = filtered[:n]

        self.quiz_state = {
            "name": name,
            "subject_filter": subject if subject else "ALL",
            "level_filter": level if level else "ALL",
            "questions": selected,
            "index": 0,
            "correct": 0,
            "wrong": 0,
            "neg_mark": neg_mark,
        }
        self.selected_option_index = None
        info_label.text = ""
        self.load_question()
        self.sm.current = "quiz"

    def load_question(self):
        if not self.quiz_state:
            return
        quiz_screen = self.sm.get_screen("quiz")
        qs = self.quiz_state["questions"]
        idx = self.quiz_state["index"]
        total = len(qs)
        q = qs[idx]

        quiz_screen.ids.question_label.text = q["question"]
        quiz_screen.ids.opt1.text = "1. " + q["options"][0]
        quiz_screen.ids.opt2.text = "2. " + q["options"][1]
        quiz_screen.ids.opt3.text = "3. " + q["options"][2]
        quiz_screen.ids.opt4.text = "4. " + q["options"][3]
        quiz_screen.ids.progress_label.text = f"Question {idx+1}/{total}"

        self.selected_option_index = None
        for btn in [quiz_screen.ids.opt1, quiz_screen.ids.opt2, quiz_screen.ids.opt3, quiz_screen.ids.opt4]:
            btn.background_color = (0.18, 0.18, 0.25, 1)

    def select_option(self, option_index):
        if not self.quiz_state:
            return
        self.selected_option_index = option_index
        quiz_screen = self.sm.get_screen("quiz")
        buttons = [quiz_screen.ids.opt1, quiz_screen.ids.opt2, quiz_screen.ids.opt3, quiz_screen.ids.opt4]
        for i, btn in enumerate(buttons):
            if i == option_index:
                btn.background_color = (0.27, 0.34, 0.8, 1)
            else:
                btn.background_color = (0.18, 0.18, 0.25, 1)

    def next_question(self):
        if not self.quiz_state:
            return
        if self.selected_option_index is None:
            # no toast - ignore click
            return

        qs = self.quiz_state["questions"]
        idx = self.quiz_state["index"]
        q = qs[idx]
        correct_index = q["answer_index"]

        if self.selected_option_index == correct_index:
            self.quiz_state["correct"] += 1
        else:
            self.quiz_state["wrong"] += 1

        self.quiz_state["index"] += 1

        if self.quiz_state["index"] >= len(qs):
            self.finish_quiz()
        else:
            self.load_question()

    def finish_quiz(self):
        st = self.quiz_state
        if not st:
            return

        correct = st["correct"]
        wrong = st["wrong"]
        total = len(st["questions"])
        marks_per_q = 1.0
        neg = st["neg_mark"]

        raw = correct * marks_per_q
        neg_loss = wrong * neg
        final_score = raw - neg_loss
        if final_score < 0:
            final_score = 0.0
        max_marks = total * marks_per_q
        percentage = (final_score / max_marks) * 100 if max_marks > 0 else 0.0

        result_record = {
            "name": st["name"],
            "subject_filter": st["subject_filter"],
            "level_filter": st["level_filter"],
            "correct": correct,
            "wrong": wrong,
            "total": total,
            "marks_per_question": marks_per_q,
            "negative_per_wrong": neg,
            "final_score": final_score,
            "percentage": percentage,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        append_result(result_record)

        result_screen = self.sm.get_screen("result")
        summary = (
            f"Name: {st['name']}\n"
            f"Subject: {st['subject_filter']}\n"
            f"Level: {st['level_filter']}\n\n"
            f"Correct: {correct}\n"
            f"Wrong: {wrong}\n"
            f"Final Marks: {final_score:.2f} / {max_marks:.2f}\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Negative: -{neg} per wrong"
        )
        result_screen.ids.result_label.text = summary

        self.quiz_state = None
        self.selected_option_index = None
        self.sm.current = "result"

    def refresh_history(self):
        history_screen = self.sm.get_screen("history")
        box = history_screen.ids.history_box
        box.clear_widgets()
        from kivy.uix.label import Label
        results = load_results()
        if not results:
            box.add_widget(Label(text="No results yet.", color=(1,1,1,1)))
            return
        for r in reversed(results):
            txt = (
                f"{r.get('timestamp','')} | "
                f"{r.get('name','')} | "
                f"{r.get('final_score',0):.1f}/{r.get('total',0)} "
                f"({r.get('percentage',0):.1f}%)"
            )
            box.add_widget(Label(text=txt, color=(1,1,1,1), halign="left"))
        
if _name_ == "_main_":
    QuizApp().run()
