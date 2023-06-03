from .classes import Time,Routine
import random

def convert_to_12_hour(time_24h):
    hour = time_24h.split(":")
    if len(hour) == 3:
        hour,minute,second = hour 
        second = int(second)
    elif len(hour) == 2:
        second = "00"
        hour, minute = hour
    
    hour = int(hour)
    minute = int(minute)

    period = 'AM' if hour < 12 else 'PM'
    hour = hour % 12
    if hour == 0:
        hour = 12
    hour = str(hour).rjust(2,"0")
    minute = str(minute).rjust(2,"0")
    second = str(second).rjust(2,"0")
    time_12h = f"{hour}:{minute}:{second} {period}"
    return time_12h

def get_fixed(s):
    t = ""
    for line in s.split("\n"):
        if "-" in line:
            title,start,end = line.split("-")
            t += f"{title} - {convert_to_12_hour(start)} - {convert_to_12_hour(end)}"
        t+="\n"
    
    return t.strip()

def get_needed(s):
    t = ""
    for line in s.split("\n"):
        if "-" in line:
            title,start,end = line.split("-")
            t += f"{title} - {convert_to_12_hour(start)} - {convert_to_12_hour(end)}"
        t+="\n"
    
    return t.strip()

def get_preferred(s):
    preferred_dict = {}
    for line in s.split("\n"):
        line = line.strip()
        if not line:
            continue
        tag,start,end = line.split("-")
        tag = tag.strip()
        start = Time(convert_to_12_hour(start))
        end = Time(convert_to_12_hour(end))
        if tag in preferred_dict:
            preferred_dict[tag] += ((start,end),)
        else:
            preferred_dict[tag] = ((start,end),)
    return preferred_dict


def get_total_time(l):
    l = l.split("\n")
    total = Time("00:00am")
    for i in l:
        i = i.split("-")[1].strip(" H")
        # i.strip("H")
        total += Time(f"{i}am")
    return total

def get_tags(l):
    l = l.split("\n")
    t=[]
    for i in l:
        i = i.split("-")[0].strip(" ")
        t.append(i)
    return t    


def main(FIXED_ROUTINES,NEEDED_STUFFS,PREFERRED):
    FIXED_ROUTINES = get_fixed(FIXED_ROUTINES)
    NEEDED_STUFFS = get_needed(NEEDED_STUFFS)
    preferred_dict = get_preferred(PREFERRED)
    r = Routine()
    r.add_fixed(FIXED_ROUTINES)

    # r.display()
    # print(r.data)

    assert (r.get_time_left()) >= (get_total_time(NEEDED_STUFFS)),f"TIME SHORTAGE \nTime left to Assign:{r.get_time_left()} \nTime needed to Assign:{get_total_time(NEEDED_STUFFS)}"

    tags = get_tags(NEEDED_STUFFS)
    preferred_tags = list(preferred_dict.keys())




    not_allowed=None
    l = [i.split("-") for i in NEEDED_STUFFS.split("\n")]
    # print(l,tags,sep="\n")

    # print(tags)
    while not r.completed() and tags:
        # get tags
        if len(preferred_tags) > 0:
            tag = random.choice(preferred_tags)
        #ignore not allowed
        if len(tags)>1:
            while tag == not_allowed:
                tag = random.choice(tags)
            not_allowed = tag
        else:
            tag = tags[0]
        # print(tag)
        
        #get consistency and total time
        for i in l:
            if tag.lower() in i[0].lower():
                total_time = Time(i[1])
                consistency = Time(i[2])
                break
        #get preferred time
        
        # print(tag,total_time,r.get_total_time_for_tag(tag))
        #hours needed
        required_time = total_time - r.get_total_time_for_tag(tag)
        #if completed remove the tag
        if required_time.iszero():
            # print("Removing:",tag)
            tags.remove(tag)
            
            if tag in preferred_tags:
                preferred_tags.remove(tag)
            continue
        elif consistency > required_time:
            consistency = required_time
        #get start time
        # if preferred time available or not

        if consistency.iszero():
            consistency = required_time

        if tag in preferred_dict:
            preferred_time_list = preferred_dict[tag]
            start = Time(preferred_time_list[0][0])
            end = start + consistency
            x = r.get_available(start,end)
            
            while not (x and (x[0] or x[1])):
                s,e = preferred_time_list[0]
                s = Time(s)
                e = Time(e)
                if end < e:
                    start = end 
                    end = start+consistency
                    x = r.get_available(start,end)
                else:
                    preferred_time_list = list(preferred_time_list)
                    preferred_time_list.pop(0)
                    preferred_dict[tag] = tuple(preferred_time_list)
                if not preferred_time_list:
                    del preferred_dict[tag]
                    # preferred_tags.remove(tag)
                    break
            if x and (x[0] or x[1]):
                r.add(tag,*x)
        else:
            start = r.get_leisure_time()
            end = start + consistency
            x = r.get_available(start,end)
            if x and (x[0] or x[1]):
                r.add(tag,*x)
        
        # print("Routine:")
        # r.display()
    # print("\n\n")
    
    return r


if __name__ == '__main__':
    # main(FIXED_ROUTINES,NEEDED_STUFFS,PREFERRED)
    pass