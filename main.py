import flet
from core import Core


def main(page: flet.Page):
    core = Core(page=page)


if __name__ == "__main__":
    flet.app(target=main, view=flet.WEB_BROWSER, port=5211, upload_dir="uploads")
