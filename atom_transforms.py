transforms = [
    # Wormhole_0, Flower_0: "xyz"
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: (  u,  v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: (  u, -v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: ( -u,  v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: ( -u, -v,  w)},
    # Wormhole_0, Flower_0: "yxz"
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: (  v,  u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: (  v, -u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: ( -v,  u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: ( -v, -u,  w)},
    
    # Wormhole_0, Flower_1: "xy(-z)"
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: (  u,  v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: (  u, -v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: ( -u,  v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: ( -u, -v, -w)},
    # Wormhole_0, Flower_1: "yx(-z)"
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: (  v,  u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: (  v, -u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: ( -v,  u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: ( -v, -u, -w)},
    
    # Wormhole_1, Flower_2: "zxy"
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w,  u,  v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w,  u, -v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w, -u,  v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w, -u, -v)},
    # Wormhole_1, Flower_2: "zyx"
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w,  v,  u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w,  v, -u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w, -v,  u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w, -v, -u)},
    
    # Wormhole_1, Flower_3: "(-z)xy"
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w,  u,  v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w,  u, -v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w, -u,  v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w, -u, -v)},
    # Wormhole_1, Flower_3: "(-z)yx"
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w,  v,  u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w,  v, -u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w, -v,  u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w, -v, -u)},
    
    # Wormhole_2, Flower_4: "xzy"
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: (  u,  w,  v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: (  u,  w, -v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: ( -u,  w,  v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: ( -u,  w, -v)},
    # Wormhole_2, Flower_4: "yzx"
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: (  v,  w,  u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: (  v,  w, -u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: ( -v,  w,  u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: ( -v,  w, -u)},
    
    # Wormhole_2, Flower_5: "x(-z)y"
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: (  u, -w,  v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: (  u, -w, -v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: ( -u, -w,  v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: ( -u, -w, -v)},
    # Wormhole_2, Flower_5: "y(-z)x"
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: (  v, -w,  u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: (  v, -w, -u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: ( -v, -w,  u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: ( -v, -w, -u)},
]