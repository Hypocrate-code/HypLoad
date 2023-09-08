import os
import time

from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
import json
from kivy.resources import resource_add_path, resource_find
import threading
from pytube import YouTube, Playlist
from kivy.utils import platform
from kivy.clock import mainthread
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import webbrowser

############# setup basic settings###############
# Config.set('kivy', 'show_touches', 0)
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

print(platform)

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    from androidstorage4kivy import SharedStorage
    # from kivy.metrics import Metrics
    from kivy.setupconfig import USE_SDL2
    if USE_SDL2:
        Hardware = autoclass('org.renpy.android.Hardware')
        dpi = Hardware.getDPI()
    else:
        import android
        dpi = android.get_dpi()
    print("the screen's dpi is : ", dpi)
    width = (Window.system_size[0] * 2.54) / dpi
    print("the screen's approximate's width is : ", width)
    if width >= 6.2:
        scale_factor = 1.1
        print("width above 6.2")
    elif width >= 5 and width < 6.2:
        scale_factor = 0.93
        print("width between 5 and 6.2")
    elif width >= 4.5 and width < 5:
        scale_factor = 0.9
elif platform == "win" or platform == "linux":
    Window.fullscreen = 'auto'
    dpi = Window.dpi
    print("the screen's dpi is : ", dpi)
    width = (Window.system_size[0] * 2.54) / dpi
    print("the screen's approximate's width is : ", width)
    scale_factor = 1.35

########## end of  setup basic settings###########

def change_attr_on_lang(screen, id, attribute, frval, enval):
    with open("options.json", "r") as options:
        options_read = options.read()
        options_json = json.loads(options_read)
        if options_json["language"] == "fr":
            setattr(sm.get_screen(screen).ids[id], attribute, frval)
        else:
            setattr(sm.get_screen(screen).ids[id], attribute, enval)

