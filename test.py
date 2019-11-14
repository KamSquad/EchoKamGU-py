from kivy.app import App
from kivy.uix.button import Button


class KofeString(App):
    def build(self):
        return Button(text = "kofe String!!!!",
                      font_size = 30,
                      on_press = self.btn_press,
                      background_color = [1,0,0,1])     #rgba
    def btn_press(self, instance):
        print('eeeeee, i like kofe and string!')
        instance.text = 'i like kofe and string!'

if __name__ == "__main__":
    KofeString().run()

