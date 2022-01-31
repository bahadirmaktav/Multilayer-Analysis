from msilib.schema import CheckBox
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

class MainLayout(BoxLayout):
    pass

class MaterialProperitiesInputLayout(BoxLayout):
    pass

class DesignWavelengthInputLayout(BoxLayout):
    pass

class ThicknessDividerCoefficientLayout(BoxLayout):
    pass

class WavelengthRangeLayout(BoxLayout):
    pass

class StepSizeIn1nmLayout(BoxLayout):
    pass

class MultilayerSequenceLayout(BoxLayout):
    pass

class LabelWidget(Label):
    pass

class TextInputWidget(TextInput):
    pass

class CheckBoxWidget(CheckBox):
    pass

class MultilayerAnalysisApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    Window.clearcolor = (0.08, 0.26, 0.31, 1)
    MultilayerAnalysisApp().run()
