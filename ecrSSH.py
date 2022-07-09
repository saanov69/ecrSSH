# This Python file uses the following encoding: utf-8
# Python 3.9.5
# провенено 'mikrotik_routeros','linux'
#########################################
####### Execute commands remotly with SSH
#########################################
#
#
#
#from email.errors import NonASCIILocalPartDefect
from datetime import date
from netmiko import ConnectHandler
import PySimpleGUI as sg
import datetime
import time
import sys
import os
import logging


class ExecuteCommands:
    def __init__(self, oParent, lData):
        self.oParent = oParent
        self.device_type = {
            "device_type":  lData[3],
            "host": lData[2],
            "username": lData[5],
            "password": lData[6],
            "secret": lData[7],
        }
        self.lCommands = lData[8].split('\n')
        self.DateTime = datetime.datetime.now()
        self.sDate  = (f'{self.DateTime.strftime("%Y_%m_%d")}')
        self.sTime  = (f'{self.DateTime.strftime("%H_%M_%S")}')
        self.sIp  = lData[2]
        if not os.path.isdir('Logs/'+self.sDate):
            os.makedirs('Logs/'+self.sDate)            
        self.sLogFileName  = 'Logs/' + self.sDate +'/'+ lData[4] + '__' + self.sIp + '__' + self.sDate + '__' + self.sTime + '.txt'
        self.FindPrompt  = ''
        self.SendCommand  = ''
        self.DateTimeStart = None
        self.TimerStartStop = None
        self.DateTimeStartAll = None
        self.TimerStartStopAll = None
        

    def send_now(self):
        self.oParent.window.enable = False
        with open(self.sLogFileName, "w") as external_file:
            try:
                self.DateTimeStartAll = datetime.datetime.now()
                self.DateTimeStart = datetime.datetime.now()
                print(f"\n>--start CONNECT: {self.DateTimeStart} ---")
                print(f"\n>--start CONNECT: {self.DateTimeStart} ---", file=external_file)
                net_connect = ConnectHandler(**self.device_type)
                if 'cisco' in self.device_type:
                # Call 'enable()' method to elevate privileges
                    net_connect.enable()
                self.TimerStartStop = datetime.datetime.now() - self.DateTimeStart
                print(f"----------now CONNECT: {self.TimerStartStop} sec---------<")
                print(f"----------now CONNECT: {self.TimerStartStop} sec---------<", file=external_file)

                for self.command in self.lCommands:
                    self.DateTimeStart = datetime.datetime.now()
                    print(f">---time start: {self.DateTimeStart} -----")
                    print(f">---time start: {self.DateTimeStart} -----", file=external_file)
                    self.command = self.command.replace('[DATE]', self.sDate)
                    self.command = self.command.replace('[TIME]', self.sTime)
                    self.FindPrompt = net_connect.find_prompt()
                    self.SendCommand = net_connect.send_command(self.command, read_timeout=10, strip_prompt=True, strip_command=False)
                    print(self.FindPrompt)
                    print(self.SendCommand)
                    print(self.FindPrompt, file=external_file)
                    print(self.SendCommand, file=external_file)
                    self.TimerStartStop = datetime.datetime.now() - self.DateTimeStart
                    print(f"----command time left: {self.TimerStartStop} sec----<\n")
                    print(f"----command time left: {self.TimerStartStop} sec----<\n", file=external_file)
                    #time.sleep(0.1)
                print(f"Log files: {self.sLogFileName}")
                print(f"Log files: {self.sLogFileName}", file=external_file)
                self.TimerStartStopAll = datetime.datetime.now() - self.DateTimeStartAll
                print(f"-----DEVICE time left: {self.TimerStartStopAll} sec----<\n")
                print(f"-----DEVICE time left: {self.TimerStartStopAll} sec----<\n", file=external_file)
                external_file.close()
                self.oParent.window.enable = True
                return True
            except Exception as e:
                print(f"\nUnexpected error occurred while connecting to host: {e}")
                print(f"\nUnexpected error occurred while connecting to host: {e}", file=external_file)
                self.TimerStartStop = datetime.datetime.now() - self.DateTimeStart
                print(f"----command time left: {self.TimerStartStop} sec----<\n")
                print(f"----command time left: {self.TimerStartStop} sec----<\n", file=external_file)
                print(f"Log files: {self.sLogFileName}")
                print(f"Log files: {self.sLogFileName}", file=external_file)
                self.TimerStartStopAll = datetime.datetime.now() - self.DateTimeStartAll
                print(f"-----DEVICE time left: {self.TimerStartStopAll} sec----<\n")
                print(f"-----DEVICE time left: {self.TimerStartStopAll} sec----<\n", file=external_file)
                external_file.close()
                self.oParent.window.enable = True
                return False

        
