from string import ascii_uppercase, digits

matrix = [
    ['5/B', 'B/R', 'M/G', 'Y/5', '4/1', 'R/W', '6/4', '1/6', '2/3', '3/M', 'G/Y', 'W/2'], #A
    ['2/R', '6/M', '4/3', '5/B', 'R/5', 'Y/2', '1/G', 'M/Y', 'W/6', '3/4', 'B/W', 'G/1'], #B
    ['M/Y', '2/4', 'Y/R', '3/5', 'W/2', 'G/B', '1/W', 'R/3', '5/G', '4/6', 'B/M', '6/1'], #C
    ['5/6', '6/3', '1/4', 'M/2', 'R/Y', '2/M', 'W/R', 'B/G', 'Y/W', '3/B', 'G/1', '4/5'], #D
    ['B/R', 'W/2', '2/3', '1/4', 'M/B', '5/6', 'Y/W', 'R/M', 'G/Y', '6/G', '3/5', '4/1'], #E
    ['R/Y', '2/G', '1/M', 'Y/5', '5/R', 'W/B', '6/3', 'B/1', 'M/4', 'G/6', '3/2', '4/W'], #F
    ['Y/1', '5/4', '2/W', 'R/Y', '1/R', 'B/3', '6/G', 'G/6', 'M/B', 'W/5', '4/2', '3/M'], #G
    ['3/5', 'W/Y', 'G/2', '2/B', '5/G', 'M/R', 'B/3', '1/4', '4/6', 'Y/M', '6/W', 'R/1'], #H
    ['R/M', '4/5', '5/W', 'B/1', 'M/6', '3/2', 'W/B', 'G/Y', 'Y/R', '1/4', '6/G', '2/3'], #I
    ['W/B', 'R/6', '5/Y', '4/1', '2/5', 'Y/3', 'M/W', '3/2', 'B/G', 'G/M', '1/R', '6/4'], #J
    ['6/4', 'B/2', 'W/G', 'R/5', 'G/1', '2/Y', 'Y/R', 'M/B', '1/6', '3/W', '5/3', '4/M'], #K
    ['6/4', 'B/5', 'W/6', '1/G', 'R/2', '4/R', 'G/W', '3/M', '2/B', 'Y/3', '5/Y', 'M/1'], #L
    ['W/3', '3/G', '2/4', 'Y/M', 'M/2', 'R/5', '6/R', 'B/6', 'G/Y', '5/B', '1/W', '4/1'], #M
    ['1/Y', '6/M', '2/1', 'G/R', '3/G', '5/B', 'R/4', '4/3', 'W/2', 'Y/W', 'B/5', 'M/6'], #N
    ['R/5', '3/G', '2/3', 'W/4', 'B/2', '1/M', '5/6', 'M/1', '4/Y', 'G/B', '6/R', 'Y/W'], #O
    ['1/4', '4/B', '6/2', '3/W', 'M/R', 'Y/6', 'B/Y', '2/G', '5/M', 'G/5', 'R/3', 'W/1'], #P
    ['5/G', 'M/B', '4/W', 'Y/2', 'R/M', 'W/4', '6/1', '3/6', 'B/Y', '1/5', 'G/R', '2/3'], #Q
    ['M/G', '5/6', 'G/M', 'W/5', 'Y/2', 'R/4', 'B/1', '1/B', '2/R', '4/3', '6/W', '3/Y'], #R
    ['R/Y', '6/5', '5/G', 'G/B', 'W/M', '4/3', '1/W', 'B/1', '3/6', '2/4', 'Y/2', 'M/R'], #S
    ['G/3', 'B/2', '6/W', 'M/B', '1/5', 'Y/4', '5/M', 'W/R', '4/6', '3/Y', '2/G', 'R/1'], #T
    ['5/1', 'W/3', '4/5', '3/4', 'Y/W', '1/Y', 'B/G', '6/2', 'M/6', 'G/R', '2/M', 'R/B'], #U
    ['M/6', '6/B', '1/G', '3/5', 'W/R', 'B/4', 'G/M', 'R/1', '2/W', '5/2', '4/Y', 'Y/3'], #V
    ['Y/M', 'B/1', '5/3', '2/G', '3/2', 'R/5', '1/4', 'W/6', '4/W', 'G/R', 'M/Y', '6/B'], #W
    ['4/2', 'R/B', 'W/5', 'Y/M', '2/Y', '5/1', 'B/R', 'G/3', 'M/G', '3/6', '6/W', '1/4'], #X
    ['G/Y', '1/R', '5/4', '4/G', '3/B', 'M/6', '2/5', 'Y/2', 'R/1', 'W/3', 'B/W', '6/M'], #Y
    ['G/B', 'B/G', '1/5', 'M/1', '3/M', 'R/3', 'Y/W', '6/Y', '5/2', '4/6', 'W/R', '2/4'], #Z
    ['2/R', 'R/B', '5/G', 'W/2', 'Y/1', '4/Y', '3/5', '1/M', 'B/W', 'G/6', '6/4', 'M/3'], #0
    ['R/4', 'W/6', '3/2', '2/W', '4/Y', '6/5', 'B/R', '5/G', 'Y/B', 'G/M', 'M/1', '1/3'], #1
    ['4/B', 'B/3', '6/4', 'W/1', 'M/Y', 'R/6', 'G/5', 'Y/W', '5/2', '2/R', '3/G', '1/M'], #2
    ['B/6', 'M/3', '4/B', '1/4', '2/5', 'Y/1', 'G/Y', 'R/W', 'W/G', '5/2', '6/M', '3/R'], #3
    ['M/R', '2/B', 'W/5', '6/Y', 'B/3', '4/2', 'G/1', 'Y/6', '5/G', '3/M', 'R/W', '1/4'], #4
    ['Y/1', '5/6', '1/W', 'W/4', 'B/G', 'G/5', '4/M', '2/B', '3/R', '6/3', 'M/2', 'R/Y'], #5
    ['3/4', 'W/B', 'Y/G', '5/M', 'R/1', 'G/W', '1/2', '6/Y', 'B/R', 'M/6', '4/3', '2/5'], #6
    ['4/G', '6/5', 'Y/4', 'G/B', '3/1', 'M/Y', '5/3', '1/M', '2/R', 'R/2', 'B/W', 'W/6'], #7
    ['Y/B', 'R/2', 'W/R', '5/3', '1/W', '3/5', 'B/M', 'G/4', '6/Y', '4/G', '2/1', 'M/6'], #8
    ['G/Y', '3/1', '5/M', 'R/2', '6/W', 'M/B', 'Y/6', '2/4', '4/G', 'B/5', '1/R', 'W/3']  #9
]

class LightCycle:
    def __init__(this, serial, colors):
        """ serial: bomb serial number (string)
            colors: light cycle colors, separated by spaces if desired """
        this.serial = serial.upper()
        this.colors = colors.upper().split() if " " in colors else list(colors.upper())
        this.initial_colors = list(this.colors)
        this.apply_changes()

    def produce_combinations(this):
        out = zip(this.serial, this.serial[::-1])
        return ("".join(i) for i in out)

    def get_changes(this):
        for combo in this.produce_combinations():
            col,row = map((ascii_uppercase+digits).index, combo)
            yield matrix[col][row//3]

    def apply_changes(this):
        def parse(i):
            if i.isalpha():
                return this.colors.index(i)
            else:
                return int(i)-1
        for change in this.get_changes():
            one,two = map(parse,change.split("/"))
            tmp = this.colors[one]
            this.colors[one] = this.colors[two]
            this.colors[two] = tmp

if __name__ == "__main__":
    serial = input("Serial: ")
    colors = input("Colors: ")
    lc = LightCycle(serial, colors)
    print(lc.colors)
