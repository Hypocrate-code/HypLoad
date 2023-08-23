import os
# import time
# from kivy.lang import Builder
# from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
import json
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path, resource_find
import threading
from pytube import YouTube, Playlist
from kivy.utils import platform
from kivy.clock import mainthread
import webbrowser

############# setup basic settings################

Window.clearcolor = (1, 1, 1, 1)
# Config.set('kivy', 'show_touches', 0)
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

caca = False

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage
    if Window.width <= 700:
        caca = True


def change_attr_on_lang(screen, id, attribute, frval, enval):
    with open("options.json", "r") as options:
        options_read = options.read()
        options_json = json.loads(options_read)
        if options_json["language"] == "fr":
            setattr(sm.get_screen(screen).ids[id], attribute, frval)
        else:
            setattr(sm.get_screen(screen).ids[id], attribute, enval)
        
    
########## end of  setup basic settings###########

class HypLoadApp(App):
    resource_add_path("fonts")
    Roboto_font = resource_find('Roboto-Medium.ttf')
    Roboto_bold_font = resource_find('Roboto-Black.ttf')

    def color(self, r, g, b, a):
        return (r / 255, g / 255, b / 255, a / 255)
    def auto_width(self, element):
        return len(element.text) * (element.font_size / 1.8)
    def text_size(self, size):
        if size == "small":
            pass
        if size == "small medium":
            return str(Window.width * 0.014) + "dp"
        if size == "medium":
            return str(Window.width * 0.017) + "dp"
        if size == "medium big":
            return str(Window.width * 0.02
            ) + "dp"
   
    def init_text(self, lang):
        print(self.text_size('medium'))
        with open('data.json', 'r', encoding="utf-8") as data:
            data_read = data.read()
            data_json = json.loads(data_read)
            for screen in sm.screens:
                for id in screen.ids:
                    if not ('no_trad') in id:
                        if "input" in id:
                            screen.ids[id].hint_text = data_json[lang][id]
                        else:
                            screen.ids[id].text = data_json[lang][id]
        change_attr_on_lang("music_playlist_download_screen", "MPDS_validate_link_btn", "width", 160, 180)
        change_attr_on_lang("music_single_download_screen", "container_download_screen_no_trad", "width", 850, 770)
        change_attr_on_lang("music_single_download_screen", "MSDS_validate_link_btn", "width", 240, 210)
        change_attr_on_lang("start_screen","SS_grid_for_btn_no_trad", "width", 740, 650)
        change_attr_on_lang("options_and_infos_screen", "OAIS_grid_container_no_trad", "width", 740, 650)
        
        
        
    def build(self):
        sm.add_widget(LanguageScreen(name='language_screen'))
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(MusicSingleDownloadScreen(name='music_single_download_screen'))
        sm.add_widget(MusicPlaylistDownloadScreen(name='music_playlist_download_screen'))
        sm.add_widget(OptionsAndInfosScreen(name="options_and_infos_screen"))
        

        with open('options.json', 'r', encoding="utf-8") as options:

            options_read = options.read()
            options_json = json.loads(options_read)
            if not (options_json.get('language')):
                sm.current = 'language_screen'
            else:
                self.init_text(options_json['language'])
                
                sm.transition = NoTransition()
                sm.current = 'start_screen'
        return sm
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if hasattr(sm.children[0], "back_btn"):
                print(sm.children[0])
                sm.children[0].back_btn()
                return True
            else :

                return False
        return True 
    
    def test(self):
        webbrowser.open("https://google.com")


class StartScreen(Screen):
    def on_pre_enter(self, *args):
        sm.transition = SlideTransition(direction='left', duration = .3)
        #first_element = self.ids["SS_single_btn"]
        #app.auto_width(first_element)
     
        