class ecrsshModify:
    def __init__(self, oSg, oParent, nRecno, lData, cEvent):
        self.oParent = oParent
        self.sg = oSg
        self.cEvent = ''
        self.cValues = ''
        self.nRecno = nRecno
        self.lData = lData
        # ------ Возможные варианты device_type из netmiko ------ #
        self.lDevType:list = ['a10','accedian','adtran_os','alcatel_aos','alcatel_sros',
            'allied_telesis_awplus','apresia_aeos','arista_eos','aruba_os',
            'aruba_osswitch','aruba_procurve','avaya_ers','avaya_vsp',
            'broadcom_icos','brocade_fastiron','brocade_fos',
            'brocade_netiron','brocade_nos','brocade_vdx',
            'brocade_vyos','calix_b6','cdot_cros','centec_os',
            'checkpoint_gaia','ciena_saos','cisco_asa','cisco_ftd',
            'cisco_ios','cisco_nxos','cisco_s300','cisco_tp',
            'cisco_viptela','cisco_wlc','cisco_xe','cisco_xr',
            'cloudgenix_ion','coriant','dell_dnos9','dell_force10',
            'dell_isilon','dell_os10','dell_os6','dell_os9',
            'dell_powerconnect','dell_sonic','dlink_ds','eltex',
            'eltex_esr','endace','enterasys','ericsson_ipos',
            'extreme','extreme_ers','extreme_exos','extreme_netiron',
            'extreme_nos','extreme_slx','extreme_tierra',
            'extreme_vdx','extreme_vsp','extreme_wing','f5_linux',
            'f5_ltm','f5_tmsh','flexvnf','fortinet','generic',
            'generic_termserver','hp_comware','hp_procurve',
            'huawei','huawei_olt','huawei_smartax','huawei_vrpv8',
            'ipinfusion_ocnos','juniper','juniper_junos','juniper_screenos',
            'keymile','keymile_nos','linux','mellanox','mellanox_mlnxos',
            'mikrotik_routeros','mikrotik_switchos','mrv_lx','mrv_optiswitch',
            'netapp_cdot','netgear_prosafe','netscaler','nokia_sros',
            'oneaccess_oneos','ovs_linux','paloalto_panos','pluribus',
            'quanta_mesh','rad_etx','raisecom_roap','ruckus_fastiron',
            'ruijie_os','sixwind_os','sophos_sfos','supermicro_smis',
            'tplink_jetstream','ubiquiti_edge','ubiquiti_edgerouter',
            'ubiquiti_edgeswitch','ubiquiti_unifiswitch','vyatta_vyos',
            'vyos','watchguard_fireware','yamaha','zte_zxros','zyxel_os']
        
