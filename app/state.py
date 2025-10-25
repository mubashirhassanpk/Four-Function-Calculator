import reflex as rx
import math
import logging


class CalculatorState(rx.State):
    display: str = "0"
    current_operand: str = ""
    previous_operand: str = ""
    operation: str = ""
    has_error: bool = False

    def _format_display(self, value: str) -> str:
        if self.has_error:
            return "Error"
        if not value:
            return "0"
        try:
            num = float(value)
            if num == 0:
                return "0"
            if abs(num) > 1000000000000.0 or (abs(num) < 1e-09 and num != 0):
                return f"{num:.2e}"
            if num == int(num):
                return str(int(num))
            return str(round(num, 9))
        except (ValueError, TypeError) as e:
            logging.exception(f"Error formatting display: {e}")
            self.has_error = True
            return "Error"

    @rx.var
    def formatted_display(self) -> str:
        return self._format_display(self.display)

    def _calculate(self):
        try:
            prev = float(self.previous_operand)
            curr = float(self.current_operand)
            if self.operation == "+":
                result = prev + curr
            elif self.operation == "-":
                result = prev - curr
            elif self.operation == "*":
                result = prev * curr
            elif self.operation == "/":
                if curr == 0:
                    self.has_error = True
                    return
                result = prev / curr
            else:
                result = curr
            self.display = str(result)
            self.current_operand = str(result)
            self.previous_operand = ""
            self.operation = ""
        except (ValueError, ZeroDivisionError) as e:
            logging.exception(f"Error during calculation: {e}")
            self.has_error = True
            self.display = "Error"

    @rx.event
    def on_digit_click(self, digit: str):
        if self.has_error:
            self.clear_all()
        if self.display == "0" and digit != ".":
            self.display = ""
        if digit == "." and "." in self.display:
            return
        if len(self.display) >= 15:
            return
        self.display += digit
        self.current_operand = self.display

    @rx.event
    def on_operator_click(self, op: str):
        if self.has_error:
            return
        if self.current_operand == "" and self.previous_operand == "":
            return
        if self.previous_operand != "" and self.current_operand != "":
            self._calculate()
            if self.has_error:
                self.display = "Error"
                return
        self.operation = op
        if self.current_operand != "":
            self.previous_operand = self.current_operand
        self.current_operand = ""
        self.display = "0"

    @rx.event
    def on_equals_click(self):
        if self.has_error or self.operation == "" or self.previous_operand == "":
            return
        if self.current_operand == "":
            self.current_operand = self.previous_operand
        self._calculate()
        if self.has_error:
            self.display = "Error"

    @rx.event
    def on_clear_click(self):
        self.clear_all()

    @rx.event
    def clear_all(self):
        self.display = "0"
        self.current_operand = ""
        self.previous_operand = ""
        self.operation = ""
        self.has_error = False

    @rx.event
    def on_delete_click(self):
        if self.has_error:
            self.clear_all()
            return
        if self.display != "0" and len(self.display) > 0:
            self.display = self.display[:-1]
            if self.display == "":
                self.display = "0"
        self.current_operand = self.display