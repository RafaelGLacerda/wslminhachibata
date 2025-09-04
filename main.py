from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import yt_dlp
import threading
import os


class DownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.add_widget(Label(text="📥 Downloader de Vídeos", font_size=22, size_hint=(1, 0.1)))

        # Entrada de links
        self.links_input = TextInput(
            hint_text="Cole os links (um por linha)...",
            multiline=True,
            size_hint=(1, 0.3),
        )
        self.add_widget(self.links_input)

        # Botão
        self.download_btn = Button(
            text="⬇️ Baixar",
            size_hint=(1, 0.1),
            background_color=(0, 0.6, 0.3, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)

        # Área de status
        self.log_area = GridLayout(cols=1, size_hint_y=None)
        self.log_area.bind(minimum_height=self.log_area.setter("height"))

        scroll = ScrollView(size_hint=(1, 0.5))
        scroll.add_widget(self.log_area)
        self.add_widget(scroll)

    def log(self, msg):
        Clock.schedule_once(lambda dt: self._add_log(msg))

    def _add_log(self, msg):
        self.log_area.add_widget(Label(text=msg, font_size=14, size_hint_y=None, height=30))

    def start_download(self, instance):
        links = [l.strip() for l in self.links_input.text.split("\n") if l.strip()]
        if not links:
            self.log("⚠️ Insira ao menos um link!")
            return
        threading.Thread(target=self.download_videos, args=(links,), daemon=True).start()

    def download_videos(self, links):
        self.log("🚀 Iniciando downloads...")
        download_path = os.path.expanduser("~")

        for link in links:
            self.log(f"Baixando: {link}")
            try:
                ydl_opts = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    'format': 'best',
                    'quiet': True,
                    'noprogress': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                self.log(f"✅ Concluído: {link}")
            except Exception as e:
                self.log(f"❌ Erro: {str(e)}")
        self.log("🎉 Downloads finalizados!")


class VideoDownloaderApp(App):
    def build(self):
        return DownloaderUI()


if __name__ == "__main__":
    VideoDownloaderApp().run()
