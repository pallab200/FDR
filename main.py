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

<IconListItem>
    IconLeftWidget:
        icon: root.icon

BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)

    MDDropDownItem:
        id: drop_item
        pos_hint: {'center_x': .5, 'center_y': .5}
        text: 'Monthly Savings (DPS)'  # Updated item name to "Monthly Savings (DPS)"
        on_release: app.menu.open()

    # Principal
    Label:
        text: "Investment:"
        color: (0, 0, 0, 1)  # Set text color to black

    TextInput:
        id: principal_entry
        multiline: False
        input_type: 'number'  # Set the input type to number

    # Interest Rate
    Label:
        text: "Interest Rate:"
        color: (0, 0, 0, 1)  # Set text color to black

    TextInput:
        id: interest_rate_entry
        multiline: False
        input_type: 'number'  # Set the input type to number

    # Duration (Years)
    Label:
        text: "Years:"
        color: (0, 0, 0, 1)  # Set text color to black

    TextInput:
        id: duration_years_entry
        multiline: False
        input_type: 'number'  # Set the input type to number

    # Duration (Months)
    Label:
        text: "Months:"
        color: (0, 0, 0, 1)  # Set text color to black

    TextInput:
        id: duration_months_entry
        multiline: False
        input_type: 'number'  # Set the input type to number

    # Deduction options - using nested horizontal BoxLayouts
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)

        CheckBox:
            id: deduct_10_percent_check
            size_hint: None, None
            size: dp(48), dp(48)

        Label:
            text: "Vat 10%"
            size_hint: None, None
            size: Window.width * 0.4, dp(48)
            color: (0, 0, 0, 1)  # Set text color to black

        CheckBox:
            id: deduct_15_percent_check
            size_hint: None, None
            size: dp(48), dp(48)

        Label:
            text: "Vat 15%"
            size_hint: None, None
            size: Window.width * 0.4, dp(48)
            color: (0, 0, 0, 1)  # Set text color to black

    # Calculate button
    Button:
        text: "Calculate"
        size_hint: None, None
        width: Window.width * 1
        height: dp(48)
        on_press: app.calculate_interest(self)

    # Exit button
    Button:
        text: "Exit"
        size_hint: None, None
        width: Window.width * 0.2
        height: dp(36)
        on_press: app.exit_app(self)
'''
def convert_to_words(number):
    words = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
        10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
        17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty',
        60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'
    }

    if number < 0:
        return "minus " + convert_to_words(abs(number))

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
            return words[hundreds] + " hundred " + convert_to_words(remainder)
        else:
            return words[hundreds] + " hundred"

    if number < 100000:
        thousands = number // 1000
        remainder = number % 1000
        if remainder > 0:
            return convert_to_words(thousands) + " thousand " + convert_to_words(remainder)
        else:
            return convert_to_words(thousands) + " thousand"

    if number < 10000000:
        lakhs = number // 100000
        remainder = number % 100000
        if remainder > 0:
            return convert_to_words(lakhs) + " lac " + convert_to_words(remainder)
        else:
            return convert_to_words(lakhs) + " lac"

    crores = number // 10000000
    remainder = number % 10000000
    if remainder > 0:
        return convert_to_words(crores) + " crore " + convert_to_words(remainder)
    else:
        return convert_to_words(crores) + " crore"

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class DepositCalculatorApp(MDApp):
    selected_calculation = 'Monthly Savings (DPS)'
    main_button = None

    def build(self):
        layout = Builder.load_string(KV)

        # Dropdown list
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": "Monthly Savings (DPS)",  # Updated item name to "Monthly Savings (DPS)"
                "height": dp(56),
                "on_release": lambda x="Monthly Savings (DPS)": self.on_dropdown_select(x),
            },
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": "Fixed Deposit (FDR)",  # Updated item name to "Fixed Deposit (FDR)"
                "height": dp(56),
                "on_release": lambda x="Fixed Deposit (FDR)": self.on_dropdown_select(x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=layout.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        return layout

    def on_dropdown_select(self, text_item):
        self.selected_calculation = text_item
        self.root.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def calculate_interest(self, instance):
        # Get user input values
        principal_str = self.root.ids.principal_entry.text.strip()
        interest_rate_str = self.root.ids.interest_rate_entry.text.strip()
        duration_years_str = self.root.ids.duration_years_entry.text.strip()
        duration_months_str = self.root.ids.duration_months_entry.text.strip()

        # Validate required fields are not empty
        if not all([principal_str, interest_rate_str]):
            warning_popup = Popup(title='Warning',
                                  content=Label(text='Principal and Interest Rate fields are required.'),
                                  size_hint=(None, None),
                                  size=(400, 200))
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

        if self.selected_calculation == "Fixed Deposit (FDR)":
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

        elif self.selected_calculation == "Monthly Savings (DPS)":
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


        # Display the result in a popup
        result_popup = Popup(title='Result',
                             content=Label(text=f"Total investment: {only_total_investment:.2f} TK\n"
                                                f"In Word: {only_total_investment_words} taka only\n"
                                                f"Total interest: {total_interest:.2f} TK\n"
                                                f"Excess duty: {excess_duty:.2f} TK\n"
                                                f"Total Value: {net_total_investment:.2f} TK\n"
                                                f"In Word: {total_investment_words} taka only\n"),
                                                
                             size_hint=(None, None),
                             size=(400, 200))
        result_popup.open()

    def exit_app(self, instance):
        self.stop()

if __name__ == '__main__':
    DepositCalculatorApp().run()
