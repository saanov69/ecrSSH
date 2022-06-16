# This Python file uses the following encoding: utf-8
#########################################
####### Execute commands remotly with SSH
#########################################
#
#
import PySimpleGUI as sg
import datetime
import time

import sys
import os

class ecrsshModify:
    def __init__(self, oSg, oParent, nRecno, lData, cEvent):
        self.oParent = oParent
        self.sg = oSg
        self.nRecno = nRecno
        self.lData = lData

        storage64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAABGdBTUEAALGPC/xhBQAAAwBQTFRFAAAABwcHDQ0NDg4ODw8PFxcXGRkZGhoaGxsbHh4eIyMjJSUlJiYmJycnKCgoMTExMjIyNTU1NjY2Nzc3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAouNksgAAAQB0Uk5T////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AFP3ByUAAAAJcEhZcwAADdQAAA3UAe+RuhUAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjEuMWMqnEsAAAC5SURBVChTfZLbDsMgDEPpbb3TDv7/W7PYuAztYUeqhO2QAGowkXIMIeYkaSU4QsNBi4GcyhNINpTglmq4GWSphvy/ldkuLXZ4HmAxy3NmFJaA4guKGCwsjClfV05+fWdhYBtFw+amB292aygW3M7fsPTwjmadZkCvHEtWaAYTViBqVwgTA3tJVnB6D/xhaimItDhjMBvlhtFsaIafnEtOaAY/twAw/eslK70CbX8obUvgJNw9Jv0+Zh8D4s5+VAm/LwAAAABJRU5ErkJggg=='
        close64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsSAAALEgHS3X78AAAE30lEQVRIiZ2VXYgdRRqGn6+quvucM/85iRoTNevMBJFEWY0GFQTBC1HBlaz/jMpoFFfXBdmFvdiLvRIEFRHFGBXMjUQhF/6Bol6sSNaIruCNir/R/Dlx5iRzck736e6qby/6JDlx9CIWFN10Ue/7vW+9X7XcDn8bryWPL2vERkNQQPj9Q72K7F3s7Hxb9bZ98L0bj91jt1y23kxNTxIEGUQ/aTYR6WW9cud/Prx01zf7/7FP5EHXHG7Y6bVTpBPLMSegCWKEEMKvkihgjEWDP+FbEjxTa1bjv9l/CsIKF3ypHhUDSFGACCKC956iKKjV6/hfkCjgUNK0TW1oCA3h+EJk8UUBYFCsQaSyRajArUWLnEONcTrT68nTLtZaEKmmMTiUlsREGy9HO0dgcL1y6lgtZrAsEYFexhwxq2buYfru+1mcOo+828UYg4rgUH7OSkY3zbDq1lkaV1yFP9TqEyy18jiBCMF7DjYmOOu+hxifnCSKItZuvp/F6fPJ05TEwE+dHhN33MfpGy4iFAVjf7qF8etvBV9y1IilBApGIMt6TExOM372JKqKqhLFMdOz93Jk6jx+bHVoztzLyj9eiHqP2Gq7O3UlGAuq1RwYDlUwhoChMdSAz3ZxaEeD8T/fBggaAnGtxpqZWdKFBSbOPLMCCQGJItJPdrHw4lOYRgNsBM6dSCDGErIuodtGkhoyPEr68U5svcbI1ZsQY0CV2vAw9ZGRKjEiSBTR/fQjDm9/AddcjqoSul182kYHVDhJauRffUH7wD7ilatxzVOwI6PM7XiJLO2x4rob0CgGVTSEKigidD94j/ltW9Dg0b0/4BfmyQ8ewKUdWLZ6wCIB9SXFXJvQ+hLkc6QeEznHf199jY1rpjh1w0ZUFTGm7z18/tSj2Hffor5shKLdhhJCADMcw7IlKRIkAqkJRIa4LPl6d5c/PPJkBd5vpArcArD+ue101l1Md08bFxuIBUlOyOUggUIAVIl94Kv5wKqtz7L+7r/0bRHEmApcFbwnHhljw6tv0b3kEtK5gDWmj/GbfQAWZbdaztjyPOfP3oN6D8GDCO133uDAvx9CyxKsRX1JMjbBBa+8Rnbl5RSpR35RfXUGfVLnYGFBcTfdwLo77yLkPYy14CLa773JngfuoNy7QOh2WPnw09WVkufUm8s598G/s+eT9wmBJZ1m+sVTFNBc4Wi8vJ3v//kAJk7AOhbf3MGezTfjWwuYCcv8s1s58K+/okWOxDGdjz5g7+YZtKRSoL+igCp5FKVntGk48sTTzDWb1C+4mB833wgETD2CELBjEfNbtyAjo4xdcz27N11L6B5GGoZQhN+26KiSoII9LebnJx9BkggzNIQkyfEdItiRQGvbM7S2bQHJMGN1NO8ds2dQhBORYBCjAFEE1kFSw0QxuAiTJCAGce64vz4gviTkOTJcErIMMRbyDIxg7bHTFnc47clcmpdj43VkeBRJEkytgdTqSL2OiRMkSRDroH9t4EtCUaBZhmYpIUurZ9pFfVnuX+w62xfjeq3D3/6vbifXrT1XkzgWdREmipA4RlwMUYRY21cg/X+lJ5gSbIHGOVovCHmOCSX7DrbMx599icIhVI2cA5c5mC1gbGnITm4oqAOr0PoOXs9g51HAGiITyCDByXDp4KuiaoESmP8/YC0Y5GajmEsAAAAASUVORK5CYII='
        toolbar_buttons = [[sg.Button('', image_data=storage64[22:], button_color=('white', sg.COLOR_SYSTEM_DEFAULT), pad=(0, 0), key='-storage-'),
                            sg.Button('', image_data=close64[22:],button_color=('white', sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-close-')]]
        self.layout = [
            #[sg.Frame('', toolbar_buttons, title_color='white', background_color=sg.COLOR_SYSTEM_DEFAULT, pad=(0, 0))],
            [self.sg.T('status   ', size=(10, 1)), self.sg.Combo(values=('execute', 'nothing'), default_value=self.lData[0], readonly=True, key='-STATUS-', size=(100, 1))],
            [self.sg.T('name job ', size=(10, 1)), self.sg.Input(self.lData[1], key='-OPERATION-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('IP       ', size=(10, 1)), self.sg.Input(self.lData[2], key='-IP-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('model    ', size=(10, 1)), self.sg.Combo(values=('qteq    ', 'avaya   ', 'Linux'), default_value=self.lData[3], readonly=False, key='-MODEL-', size=(100, 1))],
            [self.sg.T('ID device', size=(10, 1)), self.sg.Input(self.lData[4], key='-IDdevice-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('login    ', size=(10, 1)), self.sg.Input(self.lData[5], key='-LOGIN-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('password ', size=(10, 1)), self.sg.Input(self.lData[6], key='-PASSWORD-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('commads  ', size=(10, 1)), self.sg.Multiline(self.lData[7], key='-COMMANDS-', size=(100, 15), do_not_clear=False)],
	    [self.sg.Button('Save', key='--SAVE--'), self.sg.Button('Cancel', key='--CANCEL--')],
            [self.sg.Text('Please press: <F2> - Save or <Esc> - Cancel', relief=self.sg.RELIEF_SUNKEN, size=(120, 1), pad=(0, 3), key='-status-')]
                       ]


        self.window = sg.Window('Edit Device', self.layout, force_toplevel=True, use_default_focus=True, return_keyboard_events=True, finalize=False)

        #Сделать текущее окно модальным
        self.window.Finalize()
        self.window.TKroot.transient()
        self.window.TKroot.grab_set()
        self.window.TKroot.focus_force()
        print(nRecno, lData ,cEvent)

    def eventread(self):

        # ------ Definition Events cycle ------ #
        # ------ Определение цикла обработки ожидания события ------ #
        while True:
            # ------ Get Definition Event ------ #
            # ------ Получение ожидаемого события ------ #
            event, values = self.window.read(300)
            # ------ Test Definition Event on EXIT------ #
            # ------ Проверка ожидаемого события на завершение------ #
            self.Handler(event, values)
            if event in (self.sg.WIN_CLOSED, '--CANCEL--'):
                # ------ EXIT------ #
                # ------ Действительно завершение------ #
                self.window.close()
                break

    def Handler(self, cEvent, cValue):
        if (cEvent == '--SAVE--' or cEvent == 'F2:68') and self.oParent.cEvent in ['--EDIT--', 'Edit...']:
            self.SaveData(self.nRecno, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            # ------ Interfaces CLOSE------ #
            # ------ Интерфейс закрыт------ #
            self.window.close()
        if (cEvent == '--SAVE--' or cEvent == 'F2:68') and self.oParent.cEvent in ['--APPEND--', 'Append...']:
            self.oParent.data.append(['', '', '', '', '', '', '', ''])
            self.oParent.recno = self.oParent.recount
            self.SaveData(-1, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            # ------ Interfaces CLOSE------ #
            # ------ Интерфейс закрыт------ #
            self.window.close()
        if (cEvent == '--SAVE--' or cEvent == 'F2:68') and self.oParent.cEvent in ['--APPENDCOPY--', 'Append copy...']:
        # Сохранить 
            self.oParent.data.append(['', '', '', '', '', '', '', ''])
            self.oParent.recno = self.oParent.recount
            self.SaveData(-1, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            # ------ Interfaces CLOSE------ #
            # ------ Интерфейс закрыт------ #
            self.window.close()
        if  cEvent == 'Escape:9':
            # ------ Interfaces CLOSE------ #
            # ------ Интерфейс закрыт------ #
            self.window.close()
              


    def SaveData(self, cRecNo, cValue):
        self.oParent.data[cRecNo][0] = cValue['-STATUS-']
        self.oParent.data[cRecNo][1] = cValue['-OPERATION-']
        self.oParent.data[cRecNo][2] = cValue['-IP-']
        self.oParent.data[cRecNo][3] = cValue['-MODEL-']
        self.oParent.data[cRecNo][4] = cValue['-IDdevice-']
        self.oParent.data[cRecNo][5] = cValue['-LOGIN-']
        self.oParent.data[cRecNo][6] = cValue['-PASSWORD-']
        self.oParent.data[cRecNo][7] = cValue['-COMMANDS-']
 

class ecrssh:
    # ------ Definition Main Interfaces objects------ #
    # ------ Определение интерфейсного объекта ------ #
    fStart = True
    header_list:list = ['status', '       name job        ', 'IP', '  model  ', '    ID device    ', '  login   ']

    def __init__(self, oSg):
        self.version = '(ver. 0.0.1)' 
        self.date = datetime.datetime.now()
        # ------ Menu Definition ------ #
        # ------ Определение МЕНЮ ------ #
        self.menu_def:list = [['&File', ['!&Open...', '&Save', '---', 'E&xit']],
                         ['&Table', ['&Append...', 'Append &copy...', '---', '&Edit...', '---', '&Delete'], ],
                         ['&Run', ['&MARK', '---', '&Start', '!&Pause', '!&Stop']],
                         ['&About...'],
                         ]
        # ------ Link interfaces object ------ #
        # ------ присвоение ссылки на объект интерфейса ------ #
        self.sg:Object = oSg
        self.msg1:String = 'main.json '
        self.settings = self.sg.UserSettings(path='.')
        self.data:list = self.settings['data']
        #print(hasattr(self, 'data'), self.data,type(self.data),not self.data)
        if not self.data:
            self.data:list = [['execute', '', 'x.x.x.x', '', '', 'admin', '', '']]
#            self.recount = 1
        
        self.recno = 0
        self.recount = len(self.data)
        # ------ Fiels Input/Output Definition ------ #
        # ------ Определение полей ввода/вывода ------ #
        self.layout = [[self.sg.Menu(self.menu_def)],
                       [self.sg.Text(f' ', key='--Tttt--')],
                       [self.sg.Table(key='-DEVICE-',
                                      size=(110, 25),
                                      values=self.data,
                                      headings=self.header_list,
                                      display_row_numbers=False,
                                      justification='left',
                                      auto_size_columns=True,
                                      num_rows=min(20, 20))],
                       [self.sg.Button('Append...', key='--APPEND--'), self.sg.Button('Append copy...', key='--APPENDCOPY--'),
                        self.sg.Button('Edit...', key='--EDIT--'), self.sg.Button('Delete', key='--DELETE--'),
                        self.sg.Text('                        '),
                        self.sg.Button('Mark', key='--MARK--'),
                        self.sg.Text('                         '),
                        self.sg.Button('Start', key='--START--'), self.sg.Button('Pause', key='--PAUSE--'), self.sg.Button('Stop', key='--STOP--')],
                       [self.sg.Output(size=(120, 15), background_color='black', text_color='white')],
                       [self.sg.Text('', relief=self.sg.RELIEF_SUNKEN, size=(25, 1), pad=(0, 3), key='-records-'),
                        self.sg.Text(self.msg1, relief=self.sg.RELIEF_SUNKEN, size=(75, 1), pad=(0, 3), key='-status-'),
                        self.sg.Text('', relief=self.sg.RELIEF_SUNKEN, size=(25, 1), justification='right', pad=(0, 3), key='-TIMER-')]
                       ]

        # ------ Make interfaces object ------ #
        # ------ Создание объекта интерфейса ------ #
        self.screen_size = self.sg.Window.get_screen_size()
        self.location = self.screen_size[0] // 2, self.screen_size[1] - 200
        # set a default location centered and near the bottom of the screen
        self.window = sg.Window(f'Execute commands remotly with SSH {self.version}', self.layout, location=self.location, return_keyboard_events=True, use_default_focus=True)
                                #, finalize=False, moodel=True return_keyboard_events=True, 


    def eventread(self):
        # ------ Definition Events cycle ------ #
        # ------ Определение цикла обработки ожидания события ------ #
        while True:
           #print(self.date, self.time_string)
            # ------ Get Definition Event ------ #
            # ------ Получение ожидаемого события ------ #
            self.cEvent, self.cValue = self.window.read(300)
            # ------ Test Definition Event on EXIT------ #
            # ------ Проверка ожидаемого события на завершение------ #
            if self.cEvent in (self.sg.WIN_CLOSED, 'Exit'):
                # ------ EXIT------ #
                # ------ Действительно завершение------ #
                self.window.close()
                # ------ Interfaces CLOSE------ #
                # ------ Интерфейс закрыт------ #
                self.settings['data'] = self.data
                break
            else:
                if self.KeyPressHandler():
                # ------ Handling events coming from controls------ #
                # ------ Обработка событий поступающих от элементов управления ------ #
                    self.Handler()
        

    def KeyPressHandler(self):
        #print('KeyPressHandler<', self.cEvent, self.cValue)
        
        if self.fStart == True:
        # execute только при запуске для получения фокуса таблицей
           self.refresh()
           self.fStart = False
#           print(os.path.dirname(sys.executable))
#           print(self.settings)
           return False
        else:
            self.recno = self.cValue['-DEVICE-'][0]
            self.recount = len(self.data)
            self.window['-records-'].update(f'record: {self.recno}/{len(self.data)}')
            self.window['-status-'].update(f'{self.msg1} {self.cEvent}')
            self.date = datetime.datetime.now()
            self.window['-TIMER-'].update(f'{self.date}')

        if self.cEvent == 'Home:110':
        #переход в начало таблицы
            self.recno = 0
            self.refresh()
            return False

        if self.cEvent == 'End:115':
        #переход в конец таблицы
            self.recno = self.recount-1
            self.refresh()
            return False

        if self.cEvent == 'F4:70':
        #переход к редактированию строки таблицы
            self.cEvent = '--EDIT--'
            self.Handler()
            return False

        if self.cEvent == 'F5:71':
        #переход к редактированию строки таблицы
            self.cEvent = '--APPEND--'
            self.Handler()
            return False

        if self.cEvent == 'F6:72':
        #переход к редактированию строки таблицы
            self.cEvent = '--APPENDCOPY--'
            self.Handler()
            return False

        if self.cEvent == 'F2:68':
        #переход к редактированию строки таблицы
            self.cEvent = '--START--'
            self.Handler()
            return False

        if self.cEvent == self.cEvent == 'space:65':
        #переключение режима обработки
            self.cEvent = '--MARK--'
            self.Handler()
            return False

        return True

    def refresh(self):
        self.window.enable = False
        # # Re-Grab table focus using ttk
        # self.window['-DEVICE-'].SetFocus(force=True)
        # table_row = self.window['-DEVICE-'].Widget.get_children()[current_row]
        # self.window['-DEVICE-'].Widget.selection_set(table_row)  # move selection
        # self.window['-DEVICE-'].Widget.focus(table_row)  # move focus
        # self.window['-DEVICE-'].Widget.see(table_row)  # scroll to show it
        self.window['-DEVICE-'].update(values=self.data)
        self.window['-DEVICE-'].SetFocus(force=True)
        self.window['-DEVICE-'].Widget.selection_set(self.recno+1)
        self.window['-DEVICE-'].Widget.focus(self.recno+1)  # move focus
        self.window['-DEVICE-'].Widget.see(self.recno+1)  # scroll to show it
        self.window.enable = True
        return

    def Handler(self):
    ## ------ Handler events------ #
    ## ------ Обработка поступивших событий от элементов управления------ #
        if self.cEvent in ['--MARK--', 'MARK']:
            self.window.enable = False
            if self.data[self.recno][0] == 'execute':
                self.data[self.recno][0] = 'nothing'
            else:
                self.window.enable = False
                self.data[self.recno][0] = 'execute'
            self.refresh()
        elif self.cEvent in ['--EDIT--', 'Edit...']:
            self.window.enable = False
            self.oedit = ecrsshModify(sg, self, self.recno, self.data[self.recno], self.cEvent).eventread()
            self.refresh()
        elif self.cEvent in ['--APPEND--', 'Append...']:
            self.window.enable = False
            self.oedit = ecrsshModify(sg, self, self.recno, ['execute', '', 'x.x.x.x', 'Linux', 'id'+str(self.recount), 'admin', '', ''], self.cEvent).eventread()
            self.refresh()
        elif self.cEvent in ['--APPENDCOPY--', 'Append copy...']:
            self.window.enable = False
            self.oedit = ecrsshModify(sg, self, self.recno, self.data[self.recno], self.cEvent).eventread()
            self.refresh()
        elif self.cEvent in ['--DELETE--', 'Delete']:
            self.window.enable = False
            self.data.remove(self.data[self.recno])
            if not self.data:
                self.data:list = [['execute', '', 'x.x.x.x', '', '', 'admin', '', '']]
            self.recno -= self.recno
            self.refresh()
        elif self.cEvent in ['--START--', 'Start']:
            print('--START--')
            time.sleep(10)
            print('--STOP--')
        elif self.cEvent in ['--PAUSE--', 'Pause']:
            pass
        elif self.cEvent in ['--STOP--', 'Stop']:
            pass
        elif self.cEvent == 'Save':
            self.settings['data'] = self.data
            print('save to file [main.json]')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    

    _SCREEN = ecrssh(sg).eventread()
