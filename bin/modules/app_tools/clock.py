from time import sleep, localtime

"""Appends a zero to a number if it is below 10, negative numbers do not apply"""
def append_zero(number: int) -> str:
        if number < 10: return f"0{number}"
        else: return number
            
"""Selects the correct time period of the day if using a 12 hour format"""
def time_period(hour: int) -> str:
        if hour > 11: return "PM"
        else: return "AM"

"""Can count one number up or down, returns a list of the new number and a carry out number if 
counter reaches the stop value"""
def counter(number: int = 0, stop: int = 59, reset: int = 0, direction: str = "up") -> list[int,int]:
        if (number == stop):
            number = reset
            carry_out = 1
        else: 
            carry_out = 0
            match direction:
                case "up": number += 1
                case "down": number -= 1
                case _: raise ValueError("Not a valid string argument! Try using 'up' or 'down.'")
        return [number, carry_out]

"""Formats given hour to a 12 hour format or a 24 hour format"""    
def _normal_time(hour: int) -> int:
    if localtime()[3] == 0: return 12
    if hour > 12: return hour - 12
    else: return hour
         
"""Gets the available date from the users computer"""
def get_computer_date(format: str = "mm/dd/yyyy") -> str:
        match format:
            case "mm/dd/yyyy": return f"{localtime()[1]}/{localtime()[2]}/{localtime()[0]}"
            case "dd/mm/yyyy": return f"{localtime()[2]}/{localtime()[1]}/{localtime()[0]}"
            case "yyyy/mm/dd": return f"{localtime()[0]}/{localtime()[1]}/{localtime()[2]}"
            case "yyyy/dd/mm": return f"{localtime()[0]}/{localtime()[2]}/{localtime()[1]}"
            case _: raise ValueError("Not a valid string argument! Try using the format: 'mm/dd/yyyy.'")
             
"""Gets the available time from the users computer, can be a 12 hour format or a 24 hour format. 
Return as a list to use for other functions""" 
def get_computer_time(format: int = 12, return_as_list: bool = False, disable_seconds: bool = False) -> str|list[int]:
    if return_as_list: return [int(localtime()[3]), int(localtime()[4]), int(localtime()[5])]
    elif format == 24: 
        if disable_seconds: return f"{append_zero(localtime()[3])}:{append_zero(localtime()[4])}"
        else: return f"{append_zero(localtime()[3])}:{append_zero(localtime()[4])}:{append_zero(localtime()[5])}"
    elif format == 12: 
        if disable_seconds: return f"{append_zero(_normal_time(localtime()[3]))}:{append_zero(localtime()[4])} {time_period(localtime()[3])}"      
        else: return f"{append_zero(_normal_time(localtime()[3]))}:{append_zero(localtime()[4])}:{append_zero(localtime()[5])} {time_period(localtime()[3])}"      

"""Finds the future time from the current time and returns as one string."""    
def time_ahead(current_time: list[int] = [12, 50, 30], future_time_ahead: list[int] = [1, 30, 00], format: int = 12) -> str:
        new_time=[current_time[0] + future_time_ahead[0], current_time[1] + future_time_ahead[1], current_time[2] + future_time_ahead[2]]

        if (new_time[2] >= 60):
            new_time[1] += int(new_time[2] / 60)
            new_time[2] -= 60
            
        if (new_time[2] == 60): new_time[2] = 0
            
        if (new_time[1] >= 60):
            new_time[0] += int(new_time[1] / 60)
            new_time[1] -= 60
        
        if (new_time[1] == 60): new_time[1] = 0

        if (new_time[0] >= 24): new_time[0] -= 24

        if format == 24: return f"{append_zero(_normal_time(new_time[0], format))}:{append_zero(new_time[1])}:{append_zero(new_time[2])}"
        else: return f"{append_zero(_normal_time(new_time[0]))}:{append_zero(new_time[1])}:{append_zero(new_time[2])} {time_period(new_time[0])}"

if __name__ == "__main__":
    print(append_zero(6))
    print(time_period(15))
    print(counter(4))
    print(get_computer_date())
    print(get_computer_time())
    print(time_ahead())