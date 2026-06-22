#import built-in modules
import sys

__version__ = "0.3.0"

__path_separator__: str = ""
if sys.platform == "darwin" or sys.platform.startswith("lin") == True: __path_separator__ = "/"
elif sys.platform.startswith("win"): __path_separator__ = "\\"

def parse_dir_path(path: str, stop_at_dir: str) -> str:
    path_array: list = []
    single_dir: str = ""
    instance: int = 0
    final_path: str = ""
        
    while True:
        if single_dir == stop_at_dir:
            path_array.append(single_dir)
            break

        if path[instance] == __path_separator__:
            path_array.append(single_dir+__path_separator__)
            single_dir = ""
            instance += 1

        single_dir += path[instance]
        instance += 1

    for i in path_array: final_path += i
    return final_path

__base_dir__ = parse_dir_path(__file__, "XSI_0.3.0")
__icon_dir__ = f"{__base_dir__}{__path_separator__}icons{__path_separator__}"
__file_dir__ = f"{__base_dir__}{__path_separator__}cache{__path_separator__}"
__help_path__ = f"{__base_dir__}{__path_separator__}bin{__path_separator__}tools{__path_separator__}XSI_help.pdf"
__system__ = sys.platform