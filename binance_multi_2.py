import flet as ft
import requests
import time
import ccxt
import random
from web3 import Web3
import xlrd
import pandas


def get_balance_binance(symbol, API_KEY, API_SECRET):
    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    return account_binance.fetch_balance()['total'][symbol]

def binance_withdraw(address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET):

    account_binance = ccxt.binance({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        account_binance.withdraw(
            code    = symbolWithdraw,
            amount  = amount_to_withdrawal,
            address = address,
            tag     = None, 
            params  = {
                "network": network
            }
        )
        return ft.Text(f">>> Успешно | {address} | {amount_to_withdrawal}", color="Green")
    except Exception as error:
        return ft.Text(f">>> Неудачно | {address} | ошибка : {error}", color="Red")

stop_flag = False


def map_token_to_network_dropdown(token):
    match token:
        case 'ETH':
            return [ft.dropdown.Option("ETH"), ft.dropdown.Option("BSC"), ft.dropdown.Option("ARBITRUM"), ft.dropdown.Option("OPTIMISM")]
        case 'BNB':
            return [ft.dropdown.Option("BNB")]
        case 'AVAX':
            return [ft.dropdown.Option("AVAX"), ft.dropdown.Option("AVAXC")]
        case 'MATIC':
            return [ft.dropdown.Option("Polygon")]
        case 'FTM':
            return [ft.dropdown.Option('FTM')]
        case 'USDT':
            return [ft.dropdown.Option("BSC"), ft.dropdown.Option("AVAX"), ft.dropdown.Option("MATIC")]
        case 'USDC':
            return [ft.dropdown.Option("BSC"), ft.dropdown.Option("AVAX"), ft.dropdown.Option("MATIC")]
        case 'ARB':
            return [ft.dropdown.Option('ARB')]
        case 'APT':
            return [ft.dropdown.Option('APT')]
        case 'ATOM':
            return [ft.dropdown.Option("ATOM"), ft.dropdown.Option("BSC")]
        case 'SUI':
            return [ft.dropdown.Option("SUI")]
        case 'OP':
            return [ft.dropdown.Option("OPTIMISM")]




def separate_wallets(path, page, lv):
        with open(path, "r") as f:
            wallets_list = [row.strip() for row in f]
        lv.controls.append(ft.Text(f"{len(wallets_list)} strings imported", color="Blue"))
        page.update()
        return wallets_list


def binance_column(page):

    def start_click(e):
        global stop_flag
        stop_flag = False
        lv.controls.append(ft.Text(f'start clicked'))
        page.update()
        if check_to_correct_values():
            try:
                lv.controls.append(ft.Text(f'Block try, starting for'))
                page.update()
                for wallet in separate_wallets(wallets_file_path.value, page, lv):
                    if stop_flag:
                        lv.controls.append(ft.Text(f"Stopped"))
                        page.update()
                        break
                    amount_to_withdrawal = round(random.uniform(float(amount_from.value), float(amount_to.value)), int(round_int.value)) # 6 - это число знаков после запятой
                    lv.controls.append(ft.Text(f"Amount_to_withdrawal {amount_to_withdrawal}", color="Blue"))
                    page.update()
                    lv.controls.append(binance_withdraw(wallet, amount_to_withdrawal, token_dropdown.value, network_dropdown.value, api_key_string.value, api_secret_string.value))
                    wait = random.randint(int(sleep_from.value), int(sleep_to.value))
                    lv.controls.append(ft.Text(f'{wait} seconds to wait'))
                    page.update()
                    time.sleep(wait)
                lv.controls.append(ft.Text(f'{wait} seconds to wait'))    
            except Exception as error:
                lv.controls.append(ft.Text(f"Line {error}", color="Red"))
                page.update()
        else:
            lv.controls.append(ft.Text(f'Please, fill the blank fields'))
            page.update()


    


    def check_to_correct_values():

        api_key_string.error_text = "" if api_key_string.value else "Please enter API_key from binance"
        api_secret_string.error_text = "" if api_secret_string.value else "Please enter secret_key from binance"
        token_dropdown.error_text = "" if token_dropdown.value else "did not choose"
        network_dropdown.error_text = "" if network_dropdown.value else "did not choose"
        round_int.error_text = "" if round_int.value else "did not choose"
        amount_from.error_text = "" if amount_from.value else "-"
        amount_to.error_text = "" if amount_to.value else "-"
        sleep_from.error_text = "" if sleep_from.value else "-"
        sleep_to.error_text = "" if sleep_to.value else "-"
        
        try:
            if float(amount_from.value) > float(amount_to.value):
                amount_from.error_text = "more than"
        except:
            pass
        try:
            if int(sleep_from.value) >= int(sleep_to.value):
                sleep_from.error_text = "more than"
        except:
            pass

        page.update()

        errors = [api_key_string.error_text, api_secret_string.error_text, token_dropdown.error_text, network_dropdown.error_text, round_int.error_text, amount_from.error_text, amount_to.error_text, sleep_from.error_text, sleep_to.error_text]

        for error in errors:
            if error == "":
                return False
        return True   
     

    def copy_to_clipboard(e):
        ip = requests.get('https://ident.me').text #https://icanhazip.com
        page.set_clipboard(ip)
        page.show_snack_bar(ft.SnackBar(ft.Text(f"Copied {ip}"), open=True))

    
    def stop_click(e):
        global stop_flag
        stop_flag = True

    def balance_click(e):
        if token_dropdown.value == None:
            balance_view.value = f'Выбери выше токен'
            page.update()
        else:
            balance_view.value = f''
            balance_progress.visible = True
            page.update()
            amount = get_balance_binance(symbol=token_dropdown.value, API_KEY=api_key_string.value, API_SECRET=api_secret_string.value)
            balance_view.value = f'{amount}  {token_dropdown.value}'
            balance_progress.visible = False
            page.update()

    def network_for_token(e):
        network_dropdown.options = map_token_to_network_dropdown(token_dropdown.value)
        page.update()


    ip = requests.get('https://ident.me').text #"https://api.ipify.org
    page.window_width=500
    page.window_height=800
    ipToWL = ft.Row(controls=[ft.Text(value=f"добавь свой ip", style=ft.TextThemeStyle.TITLE_MEDIUM), ft.TextButton(text=ip, on_click = copy_to_clipboard), ft.Text(value="в WL_Binance", style=ft.TextThemeStyle.TITLE_MEDIUM)])
    api_key_string = ft.TextField(label="API_KEY", height=60, width=450)
    api_secret_string = ft.TextField(label="API_secret", height=60, width=450)
    #wallets_path = ft.TextField(hint_text="path/wallets.txt in format 1perString", label="wallets.txt", helper_text='if file wallets.txt is in the same folder, leave this empty')

    token_dropdown = ft.Dropdown(width=100, border_radius=30, options=[ft.dropdown.Option("BNB"), ft.dropdown.Option("USDT"), ft.dropdown.Option("MATIC"), ft.dropdown.Option("ETH"), ft.dropdown.Option("FTM"), ft.dropdown.Option("AVAX"), ft.dropdown.Option("USDC"), ft.dropdown.Option("ARB"), ft.dropdown.Option("OP"), ft.dropdown.Option("SUI"), ft.dropdown.Option("ATOM")], on_change=network_for_token)
    network_dropdown = ft.Dropdown(width=120, border_radius=30, options=[ft.dropdown.Option("BSC"), ft.dropdown.Option("POLYGON"), ft.dropdown.Option("ETH")])
    chooses = ft.Row(controls=[ft.Text("Choose token"),token_dropdown, ft.Text("Choose network"),network_dropdown])
    amount_from = ft.TextField(label="from", width=100, value=0.01, height=50)
    amount_to = ft.TextField(label="to", width=100, value=0.01, height=50)
    round_int = ft.Dropdown(width=50, height=60, border_radius=3, value="4", options=[ft.dropdown.Option("3"), ft.dropdown.Option("4"), ft.dropdown.Option("5"), ft.dropdown.Option("6")]) # ft.TextField(label="round", width=100, value=4, height=50, border_radius=5)
    round_row = ft.Row(controls=[ft.Text("Количество знаков после ,"), round_int])
    amount = ft.Row(controls=[ft.Text("Input an amount into each wallet"), amount_from, amount_to])
    
    sleep_from = ft.TextField(label="from", hint_text="sec", width=100, value=10, height=50)
    sleep_to = ft.TextField(label="to", hint_text="sec", width=100, value=30, height=50)
    sleep = ft.Row(controls=[ft.Text("Sleep"),sleep_from, sleep_to])
    # apiKeyRow = ApiInput("API_KEY").make_row()
    # apiKeyRow2 = ApiInput("API_secret").make_row()
    # pathRow = ApiInput("path/wallets.txt in format 1perString").make_row()
    
    
    start_button = ft.ElevatedButton(text='Start', on_click=start_click)
    stop_button = ft.ElevatedButton(text='Stop', on_click=stop_click)
    balance_button = ft.ElevatedButton(text='Balance:', on_click=balance_click)
    balance_view = ft.Text(f"")
    balance_progress = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
    buttons = ft.Row(controls=[start_button, stop_button, balance_button, balance_progress,  balance_view])
    lv = ft.ListView(expand=1, auto_scroll=True)
    
    def wallets_file_result(e: ft.FilePickerResultEvent):
        wallets_file_path.value = e.files[0].path if e.files else "Cancelled!"
        wallets_file_path.update()
        

    wallets_file_dialog = ft.FilePicker(on_result=wallets_file_result)
    wallets_file_path = ft.Text("кошельки.txt")


    files_button = ft.Row([ft.ElevatedButton("Pick file",icon=ft.icons.UPLOAD_FILE, on_click=lambda _: wallets_file_dialog.pick_files(),), wallets_file_path])
    page.overlay.extend([wallets_file_dialog])
    # page.add(ipToWL, api_key_string, api_secret_string, files_button, chooses,round_row, amount, sleep, buttons, lv)    

    return ft.Column(controls=[ipToWL, api_key_string, api_secret_string, files_button, chooses,round_row, amount, sleep, buttons, lv])






def collector_native(page):
    lv = ft.ListView(expand=1, auto_scroll=True)
    
    def wallets_file_result(e: ft.FilePickerResultEvent):
        wallets_file_path.value = e.files[0].path if e.files else "Cancelled!"
        wallets_file_path.update()
        

    wallets_file_dialog = ft.FilePicker(on_result=wallets_file_result)
    wallets_file_path = ft.Text("address:private_key")

    destination_address = ft.TextField(label="to")
    amount = ft

    sleep_from = ft.TextField(label="from", hint_text="sec", width=100, value=10, height=50)
    sleep_to = ft.TextField(label="to", hint_text="sec", width=100, value=30, height=50)
    sleep = ft.Row(controls=[ft.Text("Sleep"),sleep_from, sleep_to])

    files_button = ft.Row([ft.ElevatedButton("Pick file",icon=ft.icons.UPLOAD_FILE, on_click=lambda _: wallets_file_dialog.pick_files(),), wallets_file_path])
    page.overlay.extend([wallets_file_dialog])
    #for wallet in separate_wallets(wallets_file_path.value):
    return ft.Column(controls=[files_button, destination_address, lv])



def wallets_balance_checker(page):
    lv = ft.ListView(expand=1, auto_scroll=True)
    
    def wallets_file_result(e: ft.FilePickerResultEvent):
        wallets_file_path.value = e.files[0].path if e.files else "Cancelled!"
        wallets_file_path.update()
        

    wallets_file_dialog = ft.FilePicker(on_result=wallets_file_result)
    wallets_file_path = ft.Text("addresses to be checked")

    
    files_button = ft.Row([ft.ElevatedButton("Pick file",icon=ft.icons.UPLOAD_FILE, on_click=lambda _: wallets_file_dialog.pick_files(),), wallets_file_path])
    page.overlay.extend([wallets_file_dialog])


    def network_for_token(e):
        network_dropdown.options = map_token_to_network_dropdown(token_dropdown.value)
        page.update()


    
    def start_click(e):
        lv.controls.append(ft.Text(f'start clicked'))
        page.update()
        try:
            wallets, balances, network, token = [], [], [], []
            for wallet in separate_wallets(wallets_file_path.value, page, lv):
                wallets.append(wallet)
                balances.append(checker(wallet))
                network.append(network_dropdown.value)
                token.append(token_dropdown.value)
            
            df = pandas.DataFrame()
            df['wallet'] = wallets
            df['balance'] = balances
            df['token'] = token
            df['network'] = network
            writer = pandas.ExcelWriter('./sheet.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='@pandaonchain', index=False)

            writer.sheets['@pandaonchain'].set_column('A:A', 50)
            writer.sheets['@pandaonchain'].set_column('B:B', 13)
            writer.sheets['@pandaonchain'].set_column('C:C', 10)
            writer.sheets['@pandaonchain'].set_column('D:D', 10)
            writer.save()
            lv.controls.append(ft.Text(f'sheet complete'))
            page.update()
        except Exception as error:
            lv.controls.append(ft.Text(f'{error}'))
            page.update()


    def checker(adrs):
        rpc = "https://rpc.ankr.com/eth_goerli"
        web3 = Web3(Web3.HTTPProvider(rpc))
        check_sum = web3.to_checksum_address(adrs)
        balance = web3.eth.get_balance(check_sum)
        return web3.from_wei(balance, "ether")


    token_dropdown = ft.Dropdown(width=100, border_radius=30, options=[ft.dropdown.Option("BNB"), ft.dropdown.Option("USDT"), ft.dropdown.Option("MATIC"), ft.dropdown.Option("ETH"), ft.dropdown.Option("FTM"), ft.dropdown.Option("AVAX"), ft.dropdown.Option("USDC"), ft.dropdown.Option("ARB"), ft.dropdown.Option("OP"), ft.dropdown.Option("SUI"), ft.dropdown.Option("ATOM")], on_change=network_for_token)
    network_dropdown = ft.Dropdown(width=120, border_radius=30, options=[ft.dropdown.Option("BSC"), ft.dropdown.Option("POLYGON"), ft.dropdown.Option("ETH")])
    choises = ft.Row(controls=[ft.Text("Choose token"),token_dropdown, ft.Text("Choose network"),network_dropdown])
    start_button = ft.ElevatedButton(text='Start', on_click=start_click)

    return ft.Column(controls=[files_button, choises, start_button, lv])



def main(page: ft.page):

    page.title = "Binance multisender by @pandaonchain"

    tabss = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Binance multisender",
                content=ft.Container(
                    content=binance_column(page)
                ),
            ),
            ft.Tab(
                text="Collector native",
                content=ft.Container(
                    content=collector_native(page)
                ),
            ),
            ft.Tab(
                text="Wallets Balance Checker",
                icon=ft.icons.SETTINGS,
                content=ft.Container(
                    content=wallets_balance_checker(page)
                ),
            ),
        ],
    )
    page.add(tabss)#api_key_string, api_secret_string, files_button, chooses,round_row, amount, sleep, buttons, lv, button)

ft.app(target=main)