import subprocess
import os
import time
from urllib.error import URLError, HTTPError
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
Config.set('kivy', 'show_touches', 0)
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

print(platform)
print(os.listdir(os.getcwd()))

if platform == "android":
    from jnius import autoclass, cast
    from jnius import *
    ffmpeg_for_android = autoclass('com.sahib.pyff.ffpy')
    from android.permissions import request_permissions, Permission
    from android.runnable import run_on_ui_thread
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
    Window.size = (Window.height * 2 / 3, Window.height)
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
        to_be_sure()
        self.value = 0
        self.text_color = 1, 1, 1, 1
        self.text_input_bg = (0.95, 0.95, 0.95, 1)
        self.bg_color_for_video_res_btn = self.color(255, 44, 56, 190)
        # self.light_grey = self.color(248, 246, 246, 255)
        super(HypLoadApp, self).__init__(**kwargs)

    def color(self, r, g, b, a):
        return (r / 255, g / 255, b / 255, a / 255)
    def p_to_dp(self, pixels):
        calc = round(pixels * (160 / 440) * scale_factor, 2)
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
        change_attr_on_lang("music_playlist_download_screen", "MPDS_validate_link_btn", "width", app.p_to_dp(160),
                            app.p_to_dp(180))
        change_attr_on_lang("music_single_download_screen", "container_download_screen_no_trad", "width",
                            app.p_to_dp(790), app.p_to_dp(730))
        change_attr_on_lang("music_single_download_screen", "MSDS_validate_link_btn", "width", app.p_to_dp(240),
                            app.p_to_dp(210))
        change_attr_on_lang("start_screen", "SS_grid_for_btn_no_trad", "width", self.p_to_dp(665), self.p_to_dp(590))
        change_attr_on_lang("options_and_infos_screen", "OAIS_grid_container_no_trad", "width", app.p_to_dp(665),
                            app.p_to_dp(620))
        self.update_only_audio_btn()
        sm.get_screen("options_and_infos_screen").init_color_btn_text()

    def build(self):
        sm.add_widget(LanguageScreen(name='language_screen'))
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(MusicSingleDownloadScreen(name='music_single_download_screen'))
        sm.add_widget(MusicPlaylistDownloadScreen(name='music_playlist_download_screen'))
        sm.add_widget(OptionsAndInfosScreen(name="options_and_infos_screen"))
        sm.add_widget(ChooseResolutionScreen(name="choose_resolution_screen"))
        sm.add_widget(PlaylistScreen(name="playlist_screen"))
        sm.add_widget(CustomResolutionScreen(name="custom_resolution_screen"))
        sm.add_widget(SavedLinksScreen(name="saved_links_screen"))
        self.icon = "assets/hypload_icon.png"
        self.wait = False
        return sm

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
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

    def hook_keyboard(self, window, key, *args):
        if key == 27:
            if hasattr(sm.children[0], "back_btn"):
                sm.children[0].back_btn()
                return True
            else:
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

    def update_only_audio_btn(self):
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

    def open_web_page(self, url):
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
        sm.transition = SlideTransition(direction='left', duration=.3)
        # first_element = self.ids["SS_single_btn"]
        # app.auto_width(first_element)


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
                self.ids.MSDS_label.text = "Entrez le lien de votre vidéo YouTube" if options_json[
                                                                                          'language'] == 'fr' else "Enter the link of your YouTube video"

    def download(self):
        url = self.ids.input_of_youtube_link.text
        first_widget_to_remove = self.ids.enter_link_grid_no_trad
        second_widget_to_remove = self.ids.only_audio_btn_no_trad
        widget_parent = self.ids.container_download_screen_no_trad
        self.progress_bar = my_progress_bar(widget_parent)
        thread = threading.Thread(target=download_yt_music,
                                  args=[self, url, first_widget_to_remove, second_widget_to_remove, widget_parent,
                                        self.progress_bar])
        thread.start()

    @mainthread
    def on_progress(self, stream, chunk_we_dont_care, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_value = (bytes_downloaded / total_size) * 100
        print(progress_value)
        self.progress_bar.update_progress(None, progress_value)

    @mainthread
    def on_complete(self, stream, filepath, *args):
        widget_parent = self.ids.container_download_screen_no_trad
        if len(args) > 0:
            self.cancel_or_finish(self.copy_of_grid, self.copy_of_audio_btn, widget_parent, self.progress_bar, "no_stream")
        else:
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
        if first_rm.parent or second_rm.parent:
            return
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
        if arg == "finish":
            self.progress_bar.update_progress(None, 100)
            self.ids.MSDS_label.text = f"Votre vidéo a bien été téléchargée.\nEntrez le lien d'une autre vidéo" if \
                    options_json['language'] == 'fr' else f"Your video has been downloaded.\nDownload another video :"
        if arg == "no_stream":
            self.ids.MSDS_label.text = "La résolution demandée n'est pas disponible,\nveuillez changer vos paramètres." if options_json["language"] == "fr" else "The video's resolution asked isn't available,\nplease change your parameters for this download."
        self.ids.container_download_screen_no_trad.pos_hint = {"center_x": 0.5, 'center_y': 0.52}
        pa.remove_widget(pb)
        pa.add_widget(first_rm)
        pa.add_widget(second_rm)
        self.ids.input_of_youtube_link.text = ""


from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage


def change_img_only_audio(instance, source):
    self = instance.parent.parent.parent
    self.type = "video" if self.type == "audio" else "audio"
    instance.parent.children[0].source = source.replace("audio", "film") if "audio" in source else source.replace(
        "film", "audio")
    instance.parent.parent.children[0].children[0].source = self.not_checked_box if check_if_file_is_downloaded(
        make_a_filename(self.title), self.type) else self.checked_box


def change_check_box_img(instance):
    instance.second_btn.img.source = instance.checked_box if instance.second_btn.img.source == instance.not_checked_box else instance.not_checked_box


class Item_Of_List(GridLayout):
    def __init__(self, title, thumbnail, author, views, **kwargs):
        self.title = title
        print(title)
        print(thumbnail)
        print(views)
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
            btn_img = f"assets/audio_{options_json['color_mode']}.png" if options_json[
                "only_audio"] else f"assets/film_{options_json['color_mode']}.png"
            self.checked_box = f"assets/checked_box_{options_json['color_mode']}.png"
            self.not_checked_box = f"assets/not_checked_box_{options_json['color_mode']}.png"
        super(Item_Of_List, self).__init__(**kwargs)
        with self.canvas:
            Color(*app.light_grey)
            self.rect = RoundedRectangle(pos=self.pos,
                                         size=(self.size[0], self.size[1] - app.translate_dp_to_p(app.p_to_dp(7.5))),
                                         radius=[app.translate_dp_to_p(app.p_to_dp(25))])
        self.type = "audio" if options_json["only_audio"] else "video"
        self.update = True
        self.orientation = "lr-tb"
        self.rows = 1
        self.cols = 3
        self.size_hint: (1, None)
        self.height = app.p_to_dp(215)
        self.padding = [app.p_to_dp(24), app.p_to_dp(27), app.p_to_dp(24), app.p_to_dp(27)]
        self.spacing = [app.p_to_dp(20), app.p_to_dp(0)]
        self.thumbnail_img = AsyncImage(source=thumbnail, size_hint=(None, None))
        self.thumbnail_img.height = self.height - (self.padding[1] * 2)
        self.thumbnail_img.width = self.thumbnail_img.height / 0.75
        self.container_of_data = GridLayout(orientation="tb-lr", cols=1, size_hint=(None, None), width=app.p_to_dp(500),
                                            height=app.p_to_dp(170), padding=[0, app.p_to_dp(12)])

        #### TITLE OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.label = Label(text=f"{title}")
        self.label.height = app.p_to_dp(50)
        self.max_lines = 1
        self.label.valign = "top"
        self.label.halign = "left"
        self.label.size_hint = (None, None)
        self.label.width = self.container_of_data.width
        self.label.font_name = app.Roboto_font
        self.label.color = app.text_color
        self.label.font_size = app.text_size("small medium")
        self.label.shorten = True
        self.label.split_str = "..."
        self.label.shorten_from = "right"

        ####  AUTHOR OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.author = Label(text=f"{prep}{author}")
        self.author.height = app.p_to_dp(46)
        self.author.valign = "top"
        self.author.halign = "left"
        self.author.size_hint = (None, None)
        self.author.width = self.container_of_data.width - app.translate_dp_to_p(app.p_to_dp(60))
        self.author.font_name = app.Roboto_i_font
        self.author.color = app.text_color
        self.author.font_size = app.p_to_dp(30)

        ####  VIEWS OF THE VIDEO, WIDGET IN PLAYLIST  ####
        self.views_counter = Label(text=f"{change_number_in_appropriate_form(views)} {word}")
        self.views_counter.height = app.p_to_dp(50)
        self.views_counter.valign = "bottom"
        self.views_counter.halign = "left"
        self.views_counter.size_hint = (None, None)
        self.views_counter.width = self.container_of_data.width
        self.views_counter.font_name = app.Roboto_light_font
        self.views_counter.color = app.text_color
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
        self.first_btn.img = Image(source=btn_img)
        self.first_btn.btn = Button()
        self.first_btn.btn.background_active = ""
        self.first_btn.btn.background_normal = ""
        self.first_btn.btn.background_down = ""
        self.first_btn.btn.background_color = 0, 0, 0, 0
        self.first_btn.btn.bind(on_press=lambda x: change_img_only_audio(x, self.first_btn.img.source))
        self.first_btn.add_widget(self.first_btn.btn)
        self.first_btn.add_widget(self.first_btn.img)

        self.second_btn = AnchorLayout()
        self.second_btn.size_hint = (1, None)
        self.second_btn.height = self.btns.width * 0.88
        self.second_btn.pos_hint = {"center_x": 0.48, "center_y": 0.25}
        self.second_btn.img = Image(source=self.not_checked_box if check_if_file_is_downloaded(make_a_filename(title),
                                                                                               self.type) else self.checked_box)
        self.second_btn.btn = Button()
        self.second_btn.btn.background_active = ""
        self.second_btn.btn.background_normal = ""
        self.second_btn.btn.background_down = ""
        self.second_btn.btn.background_color = 0, 0, 0, 0
        self.second_btn.btn.bind(on_press=lambda y: change_check_box_img(self))
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
    def on_enter(self, *args):
        sm.transition.direction = "left"

    def on_pre_enter(self, *args):
        if getattr(self, "is_loading", None):
            parent = sm.get_screen("music_playlist_download_screen").children[0]
            parent.remove_widget(self.loading)
            parent.remove_widget(self.pb)
            parent.add_widget(self.container)

    def on_leave(self, *args):
        if getattr(self, "is_loading", None):
            parent = sm.get_screen("music_playlist_download_screen").children[0]
            parent.remove_widget(self.loading)
            print("koa")
            parent.remove_widget(self.pb)
            parent.add_widget(self.container)
        else:
            with open('options.json', 'r', encoding="utf-8") as options:
                options_read = options.read()
                options_json = json.loads(options_read)
            self.ids.container_playlist_download_screen_no_trad.children[2].text = "Entrez le lien de votre playlist YouTube" if options_json[
                                                                                           "language"] == "fr" else "Enter the link of your YouTube playlist"
            sm.get_screen("music_playlist_download_screen").children[0].children[0].children[1].children[1].text = ""

    def load(self):
        url = self.ids.input_of_youtube_playlist_link.text
        self.container = self.ids.container_playlist_download_screen_no_trad
        with open('options.json', 'r', encoding="utf-8") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
        self.loading = Label()
        self.loading.text = "Loading your playlist..." if options_json[
                                                              "language"] == "en" else "Chargement de votre playlist..."
        self.is_loading = True
        self.loading.font_size = app.text_size("small medium")
        self.loading.font_name = app.Roboto_font
        self.loading.color = app.text_color
        self.loading.pos_hint = {"center_y": 0.585}
        self.loading.size_hint_y = None
        self.loading.height = app.p_to_dp(100)
        parent = sm.get_screen("music_playlist_download_screen").children[0]
        parent.remove_widget(self.container)
        self.pb = my_progress_bar(self.ids.container_playlist_download_screen_no_trad)
        thread = threading.Thread(target=init_yt_playlist,
                                  args=[self, url, parent, self.container, self.pb, self.loading])
        thread.start()

    @mainthread
    def init_interface(self, pa, pb, loading):
        pa.add_widget(pb)
        pa.add_widget(loading)

    @mainthread
    def cancel_or_finish(self, pa, container, pb, loading, type, title):
        self.is_loading = False
        print(pa.children)
        pa.remove_widget(pb)
        pa.remove_widget(loading)
        print(pa.children)
        with open('options.json', 'r', encoding="utf-8") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            if type == "error":
                container.children[2].text = "Une erreur est survenue, votre lien est invalide." if options_json["language"] == "fr" else "An error occured, your link is invalid."
                with open('links.json', 'r+') as links:
                    links_read = json.load(links)
                for i, el in enumerate(links_read['links']):
                    print(i, el)
                    if el[1] == container.children[1].children[1].text:
                        links_read['links'].pop(i)
                        text = "Playlist deleted" if options_json['language'] == "en" else "Playlist supprimée"
                        send_toast_notification(text)
            elif type == "finish":
                with open('links.json', 'r+') as links:
                    links_read = json.load(links)
                    is_in = False
                    for element in links_read["links"]:
                        if container.children[1].children[1].text == element[1]:
                            is_in = True
                    if not is_in:
                        links_read["links"].append((title, container.children[1].children[1].text))
                        if platform == "android":
                            try:
                                text = "Playlist sauvegardée !" if options_json["language"] == "fr" else "Playlist saved !"
                                send_toast_notification(text)
                            except Exception as e:
                                print("marche passss")
                    links.seek(0)
                    links.truncate()
                    json.dump(links_read, links, indent=4)
                container.children[2].text = "Entrez le lien de votre playlist YouTube" if options_json[
                                                                                               "language"] == "fr" else "Enter the link of your YouTube playlist"
            elif type == "internet_error":
                container.children[2].text = "Pas de connexion internet." if options_json[
                                                                                              "language"] == "fr" else "No internet connexion."
        container.children[1].children[1].text = ""
        pa.add_widget(container)

    @mainthread
    def to_playlist_screen(self):
        sm.current = "playlist_screen"

    @mainthread
    def add_title(self, title):
        label = Label(text=title)
        label.halign = "left"
        label.font_name = app.Roboto_bold_font
        label.color = app.text_color
        label.size_hint = (None, 1)
        label.width = app.p_to_dp(700)
        label.valign = "center"
        label.font_size = app.p_to_dp(45)
        label.padding = [app.p_to_dp(18), app.p_to_dp(10)]
        label.text_size = label.size
        label.shorten = True
        label.split_str = "..."
        label.shorten_from = "right"
        container_of_title = sm.get_screen('playlist_screen').ids.title_container_no_trad
        if len(container_of_title.children) >1:
            sm.get_screen('playlist_screen').on_leave()
        container_of_title.add_widget(label)

    @mainthread
    def add_a_video(self, video_stream):
        parent = sm.get_screen('playlist_screen').ids.playlist_loaded_no_trad
        print(video_stream.views)
        widget = Item_Of_List(video_stream.title, f"https://img.youtube.com/vi/{video_stream.video_id}/0.jpg",
                              video_stream.author, video_stream.views)
        widget.stream = video_stream
        parent.add_widget(widget)
        widget.width = parent.width

    @mainthread
    def back_btn(self):
        if getattr(self, "is_loading", None):
            return False
        sm.transition.direction = "right"
        sm.current = "start_screen"

class SavedLinksScreen(Screen):
    def on_pre_enter(self, *args):
        container = self.ids.SLS_container_no_trad
        with open("links.json") as links_file:
            links_read = links_file.read()
            links_dict = json.loads(links_read)
        if len(links_dict["links"]) == 0:
            with open("options.json") as options_file:
                options_read = options_file.read()
                options = json.loads(options_read)
            self.img = Image(size_hint = (None, None),size=(app.p_to_dp(850), app.p_to_dp(850)), pos_hint={'center_x': 0.5, 'center_y':0.5})
            self.img.source = f"assets/gideon_the_pigeon_{options['color_mode']}_{options['language']}.png"
            print(Window.width)
            self.children[0].add_widget(self.img)
        else:
            for link in links_dict["links"]:
                try:
                    container.add_widget(A_Playlist_Item(link[0], link[1]))
                except Exception as e:
                    print(e)
    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "start_screen"
    def on_leave(self, *args):
        container = self.ids.SLS_container_no_trad
        if getattr(self, "img", None):
            self.children[0].remove_widget(self.img)
        while len(container.children) > 0:
            container.remove_widget(container.children[0])
class MainScreenManager(ScreenManager):
    pass


sm = ScreenManager()


class LanguageScreen(Screen):
    def setLanguage(self, lang):
        already = False
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            if options_data.get('language'):
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
            self.background_rect = RoundedRectangle(
                pos=(parent.pos[0], parent.pos[1] + app.translate_dp_to_p(app.p_to_dp(155))),
                size=(parent.width, self.height), radius=[self.height / 2])
            Color(*app.bg_color_for_video_res_btn)
            self.progress_rect = RoundedRectangle(pos=(parent.pos[0] + app.translate_dp_to_p(app.p_to_dp(7.5)),
                                                       parent.pos[1] + app.translate_dp_to_p(app.p_to_dp(162))), size=(
                ((parent.size[0] - app.translate_dp_to_p(app.p_to_dp(10))) / 100) * self.progress_value,
                app.translate_dp_to_p(app.p_to_dp(20))), radius=[app.translate_dp_to_p(app.p_to_dp(10))])
        self.bind(progress_value=self.update_progress)

    @mainthread
    def update_progress(self, instance, value):
        self.progress_rect.size = (((self.par.size[0] - app.translate_dp_to_p(app.p_to_dp(15))) / 100) * value,
                                   app.translate_dp_to_p(app.p_to_dp(20)))

class A_loading_button(Button):
    def __init__(self, **kwargs):
        super(A_loading_button, self).__init__(**kwargs)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
        self.text = "Charger" if options_json["language"] == "fr" else "Load"
        self.font_size = app.text_size("small medium")
        self.font_name = app.Roboto_bold_font

        with self.canvas.before:
            Color(1,0,0,1)
            self.rect = RoundedRectangle(pos=self.pos,
                                         size=self.size,
                                         radius=[app.translate_dp_to_p(app.p_to_dp(12))])
        self.background_active = ""
        self.background_normal = ""
        self.background_down = ""
        self.background_color = 0, 0, 0, 0
        self.size_hint = (1, None)
        self.height = app.p_to_dp(80)
    def on_size(self, *args):
        self.rect.size = self.size
    def on_pos(self, *args):
        self.rect.pos = self.pos
class A_Playlist_Item(GridLayout):
    def __init__(self, title, link, **kwargs):
        self.link = link
        super(A_Playlist_Item, self).__init__(**kwargs)
        with self.canvas:
            Color(*app.light_grey)
            self.rect = RoundedRectangle(pos=(self.pos[0],self.pos[1] - app.translate_dp_to_p(app.p_to_dp(2))),
                                         size=self.size,
                                         radius=[app.translate_dp_to_p(app.p_to_dp(16))])
        self.btn = A_loading_button()
        self.btn.bind(on_press=lambda x: set_a_playlist_link(self.link))
        self.cols = 2
        self.size_hint = (1, None)
        self.height = app.p_to_dp(120)
        self.padding = [app.p_to_dp(32),0,0,0]
        self.spacing = [app.p_to_dp(22)]
        self.title_of_playlist = Label(text = title)
        self.title_of_playlist.color = app.text_color
        self.title_of_playlist.font_name = app.Roboto_font
        self.title_of_playlist.font_size = app.text_size("small medium")
        self.title_of_playlist.halign = "left"
        self.title_of_playlist.valign = "center"
        self.title_of_playlist.size_hint = (None, None)
        self.title_of_playlist.width = app.p_to_dp(575)
        self.title_of_playlist.height = self.height
        self.title_of_playlist.text_size = self.title_of_playlist.size
        self.title_of_playlist.shorten = True
        self.title_of_playlist.split_str = "..."
        self.title_of_playlist.shorten_from = "right"

        self.my_layout = AnchorLayout(size_hint=(None, 1), width=app.p_to_dp(200), padding=[0,app.p_to_dp(7),0,0])
        self.add_widget(self.title_of_playlist)
        self.my_layout.add_widget(self.btn)
        self.add_widget(self.my_layout)
    def on_size(self, *args):
        self.rect.size = self.size
    def on_pos(self, *args):
        self.rect.pos = (self.pos[0],self.pos[1] - app.translate_dp_to_p(app.p_to_dp(2)))

def set_a_playlist_link(lien):
    sm.current = "music_playlist_download_screen"
    sm.get_screen("music_playlist_download_screen").ids.input_of_youtube_playlist_link.text = lien
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
            options_json = json.loads(options_read)
            clr_mod = options_json["color_mode"]
            if clr_mod == "dark":
                # EVERYTHING RELATED TO DARK MODE
                app.text_input_bg = app.color(66, 66, 66, 255)
                app.background_of_the_app = app.color(33, 33, 33, 255)
                app.text_color = app.color(255, 255, 255, 225)
                app.light_grey = app.color(48, 48, 48, 255)
                app.bg_color_for_video_res_btn = app.color(255, 44, 56, 190)
            else:
                # EVERYTHING RELATED TO LIGHT MODE
                app.text_input_bg = (0.95, 0.95, 0.95, 1)
                app.background_of_the_app = app.color(250, 250, 250, 255)
                app.text_color = app.color(72, 75, 106, 255)
                app.light_grey = app.color(242, 240, 240, 255)
                app.bg_color_for_video_res_btn = app.color(171, 135, 255, 35)
            Window.clearcolor = tuple(app.background_of_the_app)
            sm.get_screen("language_screen").ids.hello_img_no_trad.source = f"assets/hello_{clr_mod}.png"
            sm.get_screen("language_screen").ids.bonjour_img_no_trad.source = f"assets/bonjour_{clr_mod}.png"
            return True

    def change_color_mode(self):
        with open('options.json', 'r+') as options_file:
            options_data = json.load(options_file)
            value = options_data["color_mode"]
            if value == "dark":
                options_data["color_mode"] = "light"
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
        sm.transition.direction = "right"
        sm.current = "start_screen"


@mainthread
def launch_progress_update_actual_pb(value):
    app.actual_pb.update_progress(None, value)


class PlaylistScreen(Screen):
    def launch_yt_playlist(self):
        launching_thread = threading.Thread(target=self.download_yt_playlist)
        launching_thread.start()

    def download_yt_playlist(self):
        music_playlist_dl_screen = sm.get_screen("music_playlist_download_screen")
        with open("options.json", "r") as file:
            options_read = file.read()
            options_json = json.loads(options_read)
        widgets = sm.get_screen("playlist_screen").children[0].children[1].children[0].children
        try:
            list_of_download_links = []
            list_of_types = []
            ## init of videos to download
            num_of_element_to_dl = 0
            is_empty = True
            for element in widgets:
                if "assets/checked_box" in element.second_btn.img.source:
                    num_of_element_to_dl += 1
                    list_of_download_links.append(f"https://www.youtube.com/watch?v={element.stream.video_id}")
                    list_of_types.append(element.type)
                    is_empty = False
                else:
                    list_of_download_links.append(None)
                    list_of_types.append(None)
            if is_empty:
                music_playlist_dl_screen.is_loading = False
                self.back_btn()
            else:
                self.back_btn(music_playlist_dl_screen)
                init_progress(music_playlist_dl_screen)
                percent = 100 / num_of_element_to_dl
                total = 0
            ## launch of downloads
                for iterator in range(len(widgets)):
                    loading_name = widgets[iterator].stream.title[:27] + "..." if len(widgets[iterator].stream.title) > 27 else widgets[iterator].stream.title
                    print(loading_name)
                    music_playlist_dl_screen.loading.text = f"Télécharge : {loading_name}" if options_json['language'] == 'fr' else f"Downloading : {loading_name}"
                    if not list_of_types[iterator]:
                        continue
                    if platform == "android":
                        send_notification(loading_name)
                    total+=percent
                    launch_progress_update_actual_pb(total)
                    pytube_object = YouTube(list_of_download_links[iterator])
                    download(pytube_object, list_of_types[iterator], make_a_filename(pytube_object.title))
            # #downloads finished
            #     while not getattr(app, "actual_pb", None):
            #         pass
                launch_progress_update_actual_pb(100)
                music_playlist_dl_screen.cancel_or_finish(music_playlist_dl_screen.children[0], music_playlist_dl_screen.container, app.actual_pb,music_playlist_dl_screen.loading,"finish", None)
                music_playlist_dl_screen.is_loading = False
        except HTTPError:
            music_playlist_dl_screen.cancel_or_finish(music_playlist_dl_screen.children[0], music_playlist_dl_screen.container, app.actual_pb,music_playlist_dl_screen.loading,"error", None)
            to_be_sure()
            print("ufck off, http error")
            print(list_of_download_links)
        except URLError:
            print("fdsfds")
            while not (getattr(app, "actual_pb", None) and music_playlist_dl_screen.loading in music_playlist_dl_screen.children[0].children):
                pass
            music_playlist_dl_screen.cancel_or_finish(music_playlist_dl_screen.children[0], music_playlist_dl_screen.container, app.actual_pb,music_playlist_dl_screen.loading,"internet_error"), None
            to_be_sure()
        except Exception as e:
            music_playlist_dl_screen.cancel_or_finish(music_playlist_dl_screen.children[0], music_playlist_dl_screen.container, app.actual_pb,music_playlist_dl_screen.loading,"error", None)
            print("c'est la merde ", e)
            print(type(e))
            to_be_sure()
            app.wait = False

    def on_leave(self, *args):
        self.ids.playlist_loaded_no_trad.children = []
        self.ids.title_container_no_trad.remove_widget(self.ids.title_container_no_trad.children[0])

    @mainthread
    def back_btn(self, *args):
        sm.transition.direction = "right"
        sm.current = "music_playlist_download_screen"
        if len(args)>0:
            args[0].is_loading = True


@mainthread
def init_progress(screen):
    app.actual_pb = my_progress_bar(screen.children[0].children[0])
    screen.children[0].remove_widget(screen.container)
    screen.init_interface(screen.children[0], app.actual_pb, screen.loading)
class ChooseResolutionScreen(Screen):
    def on_pre_start(self, *args):
        sm.transition.direction = "left"

    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "options_and_infos_screen"

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
                        btn.bg_color = app.bg_color_for_video_res_btn
                    else:
                        btn.bg_color = app.light_grey


class CustomResolutionScreen(Screen):
    def back_btn(self):
        sm.transition.direction = "right"
        sm.current = "choose_resolution_screen"


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
        if app.wait:
            raise OSError
        yt = YouTube(url)
        options = check_dl_preferencies_single()
        if check_if_file_is_downloaded(make_a_filename(yt.title), "audio" if options[0] else "video"):
            raise FileExistsError
        try:
            self.init_progress_bar(first_to_rm, second_to_rm, parent, pb)
            with open("options.json") as file:
                options_read = file.read()
                options_json = json.loads(options_read)
                loading_name = yt.title[:27] + "..." if len(yt.title) > 27 else yt.title
                self.ids.MSDS_label.text = f"{'Télécharge' if options_json['language'] == 'fr' else 'Downloading'} : {loading_name}"
                if platform == "android":
                    send_notification(loading_name)
            yt.register_on_progress_callback(self.on_progress)
            yt.register_on_complete_callback(self.on_complete)
            if options[0]:
                good_one = yt.streams.get_audio_only()
                file_name = "{0}.mp3".format(make_a_filename(good_one.title))
            else:
                need_audio = False
                if options[1] == "highest":
                    good_one = yt.streams.get_highest_resolution()
                elif options[1] == "lowest":
                    good_one = yt.streams.get_lowest_resolution()
                elif options[1] == "144p":
                    good_one = yt.streams.get_by_itag(160)
                    need_audio = True
                elif options[1] == "240p":
                    good_one = yt.streams.get_by_itag(133)
                    need_audio = True
                elif options[1] == "360p":
                    good_one = yt.streams.get_by_itag(18)
                    need_audio = True
                elif options[1] == "480p":
                    need_audio = True
                    good_one = yt.streams.get_by_itag(135)
                elif options[1] == "720p":
                    good_one = yt.streams.get_by_itag(22)
                elif options[1] == "1080p":
                    good_one = yt.streams.get_by_itag(137)
                    need_audio = True
                if not good_one:
                    self.on_complete(None, None, "ah")
                    return False
                if platform == "win" or platform == "linux":
                    file_name = "videos_for_pc_users/{0}.mp4".format(make_a_filename(good_one.title))
                else:
                    file_name = "{0}.mp4".format(make_a_filename(good_one.title))
                    print("le file name vient d'être set : ", file_name)
            if options[0]:
                if platform == "android":
                    good_one.download(filename=file_name)
                    convert_file_location(file_name, "audio")
                elif platform == "win" or platform == "linux":
                    good_one.download(filename=file_name, output_path="musics_for_pc_users")
            else:
                if need_audio:
                    app.wait = True
                    try:
                        print(good_one)
                        good_one.download(filename="video.mp4")
                        audio_for_merge = yt.streams.get_audio_only()
                        audio_for_merge.download(filename="audio.mp3")
                        ffmpeg_command = [
                            'ffmpeg.exe',
                            '-i', "video.mp4",
                            '-i', "audio.mp3",
                            '-c:v', 'copy',
                            '-c:a', 'aac',
                            file_name
                        ]
                        print("start downloadd")
                        print(os.listdir(os.getcwd()))
                        if platform == "android":
                            ffmpeg_for_android.Run(f"-i video.mp4 -i audio.mp3 -c:v copy -c:a aac {file_name}")
                        else:
                            subprocess.run(ffmpeg_command)
                        print("downloadd finished")
                        print(os.listdir(os.getcwd()))
                        if platform == "android":
                            while not file_name in os.listdir(os.getcwd()):
                                print(file_name, " alors que ", os.listdir(os.getcwd()))
                                pass
                            convert_file_location(file_name, "video")
                            print("après le convert_file_loc ", os.listdir(os.getcwd()))
                        app.wait = False
                    except Exception as e:
                        print(e)
                        to_be_sure()
                        app.wait = False
                else:
                    if platform == "android":
                        good_one.download(filename=file_name)
                        convert_file_location(file_name, "video")
                    elif platform == "win" or platform == "linux":
                        good_one.download(filename=file_name, output_path="videos_for_pc_users")

        except Exception as e:
            self.cancel_or_finish(first_to_rm, second_to_rm, parent, pb, "cancel")
            print("exception", e)
    except URLError:
        reset_text(self.ids.input_of_youtube_link)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "Probablement pas de connexion internet." if options_json[
                                                                                        "language"] == "fr" else "Probably no internet connexion."
    except FileExistsError:
        reset_text(self.ids.input_of_youtube_link)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "La vidéo a déjà été téléchargée." if options_json[
                                                                                 'language'] == 'fr' else "This video has already been downloaded."
    except OSError:
        reset_text(self.ids.input_of_youtube_link)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "Finalisation du téléchargement précédent.\n(peut prendre quelques minutes)" if \
                options_json[
                    'language'] == 'fr' else "Waiting for the previous download to end\n(can take a few minutes)"
    except Exception as e:
        print('marche pas', e)
        reset_text(self.ids.input_of_youtube_link)
        with open("options.json") as options:
            options_read = options.read()
            options_json = json.loads(options_read)
            self.ids.MSDS_label.text = "Votre lien est incorrect, vérifiez et réessayer." if options_json[
                                                                                                 'language'] == 'fr' else "Your link is incorrect, verify and retry."


def init_yt_playlist(self, url, pa, base_container, pb, loading):
    try:
        playlist = Playlist(url)
        self.init_interface(pa, pb, loading)
        percent = 50 / (len(playlist.videos) + 1)
        print(playlist.title)
        total = 50
        self.pb.update_progress(None, total)
        self.add_title(playlist.title)
        total += percent
        self.pb.update_progress(None, total)
        for video in playlist.videos:
            self.add_a_video(video)
            total += percent
            self.pb.update_progress(None, total)
            time.sleep(.1)
        self.to_playlist_screen()
        self.cancel_or_finish(pa, base_container, pb, loading, "finish", playlist.title)
    except URLError:
        self.cancel_or_finish(pa, base_container, pb, loading, "internet_error", None)
    except KeyError:
        self.cancel_or_finish(pa, base_container, pb, loading, "error", None)
    except Exception as e:
        print("wtff", e)
        print("wtff", type(e))
        self.cancel_or_finish(pa, base_container, pb, loading, "error", None)


def download(stream, type, title):
    if type == "video":
        need_audio = False
        options = check_dl_preferencies_single()
        if options[1] == "highest":
            good_one = stream.streams.get_highest_resolution()
        elif options[1] == "lowest":
            good_one = stream.streams.get_lowest_resolution()
        elif options[1] == "144p":
            good_one = stream.streams.get_by_itag(160)
            need_audio = True
        elif options[1] == "240p":
            good_one = stream.streams.get_by_itag(133)
            need_audio = True
        elif options[1] == "360p":
            good_one = stream.streams.get_by_itag(18)
            need_audio = True
        elif options[1] == "480p":
            need_audio = True
            good_one = stream.streams.get_by_itag(135)
        elif options[1] == "720p":
            good_one = stream.streams.get_by_itag(22)
        elif options[1] == "1080p":
            good_one = stream.streams.get_by_itag(137)
            need_audio = True
        if platform == "win" or platform == "linux":
            file_name = "videos_for_pc_users/{0}.mp4".format(make_a_filename(title))
        else:
            file_name = "{0}.mp4".format(make_a_filename(title))
            print("le file name vient d'être set : ", file_name)
        if need_audio:
            app.wait = True
            if not good_one:
                return False
            good_one.download(filename="video.mp4")
            audio_for_merge = stream.streams.get_audio_only()
            audio_for_merge.download(filename="audio.mp3")
            ffmpeg_command = [
                'ffmpeg.exe',
                '-i', "video.mp4",
                '-i', "audio.mp3",
                '-c:v', 'copy',
                '-c:a', 'aac',
                file_name
            ]
            print("start downloadd")
            print(os.listdir(os.getcwd()))
            if platform == "android":
                ffmpeg_for_android.Run(f"-i video.mp4 -i audio.mp3 -c:v copy -c:a aac {file_name}")
            else:
                subprocess.run(ffmpeg_command)
            to_be_sure()
            print("downloadd finished")
            print(os.listdir(os.getcwd()))
            if platform == "android":
                while not file_name in os.listdir(os.getcwd()):
                    pass
                convert_file_location(file_name, "video")
                print("après le convert_file_loc ", os.listdir(os.getcwd()))
            app.wait = False
        else:
            if platform == "android":
                good_one.download(filename=file_name)
                convert_file_location(file_name, "video")
            elif platform == "win" or platform == "linux":
                good_one.download(filename=file_name)
    elif type == "audio":
        good_one = stream.streams.get_audio_only()
        name_of_file = "{0}.mp3".format(make_a_filename(title))
        output = os.getcwd() if platform == "android" else "musics_for_pc_users"
        good_one.download(filename=name_of_file, output_path=output)
        if platform == "android":
            convert_file_location(name_of_file, type)


def convert_file_location(file, type):
    print("file name reçu dans convert_file_location ", file)
    print("listdir avant le convert_file_location ", os.listdir(os.getcwd()))
    try:
        Environment = autoclass('android.os.Environment')
        if type == "audio":
            folder = Environment.DIRECTORY_MUSIC + "/HypLoad"
        elif type == "video":
            folder = Environment.DIRECTORY_MOVIES + "/HypLoad"
        place_of_file = os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), folder)
        if not os.path.exists(place_of_file):
            os.mkdir(place_of_file)
        SS = SharedStorage()
        SS.copy_to_shared(os.path.join(os.getcwd(), file), collection=folder)
        print(os.listdir(os.getcwd()))
        os.remove(file)
        to_be_sure()
    except Exception as e:
        print("oh !", e)


