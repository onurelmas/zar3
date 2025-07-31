import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random
import os
from kivy.animation import Animation
from kivy.core.audio import SoundLoader # Ses yükleyiciyi içe aktar

# Arka plan rengini ayarla
Window.clearcolor = (0.93, 0.93, 0.93, 1) # RGBA

class DiceApp(App):
    def build(self):
        self.root_layout = FloatLayout()
        self.dice_images = []
        self.anim_duration = 1
        self.dice_sound = None # Ses nesnesi için değişken

        # Zar görsellerini yükle
        for i in range(1, 7):
            path = os.path.join('dice_images', f'dice ({i}).png')
            if not os.path.exists(path):
                print(f"Hata: Resim dosyası bulunamadı: {path}")
                continue
            self.dice_images.append(path)

        # Ses dosyasını yükle
        sound_path = os.path.join('dice_sounds', 'shaking-and-rolling-dice.mp3')
        if os.path.exists(sound_path):
            self.dice_sound = SoundLoader.load(sound_path)
            if self.dice_sound:
                print(f"Ses dosyası yüklendi: {sound_path}")
            else:
                print(f"Hata: Ses dosyası yüklenemedi: {sound_path}")
        else:
            print(f"Uyarı: Ses dosyası bulunamadı: {sound_path}. Lütfen 'dice_sounds' klasörünü kontrol edin.")

        # Başlangıçta iki zar oluştur ve göster
        self.dice1 = Image(source=self.get_random_dice_image(), allow_stretch=True, keep_ratio=True)
        self.dice2 = Image(source=self.get_random_dice_image(), allow_stretch=True, keep_ratio=True)
        self.dice1.opacity = 1
        self.dice2.opacity = 1

        self.root_layout.add_widget(self.dice1)
        self.root_layout.add_widget(self.dice2)

        Window.bind(size=self.update_dice_positions)
        self.update_dice_positions(Window, Window.size)

        Window.bind(on_touch_down=self.on_touch_down)

        return self.root_layout

    def get_random_dice_image(self):
        if not self.dice_images:
            print("Uyarı: Zar görseli bulunamadı. Lütfen 'dice_images' klasörünü kontrol edin.")
            return None
        return random.choice(self.dice_images)

    def on_touch_down(self, instance, touch):
        self.animate_dice()
        # Ses dosyasını çal
        if self.dice_sound:
            self.dice_sound.play()
        return True

    def animate_dice(self):
        # Mevcut zarlar için büyüme ve kaybolma animasyonu
        anim_out1 = Animation(opacity=0, scale_x=1.5, scale_y=1.5, duration=self.anim_duration)
        anim_out2 = Animation(opacity=0, scale_x=1.5, scale_y=1.5, duration=self.anim_duration)

        def finish_anim_out1(*args):
            self.dice1.source = self.get_random_dice_image()
            self.dice1.scale_x = 1
            self.dice1.scale_y = 1
            anim_in1.start(self.dice1)

        def finish_anim_out2(*args):
            self.dice2.source = self.get_random_dice_image()
            self.dice2.scale_x = 1
            self.dice2.scale_y = 1
            anim_in2.start(self.dice2)

        anim_out1.bind(on_complete=finish_anim_out1)
        anim_out2.bind(on_complete=finish_anim_out2)
        anim_out1.start(self.dice1)
        anim_out2.start(self.dice2)

        # Yeni zarlar için büyükten küçüğe görünme animasyonu
        anim_in1 = Animation(opacity=1, scale_x=1, scale_y=1, duration=self.anim_duration)
        anim_in2 = Animation(opacity=1, scale_x=1, scale_y=1, duration=self.anim_duration)
        self.dice1.opacity = 0
        self.dice1.scale_x = 0.5
        self.dice1.scale_y = 0.5
        self.dice2.opacity = 0
        self.dice2.scale_x = 0.5
        self.dice2.scale_y = 0.5


    def update_dice_positions(self, instance, value):
        window_width, window_height = value

        if window_width < window_height:
            longer_dim = window_height
            shorter_dim = window_width
            is_portrait = True
        else:
            longer_dim = window_width
            shorter_dim = window_height
            is_portrait = False

        dice_size = shorter_dim / 3

        if (longer_dim - 2 * dice_size) < 0:
            gap_and_padding = (longer_dim - 2 * dice_size) / 3 if longer_dim > 2 * dice_size else 10
            edge_padding = gap_and_padding
            gap_between_dice = gap_and_padding
        else:
            edge_padding = (longer_dim - 2 * dice_size) / 3
            gap_between_dice = edge_padding

        if is_portrait:
            center_x = (window_width - dice_size) / 2
            self.dice1.pos = (center_x, window_height - edge_padding - dice_size)
            self.dice2.pos = (center_x, window_height - edge_padding - dice_size - gap_between_dice - dice_size)
        else:
            center_y = (window_height - dice_size) / 2
            self.dice1.pos = (edge_padding, center_y)
            self.dice2.pos = (edge_padding + dice_size + gap_between_dice, center_y)

        self.dice1.size_hint = (None, None)
        self.dice1.size = (dice_size, dice_size)
        self.dice2.size_hint = (None, None)
        self.dice2.size = (dice_size, dice_size)
        self.dice1.scale_x = 1
        self.dice1.scale_y = 1
        self.dice2.scale_x = 1
        self.dice2.scale_y = 1


# Uygulamayı çalıştır
if __name__ == '__main__':
    if not os.path.exists('dice_images'):
        print("Uyarı: 'dice_images' klasörü bulunamadı. Lütfen zar görsellerini bu klasöre yerleştirin.")
        print("Uygulama düzgün çalışmayabilir.")
    if not os.path.exists('dice_sounds'):
        print("Uyarı: 'dice_sounds' klasörü bulunamadı. Lütfen ses dosyasını bu klasöre yerleştirin.")
        print("Zar atıldığında ses çalmayabilir.")

    DiceApp().run()