import random


class Time:
    def __init__(self, s: str) -> None:
        if isinstance(s, Time):
            self.hour = s.hour
            self.min = s.min
            self.sec = s.sec
            return
        else:
            self.hour = 0
            self.min = 0
            self.sec = 0

        s = s.lower().strip()
        if ("am" in s) or ("pm" in s) or (s.count(":") == 2):
            try:
                self.hour, self.min = tuple(map(int, s.strip("apm").split(":")))
            except ValueError:
                self.hour, self.min, self.sec = tuple(map(int, s.strip("apm").split(":")))
            if "am" in s.lower() and self.hour == 12:
                self.hour = 0
            elif "pm" in s.lower():
                if self.hour == 12:
                    pass
                else:
                    self.hour += 12

            self.min += self.sec // 60
            self.sec %= 60
            self.hour += self.min // 60
            self.min %= 60
        else:
            print("Unknown Time:", s)
            input()

    def __str__(self) -> str:
        return str(self.hour).rjust(2, "0") + ":" + str(self.min).rjust(2, "0") + ":" + str(self.sec).rjust(2, "0")

    def __repr__(self):
        return str(self.hour).rjust(2, "0") + ":" + str(self.min).rjust(2, "0") + ":" + str(self.sec).rjust(2, "0")

    def __gt__(self, t) -> bool:
        if self.hour < t.hour:
            return False
        elif self.hour > t.hour:
            return True
        elif self.min < t.min:
            return False
        elif self.min > t.min:
            return True
        else:
            return False

    def __bool__(self):
        return self != Time("00:00am")

    def __eq__(self, t):
        return self.hour == t.hour and self.min == t.min and self.sec == t.sec

    def __ge__(self, t):
        return self.__gt__(t) or self.__eq__(t)

    def __sub__(self, t):
        assert self >= t
        return Time.difference(self, t)

    def __lt__(self, t):
        return not self.__ge__(t)

    def __le__(self, t):
        return not self.__gt__(t)

    @staticmethod
    def difference(t1, t2):
        large = t1 if t1 > t2 else t2
        small = t1 if large is t2 else t2

        h = large.hour - small.hour
        m = large.min - small.min
        apm = "AM"
        if h == 12:
            apm = "PM"
        return Time(f"{h}:{m}{apm}")

    def __add__(self, t):
        hour = self.hour + t.hour
        ap = "pm" if hour == 12 else "am"
        return Time(f"{hour}:{self.min + t.min}:{self.sec + t.sec}{ap}")

    def iszero(self):
        return self.hour == 0 and self.min == 0 and self.sec == 0


class Routine:
    def __init__(self):
        self.data = {}  # format - "name":(start,end),"name2":(start,end)
        self.symbol = "".join(random.sample("!@#$%^&*():;?/>,<.|}{][+=_-", 5))
        # print(self.symbol)

    def get_available(self, start, end):
        assert start < end, f"starting time({start}) should be less than ending time({end})"

        for i in self.data.values():
            if start >= i[1]:
                continue
            elif start >= i[0]:
                if end <= i[1]:
                    return None  # returns 0
                else:
                    return self.get_available(i[1], end)
            elif start <= i[0]:
                if end <= i[0]:
                    return start, end
                else:
                    return self.get_available(start, i[0])
            else:
                print("Else part")

        return start, end

    def display(self):
        for i in self.data.items():
            name = i[0]
            if self.symbol in name:
                name = name.split(self.symbol)[0]
            print(name, "-", i[1])

    def display_stylish(self):
        # get max length
        length = len(max(list(self.data.keys()), key=len))
        print("NAME".center(length), "START".center(10), "END".center(10), sep="|")
        print("-" * length, "-" * 10, "-" * 10, sep="|")
        for i in self.data.items():
            name = i[0]
            if self.symbol in name:
                name = name.split(self.symbol)[0]
            print(name.center(length), str(i[1][0]).center(10), str(i[1][1]).center(10), sep="|", end="\n")

    def add_fixed(self, s):
        for i in s.split("\n"):
            name, start, end = i.split("-")
            name = name.strip(" ")
            start = Time(start.strip(" "))
            end = Time(end.strip(" "))

            start, end = self.get_available(start, end)
            if start or end:
                if name in self.data:
                    no = 0
                    while True:
                        virtual_name = name + self.symbol + str(no)
                        if virtual_name in self.data:
                            no += 1
                        else:
                            break
                    self.data[virtual_name] = (start, end)
                else:
                    self.data[name] = (start, end)
        self.sort()

    def get_time_left(self):
        total = Time("24:00am")
        for i in self.data.values():
            t = Time.difference(i[0], i[1])
            print(total, t, end=" ")
            total -= t
            print(total)
        return total

    def sort(self):
        tags = list(self.data.keys())
        tags.sort(key=lambda x: self.data[x][0])
        d = {}
        for i in tags:
            d[i] = self.data[i]
        self.data = d

    def add(self, name, start, end):
        if start.hour > 12 > end.hour:
            self.add(name, start, Time("11:59:59pm"))
            self.add(name, Time("12:00am"), end)
            return
        if name in self.data:
            no = 0
            while True:
                virtual_name = name + self.symbol + str(no)
                if virtual_name in self.data:
                    no += 1
                else:
                    break
            self.data[virtual_name] = (start, end)
        else:
            self.data[name] = (start, end)
        self.sort()

    def completed(self):
        t = Time("00:00am")
        for i in self.data.values():
            t += Time.difference(i[0], i[1])
        return t >= Time("23:59am")

    def get_total_time_for_tag(self, tagname):
        t = Time("00:00am")
        if tagname in self.data:
            t += Time.difference(*self.data[tagname])
            no = 0
            while True:
                virtual_name = tagname + self.symbol + str(no)
                if virtual_name in self.data:
                    t += Time.difference(*self.data[virtual_name])
                    no += 1
                else:
                    break
        return t

    def get_leisure_time(self):
        time = Time("00:00am")
        for i in self.data:
            start = self.data[i][0]
            end = self.data[i][1]
            if start <= time <= end:
                time = end
            else:
                break

        return time

    def summarize(self):
        d = {}
        for tag in self.data:
            name = tag.split(self.symbol)[0]
            if name in d:
                d[name] += Time.difference(self.data[tag][0], self.data[tag][1])
            else:
                d[name] = Time.difference(self.data[tag][0], self.data[tag][1])
        return d

class Result:
    def __init__(self,title,start,end):
        self.title = title 
        self.start = start
        self.end = end 

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

    time_12h = f"{hour:02d}:{minute:02d}:{second:02d} {period}"
    return time_12h

def decorate():
    print("="*25)


"""
To result
=========================
#fixed
Sleep - 00:00 - 08:00
Eat - 11:00 - 12:00
College - 15:00 - 18:00

#needed
Play_extra - 3:0:00 - 1:00:00
See movue_extra - 1:00:00 - 00:20:00

#preferred
Play - 18:00 - 21:00
See movue - 13:00 - 15:00


=========================
"""