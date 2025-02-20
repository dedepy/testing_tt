from imports import *
load_dotenv()

#Проверка аутентификации и авторизации пользователя
class Login:
    def __init__(self, url,username,password):
        self.url = url
        self.username = username  # Сохраняем имя пользователя
        self.password = password  # Сохраняем пароль
        self.driver = None
    def start_driver(self):
        #Инициализация драйвера
        options = Options()
        #options.add_argument("--headless=new")  # Запуск в фоновом режиме
        self.driver = webdriver.Chrome(options=options)

    def login(self,username,password):
        self.start_driver()
        self.driver.get(self.url)
        time.sleep(3)  # Ждём загрузку страницы
        #Ввод логина
        login =self.driver.find_element(By.XPATH,'//*[@id="user-name"]')
        login.send_keys(username)
        time.sleep(3)
        #Ввод пароля
        login = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        login.send_keys(password)
        time.sleep(3)
        #Вход
        submit = self.driver.find_element(By.XPATH,'//*[@id="login-button"]')
        submit.click()
        time.sleep(5)
    def logout(self):
        menu_b = self.driver.find_element(By.ID,'react-burger-menu-btn')
        menu_b.click()
        time.sleep(1)
        logout_b = self.driver.find_element(By.ID,'logout_sidebar_link')
        logout_b.click()
        time.sleep(3)




try:
    url = os.getenv('url')
    username = os.getenv('name')
    password = os.getenv('password')
    # Вызов класса
    log = Login(url,username,password)
    log.login(username,password)
    log.logout()
except Exception as e:
    print(e)