class MusicSingleDownloadScreen(Screen):
    def on_enter(self, *args):
        self.copy_of_grid = self.ids.enter_link_grid_no_trad
        
    def download(self):
        url = self.ids.input_of_youtube_link.text
        widget_to_remove = self.ids.enter_link_grid_no_trad
        widget_parent = self.ids.container_download_screen_no_trad
        self.progress_bar = ProgressBar()
        thread = threading.Thread(target=download_yt_music, args=[self, url, widget_to_remove, widget_parent, self.progress_bar])
        thread.start()

    def on_progress(self, stream, chunk_we_dont_care, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_value = (bytes_downloaded / total_size) * 100
        self.children[0].children[0].children[0].value = progress_value
    def on_complete(self, stream, filepath, *args):
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = f"Votre vidéo a été téléchargée." if options_json['language'] == 'fr' else f"Your video has been downloaded.\nDownload another video :"
        print(self, stream, filepath)
        print("ah", *args)
        
        widget_parent = self.ids.container_download_screen_no_trad
        self.cancel_or_finish(self.copy_of_grid, widget_parent, self.progress_bar)
       
    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "start_screen"

    @mainthread
    def init_progress_bar(self, rm, pa, pb):
        pa.remove_widget(rm)
        pa.add_widget(pb)
    def cancel_or_finish(self, rm, pa, pb):
        pa.remove_widget(pb)
        pa.add_widget(rm)
        self.ids.input_of_youtube_link.text = ""

class MusicPlaylistDownloadScreen(Screen):
    def download(self):
        url = self.ids.input_of_youtube_playlist_link.text
        # widget_to_remove = self.ids.enter_link_grid_no_trad
        # widget_parent = self.ids.container_download_screen_no_trad
        # widget_parent.remove_widget(widget_to_remove)
        # progress_bar = ProgressBar()
        # widget_parent.add_widget(progress_bar)
        thread = threading.Thread(target=download_yt_playlist, args=[self, url, "music"])
        thread.start()
    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "start_screen"

class MainScreenManager(ScreenManager):
    pass


sm = ScreenManager()


class LanguageScreen(Screen):
    def setLanguage(self, lang):
        already = False
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            if options_data.get('language') :
                already = True
            options_data['language'] = lang
            options_file.seek(0)  # Déplacer la position du curseur au début du fichier
            json.dump(options_data, options_file, indent=4)
        app.init_text(lang)
        if already:
            sm.transition.direction = "right"
            sm.current = "options_and_infos_screen"
        else:
            sm.current = "start_screen"
        
    def back_btn(self):
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            if options_json.get('language'):
       
                sm.transition.direction = "right"
                sm.current = "options_and_infos_screen"
            else:
                app.stop()
            

class OptionsAndInfosScreen(Screen):
    def on_start(self, *args):
        sm.transition.direction = "left"
        
    def back_btn(self):
        sm.transition.direction ="right"
        sm.current="start_screen"
 
######FUNCTIONS FOR ALL PYTUBE AND DOWNLOAD THINGS ##########

def download_yt_music(self, url, to_rm, parent, pb):
    try:
        yt = YouTube(url)
        try:
            self.init_progress_bar(to_rm, parent, pb)
            yt.register_on_progress_callback(self.on_progress)
            yt.register_on_complete_callback(self.on_complete)
            good_one = yt.streams.get_by_itag(140)
        # good_one = yt.streams.get_highest_resolution()
        # with open("options.json") as options:
        #     options_read = options.read()
        #     options_json = json.loads(options_read)
        #     path = options_json['path_to_music_folder']
            good_one.download(output_path=os.getcwd())
            print(good_one.default_filename, yt.title)
            if platform == "android":
                convert_file_location(good_one.default_filename, "music")   
        except Exception as e:
            self.cancel_or_finish(to_rm, parent, pb)
            print(e)
            
    except Exception as e:
        print('marche pas', e)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "Votre lien est incorrect, vérifiez et réessayer." if options_json['language'] == 'fr' else "Your link is incorrect, verify and retry."
            
def download_yt_playlist(self, url, type):
    try:
        playlist = Playlist(url)
        for video_stream in playlist.videos:
            if type == "music":
                video = video_stream.streams.get_audio_only()
            elif type == "video":
                video = video_stream.streams.get_highest_resolution()
            video.download()
            if platform == "android":
                convert_file_location(video.default_filename, type)
    except Exception as e:
        print(e)

def convert_file_location(video, type):
    try:
        Environment = autoclass('android.os.Environment')
        if type == "music":
            place_of_file = Environment.DIRECTORY_MUSIC
        elif type == "video":
            place_of_file = Environment.DIRECTORY_MOVIES
        SS = SharedStorage()
        SS.copy_to_shared(os.path.join(os.getcwd(), video), collection=place_of_file)
    except Exception as e:
        print("oh !", e)

######END OF FUNCTIONS FOR ALL PYTUBE AND DOWNLOAD THINGS ##########

if __name__ == '__main__':
    app = HypLoadApp()
    app.run()