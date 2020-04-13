class Cella:
    def __init__(self, init_str):
        cols = {82: "red", 66: "blue", 71: "green", 32: "white"}

        self.x = init_str['userX']
        self.y = init_str['userY']
        self.color = cols[init_str['userVal']]

    def __repr__(self) -> str:
        str_ = f"x: {self.x}\ty: {self.y}\tcolor: {self.color}"

        return str_

    def to_csv(self) -> str:
        str_ = f"{self.x},{self.y},{self.color}\n"
        return str_
