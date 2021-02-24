import sys
import optparse
import atexit
import subprocess
import logging, traceback

from PyQt5.QtWidgets import QApplication
from youtube_dl.compat import compat_get_terminal_size
from app import github_db
from base.common import establishConnection, retreive_temp_data

columns = compat_get_terminal_size().columns # you could call this 'hipity hopity this is now my property'
max_width = columns if columns else 80
max_help_position = 80
fmt = optparse.IndentedHelpFormatter(width=max_width, max_help_position=max_help_position)

kw = {
    'formatter': fmt,
    'usage': '%prog [OPTIONS]',
    'conflict_handler': 'resolve'
}

parser = optparse.OptionParser(**kw)
parser.add_option('-h', '--help',
                  action='help',
                  help='Print this help message and exit')
parser.add_option('-u', '--username',
                  type=str,
                  help='Email for Tassomai',
                  default='')
parser.add_option('-p', '--password',
                  type=str,
                  help='Tassomai Password',
                  default='')
parser.add_option('--no-stats',
                  action='store_true',
                  help='Do not show the stats when finished.',
                  default=False)
parser.add_option('--close',
                  action='store_true',
                  help='Close when finished.',
                  default=False)
parser.add_option('--max-quizes',
                  metavar='NUMBER',
                  type=int,
                  help='Maximum number of quizes to do',
                  default=1000)
parser.add_option('--start',
                  action='store_true',
                  help='Automatically start the automation',
                  default=False)
parser.add_option('--gui-frameless',
                  action='store_true',
                  help='Make the GUI hidden but still runs in the background.',
                  default=False)
parser.add_option('--daily',
                  action='store_true',
                  help='Finish when daily goal is complete.',
                  default=False)
parser.add_option('--bonus',
                  action='store_true',
                  help='Finish when bonus goal is complete.',
                  default=False)
parser.add_option('--delay',
                  type=str,
                  help='Add a specified delay (use --delay-amount or by default its between 1-4) between '
                       'each quiz/question. Specify \'quiz\' or \'question\' in the params.',
                  default='none')
parser.add_option('--delay-amount',
                  metavar='DECIMAL(S)',
                  type=str,
                  help='The delay to use. e.g: --delay-amount=1.23,1.51 to randomise it OR --delay-amount=1 to be specific. '
                       'This only works when you\'ve used --delay aswell!',
                  default="0")
parser.add_option('--random',
                  metavar='NUMBER',
                  type=int,
                  help='Make it so you answer a question incorrectly every X questions.',
                  default=0)

(options, args) = parser.parse_args()

if __name__ == '__main__':
    try:
        from gui import Window

        app = QApplication(sys.argv)

        win = Window(show_stats=not options.no_stats, close=options.close)

        if not options.gui_frameless:
            win.show()
        if options.username != '':
            win.ui.emailTassomai.setText(options.username)
        if options.password != '':
            win.ui.passwordTassomai.setText(options.password)
        if options.delay != 'none':
            win.ui.delay.setChecked(True)
            if options.delay in ['quiz', 'question']:
                win.ui.whenDelay.setCurrentText(options.delay)
            if options.delay_amount != "0":
                if ',' in options.delay_amount:
                    try:
                        v1, v2 = tuple(map(lambda k: float(k), options.delay_amount.split(',')))
                    except:
                        win.ui.delay.setChecked(False)
                    win.ui.amountOfDelay.setValue(v1)
                    win.ui.amountOfDelay2.setValue(v2)
                else:
                    try: float(options.delay_amount)
                    except: win.ui.delay.setChecked(False)
                    amount = float(options.delay_amount) if float(options.delay_amount) <= 25.00 else 25.00
                    win.ui.amountOfDelay.setValue(amount)
                    win.ui.amountOfDelay2.setValue(amount)
        if options.random > 0:
            amount = options.random if options.random <= 600 else 600
            win.ui.randomness.setChecked(True)
            win.ui.randomnessAmount.setValue(amount)

        if options.daily and options.bonus:
            win.ui.bonusGoal.setChecked(True)
        else:
            win.ui.dailyGoal.setChecked(options.daily)
            win.ui.bonusGoal.setChecked(options.bonus)

        win.ui.maxQuizes.setValue(abs(options.max_quizes))

        @atexit.register
        def on_exit():
            if establishConnection():
                print('Updating private database...')
                subprocess.call([github_db, '-p', win.database.folder, '-g'], shell=True, stdout=sys.stdout)
                content = retreive_temp_data(win.database.folder)
                content.update(win.database.all())
                win.database.store(content)

                subprocess.call([github_db, '-e', win.database.filename], shell=True)
                print('Successfully updated!')
            else:
                print('Unable to update the private database.')

        if options.start:
            win.ui.startButton.click()

        sys.exit(app.exec())
    except Exception:
        if not traceback.format_exc().__contains__('SystemExit'):
            logging.error(traceback.format_exc())