######END OF FUNCTIONS FOR ALL PYTUBE AND DOWNLOAD THINGS ##########

######START OF FUNCTIONS WITH LIL UTILITIES ##########
@mainthread
def reset_text(el):
    el.text = ""


def to_be_sure():
    if "audio.mp3" in os.listdir(os.getcwd()):
        os.remove("audio.mp3")
    if "video.mp4" in os.listdir(os.getcwd()):
        os.remove("video.mp4")


def check_if_file_is_downloaded(title, type):
    if platform == "android":
        Environment = autoclass('android.os.Environment')
        if type == "audio":
            folder = Environment.DIRECTORY_MUSIC
            source = title + ".mp3"
        elif type == "video":
            folder = Environment.DIRECTORY_MOVIES
            source = title + ".mp4"
        place_of_file = os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), folder, "HypLoad")
        if not os.path.exists(place_of_file):
            os.mkdir(place_of_file)
        print(place_of_file)
        print("listdir hypload", os.listdir(place_of_file))
        print("listdir à la base", os.listdir(os.path.join(Environment.getExternalStorageDirectory().getAbsolutePath(), folder)))
        print(source in os.listdir(place_of_file))
        return source in os.listdir(place_of_file)
    elif platform == "win" or platform == "linux":
        print("le titre est ", title, " et le type est ", type)
        if type == "audio":
            source = title + ".mp3"
        elif type == "video":
            source = title + ".mp4"
        print("la source est ", source)
        print("renvoie ", source in os.listdir("musics_for_pc_users"))
        print("'pourtant : ", os.listdir("musics_for_pc_users"))
        return source in os.listdir("musics_for_pc_users") if type == "audio" else source in os.listdir(
            "videos_for_pc_users")


