def parse_dir_path(path: str, stop_at_dir: str) -> str:
    path_array: list = []
    single_dir: str = ""
    instance: int = 0
    final_path: str = ""
        
    while True:
        if single_dir == stop_at_dir:
            path_array.append(single_dir)
            break

        if path[instance] == "\\":
            path_array.append(single_dir+"\\")
            single_dir = ""
            instance += 1

        single_dir += path[instance]
        instance += 1

    for i in path_array: final_path += i
    return final_path
    
def parse_packet_info(msg: str) -> int:
    index: int = 0
    check_exception: int = 0
    number_str: str = ""
    while True:
        if index == len(msg): break
        try:
            check_exception = int(msg[index])
            number_str += str(msg[index])
        except: pass
        index += 1
    try: return int(number_str)
    except: return 1
        
def read_until(string_object: str, character: str) -> str:
    index: int = 0
    new_string_array: list = []
    new_string: str = ""
        
    while True:
        if string_object[index] == character: break
        else: new_string_array.append(string_object[index])
        index += 1

    for _chr in new_string_array: new_string += _chr
    return new_string