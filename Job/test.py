import gxrcAPI


def main():
    gxrc = gxrcAPI.GXRCAPI()
    urls = gxrc.get_urls()
    for url in urls:
        print(url)




if __name__ == "__main__":
    main()