def make_a_filename(str):
    return str.replace('\\', '').replace(":", "").replace('/', '').replace('<', '').replace('>', '').replace('*',
                                                                                                             '').replace(
        '?', '').replace('"', '').replace('|', '').replace(' ', '_')
@mainthread
def send_notification(content):
    print("notification pas envoyée car kvdroid est à chier")
def send_toast_notification(content):
    Build = autoclass("android.os.Build")
    AndroidString = autoclass('java.lang.String')
    Toast = autoclass('android.widget.Toast')
    activity = autoclass("org.kivy.android.PythonActivity").mActivity
    toast(content, Toast, activity, AndroidString)
if platform == "android":
    @run_on_ui_thread
    def toast(content, Toast, activity, AndroidString):
        Toast.makeText(
            activity,
            cast('java.lang.CharSequence', AndroidString(content)),
            Toast.LENGTH_LONG
        ).show()
def change_number_in_appropriate_form(num):
    number = str(num)
    division_factor = (len(number) - 1) // 3
    for i in range(division_factor):
        number = number[:((i + 1) * 3 + i) * (-1)] + ' ' + number[((i + 1) * 3 + i) * (-1):]
    return number


######END OF FUNCTIONS WITH LIL UTILITIES ##########

if __name__ == '__main__':
    app = HypLoadApp()
    app.run()