##        storage64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAMAAADXqc3KAAAABGdBTUEAALGPC/xhBQAAAwBQTFRFAAAABwcHDQ0NDg4ODw8PFxcXGRkZGhoaGxsbHh4eIyMjJSUlJiYmJycnKCgoMTExMjIyNTU1NjY2Nzc3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAouNksgAAAQB0Uk5T////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AFP3ByUAAAAJcEhZcwAADdQAAA3UAe+RuhUAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjEuMWMqnEsAAAC5SURBVChTfZLbDsMgDEPpbb3TDv7/W7PYuAztYUeqhO2QAGowkXIMIeYkaSU4QsNBi4GcyhNINpTglmq4GWSphvy/ldkuLXZ4HmAxy3NmFJaA4guKGCwsjClfV05+fWdhYBtFw+amB292aygW3M7fsPTwjmadZkCvHEtWaAYTViBqVwgTA3tJVnB6D/xhaimItDhjMBvlhtFsaIafnEtOaAY/twAw/eslK70CbX8obUvgJNw9Jv0+Zh8D4s5+VAm/LwAAAABJRU5ErkJggg=='
##        close64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsSAAALEgHS3X78AAAE30lEQVRIiZ2VXYgdRRqGn6+quvucM/85iRoTNevMBJFEWY0GFQTBC1HBlaz/jMpoFFfXBdmFvdiLvRIEFRHFGBXMjUQhF/6Bol6sSNaIruCNir/R/Dlx5iRzck736e6qby/6JDlx9CIWFN10Ue/7vW+9X7XcDn8bryWPL2vERkNQQPj9Q72K7F3s7Hxb9bZ98L0bj91jt1y23kxNTxIEGUQ/aTYR6WW9cud/Prx01zf7/7FP5EHXHG7Y6bVTpBPLMSegCWKEEMKvkihgjEWDP+FbEjxTa1bjv9l/CsIKF3ypHhUDSFGACCKC956iKKjV6/hfkCjgUNK0TW1oCA3h+EJk8UUBYFCsQaSyRajArUWLnEONcTrT68nTLtZaEKmmMTiUlsREGy9HO0dgcL1y6lgtZrAsEYFexhwxq2buYfru+1mcOo+828UYg4rgUH7OSkY3zbDq1lkaV1yFP9TqEyy18jiBCMF7DjYmOOu+hxifnCSKItZuvp/F6fPJ05TEwE+dHhN33MfpGy4iFAVjf7qF8etvBV9y1IilBApGIMt6TExOM372JKqKqhLFMdOz93Jk6jx+bHVoztzLyj9eiHqP2Gq7O3UlGAuq1RwYDlUwhoChMdSAz3ZxaEeD8T/fBggaAnGtxpqZWdKFBSbOPLMCCQGJItJPdrHw4lOYRgNsBM6dSCDGErIuodtGkhoyPEr68U5svcbI1ZsQY0CV2vAw9ZGRKjEiSBTR/fQjDm9/AddcjqoSul182kYHVDhJauRffUH7wD7ilatxzVOwI6PM7XiJLO2x4rob0CgGVTSEKigidD94j/ltW9Dg0b0/4BfmyQ8ewKUdWLZ6wCIB9SXFXJvQ+hLkc6QeEznHf199jY1rpjh1w0ZUFTGm7z18/tSj2Hffor5shKLdhhJCADMcw7IlKRIkAqkJRIa4LPl6d5c/PPJkBd5vpArcArD+ue101l1Md08bFxuIBUlOyOUggUIAVIl94Kv5wKqtz7L+7r/0bRHEmApcFbwnHhljw6tv0b3kEtK5gDWmj/GbfQAWZbdaztjyPOfP3oN6D8GDCO133uDAvx9CyxKsRX1JMjbBBa+8Rnbl5RSpR35RfXUGfVLnYGFBcTfdwLo77yLkPYy14CLa773JngfuoNy7QOh2WPnw09WVkufUm8s598G/s+eT9wmBJZ1m+sVTFNBc4Wi8vJ3v//kAJk7AOhbf3MGezTfjWwuYCcv8s1s58K+/okWOxDGdjz5g7+YZtKRSoL+igCp5FKVntGk48sTTzDWb1C+4mB833wgETD2CELBjEfNbtyAjo4xdcz27N11L6B5GGoZQhN+26KiSoII9LebnJx9BkggzNIQkyfEdItiRQGvbM7S2bQHJMGN1NO8ds2dQhBORYBCjAFEE1kFSw0QxuAiTJCAGce64vz4gviTkOTJcErIMMRbyDIxg7bHTFnc47clcmpdj43VkeBRJEkytgdTqSL2OiRMkSRDroH9t4EtCUaBZhmYpIUurZ9pFfVnuX+w62xfjeq3D3/6vbifXrT1XkzgWdREmipA4RlwMUYRY21cg/X+lJ5gSbIHGOVovCHmOCSX7DrbMx599icIhVI2cA5c5mC1gbGnITm4oqAOr0PoOXs9g51HAGiITyCDByXDp4KuiaoESmP8/YC0Y5GajmEsAAAAASUVORK5CYII='
##        toolbar_buttons = [[sg.Button('', image_data=storage64[22:], button_color=('white', sg.COLOR_SYSTEM_DEFAULT), pad=(0, 0), key='-storage-'),
##                            sg.Button('', image_data=close64[22:],button_color=('white', sg.COLOR_SYSTEM_DEFAULT), pad=(0,0), key='-close-')]]
##            #[sg.Frame('', toolbar_buttons, title_color='white', background_color=sg.COLOR_SYSTEM_DEFAULT, pad=(0, 0))],

        # ------ Определение МЕНЮ ------ #
        self.menu_def:list = [['&Doing', ['&Save          <F2>', '&Cancel       <Esc>']],]
        # ------ Определение полей ввода/вывода и элементов управления------ #
        self.layout = [[self.sg.Menu(self.menu_def)],
            [self.sg.Text(f' ', key='--INFO--')],
            [self.sg.T('status   ', size=(10, 1)), self.sg.Combo(values=('execute', 'nothing'), default_value=self.lData[0], readonly=True, key='-STATUS-', size=(100, 1))],
            [self.sg.T('name job ', size=(10, 1)), self.sg.Input(self.lData[1], key='-OPERATION-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('IP       ', size=(10, 1)), self.sg.Input(self.lData[2], key='-IP-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('model    ', size=(10, 1)), self.sg.Combo(values=(self.lDevType), default_value=self.lData[3], readonly=True, key='-MODEL-', size=(100, 1))],
            [self.sg.T('ID device', size=(10, 1)), self.sg.Input(self.lData[4], key='-IDdevice-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('login    ', size=(10, 1)), self.sg.Input(self.lData[5], key='-LOGIN-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('password ', size=(10, 1)), self.sg.Input(self.lData[6], key='-PASSWORD-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('secret   ', size=(10, 1)), self.sg.Input(self.lData[7], key='-SECRET-', size=(100, 1), do_not_clear=False)],
            [self.sg.T('commands ', size=(10, 1)), self.sg.Multiline(self.lData[8], key='-COMMANDS-', size=(100, 15), do_not_clear=False)],
	    [self.sg.Button('Save', key='--SAVE--'), self.sg.Button('Cancel', key='--CANCEL--')],
            [self.sg.T('  ', size=(100, 1))],
            [self.sg.Text('You can use variabes [DATE] and [TIME] if you need in commands ', relief=self.sg.RELIEF_SUNKEN, size=(120, 1), pad=(0, 3), key='-status-')]]
        # ------ Создание и позиционирование объекта интерфейса ------ #
#        self.window = sg.Window('Edit Device', self.layout, force_toplevel=True, use_default_focus=True, return_keyboard_events=True, finalize=False)
        self.window = sg.Window('Edit Device', self.layout, force_toplevel=True, use_default_focus=True, return_keyboard_events=True, finalize=True)
        # ------ Сделать текущее окно модальным ------ #
        self.window.Finalize()
        self.window.TKroot.transient()
        self.window.TKroot.grab_set()
        self.window.TKroot.focus_force()

    def eventread(self):
        while True:
        # ------ Определение цикла обработки ожидания события ------ #
            self.cEvent, self.cValues = self.window.read()
            # ------ Получение ожидаемого события ------ #
            self.Handler(self.cEvent, self.cValues)
            # ------ Проверка ожидаемого события на завершение------ #
            if self.cEvent in (self.sg.WIN_CLOSED, '--CANCEL--'):
                # ------ Действительно случилось завершение------ #
                self.window.close()
                break

    def Handler(self, cEvent, cValue):
        if (self.cEvent in ['Save          <F2>', '--SAVE--', 'F2:68', 'F2:113']) and self.oParent.cEvent in ['--EDIT--', 'Edit...               <F4>', 'F4:70', 'F4:115']:
        # ------ Сохранить отредактированную запись ------ #
            self.SaveData(self.nRecno, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            self.window.close()
        elif (self.cEvent in ['Save          <F2>', '--SAVE--', 'F2:68', 'F2:113']) and self.oParent.cEvent in ['--APPEND--', 'Append...          <F5>', 'F5:71', 'F5:116']:
        # ------ Сохранить отредактированную вновь добавленную запись ------ #
            self.oParent.data.append(['', '', '', '', '', '', '', '', ''])
            self.oParent.recno = self.oParent.recount
            self.SaveData(-1, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            self.window.close()
        elif  (self.cEvent in ['Save          <F2>', '--SAVE--', 'F2:68', 'F2:113']) and self.oParent.cEvent in ['--APPENDCOPY--', 'Append copy...  <F6>', 'F6:72', 'F6:117']:
        # ------ Сохранить отредактированную копию запись ------ #
            self.oParent.data.append(['', '', '', '', '', '', '', '', ''])
            self.oParent.recno = self.oParent.recount
            self.SaveData(-1, cValue)
            self.oParent.window['-DEVICE-'].update(values=self.oParent.data)
            self.window.close()
        elif  self.cEvent in ['Cancel       <Esc>', 'Escape:9', 'Escape:27']:
        # ------ Закрыть окно и выти без сохранения ------ #
            self.window.close()

    def SaveData(self, cRecNo, cValue):
    # ------ Запись значений в таблицу ------ #
        self.oParent.data[cRecNo][0] = cValue['-STATUS-']
        self.oParent.data[cRecNo][1] = cValue['-OPERATION-']
        self.oParent.data[cRecNo][2] = cValue['-IP-']
        self.oParent.data[cRecNo][3] = cValue['-MODEL-']
        self.oParent.data[cRecNo][4] = cValue['-IDdevice-']
        self.oParent.data[cRecNo][5] = cValue['-LOGIN-']
        self.oParent.data[cRecNo][6] = cValue['-PASSWORD-']
        self.oParent.data[cRecNo][7] = cValue['-SECRET-']
        self.oParent.data[cRecNo][8] = cValue['-COMMANDS-']
 

class ecrssh:
    def __init__(self, oSg):
    # ------ Определение интерфейсного объекта ------ #
        self.version = '(ver. 0.0.1)' 
        self.sg = oSg
        self.date = datetime.datetime.now()
        self._DateTimeStart = None
        self._TimerStartStop = None
        self.fStart = True
        if not os.path.isdir('Logs'):
            os.makedirs('Logs')            
        self.msg1  = 'ecrSSH.json '
        self.settings = self.sg.UserSettings(path='.')
        # ------ загружаем данные в таблицу ------ #
        self.data:list = self.settings['data']
        if self.data is None or not self.data:
        # ------ проверяем наличие данных в таблице ------ #
            self.data:list = [['execute', '', 'x.x.x.x', 'linux', 'id001', 'admin', '', 'need only for Cisco', '']]
        self.recno = 0
        self.recount = len(self.data)
        # ------ Определение Заголовков таблицы ------ #
        self.header_list:list = ['  status  ', '           name job            ', '     IP      ', '     model     ', '    ID device    ', '  login   ']
        # ------ Определение МЕНЮ ------ #
        self.menu_def:list = [['&File', ['!&Open...', '&Save', '---', 'E&xit']],
                         ['&Devices', ['&Append...          <F5>', 'Append &copy...  <F6>', '---', '&Edit...               <F4>', '---', '&Delete...           <F8>'], ],
                         ['&Run', ['&Mark/Unmark     <Space>', '---', '&Start                  <F2>', 'Start &ONE          <F3>']],]
        # ------ Определение полей ввода/вывода ------ #
        if sys.platform in "win32":
        # для Windows    
            self.size_msg = 92
        elif sys.platform in "linux":
        # для Linux
            self.size_msg = 112

        self.layout = [[self.sg.Menu(self.menu_def)],
                       [self.sg.Text(f' ', key='--Tttt--')],
                       [self.sg.Table(key='-DEVICE-',
                                      size=(140, 16),
                                      values=self.data,
                                      headings=self.header_list,
                                      display_row_numbers=False,
                                      justification='left',
                                      auto_size_columns=True,
                                      num_rows=min(16, 16))],
                       [self.sg.Button('Append...', key='--APPEND--'), self.sg.Button('Append copy...', key='--APPENDCOPY--'),
                        self.sg.Button('Edit...', key='--EDIT--'), self.sg.Button('Delete', key='--DELETE--'),
                        self.sg.Text('                   '),
                        self.sg.Button('Mark/Unmark', key='--Mark/Unmark--'),
                        self.sg.Text('                   '),
                        self.sg.Button('Start ALL SELECTED', key='--START--')],
                       [self.sg.Output(size=(151, 15), background_color='black', text_color='white', key='--OUTPUT--')],
                       [self.sg.Text('', relief=self.sg.RELIEF_SUNKEN, size=(25, 1), pad=(0, 3), key='-records-'),
                        self.sg.Text(self.msg1, relief=self.sg.RELIEF_SUNKEN, size=(self.size_msg, 1), pad=(0, 3), key='-status-'),
                        self.sg.Text('', relief=self.sg.RELIEF_SUNKEN, size=(17, 1), justification='right', pad=(0, 3), key='-TIMER-')]]

        
        # ------ Создание и позиционирование объекта интерфейса ------ #
        self.screen_size = self.sg.Window.get_screen_size()
        # set a default location centered and near the bottom of the screen
        if sys.platform in "win32":
        # для Windows    
            self.location = self.screen_size[0] - 1110, self.screen_size[1]- 720
        elif sys.platform in "linux":
        # для Linux
            self.location = self.screen_size[0] // 2, self.screen_size[1] - 200
#        self.location = self.screen_size[0], self.screen_size[1]
        self.window = sg.Window(f'Execute commands remotly with SSH {self.version}', self.layout, location=self.location, return_keyboard_events=True, use_default_focus=True, finalize=True)
                                #, finalize=False, moodel=True return_keyboard_events=True, 

        self.window.bind('<space>', '--Mark/Unmark--')      # Make sure your window is finalized first
        self.window.bind('<F2>', '--START--')      # Make sure your window is finalized first
        self.window.bind('<F3>', '--START1--')      # Make sure your window is finalized first
        self.window.bind('<F8>', '--DELETE--')      # Make sure your window is finalized first
        self.window.bind('<Home>', '--Home--')      # Make sure your window is finalized first
        self.window.bind('<End>', '--End--')      # Make sure your window is finalized first


    def refresh(self):
    # ------ Обновление объекта интерфейса ------ #
        IsEnable = self.window.enable
        self.window.enable = False
        # # Re-Grab table focus using ttk
        # self.window['-DEVICE-'].SetFocus(force=True)
        # table_row = self.window['-DEVICE-'].Widget.get_children()[current_row]
        # self.window['-DEVICE-'].Widget.selection_set(table_row)  # move selection
        # self.window['-DEVICE-'].Widget.focus(table_row)  # move focus
        # self.window['-DEVICE-'].Widget.see(table_row)  # scroll to show it
        self.window['-DEVICE-'].update(values=self.data)
        self.window['-DEVICE-'].SetFocus(force=True)
        #table_row = self.window['-DEVICE-'].Widget.get_children()[self.recno]
        self.window['-DEVICE-'].Widget.selection_set(self.recno+1)
        self.window['-DEVICE-'].Widget.focus(self.recno+1)  # move focus
        self.window['-DEVICE-'].Widget.see(self.recno+1)  # scroll to show it
        self.window.enable = True
        self.window.enable = IsEnable
        return

    def eventread(self):
    # ------ Определение цикла обработки ожидания события ------ #
        while True:
            # ------ Получение ожидаемого события ------ #
            if self.fStart == True:
                self.fStart = False
                self.window.enable = True
                self.cEvent, self.cValue = self.window.read(0)
                self.recno = 0
                self.refresh()
            else:
                self.window.enable = True
                self.cEvent, self.cValue = self.window.read(0)
                self.recno = self.cValue['-DEVICE-'][0]
            if self.cEvent in (self.sg.WIN_CLOSED, 'Exit'):
            # ------ Проверка ожидаемого события на завершение------ #
                # ------ Действительно завершение------ #
                self.window.close()
                # ------ Интерфейс закрыт------ #
                self.settings['data'] = self.data
                break
            else:
            # ------ Обработка событий поступающих от элементов управления ------ #
                self.Handler()
        
    def Handler(self):
    ## ------ Обработка поступивших событий от элементов управления------ #
        self.recount = len(self.data)
        self.window['-records-'].update(f'record: {self.recno}/{len(self.data)}')
        if self.cEvent not in ['__TIMEOUT__']:
           self.window['-status-'].update(f'{self.msg1} {self.cEvent}')
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.window['-TIMER-'].update(f'{self.date}')

        if self.cEvent in ['--Home--']:
        ## ------ переход в начало таблицы
            self.recno = 0
            self.refresh()
        elif self.cEvent in ['--End--']:
        ## ------ переход в конец таблицы
            self.recno = self.recount-1
            self.refresh()
        elif self.cEvent in ['--Mark/Unmark--', 'Mark/Unmark     <Space>']: #, 'space:65'
        ## ------ переключение режима обработки для устройства
            if self.data[self.recno][0] == 'execute':
                self.data[self.recno][0] = 'nothing'
            else:
                self.data[self.recno][0] = 'execute'
            self.refresh()
            self.settings['data'] = self.data
        elif self.cEvent in ['--EDIT--', 'Edit...               <F4>', 'F4:70', 'F4:115']:
        ## ------ переход к редактированию строки таблицы
            self.oedit = ecrsshModify(sg, self, self.recno, self.data[self.recno], self.cEvent).eventread()
            self.refresh()
            self.settings['data'] = self.data
        elif self.cEvent in ['--APPEND--', 'Append...          <F5>', 'F5:71', 'F5:116']:
        ## ------ переход к добавлению строки таблицы
            self.oedit = ecrsshModify(sg, self, self.recno, ['execute', '', 'x.x.x.x', 'linux', 'id'+str(self.recount), 'admin', '', 'need only for Cisco', '\necho [DATE] [TIME]\n'], self.cEvent).eventread()
            self.refresh()
            self.settings['data'] = self.data
        elif self.cEvent in ['--APPENDCOPY--', 'Append copy...  <F6>', 'F6:72', 'F6:117']:
        ## ------ переход к копированию и добавлению строки таблицы
            self.oedit = ecrsshModify(sg, self, self.recno, self.data[self.recno], self.cEvent).eventread()
            self.refresh()
            self.settings['data'] = self.data
        elif self.cEvent in ['--DELETE--', 'Delete...           <F8>']:
        ## ------ переход к удалению строки таблицы
            if sg.popup_yes_no(f'Do you really delete record {self.recno}?') == 'Yes':
                self.data.remove(self.data[self.recno])
                if self.data is None or not self.data:
                    self.data:list = [['execute', '', 'x.x.x.x', 'linux', 'id001', 'admin', '', 'need only for Cisco', '']]
                self.recno -= self.recno
                self.refresh()
                self.settings['data'] = self.data
        elif self.cEvent in ['--START--', 'Start                  <F2>']: #, 'F2:68', 'F2:113'
        ## ------ переход к выполнению всех комманд
            self.window['--OUTPUT--'].update('')
            self._DateTimeStart = datetime.datetime.now()
            self._TimerStartStop = None
            print('######################START ALL SELECTED######################')
            _count_ = 0
            for _device_ in self.data:
               if _device_[0] == 'execute':
                  _count_ = _count_ + 1
                  _device_[0] = 'working'
                  print(f'\n***************START {_device_[4]}********************')
                  retval = ExecuteCommands(self, _device_).send_now()
                  if retval:
                     print(f'***************FINISH {_device_[4]} OK***************')
                     _device_[0] = 'finished OK'
                  else:
                     print(f'***************ERROR {_device_[4]}***************')
                     _device_[0] = 'error'
            self._TimerStartStop = datetime.datetime.now() - self._DateTimeStart
            print(f'###############FINISH {_count_} SELECTED {self._TimerStartStop} sec###############')
            self.refresh()
        elif self.cEvent in ['--START1--', 'Start ONE          <F3>']: #, 'F3:69', 'F3:114'
        ## ------ переход к выполнению комманды
            self.window.enable = True
            print(f'\n***************START {self.data[self.recno][4]}********************')
            self.data[self.recno][0] = 'working'
            #self.refresh()
            retval = ExecuteCommands(self, self.data[self.recno]).send_now()
            if retval:
                print(f'***************FINISH {self.data[self.recno][4]} OK***************')
                self.data[self.recno][0] = 'finished OK'
            else:
                print(f'***************ERROR {self.data[self.recno][4]}***************')
                self.data[self.recno][0] = 'error'
            self.refresh()
        elif self.cEvent == 'Save':
            self.settings['data'] = self.data
            print('save to file [ecrSSH.json]')
        self.window.enable = True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _SCREEN = ecrssh(sg).eventread()
