import random
import requests
import time
from base.common import prepare, gather_answers, clean_string

class Tassomai:
    """
    Tassomai class for managing the automation.
    """
    def __init__(self, database):
        self.database = database

    async def login(self, email, password):
        """
        Log into the Tassomai page.
        """
        self.session = requests.session()
        params = {
            "email": email,
            "password": password,
            "capabilities": {"image": True, "isMobile": False, "mathjax": True}
        }
        login = self.session.post('https://kolin.tassomai.com/api/user/login/', data=params)
        try:
            auth = 'Bearer ' + login.json()['token']
        except:
            print(f'Error: \n{login.json()}')

        self.headers = {
            'Accept': "application/json; version=1.5",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-GB, en;q=0.5",
            'Host': 'kolin.tassomai.com',
            'Scheme': 'https',
            'Authorization': auth,
            'Origin': 'https://app.tassomai.com',
            'Referer': 'https://app.tassomai.com/login',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
        }

    async def extract_quiz_data(self):
        extra = await self._extract_extra_data()

        num = random.choice([0, 1])

        params = {
            "capabilities": {"image": True, "isMobile": False, "mathjax": True},
            "playlist": extra['quizzes'][num]['playlistId'],
            "course": extra['quizzes'][num]['courseId'],
            "was_recommended": True
        }

        while True:
            self.quiz_data = self.session.post('https://kolin.tassomai.com/api/quiz/', headers=self.headers,
                                               data=params).json()
            if 'questions' not in self.quiz_data:
                continue
            break
        return self.quiz_data

    async def _extract_extra_data(self):
        extra = self.session.get('https://kolin.tassomai.com/api/quiz/next/1/?capabilities=%7B%22'
                                 'image%22:true,%22isMobile%22:false,%22mathjax%22:false%7D', headers=self.headers)
        return extra.json()

    def check_daily_goal(self):
        """
        Check your daily goal.
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['goals']['disciplines']['1']['goal']['progress'])

    def daily_goal(self):
        """
        See the daily goal you need to achieve.
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['goals']['disciplines']['1']['goal']['target'])

    def check_bonus_goal(self):
        """
        Check your daily goal.
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['goals']['disciplines']['1']['stretch_goal']['progress'])


    def bonus_goal(self):
        """
        See the daily goal you need to achieve.
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['goals']['disciplines']['1']['stretch_goal']['target'])


    @property
    def is_complete(self):
        """
        Check if daily goal is complete
        """
        return [True if self.check_daily_goal() >= self.daily_goal() else False][0]

    @property
    def is_bonus_complete(self):
        """
        Check if bonus goal is complete
        """
        return [True if self.check_bonus_goal() >= self.bonus_goal() else False][0]

    @property
    def title(self):
        """
        Check the title of the quiz.
        """
        return self.quiz_data['title']

    @property
    def level(self):
        """
        Return your current level
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['level']['number'])

    @property
    def level_progress(self):
        """
        Return your current level progress
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['level']['pointsCovered'])

    @property
    def level_total(self):
        """
        Return the progress needed to reach the next level
        """
        goals = self.session.get('https://kolin.tassomai.com/api/daily-goals/', headers=self.headers)
        return int(goals.json()['level']['pointsTotal'])

    @property
    def sections(self):
        """
        Amount of sections
        """
        return len(self.quiz_data['questions'])

    async def answer_question(self, data):
        question_timer = time.perf_counter()
        current_answers = gather_answers(data.question['answers'])
        sc = str(current_answers)

        if data.question['text'] not in self.database:
            to_answer = random.choice(data.question['answers'])
            self.database[data.question['text']] = {sc: prepare(data.question['answers'])}
        else:
            if sc not in self.database[data.question['text']]:
                self.database[data.question['text']][sc] = prepare(data.question['answers'])
            for answer in data.question['answers']:
                if data.question['text'] in self.database:
                    if clean_string(answer['text']) != self.database[data.question['text']][sc] and data.force_incorrect:
                        to_answer = answer
                    if clean_string(answer['text']) == self.database[data.question['text']][sc]:
                        if data.force_incorrect:
                            continue
                        to_answer = answer
                        break
            try:
                to_answer
            except:
                if data.question['text'] in self.database:
                    if type(self.database[data.question['text']][sc]) == dict:
                        indexes = list(filter(lambda k: k is not None,
                                   [index if question_['text'] in self.database[data.question['text']][sc] else None
                                   for index, question_ in enumerate(data.question['answers'])]))
                        if len(indexes) == 0:
                            to_answer = data.question['answers'][random.randint(0, 3)]
                        else:
                            to_answer = data.question['answers'][random.choice(indexes)]
                    else:
                        to_answer = data.question['answers'][random.randint(0, 3)]
                else:
                    to_answer = data.question['answers'][random.randint(0, 3)]

        params = {
            "answer_id": to_answer['id']
        }

        print(f'-----------{self.quiz_data["questions"].index(data.question)+1}-----------')
        print(data.question['text'])
        print("Answering:", clean_string(to_answer['text']), ':', to_answer['id'])
        while True:
            try:
                answer = self.session.post(f'https://kolin.tassomai.com/api/answer/{data.question["asking_id"]}/',
                                    headers=self.headers, data=params).json()
                if 'is_correct' not in answer:
                    continue
                break
            except:
                continue
        print("Correct" if answer['is_correct'] else "Incorrect")

        end_time = time.perf_counter() - question_timer
        print(f"Completed question {self.quiz_data['questions'].index(data.question)+1} in {end_time:0.2f}s\n\n")

        if answer['is_correct']:
            if data.question['text'] in self.database:
                self.database[data.question['text']][sc] = clean_string(to_answer['text'])
            else:
                self.database[data.question['text']] = {sc: clean_string(to_answer['text'])}
        else:
            if data.question['text'] in self.database:
                if type(self.database[data.question['text']][sc]) == dict:
                    try:
                        del self.database[data.question['text']][sc][clean_string(to_answer['text'])]

                        if len(self.database[data.question['text']][sc]) == 1:
                            self.database[data.question['text']][sc] = clean_string(list(self.database[data.question['text']][sc].keys())[0])
                    except:
                        pass
            else:
                self.database[data.question['text']] = {sc: prepare(data.question['answers'])}
                del self.database[data.question['text']][sc][clean_string(to_answer['text'])]
        if type(self.database[data.question['text']][sc]) == dict:
            answers = [item for item in self.database[data.question['text']][sc]]
        else:
            answers = [self.database[data.question['text']][sc]]

        return {'question': data.question['text'], 'correct': answer['is_correct'], 'time': f"{end_time:0.2f}", 'answer': answers}, self.database
