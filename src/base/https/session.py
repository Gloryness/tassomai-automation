import time
import subprocess
import asyncio
import requests
import random
import sys
import logging, traceback

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QObject, pyqtSignal

from app import github_db, __version__

from base.common import (
    Variables,
    establishConnection,
    convert_to_time,
    calculate_percentage,
    retreive_temp_data
)
from base.https.tassomai import Tassomai

class Session(QObject):

    logger = pyqtSignal(str, dict)
    show = pyqtSignal()
    close = pyqtSignal()

    def __init__(self, base, parent=None):
        super().__init__(parent)
        self.running = False
        self.shownStats = False
        self.ui = base
        self.database = base.database
        self.cache = base.cache

    def actually_start(self):
        asyncio.run(self.start())

    async def start(self):
        """
        Start the Session.
        """
        self.ui.ui.table.clearContents()
        for i in range(6):
            self.ui.ui.table.setItem(0, i, QTableWidgetItem())
            self.ui.ui.table.setItem(1, i, QTableWidgetItem())
        self.running = True
        self.ui.ui.startButton.setEnabled(False)
        self.ui.ui.stopButton.setEnabled(True)

        self.email = self.ui.ui.emailTassomai.text()
        self.password = self.ui.ui.passwordTassomai.text()
        self.maxQuizes = self.ui.ui.maxQuizes.value()
        self.dailyGoal = self.ui.ui.dailyGoal.isChecked()
        self.bonusGoal = self.ui.ui.bonusGoal.isChecked()
        self.row = self.ui.row
        self.correct = 0
        self.incorrect = 0
        self.quizes = 0
        self.until = 0
        self.until_incorrect = self.ui.ui.randomnessAmount.value()

        if '@' not in self.email:
            self.logger.emit('TYPES=[(#c8001a, BOLD), Invalid email.]', {})
            print("Invalid email.")
            return
        if len(self.password) < 1:
            self.logger.emit('TYPES=[(#c8001a, BOLD), Must include password.]', {})
            print("Must include password.")
            return

        self.timer = time.perf_counter()

        self.cache.store({'email': self.email, 'password': self.password})

        def connect():
            self.logger.emit('TYPES=[(#0066cc, BOLD), Establishing a connection...]', {})
            print("Establishing a connection...")
            r = establishConnection()
            if r:
                self.logger.emit('TYPES=[(#0c5d09, BOLD), Successfully established connection.]', {'newlinesafter': 2})
                print("Successfully established connection.\n")
            else:
                self.logger.emit('TYPES=[(#c8001a, BOLD), Unable to establish connection.]', {})
                print("Unable to establish connection.")
                time.sleep(0.5)
                connect()
        connect()

        if __version__ != (version := self.get_version()):
            self.logger.emit('TYPES=[(#c8001a, BOLD), Your Tassomai Automation is outdated! '
                             ''f'Please update to the newest version v{version} for better performance.]', {})
            print(f"Your Tassomai Automation is outdated! Please update to the newest version v{version} for better performance.")
            return

        subprocess.call([github_db, '-p', self.database.folder, '-g'], shell=True, stdout=sys.stdout)
        content = retreive_temp_data(self.database.folder)
        self.database.store(content)

        self.logger.emit('TYPES=[(BOLD, #000000), Successfully updated local database by fetching the Private Answers Database!]', {'newlinesafter': 2})
        print("Successfully updated local database by fetching the Private Answers Database!\n")

        if not self.running:
            return

        self.tassomai = Tassomai(self.database.all())
        await self.tassomai.login(self.email, self.password) # logging in

        if not self.running:
            return

        self.logger.emit('TYPES=[(#0c5d09, BOLD), Successfully logged into Tassomai.]', {})
        print("Successfully logged into Tassomai.")

        await asyncio.sleep(2.00)

        loop = 1
        try:
            for quiz in range(self.maxQuizes):
                if not self.running:
                    subprocess.call([github_db, '-p', self.database.folder, '-g'], shell=True, stdout=sys.stdout)
                    content = retreive_temp_data(self.database.folder)
                    content.update(self.tassomai.database)
                    database = {key: value for key, value in
                                sorted(content.items(), key=lambda item: item[0])}
                    self.database.store(database)
                    return
                if self.tassomai.is_complete and self.dailyGoal:
                    break
                if self.tassomai.is_bonus_complete and self.bonusGoal:
                    break

                self.logger.emit(f'COLOR=(#0c5d09, Starting up quiz {quiz+1}.)', {'newlinesbefore': 1})
                print(f"\nQuiz {quiz+1}")

                time.sleep(0.50)

                self.quiz_data = await self.tassomai.extract_quiz_data()

                title = self.tassomai.title
                self.logger.emit(title, {'color': '#7214ff', 'bold': True, 'newlinesafter': 2})
                print(f"{title}\n")

                quiz_timer = time.perf_counter()

                for index, question in enumerate(self.quiz_data['questions']):
                    force_incorrect = False
                    if self.ui.ui.randomness.isChecked():
                        if self.until == self.until_incorrect:
                            self.until = 0
                            force_incorrect = True
                    if '  ' in question['text']:
                        question['text'] = question['text'].replace("  ", " ")
                    question_data, database = await self.tassomai.answer_question(Variables(question, force_incorrect))
                    item = self.ui.ui.table.item(self.row, 0)
                    if item is None:
                        for i in range(6):
                            self.ui.ui.table.setItem(self.row, i, QTableWidgetItem())
                        item = self.ui.ui.table.item(self.row, 0)
                    item2 = self.ui.ui.table.item(self.row, 1)
                    item3 = self.ui.ui.table.item(self.row, 2)
                    item4 = self.ui.ui.table.item(self.row, 3)
                    item5 = self.ui.ui.table.item(self.row, 4)
                    item6 = self.ui.ui.table.item(self.row, 5)
                    item.setText(str(loop))
                    item2.setText(str(index+1))
                    item3.setText(question_data['question'])
                    item4.setText(str(question_data['correct']))
                    item5.setText(str(question_data['time'])+'s')
                    item6.setText(' **OR** '.join(question_data['answer']))
                    self.logger.emit(f'Question {index+1}: {question_data["question"]}', {'color': '#0c5d09', 'bold': True})
                    self.logger.emit(f'TYPES=[(BOLD, #0066cc), Correct:] TYPES=[(BOLD, '
                                     f'{"#0c5d09" if question_data["correct"] else "#c8001a"}), '
                                     f'{question_data["correct"]}]', {})
                    self.row += 1
                    self.ui.row = self.row
                    if question_data['correct']:
                        self.correct += 1
                    else:
                        self.incorrect += 1
                    if self.ui.ui.delay.isChecked():
                        if self.ui.ui.whenDelay.currentText() == "question":
                            if self.ui.ui.amountOfDelay.value() == 0 and self.ui.ui.amountOfDelay2.value() == 0:
                                rand = round(random.uniform(1, 4), 2)
                            elif self.ui.ui.amountOfDelay.value() == self.ui.ui.amountOfDelay2.value():
                                rand = self.ui.ui.amountOfDelay.value()
                            elif self.ui.ui.amountOfDelay.value() != self.ui.ui.amountOfDelay2.value():
                                rand = round(random.uniform(self.ui.ui.amountOfDelay.value(), self.ui.ui.amountOfDelay2.value()), 2)
                            item5.setText(f"{float(question_data['time']) + rand}s")
                            await asyncio.sleep(rand)
                    self.until += 1

                end_time = time.perf_counter() - quiz_timer
                print(f"Completed quiz {loop} in {end_time:0.2f}s")
                self.logger.emit(f"Completed quiz {loop} in {end_time:0.2f}s", {'color': '#7214ff', 'bold': True})
                print(len(self.database.all()), "questions answered!\n")

                loop += 1

                if not self.running:
                    subprocess.call([github_db, '-p', self.database.folder, '-g'], shell=True, stdout=sys.stdout)
                    content = retreive_temp_data(self.database.folder)
                    content.update(self.tassomai.database)
                    database = {key: value for key, value in
                                sorted(content.items(), key=lambda item: item[0])}
                    self.database.store(database)
                    return

                self.quizes += 1

                if self.ui.ui.delay.isChecked():
                    if self.ui.ui.whenDelay.currentText() == "quiz":
                        if self.ui.ui.amountOfDelay.value() == 0 and self.ui.ui.amountOfDelay2.value() == 0:
                            rand = round(random.uniform(1, 4), 2)
                        elif self.ui.ui.amountOfDelay.value() == self.ui.ui.amountOfDelay2.value():
                            rand = self.ui.ui.amountOfDelay.value()
                        elif self.ui.ui.amountOfDelay.value() != self.ui.ui.amountOfDelay2.value():
                            rand = round(random.uniform(self.ui.ui.amountOfDelay.value(), self.ui.ui.amountOfDelay2.value()), 2)
                        await asyncio.sleep(rand)

        except:
            logging.error(traceback.format_exc())

        subprocess.call([github_db, '-p', self.database.folder, '-g'], shell=True, stdout=sys.stdout)
        content = retreive_temp_data(self.database.folder)
        content.update(self.tassomai.database)
        database = {key: value for key, value in
                    sorted(content.items(), key=lambda item: item[0])}

        self.database.store(database)

        self.shownStats = True
        self.show_stats()

        self.ui.terminate_session()

    def get_version(self):
        req = requests.get('https://raw.githubusercontent.com/Gloryness/tassomai-automation/master/version.txt')
        return req.text.strip()

    def show_stats(self):
        if self.ui.showStats:
            self.show.emit()
        print("\n\nTassomai Automation Complete!")
        print("Loading STATS...")

        timer = convert_to_time(round((time.perf_counter() - self.timer)))
        daily_goal = f'- Daily Goal: TYPES=[(BOLD, {"#0c5d09" if self.tassomai.is_complete else "#c8001a"}),' \
                     f' {"Complete" if self.tassomai.is_complete else "Incomplete"}]'
        bonus_goal = f'- Bonus Goal: TYPES=[(BOLD, {"#0c5d09" if self.tassomai.is_bonus_complete else "#c8001a"}),' \
                     f' {"Complete" if self.tassomai.is_bonus_complete else "Incomplete"}]'
        level = self.tassomai.level
        percentage = calculate_percentage(self.tassomai.level_progress, self.tassomai.level_total)
        quizes = self.quizes
        correct = self.correct
        incorrect = self.incorrect

        self.logger.emit(f'COLOR=(#0066cc, Tassomai Automation Complete!)', {'newlinesbefore': 1})
        self.logger.emit(f'STATS:', {'color': '#7214ff', 'bold': True})
        self.logger.emit(f'- Time: TYPES=[(BOLD, #0c5d09), {timer}]', {})
        self.logger.emit(daily_goal, {})
        self.logger.emit(bonus_goal, {})
        self.logger.emit(f'- Level: TYPES=[(BOLD, #0c5d09), {level} ( {percentage}% )]', {})
        self.logger.emit(f'- Finished Quizes: TYPES=[(BOLD, #0c5d09), {quizes}]', {})
        self.logger.emit(f'- Total Correct: TYPES=[(BOLD, #0c5d09), {correct}]', {})
        self.logger.emit(f'- Total Incorrect: TYPES=[(BOLD, #c8001a), {incorrect}]', {})
        print(f'STATS:')
        print(f'- Time: {timer}')
        print(f'- Daily Goal: {"Complete" if self.tassomai.is_complete else "Incomplete"}')
        print(f'- Bonus Goal: {"Complete" if self.tassomai.is_bonus_complete else "Incomplete"}')
        print(f'- Level: {level} ( {percentage}% )')
        print(f'- Finished Quizes: {quizes}')
        print(f'- Total Correct: {correct}')
        print(f'- Total Incorrect: {incorrect}')
        print("Successfully loaded STATS.")
        if self.ui.shouldClose:
            print("-- Exiting --")
            self.close.emit()