class HypLoadApp(App):
    resource_add_path("fonts")
    Roboto_font = resource_find('Roboto-Regular.ttf')
    Roboto_light_font = resource_find('Roboto-Regular.ttf')
    Roboto_i_font = resource_find('Roboto-Italic.ttf')

    Roboto_bold_font = resource_find('Roboto-Bold.ttf')
    light_grey = ListProperty()
    background_of_the_app = ListProperty()
    text_input_bg = ListProperty()
    text_color = ListProperty()
    value = NumericProperty()
    bg_color_for_video_res_btn = ListProperty()
    def __init__(self, **kwargs):
        self.value = 0
        self.text_color = 1,1,1,1
        self.text_input_bg = (0.95,0.95,0.95,1)
        self.bg_color_for_video_res_btn = self.color(255, 44, 56, 190)
        # self.light_grey = self.color(248, 246, 246, 255)
        super(HypLoadApp, self).__init__(**kwargs)
    def color(self, r, g, b, a):
        return (r / 255, g / 255, b / 255, a / 255)
    def p_to_dp(self, pixels):
        calc = round(pixels * (160/440) * scale_factor, 2)
        return str(calc) + "dp"
    def translate_dp_to_p(self, str):
        return dp(str.split("dp")[0])
    def auto_width(self, element):
        return len(element.text) * (element.font_size / 1.8)
    def text_size(self, size):
        if size == "small":
            pass
        if size == "small medium":
            return self.p_to_dp(40)
        if size == "medium":
            return self.p_to_dp(45)
        if size == "medium big":
            return self.p_to_dp(50)
    def init_text(self, lang):
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

        sm.screens[4].get_and_set_color_of_the_app()
        change_attr_on_lang("music_playlist_download_screen", "MPDS_validate_link_btn", "width", app.p_to_dp(160), app.p_to_dp(180))
        change_attr_on_lang("music_single_download_screen", "container_download_screen_no_trad", "width", app.p_to_dp(790), app.p_to_dp(730))
        change_attr_on_lang("music_single_download_screen", "MSDS_validate_link_btn", "width", app.p_to_dp(240), app.p_to_dp(210))
        change_attr_on_lang("start_screen","SS_grid_for_btn_no_trad", "width", self.p_to_dp(665), self.p_to_dp(590))
        change_attr_on_lang("options_and_infos_screen", "OAIS_grid_container_no_trad", "width", app.p_to_dp(665), app.p_to_dp(620))
        self.update_only_audio_btn()
        sm.get_screen("options_and_infos_screen").init_color_btn_text()
    def build(self):
        sm.add_widget(LanguageScreen(name='language_screen'))
        sm.add_widget(StartScreen(name='start_screen'))

        return sm
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        sm.add_widget(MusicSingleDownloadScreen(name='music_single_download_screen'))
        sm.add_widget(MusicPlaylistDownloadScreen(name='music_playlist_download_screen'))
        sm.add_widget(OptionsAndInfosScreen(name="options_and_infos_screen"))
        sm.add_widget(ChooseResolutionScreen(name="choose_resolution_screen"))
        sm.add_widget(PlaylistScreen(name="playlist_screen"))
        sm.add_widget(CustomResolutionScreen(name="custom_resolution_screen"))
        sm.get_screen("options_and_infos_screen").get_and_set_color_of_the_app()
        sm.get_screen("choose_resolution_screen").set_video_res_btns()
        self.only_audio_btns = []
        for screen in sm.screens:
            if screen.ids.get("only_audio_btn_no_trad"):
                self.only_audio_btns.append(screen.ids["only_audio_btn_no_trad"])
        with open('options.json', 'r', encoding="utf-8") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            if not (options_json.get('language')):
                sm.current = 'language_screen'
            else:
                self.init_text(options_json['language'])

                sm.transition = NoTransition()
                sm.current = 'start_screen'

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            if hasattr(sm.children[0], "back_btn"):
                sm.children[0].back_btn()
                return True
            else :

                return False
        return True
    def get_audio_only_image(self):
        with open("options.json") as file:
            options_read = file.read()
            options_json = json.loads(options_read)
            if options_json["only_audio"]:
                return f"assets/audio_{options_json['color_mode']}.png"
            else:
                return f"assets/film_{options_json['color_mode']}.png"
    def get_audio_only_text_and_width(self):
        with open("options.json") as file:
            options_read = file.read()
            options_json = json.loads(options_read)
            lang = options_json.get("language", False)
            if lang == "fr":
                if options_json["only_audio"]:
                    return ("Audio uniquement", app.p_to_dp(465))
                else:
                    return ("Audio et Vidéo", app.p_to_dp(395))
            elif lang == "en" or not lang:
                if options_json["only_audio"]:
                    return ("Only audio", app.p_to_dp(310))
                else:
                    return ("Audio and Video", app.p_to_dp(425))
            else:
                print("wtf pas de langue pour only audio")
    def  update_only_audio_btn(self):
            datas = self.get_audio_only_text_and_width()
            image = self.get_audio_only_image()
            for btn in self.only_audio_btns:
                btn.children[0].children[1].text = datas[0]
                btn.children[0].width = datas[1]
                btn.children[0].children[0].source = image
    def switch_audio_only(self):
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            options_data["only_audio"] = not options_data["only_audio"]  # Toggle the value
            options_file.seek(0)  # Déplacer la position du curseur au début du fichier
            options_file.truncate()  # Effacer le contenu existant du fichier
            json.dump(options_data, options_file, indent=4)
    def open_web_page(self,url):
        webbrowser.open(url)
    def set_video_res(self, quality):
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            options_data["video_res"] = quality
            options_file.seek(0)
            options_file.truncate()
            json.dump(options_data, options_file, indent=4)

class StartScreen(Screen):
    def on_pre_enter(self, *args):
        sm.transition = SlideTransition(direction='left', duration = .3)
        #first_element = self.ids["SS_single_btn"]
        #app.auto_width(first_element)




