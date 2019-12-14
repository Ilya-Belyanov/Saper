import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

Config.set('graphics','resizable','0');
Config.set('graphics','width','300');
Config.set('graphics','height','375');

class MainWindow(BoxLayout):

    def __init__(self, measure,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'

        #Подсчет размеров игрового поля
        self.measure = measure
        self.X= int(300 / self.measure)
        self.Y = self.X
        #Число бомб
        self.number_bomb = int(self.X * self.Y /7)
        self.number_in_label=self.number_bomb

        self.box=BoxLayout(orientation='horizontal',size_hint=(1, .20))

        # Создание верхних кнопок
        self.bt_setting = Button(text='Setting', background_color=[.5,.5,1,1],on_press=self.change,color=[0,0.9,1,1])
        self.bt_smile = Button(text=':)',color=[.7,.7,0,1],background_color=[.5,.5,1,1],on_press=self.repeat)
        self.bt_flag = Button(text='Saper', color=[1, 0, 0, 1],background_color=[.5,.5,1,1],on_press=self.flag)
        self.bt_bomb = Label(text=str(self.number_in_label),color=[0,1,0,1])

        #Верхние кнопки в боксе
        self.box.add_widget(self.bt_setting)
        self.box.add_widget(self.bt_smile)
        self.box.add_widget(self.bt_flag)
        self.box.add_widget(self.bt_bomb)

        # Создание игрового поля
        self.bt_list = []
        self.lay = GridLayout(cols=self.Y)
        for i in range(self.X):
            self.bt_X=[]
            for i in range(self.Y):
                bt_one = Button(background_color=[0.9,0.95,1,1],on_press=self.point)
                self.bt_X.append(bt_one)
                self.lay.add_widget(bt_one)

            self.bt_list.append(self.bt_X)
        # Верхняя рабочая зона и игровая добавляются на поле
        self.add_widget(self.box)
        self.add_widget(self.lay)

        # Указание на первое нажатие
        self.first_point=True
        # Бомба или флаг -бомба -True
        self.bomb_or_flag=True
        #Проверенные кнопки
        self.check_list=[]
        #Поставленные флажки
        self.flag_list=[]
        # Список бомб
        self.bomb_list = []

    # Функции верхних кнопок
    def change(self,instance):
        '''Нажатие на настройки'''
        manager.current = 'setting'

    def repeat(self,instance):
        '''Перезагрузка'''
        instance.text=":)"
        self.first_point=True
        self.check_list = []
        self.flag_list = []
        self.bomb_list=[]
        self.number_in_label=self.number_bomb
        self.bt_bomb.text = str(self.number_in_label)
        self.bt_bomb.color = [0,1,0,1]
        self.bt_flag.text = 'Saper'
        self.bomb_or_flag=True
        for i in range(self.X):
            for j in range(self.Y):
                self.bt_list[i][j].text=""
                self.bt_list[i][j].background_color = [0.9, 0.95, 1, 1]

    def flag(self,instance):
        '''Ставить точку или флаг'''
        self.bomb_or_flag= not self.bomb_or_flag
        if self.bomb_or_flag:
            self.bt_flag.text="Saper"
        else:
            self.bt_flag.text = "Flag"

    # Логика поля
    def point(self,instance):
        '''Нажатие любой кнопки'''
        #Не срабатывает при победе или проигрыше
        if self.bt_bomb.text=="DEAD" or self.bt_bomb.text=='WIN':
            pass
        #Раскрываем поле
        elif self.bomb_or_flag:
            if self.first_point:
                self.first_point=not self.first_point
                self.distribution_bomb(instance,self.number_bomb,self.X,self.Y)

            self.position(instance)
        # Ставим флажки
        else:
            if instance.text!='X' and instance not in self.check_list:
                instance.text="X"
                instance.color=[0,0,0,1]
                instance.background_color=[0.5,0.7,0.8,1]
                self.number_in_label-=1
                self.bt_bomb.text=str(self.number_in_label)
                self.flag_list.append(instance)
            elif instance.text=='X':
                instance.text = ""
                instance.background_color =  [0.9, 0.95, 1, 1]
                self.number_in_label += 1
                self.bt_bomb.text = str(self.number_in_label)
                self.flag_list.remove(instance)
            else:
                pass
        # Проверяем на победу
        self.win()

    def distribution_bomb(self,instance,number_bomb,X,Y):
        '''Распределяет бомбы в списке кнопок'''
        for i in range(number_bomb):
            x=random.randint(0,X-1)
            y=random.randint(0,Y-1)
            while self.bt_list[x][y] in self.bomb_list or self.bt_list[x][y]==instance:
                x = random.randint(0, X-1)
                y = random.randint(0, Y-1)
            self.bomb_list.append(self.bt_list[x][y])

    def position(self,instance):
        '''Выясняет позицию кнопки в списке'''
        if instance in self.bomb_list:
            self.bt_smile.text=":("
            self.bt_bomb.text="DEAD"
            self.bt_bomb.color=[1,0,0,1]
            self.disclosure()
        else:
            for i in range(self.X):
                for j in range(self.Y):
                    if self.bt_list[i][j]==instance:
                        self.count_bomb(i,j)
                        break

    def disclosure(self):
        """Раскрывает бомбы"""
        for i in range(self.X):
            for j in range(self.Y):
                if self.bt_list[i][j] in self.bomb_list:
                    self.bt_list[i][j].text="*"
                    self.bt_list[i][j].on_size = 200
                    self.bt_list[i][j].color=[1,0,0,1]
                    self.bt_list[i][j].background_color = [1, 0, 0, 1]

    def count_bomb(self,i,j):
        '''Подсчет точек вокруг'''
        if self.bt_list[i][j] not in self.check_list: # Была ли уже проверена кнопка
            count=0
            for x in range(i-1,i+2):
                for y in range(j-1,j+2):
                    if x<0 or y<0 or x>=self.X or y>=self.Y:
                        continue
                    elif self.bt_list[x][y] in self.bomb_list:
                        count+=1

            if count==0:
                self.bt_list[i][j].text='0'
                self.check_list.append(self.bt_list[i][j])
                self.bt_list[i][j].color = [1, 1, 1, 1]
                self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if (x==i and y==j) or x<0 or y<0 or x>=self.X or y>=self.Y:
                            continue
                        elif self.bt_list[x][y] in self.check_list:
                            continue
                        else:
                            self.count_bomb(x,y)
            # Постановка числа и цвета
            else:
                self.bt_list[i][j].text=str(count)
                self.check_list.append(self.bt_list[i][j])
                if count==1:
                    self.bt_list[i][j].color=[0,0,1,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==2:
                    self.bt_list[i][j].color=[0,1,0,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==3:
                    self.bt_list[i][j].color=[1,1,0,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==4:
                    self.bt_list[i][j].color=[1,0,1,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==5:
                    self.bt_list[i][j].color=[0.5,0,0,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==6:
                    self.bt_list[i][j].color=[0.5,0.5,0,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==7:
                    self.bt_list[i][j].color=[0,0,0.5,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]
                elif count==8:
                    self.bt_list[i][j].color=[0.5,0.5,0.5,1]
                    self.bt_list[i][j].background_color = [0.5, 0.9, 0.9, 1]

    def win(self):
        '''Проверяет на победу'''
        if len(self.check_list)==int((self.Y*self.X)-self.number_bomb):
            self.bt_bomb.text='WIN'
            #print(len(self.check_list),int((self.Y*self.X)-self.number_bomb))

class SecondWindow(BoxLayout):
    def __init__(self,**kwargs):
        super(SecondWindow,self).__init__(**kwargs)

        self.orientation='horizontal'
        self.box=BoxLayout(orientation='vertical',size_hint=(0.8,1))
        self.label=Label(text="Choice mode",font_size=20,color=[0,0.9,1,1])
        self.bt1 = Button(text='Easy',font_size=20,color=[0,1,0.2,1],
                          background_color=[.3,.7,0,1],on_press=self.change)
        self.bt2 = Button(text='Normal',font_size=25,color=[0,0.9,1,1],
                          background_color=[0,.5,0.5,1],on_press=self.change_two)
        self.bt3 = Button(text='Hard', font_size=30, color=[1, 0, 0, 1],
                          background_color=[1, 0.6, 0, 1],background_normal='' ,on_press=self.change_three)
        self.box.add_widget(self.label)
        self.box.add_widget(self.bt1)
        self.box.add_widget(self.bt2)
        self.box.add_widget(self.bt3)

        self.box_2 = BoxLayout(orientation='vertical',size_hint=(0.2,1))
        self.bt_i=Button(text='i',font_size=30,color=[0,0.9,1,1],
                          background_color=[.5,.5,1,1],on_press=self.info,size_hint=(1,0.2))
        self.bt_future=Button(text='R\nU\nL\nE\nS',font_size=30,color=[0,0.9,1,1],
                          background_color=[.5,.5,1,1],on_press=self.info2,size_hint=(1,0.8))
        self.box_2.add_widget(self.bt_i)
        self.box_2.add_widget(self.bt_future)

        self.add_widget(self.box)
        self.add_widget(self.box_2)

    def change(self,instance):
        manager.current='main'
    def change_two(self,instance):
        manager.current='main_two'
    def change_three(self,instance):
        manager.current='main_three'
    def info(self,instance):
        info=Info()
        popupWindow=Popup(title='Information',content=info,size_hint=(None,None),size=(250,300))
        popupWindow.open()
    def info2(self,instance):
        info = Info2()
        popupWindow = Popup(title='Information', content=info, size_hint=(None, None), size=(250, 300))
        popupWindow.open()

# Window of information
class Info(BoxLayout):
    pass
class Info2(BoxLayout):
    pass


# Мэнэджер экранов
manager=ScreenManager()
#Экраны
screen1=Screen(name='main')
screen3=Screen(name='main_two')
screen4=Screen(name='main_three')
screen2=Screen(name='setting')
#Обьекты главного экрана
saper_one=MainWindow(50)
saper_two=MainWindow(30)
saper_three=MainWindow(20)
# Добавляем обьекты на экраны
screen1.add_widget(saper_one)
screen2.add_widget(SecondWindow())
screen3.add_widget(saper_two)
screen4.add_widget(saper_three)
manager.add_widget(screen1)
manager.add_widget(screen2)
manager.add_widget(screen3)
manager.add_widget(screen4)

class SaperApp(App):
    def build(self):
      return manager

if __name__ == '__main__':
    SaperApp().run()