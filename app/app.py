import reflex as rx
from app.state import CalculatorState


def calculator_button(
    text: str, on_click: rx.event.EventType, class_name: str = ""
) -> rx.Component:
    return rx.el.button(
        text,
        on_click=on_click,
        class_name=f"relative overflow-hidden text-2xl font-semibold rounded-lg h-16 w-16 md:h-20 md:w-20 active:shadow-inner active:scale-95 transition-all duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-orange-500 {class_name}",
    )


def operator_button(op: str) -> rx.Component:
    is_active = (CalculatorState.operation == op) & (
        CalculatorState.current_operand == ""
    )
    return calculator_button(
        text=op,
        on_click=lambda: CalculatorState.on_operator_click(op),
        class_name=rx.cond(
            is_active,
            "bg-white text-orange-500 shadow-md",
            "bg-orange-500 text-white hover:bg-orange-600 shadow-lg",
        ),
    )


def digit_button(digit: str) -> rx.Component:
    return calculator_button(
        text=digit,
        on_click=lambda: CalculatorState.on_digit_click(digit),
        class_name="bg-gray-700 text-white hover:bg-gray-600 shadow-lg",
    )


def special_button(text: str, on_click: rx.event.EventType) -> rx.Component:
    return calculator_button(
        text=text,
        on_click=on_click,
        class_name="bg-gray-500 text-white hover:bg-gray-400 shadow-lg",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            CalculatorState.formatted_display,
                            class_name="text-5xl md:text-7xl font-light text-right break-all p-4",
                        ),
                        class_name="bg-gray-800 text-white rounded-t-2xl w-full h-28 md:h-32 flex items-center justify-end overflow-hidden",
                    ),
                    rx.el.div(
                        special_button("C", CalculatorState.on_clear_click),
                        special_button("DEL", CalculatorState.on_delete_click),
                        rx.el.div(),
                        operator_button("/"),
                        digit_button("7"),
                        digit_button("8"),
                        digit_button("9"),
                        operator_button("*"),
                        digit_button("4"),
                        digit_button("5"),
                        digit_button("6"),
                        operator_button("-"),
                        digit_button("1"),
                        digit_button("2"),
                        digit_button("3"),
                        operator_button("+"),
                        rx.el.div(
                            calculator_button(
                                "0",
                                on_click=lambda: CalculatorState.on_digit_click("0"),
                                class_name="bg-gray-700 text-white hover:bg-gray-600 w-full shadow-lg",
                            ),
                            class_name="col-span-2",
                        ),
                        digit_button("."),
                        calculator_button(
                            "=",
                            CalculatorState.on_equals_click,
                            "bg-orange-500 text-white hover:bg-orange-600 shadow-lg",
                        ),
                        class_name="grid grid-cols-4 gap-2 p-4",
                    ),
                    class_name="bg-gray-900 rounded-2xl shadow-2xl w-full max-w-sm mx-auto",
                ),
                class_name="font-['Lato']",
            ),
            class_name="flex items-center justify-center min-h-screen bg-gray-800 p-4",
        ),
        class_name="bg-gray-800",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)