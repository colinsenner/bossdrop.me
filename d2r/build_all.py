import util.common
import util.translations


def main():
    game_version = "1.1.67358"

    excel_dir = util.common.get_excel_dir(game_version)
    translation_dir = util.common.get_translation_dir(game_version)

    translations = util.translations.get(translation_dir)


    print(excel_dir)
    print("[+] Done")

if __name__ == '__main__':
    main()
