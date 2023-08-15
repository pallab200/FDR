from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

# Custom drop-down list code
KV = '''
#:import Window kivy.core.window.Window

BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.7, 0.7, 0.7, 1  # Gray color (R, G, B, A)
        Rectangle:
            pos: self.pos
            size: self.size

    # Principal
    Label:
        text: "Investment:"
        color: (0, 0, 0, 1)  # Set text color to black
        font_size: '30sp'
        bold: True

    TextInput:
        id: principal_entry
        multiline: False
        input_type: 'number'
        font_size: '30sp'  # Increase font size
        halign: 'center'
        


    # Interest Rate
    Label:
        text: "Interest Rate:"
        color: (0, 0, 0, 1)  # Set text color to black
        font_size: '30sp'
        bold: True

    TextInput:
        id: interest_rate_entry
        multiline: False
        input_type: 'number'  # Set the input type to number
        font_size: '30sp'  # Increase font size
        halign: 'center'

    # Duration (Years)
    Label:
        text: "Years:"
        color: (0, 0, 0, 1)  # Set text color to black
        font_size: '30sp'
        bold: True

    TextInput:
        id: duration_years_entry
        multiline: False
        input_type: 'number'  # Set the input type to number
        font_size: '30sp'  # Increase font size
        halign: 'center'

    # Duration (Months)
    Label:
        text: "Months:"
        color: (0, 0, 0, 1)  # Set text color to black
        font_size: '30sp'
        bold: True

    TextInput:
        id: duration_months_entry
        multiline: False
        input_type: 'number'  # Set the input type to number
        font_size: '30sp'  # Increase font size
        halign: 'center'

    # Deduction options - using nested horizontal BoxLayouts
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        pos_hint: {'center_x': 0.5}  # Center the BoxLayout horizontally

        CheckBox:
            id: deduct_10_percent_check
            size_hint: None, None
            size: dp(36), dp(36)

        Label:
            text: "Vat 10%"
            size_hint: None, None
            font_size: '30sp'
            size: Window.width * 0.25, dp(36)
            color: (0, 0, 0, 1)  # Set text color to black
            bold: True

        CheckBox:
            id: deduct_15_percent_check
            size_hint: None, None
            size: dp(36), dp(36)

        Label:
            text: "Vat 15%"
            size_hint: None, None
            font_size: '30sp'
            size: Window.width * 0.25, dp(36)
            color: (0, 0, 0, 1)  # Set text color to black
            bold: True

    # Buttons for investment types
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)

        Button:
            text: 'DPS'
            size_hint: None, None
            font_size: '30sp'
            width: Window.width * 0.4
            height: dp(48)
            on_release: app.on_dps_button_press()

        Button:
            text: 'FDR'
            size_hint: None, None
            font_size: '30sp'
            width: Window.width * 0.4
            height: dp(48)
            on_release: app.on_fdr_button_press()

        Button:
            text: "X"
            size_hint: None, None
            font_size: '30sp'
            width: Window.width * 0.2
            height: dp(48)
            on_press: app.exit_app(self)
'''
def convert_to_words(number):
    words = {
        0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine',
        10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen',
        17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', 50: 'Fifty',
        60: 'Sixty', 70: 'Seventy', 80: 'Eighty', 90: 'Ninety'
    }

    if number < 0:
        return "Minus " + convert_to_words(abs(number))

    if number < 20:
        return words[number]

    if number < 100:
        tens = number // 10 * 10
        ones = number % 10
        return words[tens] + "-" + words[ones] if ones > 0 else words[tens]

    if number < 1000:
        hundreds = number // 100
        remainder = number % 100
        if remainder > 0:
            return words[hundreds] + " Hundred " + convert_to_words(remainder)
        else:
            return words[hundreds] + " Hundred"

    if number < 100000:
        thousands = number // 1000
        remainder = number % 1000
        if remainder > 0:
            return convert_to_words(thousands) + " Thousand " + convert_to_words(remainder)
        else:
            return convert_to_words(thousands) + " Thousand"

    if number < 10000000:
        lakhs = number // 100000
        remainder = number % 100000
        if remainder > 0:
            return convert_to_words(lakhs) + " Lac " + convert_to_words(remainder)
        else:
            return convert_to_words(lakhs) + " Lac"

    crores = number // 10000000
    remainder = number % 10000000
    if remainder > 0:
        return convert_to_words(crores) + " Crore " + convert_to_words(remainder)
    else:
        return convert_to_words(crores) + " Crore"

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class DepositCalculatorApp(MDApp):
    selected_calculation = 'DPS'
    main_button = None

    def build(self):
        layout = Builder.load_string(KV)
        return layout

    def on_dps_button_press(self):
        self.selected_calculation = 'DPS'
        self.calculate_interest(None)  # Call calculate_interest to update the UI

    def on_fdr_button_press(self):
        self.selected_calculation = 'FDR'
        self.calculate_interest(None)  # Call calculate_interest to update the UI

    def calculate_interest(self, instance):
        # Get user input values
        principal_str = self.root.ids.principal_entry.text.strip()
        interest_rate_str = self.root.ids.interest_rate_entry.text.strip()
        duration_years_str = self.root.ids.duration_years_entry.text.strip()
        duration_months_str = self.root.ids.duration_months_entry.text.strip()

         # Calculate the desired size based on screen size ratio
        screen_width, screen_height = Window.size
        popup_width_ratio = 1  # You can adjust this ratio as needed
        popup_height_ratio = 0.3  # You can adjust this ratio as needed
        popup_width = screen_width * popup_width_ratio
        popup_height = screen_height * popup_height_ratio

        # Validate required fields are not empty
        if not all([principal_str, interest_rate_str]):
            warning_popup = Popup(title='Warning',
                                  content=Label(text='Principal, Interest Rate and Duration fields are required.',
                                        font_size='18sp'),
                                  size_hint=(None, None),
                                  size=(popup_width, popup_height))  # Set the calculated size
            warning_popup.open()
            return

        # Convert input to float values
        principal = float(principal_str)
        interest_rate = float(interest_rate_str)
        dps_years = float(duration_years_str or 0)
        dps_months = float(duration_months_str or 0)
        total_months = dps_years * 12 + dps_months

        total_interest = 0
        total_investment = 0

        if self.selected_calculation == "FDR":
            # FDR-specific calculations
            total_months = 12
            monthly_interest_rate = interest_rate / 12 / 100
            total_interest = principal * monthly_interest_rate * total_months
            total_investment = principal + total_interest
            only_total_investment = principal

            # Apply deductions if selected
            deduction_10_percent = self.root.ids.deduct_10_percent_check.active
            deduction_15_percent = self.root.ids.deduct_15_percent_check.active

            if deduction_10_percent:
                deduction = 0.1 * total_interest
                total_interest -= deduction
                total_investment -= deduction

            if deduction_15_percent:
                deduction = 0.15 * total_interest
                total_interest -= deduction
                total_investment -= deduction

        elif self.selected_calculation == "DPS":
            # DPS-specific calculations
            total_months = 12
            monthly_interest_rate = interest_rate / 12 / 100
            dps_total_months = dps_years * 12 + dps_months
            dps_total_principal = principal * dps_total_months * (dps_total_months + 1) / 2
            dps_total = dps_total_principal / 24
            yearly_interest_rate = interest_rate / 100
            total_interest = dps_total * yearly_interest_rate
            total_investment = principal * dps_total_months + total_interest
            only_total_investment = principal * dps_total_months

            # Apply deductions if selected
            deduction_10_percent = self.root.ids.deduct_10_percent_check.active
            deduction_15_percent = self.root.ids.deduct_15_percent_check.active

            if deduction_10_percent:
                deduction = 0.1 * total_interest
                total_interest -= deduction
                total_investment -= deduction

            if deduction_15_percent:
                deduction = 0.15 * total_interest
                total_interest -= deduction
                total_investment -= deduction

        # Check for excess duty conditions
        excess_duty = 0
        if 100001 <= total_investment <= 500000:
            excess_duty = 150 * (dps_years + 1)
        elif 500001 <= total_investment <= 1000000:
            excess_duty = 150 * (dps_years + 1)
        elif 1000001 <= total_investment <= 10000000:
            excess_duty = 3000 * (dps_years + 1)
        elif 10000001 <= total_investment <= 50000000:
            excess_duty = 15000 * (dps_years + 1)
        elif 50000001 <= total_investment <= 5000000000:
            excess_duty = 50000 * (dps_years + 1)

        only_total_investment_words = convert_to_words(int(only_total_investment))
        net_total_investment = total_investment - excess_duty
        total_investment_words = convert_to_words(int(net_total_investment))

        # Calculate the desired size based on screen size ratio
        screen_width, screen_height = Window.size
        popup_width_ratio = 1  # You can adjust this ratio as needed
        popup_height_ratio = 0.6  # You can adjust this ratio as needed
        popup_width = screen_width * popup_width_ratio
        popup_height = screen_height * popup_height_ratio


        # Display the result in a popup
        result_popup = Popup(title='Result',
                            content=Label(text=f"Total Investment:\n" 
                                                f"{only_total_investment:.2f} TK\n"
                                                f"In Word:\n" 
                                                f"{only_total_investment_words} Taka Only\n"
                                                f"Total Interest:\n" 
                                                f"{total_interest:.2f} TK\n"
                                                f"Excess Duty:\n"
                                                f"{excess_duty:.2f} TK\n"
                                                f"Total Value:\n"
                                                f"{net_total_investment:.2f} TK\n"
                                                f"In Word:\n"
                                                f"{total_investment_words} Taka Only\n",
                                        font_size='18sp',
                                        text_size=(popup_width * 0.9, None)),  # Adjust width as needed
                            size_hint=(None, None),
                            size=(popup_width, popup_height))  # Set the calculated size

        result_popup.open()

    def exit_app(self, instance):
        self.stop()

if __name__ == '__main__':
    DepositCalculatorApp().run()