class MusicSingleDownloadScreen(Screen):
    def on_enter(self, *args):
        self.copy_of_grid = self.ids.enter_link_grid_no_trad
        self.copy_of_audio_btn = self.ids.only_audio_btn_no_trad
    def on_leave(self, *args):
        if self.ids.get("input_of_youtube_link"):
            self.ids.input_of_youtube_link.text = ""
            with open("options.json") as options:
                options_read = options.read()
                options_json = json.loads(options_read)
                self.ids.MSDS_label.text = "Entrez le lien de votre vidéo YouTube" if options_json['language'] == 'fr' else "Enter the link of your YouTube video"
    def download(self):
        url = self.ids.input_of_youtube_link.text
        first_widget_to_remove = self.ids.enter_link_grid_no_trad
        second_widget_to_remove = self.ids.only_audio_btn_no_trad
        widget_parent = self.ids.container_download_screen_no_trad
        self.progress_bar = my_progress_bar(widget_parent)
        thread = threading.Thread(target=download_yt_music, args=[self, url, first_widget_to_remove, second_widget_to_remove, widget_parent, self.progress_bar])
        thread.start()
    @mainthread
    def on_progress(self, stream, chunk_we_dont_care, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_value = (bytes_downloaded / total_size) * 100
        print(progress_value)
        self.progress_bar.progress_value = progress_value
    @mainthread
    def on_complete(self, stream, filepath, *args):
        widget_parent = self.ids.container_download_screen_no_trad
        self.cancel_or_finish(self.copy_of_grid, self.copy_of_audio_btn, widget_parent, self.progress_bar, "finish")

    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "start_screen"

    @mainthread
    def init_progress_bar(self, first_rm, second_rm, pa, pb):
        self.ids.container_download_screen_no_trad.pos_hint = {"center_x": 0.5, 'center_y': 0.5715}
        pa.remove_widget(first_rm)
        pa.remove_widget(second_rm)
        pa.add_widget(pb)

    @mainthread
    def cancel_or_finish(self, first_rm, second_rm, pa, pb, arg):
        if arg == "finish":
            self.progress_bar.progress_value = 100
            time.sleep(.3)
            with open("options.json") as options:
                options_read = options.read()
                options_json = json.loads(options_read)
                self.ids.MSDS_label.text = f"Votre vidéo a bien été téléchargée.\nEntrez le lien d'une autre vidéo" if \
                options_json['language'] == 'fr' else f"Your video has been downloaded.\nDownload another video :"
        self.ids.container_download_screen_no_trad.pos_hint = {"center_x": 0.5, 'center_y': 0.52}
        pa.remove_widget(pb)
        pa.add_widget(first_rm)
        pa.add_widget(second_rm)
        self.ids.input_of_youtube_link.text = ""
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
def change_img_only_audio(instance, source):
    instance.type = "video" if instance.type == "audio" else "audio"
    instance.parent.children[0].source = source.replace("audio", "film") if "audio" in source else source.replace("film", "audio")
class Item_Of_List(GridLayout):
    def __init__(self, title, thumbnail, author, views, **kwargs):
        print(title)
        print(thumbnail)
        print(views)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            if options_json['language'] == "fr":
                prep = "par "
                word = "vues"
            else:
                prep = "by "
                word = "views"
            btn_img = f"assets/audio_{options_json['color_mode']}.png" if options_json["only_audio"] else f"assets/film_{options_json['color_mode']}.png"
            checked_box = f"assets/checked_box_{options_json['color_mode']}.png"
            not_checked_box = f"assets/not_checked_box_{options_json['color_mode']}.png"
        super(Item_Of_List, self).__init__(**kwargs)
        with self.canvas:
            Color(*app.light_grey)
            self.rect = RoundedRectangle(pos=self.pos, size=(self.size[0], self.size[1] - app.translate_dp_to_p(app.p_to_dp(7.5))), radius=[app.translate_dp_to_p(app.p_to_dp(25))])
        self.type = "audio" if options_json["only_audio"] else "video"
        self.update = True
        self.orientation = "lr-tb"
        self.rows = 1
        self.cols = 3
        self.size_hint: (1, None)
        self.height = app.p_to_dp(215)
        self.padding = [app.p_to_dp(24),app.p_to_dp(27),app.p_to_dp(24),app.p_to_dp(27)]
        self.spacing = [app.p_to_dp(20),app.p_to_dp(0)]
        self.thumbnail_img = AsyncImage(source = thumbnail, size_hint= (None, None))
        self.thumbnail_img.height = self.height - (self.padding[1] * 2)
        self.thumbnail_img.width = self.thumbnail_img.height / 0.75
        self.container_of_data = GridLayout(orientation="tb-lr", cols=1, size_hint= (None, None),width = app.p_to_dp(500),  height= app.p_to_dp(170), padding = [0, app.p_to_dp(12)])


        #### TITLE OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.label = Label(text =f"{title.capitalize()}")
        self.label.height=app.p_to_dp(50)
        self.max_lines = 1
        self.label.valign="top"
        self.label.halign = "left"
        self.label.size_hint=(None, None)
        self.label.width=self.container_of_data.width
        self.label.font_name = app.Roboto_font
        self.label.color=app.text_color
        self.label.font_size = app.text_size("small medium")
        self.label.shorten = True
        self.label.split_str = "..."
        self.label.shorten_from = "right"



        ####  AUTHOR OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.author = Label(text =f"{prep}{author}")
        self.author.height=app.p_to_dp(46)
        self.author.valign="top"
        self.author.halign = "left"
        self.author.size_hint=(None, None)
        self.author.width=self.container_of_data.width - app.translate_dp_to_p(app.p_to_dp(60))
        self.author.font_name = app.Roboto_i_font
        self.author.color=app.text_color
        self.author.font_size = app.p_to_dp(30)


        ####  VIEWS OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.views_counter = Label(text =f"{change_number_in_appropriate_form(views)} {word}")
        self.views_counter.height=app.p_to_dp(50)
        self.views_counter.valign="bottom"
        self.views_counter.halign = "left"
        self.views_counter.size_hint=(None, None)
        self.views_counter.width=self.container_of_data.width
        self.views_counter.font_name = app.Roboto_light_font
        self.views_counter.color=app.text_color
        self.views_counter.font_size = app.p_to_dp(30)

        self.container_of_data.add_widget(self.label)
        self.label.text_size = self.label.size

        self.container_of_data.add_widget(self.author)
        self.author.text_size = self.author.size

        self.container_of_data.add_widget(self.views_counter)
        self.views_counter.text_size = self.views_counter.size

        #### LIL BUTTONS FOR PARAMETERS OF DOWNLOADS ####
        self.btns = FloatLayout(size_hint=(None, 1))
        self.btns.width = app.p_to_dp(50)

        self.first_btn = AnchorLayout()
        self.first_btn.size_hint = (1, None)
        self.first_btn.height = self.btns.width
        self.first_btn.pos_hint = {"center_x": 0.5, "center_y": 0.7}
        # self.first_btn.text = "1"
        # self.first_btn.font_size = app.p_to_dp(15)
        self.first_btn.img = Image(source = btn_img)
        self.first_btn.btn = Button()
        self.first_btn.btn.background_active = ""
        self.first_btn.btn.background_normal = ""
        self.first_btn.btn.background_down = ""
        self.first_btn.btn.background_color = 0,0,0,0
        self.first_btn.btn.bind(on_press=lambda x: change_img_only_audio(x, self.first_btn.img.source))
        self.first_btn.add_widget(self.first_btn.btn)
        self.first_btn.add_widget(self.first_btn.img)

        self.second_btn = AnchorLayout()
        self.second_btn.size_hint = (1, None)
        self.second_btn.height = self.btns.width
        self.second_btn.pos_hint = {"center_x": 0.5, "center_y": 0.2}
        self.second_btn.img = Image(source = not_checked_box if check_if_file_is_downloaded(title+".mp4", self.type) else checked_box)
        self.second_btn.btn = Button()
        self.second_btn.btn.background_active = ""
        self.second_btn.btn.background_normal = ""
        self.second_btn.btn.background_down = ""
        self.second_btn.btn.background_color = 0, 0, 0, 0
        self.second_btn.add_widget(self.second_btn.btn)
        self.second_btn.add_widget(self.second_btn.img)

        self.btns.add_widget(self.first_btn)
        self.btns.add_widget(self.second_btn)

        self.add_widget(self.container_of_data)
        self.add_widget(self.thumbnail_img)
        self.add_widget(self.btns)

    def on_size(self, *args):
        self.rect.size = self.size
        self.update = not self.update
        if self.update:
            self.author.text_size = self.author.size

    def on_pos(self, *args):
        self.rect.pos = (self.pos[0], self.pos[1] - app.translate_dp_to_p(app.p_to_dp(7.5)))


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

    @mainthread
    def to_playlist_screen(self):
        sm.current = "playlist_screen"
    @mainthread
    def add_title(self, title):
        label = Label(text = title)
        label.halign= "left"
        label.font_name = app.Roboto_bold_font
        label.color=app.text_color
        label.size_hint= (None, 1)
        label.width=app.p_to_dp(700)
        label.valign="center"
        label.font_size = app.p_to_dp(45)
        label.padding = [app.p_to_dp(18),app.p_to_dp(10)]
        label.text_size = label.size
        label.shorten = True
        label.split_str = "..."
        label.shorten_from = "right"
        sm.get_screen('playlist_screen').ids.title_container_no_trad.add_widget(label)
    @mainthread
    def add_a_video(self, video_stream):
        parent = sm.get_screen('playlist_screen').ids.playlist_loaded_no_trad
        print(video_stream.views)
        widget = Item_Of_List(video_stream.title, f"https://img.youtube.com/vi/{video_stream.video_id}/0.jpg", video_stream.author, video_stream.views)
        parent.add_widget(widget)
        widget.width = parent.width
    @mainthread
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
            options_file.seek(0)
            options_file.truncate()
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

class my_progress_bar(Widget):
    progress_value = NumericProperty(0)
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.par = parent
        self.height = app.p_to_dp(35)
        with self.canvas:
            Color(*app.light_grey)
            self.background_rect = RoundedRectangle(pos=(parent.pos[0], parent.pos[1] + app.translate_dp_to_p(app.p_to_dp(155))), size=(parent.width, self.height), radius=[self.height/2])
            Color(*app.bg_color_for_video_res_btn)
            self.progress_rect = RoundedRectangle(pos=(parent.pos[0] + app.translate_dp_to_p(app.p_to_dp(7.5)), parent.pos[1] + app.translate_dp_to_p(app.p_to_dp(162))), size=(((parent.size[0] - app.translate_dp_to_p( app.p_to_dp(10)))/100) * self.progress_value, app.translate_dp_to_p(app.p_to_dp(20))), radius=[ app.translate_dp_to_p(app.p_to_dp(10))])
        self.bind(progress_value=self.update_progress)
    def update_progress(self, instance, value):
        self.progress_rect.size = (((self.par.size[0] - app.translate_dp_to_p( app.p_to_dp(15)))/100) * value, app.translate_dp_to_p(app.p_to_dp(20)))
class OptionsAndInfosScreen(Screen):
    def on_pre_start(self, *args):
        sm.transition.direction = "left"
    def init_color_btn_text(self):
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            clr_mod = options_json["color_mode"]
            values = {"fr": {"dark": "Mode sombre", "light": "Mode clair"},
                      "en": {"dark": "Dark mode", "light": "Light mode"}}
            lang = options_json["language"]
            value = values[lang][clr_mod]
            self.ids.color_mode_no_trad.text = value
    def get_and_set_color_of_the_app(self):
        with open("options.json") as options:
            options_read = options.read()
            print("wtf",options_read)
            options_json = json.loads(options_read)
            clr_mod = options_json["color_mode"]
            if clr_mod == "dark":
                #EVERYTHING RELATED TO DARK MODE


                app.text_input_bg = app.color(66,66,66,255)
                app.background_of_the_app = app.color(33,33,33,255)
                app.text_color = app.color(255, 255, 255,225)
                app.light_grey = app.color(48,48,48,255)
                app.bg_color_for_video_res_btn = app.color(255, 44, 56, 190)
            else:
                #EVERYTHING RELATED TO LIGHT MODE


                app.text_input_bg = (0.95,0.95,0.95,1)
                app.background_of_the_app = app.color(250, 250, 250, 255)
                app.text_color = app.color(72,75,106, 255)
                app.light_grey = app.color(242,240,240,255)
                app.bg_color_for_video_res_btn = app.color(171, 135, 255, 35)

            Window.clearcolor = tuple(app.background_of_the_app)
            return True
    def change_color_mode(self):
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            value = options_data["color_mode"]
            if value == "dark":
                options_data["color_mode"] ="light"
            else:
                options_data["color_mode"] = "dark"
            options_file.seek(0)
            options_file.truncate()
            json.dump(options_data, options_file, indent=4)

        self.get_and_set_color_of_the_app()
        sm.get_screen("options_and_infos_screen").init_color_btn_text()
        sm.get_screen("choose_resolution_screen").set_video_res_btns()
        app.update_only_audio_btn()

    def back_btn(self):
        sm.transition.direction ="right"
        sm.current="start_screen"

class PlaylistScreen(Screen):
    def on_leave(self, *args):
        self.ids.playlist_loaded_no_trad.children = []
    def back_btn(self):
        sm.transition.direction ="right"
        sm.current="music_playlist_download_screen"

class ChooseResolutionScreen(Screen):
    def on_pre_start(self, *args):
        sm.transition.direction = "left"
    def back_btn(self):
        sm.transition.direction ="right"
        sm.current="options_and_infos_screen"
    def set_video_res_btns(self):
        with open("options.json") as file:
            options_read = file.read()
            options_json = json.loads(options_read)
            res = options_json["video_res"]
            if res == "highest":
                self.ids.CRS_highest_res.bg_color = app.bg_color_for_video_res_btn
                self.ids.CRS_lowest_res.bg_color = app.light_grey
                self.ids.CRS_custom.bg_color = app.light_grey
                for btn in sm.get_screen("custom_resolution_screen").children[0].children[1].children:
                    btn.bg_color = app.light_grey
            elif res == "lowest":
                self.ids.CRS_highest_res.bg_color = app.light_grey
                self.ids.CRS_lowest_res.bg_color = app.bg_color_for_video_res_btn
                self.ids.CRS_custom.bg_color = app.light_grey
                for btn in sm.get_screen("custom_resolution_screen").children[0].children[1].children:
                    btn.bg_color = app.light_grey
            else:
                self.ids.CRS_highest_res.bg_color = app.light_grey
                self.ids.CRS_lowest_res.bg_color = app.light_grey
                self.ids.CRS_custom.bg_color = app.bg_color_for_video_res_btn
                for btn in sm.get_screen("custom_resolution_screen").children[0].children[1].children:
                    if res in btn.text:
                        btn.bg_color =  app.bg_color_for_video_res_btn
                    else:
                        btn.bg_color = app.light_grey





class CustomResolutionScreen(Screen):
    def back_btn(self):
        sm.transition.direction ="right"
        sm.current="choose_resolution_screen"

######FUNCTIONS FOR ALL PYTUBE AND DOWNLOAD THINGS ##########
def check_dl_preferencies_single():
    with open("options.json") as file:
        options_read = file.read()
        options_json = json.loads(options_read)
        if options_json["only_audio"]:
            return [True]
        else:
            return [False, options_json["video_res"]]
def download_yt_music(self, url, first_to_rm, second_to_rm, parent, pb):
    try:
        yt = YouTube(url)
        if yt.title + ".mp4" in os.listdir(os.getcwd()):
            raise FileExistsError
        try:
            self.init_progress_bar(first_to_rm, second_to_rm, parent, pb)
            with open("options.json") as options:
                options_read = options.read()
                options_json = json.loads(options_read)
                self.ids.MSDS_label.text = f"Télécharge : {yt.title[:18]}..." if options_json['language'] == 'fr' else f"Downloading : {yt.title[:18]}..."
            yt.register_on_progress_callback(self.on_progress)
            yt.register_on_complete_callback(self.on_complete)
            options = check_dl_preferencies_single()
            options = check_dl_preferencies_single()
            print(options)
            if options[0]:
                good_one = yt.streams.get_audio_only()
            else:
                if options[1] == "highest":
                    good_one = yt.streams.get_highest_resolution()
                elif options[1] == "lowest":
                    good_one = yt.streams.get_lowest_resolution()
                elif options[1] == "144p":
                    good_one = yt.streams.get_by_itag(160)
                elif options[1] == "240p":
                    good_one = yt.streams.get_by_itag(133)
                elif options[1] == "360p":
                    good_one = yt.streams.get_by_itag(18)
                elif options[1] == "480p":
                    good_one = yt.streams.get_by_itag(135)
                elif options[1] == "720p":
                    good_one = yt.streams.get_by_itag(22)
                elif options[1] == "1080p":
                    good_one = yt.streams.get_by_itag(37)

            good_one.download(output_path=os.getcwd())

            if platform == "android":
                if options[0]:
                    convert_file_location(good_one.default_filename, "music")
                else:
                    convert_file_location(good_one.default_filename, "video")
        except Exception as e:
            self.cancel_or_finish(first_to_rm,second_to_rm, parent, pb, "cancel")
            print("exception", e)
    except FileExistsError:
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "La vidéo a déjà été téléchargée." if options_json['language'] == 'fr' else "This video has already been downloaded."
    except Exception as e:
        print('marche pas', e)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "Votre lien est incorrect, vérifiez et réessayer." if options_json['language'] == 'fr' else "Your link is incorrect, verify and retry."


def download_yt_playlist(self, url, type):
    try:
        playlist = Playlist(url)
        self.add_title(playlist.title)
        for video in playlist.videos:
            self.add_a_video(video)
        self.to_playlist_screen()
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
        print(place_of_file)
        SS.copy_to_shared(os.path.join(os.getcwd(), video), collection=place_of_file)
    except Exception as e:
        print("oh !", e)

######END OF FUNCTIONS FOR ALL PYTUBE AND DOWNLOAD THINGS ##########

######START OF FUNCTIONS WITH LIL UTILITIES ##########
def check_if_file_is_downloaded(source, type):
    print(source)
    if platform == "android":
        Environment = autoclass('android.os.Environment')
        if type == "music":
            place_of_file = Environment.DIRECTORY_MUSIC
        elif type == "video":
            place_of_file = Environment.DIRECTORY_MOVIES
        return source in os.listdir(place_of_file)
    elif platform == "win" or platform == "linux":
        print('win')
        print(os.getcwd())
        print(source in os.getcwd())
        return source in os.listdir(os.getcwd())

def change_number_in_appropriate_form(num):
    number = str(num)
    division_factor = (len(number)-1)//3
    for i in range(division_factor):
        number = number[:((i+1)*3+i)*(-1)] + ' ' + number[((i+1)*3 + i)*(-1):]
    return number
# def cut_text_or_not(text, lenght):
#     print("ghfdohg", text[:lenght])
#     return f"{text[:lenght]}..." if len(text[:lenght]) < len(text) else text

######END OF FUNCTIONS WITH LIL UTILITIES ##########

if __name__ == '__main__':
    app = HypLoadApp()
    app.run()