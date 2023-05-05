import time
import random
import keyboard
import backup_ui_management
import model_manager

incanmodel = model_manager.ModelManager().get_model('t95_wisps')
serenmodel = model_manager.ModelManager().get_model('desert_sandstone')

class DivinationBot:
    def __init__(self):
        """
        Initialize the DivinationBot class.
        """
        self.inventories_converted = 0
        self.start_time = time.time() 
        # Configure max login time, at which all activity should cease and account should fade to logout.
        self.MAX_LOGIN_TIME = random.uniform(5 * 3600 + 50 * 60, 6 * 3600 + 10 * 60)
        # Configure max single-activity train time, at which point a new activity should be found.
        self.MAX_TRAIN_TIME = random.uniform(27 * 60, 35 * 60)
        # Activity time begins now.
        self.TRAIN_START_TIME = time.time()

    def harvest_wisps(self):
        """
        Find and click on inactive t95 wisps to harvest them.
        """
        backup_ui_management.find_and_click('inactive_t95_wisp', incanmodel)

    def exchange_wisps(self):
        """
        Find and click on the crater to exchange wisps.
        """
        backup_ui_management.find_and_click('crater', incanmodel)
        self.inventories_converted += 1
        print(f'Inventories converted: {self.inventories_converted}')

    def train(self):
        """
        Train divination by harvesting and exchanging wisps.
        Retry the process within a specified timeout.
        """
        retry_timeout = 20
        start_time = time.monotonic()

        while time.monotonic() - start_time < retry_timeout:
            try:
                self.harvest_wisps()
                sleep_duration1 = random.uniform(46, 65)
                print(f'sleeping for {sleep_duration1:.1f} seconds.')
                time.sleep(sleep_duration1)

                # Uncomment the following lines to enable continuous checking for Seren Spirits and Chronicles
                # while time.monotonic() - start_check_time < check_duration:
                #     if backup_ui_management.check_for('seren_spirit', serenmodel):
                #         backup_ui_management.find_and_click('seren_spirit', serenmodel)
                #     if backup_ui_management.check_for('chronicle', chroniclemodel):
                #         backup_ui_management.find_and_click('chronicle', chroniclemodel)
                #     time.sleep(0.1)  # Add a short sleep to avoid excessive CPU usage

                self.exchange_wisps()
                sleep_duration2 = random.uniform(30, 35)
                print(f'sleeping for {sleep_duration2:.1f} seconds.')
                time.sleep(sleep_duration2)
                break
            except TimeoutError as e:
                print(f'{e}. Retrying...')
        else:
            print("Could not complete action within the retry time limit. Terminating the script.")
            exit()

    def time_to_stop(self):
        """
        Check if the bot should stop running based on the elapsed time.
        """
        elapsed_time = time.time() - self.start_time
        return elapsed_time >= self.MAX_LOGIN_TIME

    def time_to_pause(self):
        """
        Check if the bot should pause training based on the elapsed training time.
        """
        elapsed_train_time = time.time() - self.TRAIN_START_TIME
        return elapsed_train_time >= self.MAX_TRAIN_TIME

    def gather_wisps(self):
        """
        Continuously gather wisps and exchange them at the crater.
        Pause and stop the bot based on elapsed time.
        """
    
        while not self.time_to_stop():
            if keyboard.is_pressed('q'):  # Check if 'q' is pressed
                break

            if self.time_to_pause():
                print("Pausing for 3 minutes.")
                time.sleep(3 * 60)
                self.TRAIN_START_TIME = time.time()
                self.MAX_TRAIN_TIME = random.uniform(27 * 60, 35 * 60)
            else:
                self.train()

if __name__ == "__main__":
    bot = DivinationBot()
    bot.gather_wisps()
