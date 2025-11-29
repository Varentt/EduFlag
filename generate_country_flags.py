import os
import csv
import math
import cairo

OUT_DIR = "flags"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 900, 600  

def save(surface, name):
    path = os.path.join(OUT_DIR, name)
    surface.write_to_png(path)
    print("Saved:", path)

def new_canvas():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    return s, cairo.Context(s)

def draw_rectangle(ctx, x, y, w, h, color):
    ctx.set_source_rgb(*color)
    ctx.rectangle(x, y, w, h)
    ctx.fill()

def draw_circle(ctx, cx, cy, r, color):
    ctx.set_source_rgb(*color)
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.fill()

# RGB helper
def rgb(hexcode):
    hexcode = hexcode.lstrip('#')
    return tuple(int(hexcode[i:i+2], 16) / 255 for i in (0, 2, 4))

quiz = []

# ------------ INDONESIA ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H/2, rgb("#FF0000"))
draw_rectangle(ctx, 0, H/2, W, H/2, rgb("#FFFFFF"))
save(s, "indonesia.png")
quiz.append(["indonesia.png", "Which country's flag is red over white?", "Indonesia"])

# ------------ JAPAN ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#FFFFFF"))
draw_circle(ctx, W/2, H/2, H*0.25, rgb("#BC002D"))
save(s, "japan.png")
quiz.append(["japan.png", "Which flag has a red circle in the center?", "Japan"])

# ------------ FRANCE ------------
s, ctx = new_canvas()
w = W/3
draw_rectangle(ctx, 0, 0, w, H, rgb("#0055A4"))
draw_rectangle(ctx, w, 0, w, H, rgb("#FFFFFF"))
draw_rectangle(ctx, 2*w, 0, w, H, rgb("#EF4135"))
save(s, "france.png")
quiz.append(["france.png", "Which flag has blue-white-red vertical stripes?", "France"])

# ------------ ITALY ------------
s, ctx = new_canvas()
w = W/3
draw_rectangle(ctx, 0, 0, w, H, rgb("#009246"))
draw_rectangle(ctx, w, 0, w, H, rgb("#FFFFFF"))
draw_rectangle(ctx, 2*w, 0, w, H, rgb("#CE2B37"))
save(s, "italy.png")
quiz.append(["italy.png", "Which flag has green-white-red vertical stripes?", "Italy"])

# ------------ GERMANY ------------
s, ctx = new_canvas()
h = H/3
draw_rectangle(ctx, 0, 0, W, h, rgb("#000000"))
draw_rectangle(ctx, 0, h, W, h, rgb("#DD0000"))
draw_rectangle(ctx, 0, 2*h, W, h, rgb("#FFCE00"))
save(s, "germany.png")
quiz.append(["germany.png", "Which flag has black-red-yellow horizontal stripes?", "Germany"])

# ------------ INDIA ------------
s, ctx = new_canvas()

saffron = rgb("#FF9933")
white   = rgb("#FFFFFF")
green   = rgb("#138808")
navy    = rgb("#000080") 

stripe_h = H / 3
draw_rectangle(ctx, 0, 0, W, stripe_h, saffron)
draw_rectangle(ctx, 0, stripe_h, W, stripe_h, white)
draw_rectangle(ctx, 0, 2*stripe_h, W, stripe_h, green)

cx, cy = W/2, H/2
r_outer = H * 0.12

# Lingkaran luar
ctx.set_source_rgb(*navy)
ctx.set_line_width(8)
ctx.arc(cx, cy, r_outer, 0, 2*math.pi)
ctx.stroke()

ctx.set_line_width(4)
for i in range(24):
    angle = (2 * math.pi / 24) * i
    x = cx + r_outer * math.cos(angle)
    y = cy + r_outer * math.sin(angle)
    ctx.move_to(cx, cy)
    ctx.line_to(x, y)
    ctx.stroke()

save(s, "india.png")
quiz.append(["india.png", "Which country's flag has saffron, white and green with a blue Ashoka Chakra?", "India"])

# ------------ BANGLADESH ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#006A4E"))
draw_circle(ctx, W*0.40, H/2, H*0.25, rgb("#F42A41"))
save(s, "bangladesh.png")
quiz.append(["bangladesh.png", "Which flag is green with a red circle slightly to the left?", "Bangladesh"])

# ------------ NIGERIA ------------
s, ctx = new_canvas()
w = W/3
draw_rectangle(ctx, 0, 0, w, H, rgb("#008751"))
draw_rectangle(ctx, w, 0, w, H, rgb("#FFFFFF"))
draw_rectangle(ctx, 2*w, 0, w, H, rgb("#008751"))
save(s, "nigeria.png")
quiz.append(["nigeria.png", "Which flag has green-white-green vertical stripes?", "Nigeria"])

# ------------ TURKEY ------------
s, ctx = new_canvas()

red = rgb("#E30A17")
white = rgb("#FFFFFF")

draw_rectangle(ctx, 0, 0, W, H, red)

cx, cy = W * 0.35, H / 2           
r_outer = H * 0.22                
r_inner = H * 0.18                 

ctx.set_source_rgb(*white)
ctx.arc(cx, cy, r_outer, 0, 2*math.pi)
ctx.fill()

ctx.set_source_rgb(*red)
ctx.arc(cx + H * 0.06, cy, r_inner, 0, 2*math.pi)
ctx.fill()

star_r_outer = H * 0.09
star_r_inner = star_r_outer * 0.4
star_x = cx + H * 0.22
star_y = cy

ctx.set_source_rgb(*white)
ctx.move_to(star_x, star_y - star_r_outer)

for i in range(1, 10):
    angle = -math.pi/2 + i * math.pi/5
    radius = star_r_inner if i % 2 else star_r_outer
    x = star_x + radius * math.cos(angle)
    y = star_y + radius * math.sin(angle)
    ctx.line_to(x, y)

ctx.close_path()
ctx.fill()

save(s, "turkey.png")
quiz.append(["turkey.png", "Which country's flag has a white crescent and a star on red?", "Turkey"])

# ------------ SWITZERLAND ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#FF0000"))

cross_w = W*0.15
cross_h = H*0.15
draw_rectangle(ctx, W/2 - cross_w/2, H*0.25, cross_w, H*0.50, rgb("#FFFFFF"))
draw_rectangle(ctx, W*0.30, H/2 - cross_h/2, W*0.40, cross_h, rgb("#FFFFFF"))
save(s, "switzerland.png")
quiz.append(["switzerland.png", "Which flag is red with a white cross?", "Switzerland"])

# ------------ BRAZIL ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#009C3B"))          

ctx.set_source_rgb(*rgb("#FFDF00"))
ctx.move_to(W/2, H*0.15)
ctx.line_to(W*0.85, H/2)
ctx.line_to(W/2, H*0.85)
ctx.line_to(W*0.15, H/2)
ctx.close_path()
ctx.fill()

draw_circle(ctx, W/2, H/2, H*0.22, rgb("#002776"))
save(s, "brazil.png")
quiz.append(["brazil.png", "Which flag is green with a yellow diamond and blue circle?", "Brazil"])

# ------------ UKRAINE ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H/2, rgb("#0057B7"))
draw_rectangle(ctx, 0, H/2, W, H/2, rgb("#FFD700"))
save(s, "ukraine.png")
quiz.append(["ukraine.png", "Which flag is blue over yellow?", "Ukraine"])


# ------------ RUSSIA ------------
s, ctx = new_canvas()
h = H/3
draw_rectangle(ctx, 0, 0, W, h, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, h, W, h, rgb("#0039A6"))
draw_rectangle(ctx, 0, 2*h, W, h, rgb("#D52B1E"))
save(s, "russia.png")
quiz.append(["russia.png", "Which flag is white-blue-red horizontal stripes?", "Russia"])


# ------------ POLAND ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H/2, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, H/2, W, H/2, rgb("#DC143C"))
save(s, "poland.png")
quiz.append(["poland.png", "Which flag is white over red?", "Poland"])


# ------------ AUSTRIA ------------
s, ctx = new_canvas()
h = H/3
draw_rectangle(ctx, 0, 0, W, h, rgb("#ED2939"))
draw_rectangle(ctx, 0, h, W, h, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, 2*h, W, h, rgb("#ED2939"))
save(s, "austria.png")
quiz.append(["austria.png", "Which flag is red-white-red horizontal stripes?", "Austria"])

# ------------ COLOMBIA ------------
s, ctx = new_canvas()
h = H/4
draw_rectangle(ctx, 0, 0, W, h*2, rgb("#FCD116"))   
draw_rectangle(ctx, 0, h*2, W, h, rgb("#003893"))   
draw_rectangle(ctx, 0, h*3, W, h, rgb("#CE1126"))   
save(s, "colombia.png")
quiz.append(["colombia.png", "Which flag is yellow, blue, red with yellow double height?", "Colombia"])

# ------------ NETHERLANDS ------------
s, ctx = new_canvas()
h = H/3
draw_rectangle(ctx, 0, 0, W, h, rgb("#AE1C28"))
draw_rectangle(ctx, 0, h, W, h, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, 2*h, W, h, rgb("#21468B"))
save(s, "netherlands.png")
quiz.append(["netherlands.png", "Which flag is red-white-blue horizontal stripes?", "Netherlands"])


# ------------ GREECE ------------
s, ctx = new_canvas()
stripe = H / 9

for i in range(9):
    color = "#0D5EAF" if i % 2 == 0 else "#FFFFFF"
    draw_rectangle(ctx, 0, stripe*i, W, stripe, rgb(color))

square = stripe * 5
draw_rectangle(ctx, 0, 0, square, square, rgb("#0D5EAF"))

draw_rectangle(ctx, square/2 - stripe/2, 0, stripe, square, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, square/2 - stripe/2, square, stripe, rgb("#FFFFFF"))
save(s, "greece.png")
quiz.append(["greece.png", "Which flag is blue-white stripes with a white cross?", "Greece"])


# ------------ SWEDEN ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#006AA7"))  

cross_w = W * 0.10
cross_h = H * 0.10
draw_rectangle(ctx, W*0.30, 0, cross_w, H, rgb("#FECC00"))
draw_rectangle(ctx, 0, H*0.45, W, cross_h, rgb("#FECC00"))
save(s, "sweden.png")
quiz.append(["sweden.png", "Which flag is blue with a yellow Scandinavian cross?", "Sweden"])

# ------------ CHINA ------------
s, ctx = new_canvas()

red = rgb("#EE1C25")
yellow = rgb("#FFFF00")
draw_rectangle(ctx, 0, 0, W, H, red)

def draw_star(cx, cy, r, color, rotate=0):
    ctx.set_source_rgb(*color)
    ctx.move_to(
        cx + r * math.cos(-math.pi/2 + rotate),
        cy + r * math.sin(-math.pi/2 + rotate)
    )
    for i in range(1, 10):
        angle = -math.pi/2 + rotate + i * math.pi/5
        radius = r * 0.4 if i % 2 else r
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.fill()

big_r = H * 0.10
draw_star(W * 0.10, H * 0.15, big_r, yellow)

small_r = big_r * 0.45
stars_pos = [
    (W * 0.20, H * 0.05, -0.4),
    (W * 0.24, H * 0.13, -0.1),
    (W * 0.24, H * 0.25,  0.2),
    (W * 0.20, H * 0.33,  0.5)
]

for (x, y, rot) in stars_pos:
    draw_star(x, y, small_r, yellow, rotate=rot)

save(s, "china.png")
quiz.append(["china.png", "Which country's flag has one big star and four small stars?", "China"])


# ------------ VIETNAM ------------
s, ctx = new_canvas()

draw_rectangle(ctx, 0, 0, W, H, rgb("#DA251D"))  

star_color = rgb("#FFFF00")
cx, cy = W/2, H/2
R = H * 0.25     
r = R * 0.4      

ctx.set_source_rgb(*star_color)
ctx.move_to(cx, cy - R)

for i in range(1, 5 * 2):
    angle = -math.pi/2 + i * math.pi/5
    radius = r if i % 2 else R
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    ctx.line_to(x, y)

ctx.close_path()
ctx.fill()

save(s, "vietnam.png")
quiz.append(["vietnam.png", "Which country's flag has a yellow star on a red background?", "Vietnam"])

# ------------ THAILAND ------------
s, ctx = new_canvas()
stripe = H / 6
draw_rectangle(ctx, 0, 0, W, stripe, rgb("#A51931"))
draw_rectangle(ctx, 0, stripe, W, stripe, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, stripe*2, W, stripe*2, rgb("#2D2A4A"))
draw_rectangle(ctx, 0, stripe*4, W, stripe, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, stripe*5, W, stripe, rgb("#A51931"))
save(s, "thailand.png")
quiz.append(["thailand.png", "Which flag has red-white-blue-white-red stripes?", "Thailand"])

# ------------ MALAYSIA ------------
s, ctx = new_canvas()

red = rgb("#CC0000")
white = rgb("#FFFFFF")
blue = rgb("#000066")
yellow = rgb("#FFD700")

stripe_h = H / 14
for i in range(14):
    color = red if i % 2 == 0 else white
    draw_rectangle(ctx, 0, i * stripe_h, W, stripe_h, color)

canton_w = W * 0.45
canton_h = H * 0.5
draw_rectangle(ctx, 0, 0, canton_w, canton_h, blue)

cx, cy = canton_w * 0.45, canton_h * 0.5
r_outer = canton_h * 0.33
r_inner = canton_h * 0.26

ctx.set_source_rgb(*yellow)
ctx.arc(cx, cy, r_outer, 0, 2*math.pi)
ctx.fill()

ctx.set_source_rgb(*blue)
ctx.arc(cx + canton_h * 0.09, cy, r_inner, 0, 2*math.pi)
ctx.fill()

r_star = canton_h * 0.18
cx_star = cx + canton_h * 0.32
cy_star = cy

ctx.set_source_rgb(*yellow)
ctx.move_to(cx_star, cy_star - r_star)

for i in range(1, 28):
    angle = -math.pi/2 + i * math.pi/14
    radius = r_star if i % 2 == 0 else r_star * 0.45
    x = cx_star + radius * math.cos(angle)
    y = cy_star + radius * math.sin(angle)
    ctx.line_to(x, y)

ctx.close_path()
ctx.fill()

save(s, "malaysia.png")
quiz.append(["malaysia.png", "Which country's flag has 14 red-white stripes and a yellow crescent and star?", "Malaysia"])

# ------------ SINGAPORE ------------
s, ctx = new_canvas()

red = rgb("#EF3340")
white = rgb("#FFFFFF")

draw_rectangle(ctx, 0, 0, W, H/2, red)
draw_rectangle(ctx, 0, H/2, W, H/2, white)

cx, cy = W * 0.18, H * 0.25
r_outer = H * 0.12
r_inner = H * 0.10

ctx.set_source_rgb(*white)
ctx.arc(cx, cy, r_outer, 0, 2 * math.pi)
ctx.fill()

ctx.set_source_rgb(*red)
ctx.arc(cx + H * 0.035, cy, r_inner, 0, 2 * math.pi)
ctx.fill()

star_r = H * 0.02
bigR = H * 0.075   

ctx.set_source_rgb(*white)

def draw_star(cx, cy, r):
    ctx.move_to(cx, cy - r)
    for i in range(1, 10):
        angle = -math.pi/2 + i * math.pi/5
        radius = r * 0.4 if i % 2 else r
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        ctx.line_to(x, y)
    ctx.close_path()
    ctx.fill()

for i in range(5):
    angle = -math.pi/2 + i * (2 * math.pi / 5)
    x = cx + bigR * math.cos(angle) + H * 0.02   
    y = cy + bigR * math.sin(angle)
    draw_star(x, y, star_r)

save(s, "singapore.png")
quiz.append(["singapore.png", "Which country's flag has a crescent and five stars?", "Singapore"])

# ------------ ISRAEL ------------
s, ctx = new_canvas()

blue = rgb("#0038B8")
white = rgb("#FFFFFF")

draw_rectangle(ctx, 0, 0, W, H, white)
stripe_height = H * 0.12
draw_rectangle(ctx, 0, 0, W, stripe_height, blue)
draw_rectangle(ctx, 0, H - stripe_height, W, stripe_height, blue)
cx, cy = W / 2, H / 2
radius_outer = H * 0.22
radius_inner = radius_outer * 0.55

ctx.set_source_rgb(*blue)
ctx.set_line_width(H * 0.035)

def draw_triangle(ctx, cx, cy, r, rotation):
    ctx.new_path()
    for i in range(3):
        angle = rotation + i * (2 * math.pi / 3)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.close_path()

draw_triangle(ctx, cx, cy, radius_outer, -math.pi/2)
ctx.stroke()
draw_triangle(ctx, cx, cy, radius_outer, math.pi/2)
ctx.stroke()

save(s, "israel.png")
quiz.append([
    "israel.png",
    "Which country's flag has a blue Star of David?",
    "Israel"
])

#------------ JORDAN ------------
s, ctx = new_canvas()

black = rgb("#000000")
white = rgb("#FFFFFF")
green = rgb("#007A3D")
red = rgb("#CE1126")

draw_rectangle(ctx, 0, 0, W, H/3, black)
draw_rectangle(ctx, 0, H/3, W, H/3, white)
draw_rectangle(ctx, 0, 2*H/3, W, H/3, green)

ctx.set_source_rgb(*red)
ctx.new_path()
ctx.move_to(0, 0)
ctx.line_to(W * 0.33, H / 2)
ctx.line_to(0, H)
ctx.close_path()
ctx.fill()

cx, cy = W * 0.11, H / 2
outer_r = H * 0.055
inner_r = outer_r * 0.45

ctx.set_source_rgb(1, 1, 1)

ctx.new_path()
for i in range(14):
    angle = -math.pi / 2 + i * math.pi / 7
    r = outer_r if i % 2 == 0 else inner_r
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    if i == 0:
        ctx.move_to(x, y)
    else:
        ctx.line_to(x, y)
ctx.close_path()
ctx.fill()

save(s, "jordan.png")
quiz.append([
    "jordan.png",
    "Which country's flag has a red triangle with a white 7-pointed star?",
    "Jordan"
])

#------------ CHILE ------------
s, ctx = new_canvas()

white = rgb("#FFFFFF")
blue = rgb("#0039A6")
red = rgb("#D52B1E")

draw_rectangle(ctx, 0, H/2, W, H/2, red)
draw_rectangle(ctx, W/3, 0, W * (2/3), H/2, white)
draw_rectangle(ctx, 0, 0, W/3, H/2, blue)

cx, cy = W/6, H/4
outer_r = H * 0.07
inner_r = outer_r * 0.45

ctx.set_source_rgb(1, 1, 1)
ctx.new_path()

for i in range(10):
    angle = -math.pi / 2 + i * math.pi / 5
    r = outer_r if i % 2 == 0 else inner_r
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    if i == 0:
        ctx.move_to(x, y)
    else:
        ctx.line_to(x, y)

ctx.close_path()
ctx.fill()

save(s, "chile.png")
quiz.append([
    "chile.png",
    "Which country's flag has a blue canton with a white star and a red bottom half?",
    "Chile"
])

# ------------ BELGIUM ------------
s, ctx = new_canvas()
stripe = W/3
draw_rectangle(ctx, 0, 0, stripe, H, rgb("#000000"))
draw_rectangle(ctx, stripe, 0, stripe, H, rgb("#FFD700"))
draw_rectangle(ctx, 2*stripe, 0, stripe, H, rgb("#D91023"))
save(s, "belgium.png")
quiz.append(["belgium.png", "Which flag is black-yellow-red vertical stripes?", "Belgium"])

# ------------ DENMARK ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#C60C30"))
draw_rectangle(ctx, W*0.30, 0, W*0.10, H, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, H*0.40, W, H*0.10, rgb("#FFFFFF"))
save(s, "denmark.png")
quiz.append(["denmark.png", "Which flag is red with a white Scandinavian cross?", "Denmark"])

# ------------ NORWAY ------------
s, ctx = new_canvas()
draw_rectangle(ctx, 0, 0, W, H, rgb("#BA0C2F"))
draw_rectangle(ctx, W*0.30, 0, W*0.10, H, rgb("#FFFFFF"))
draw_rectangle(ctx, 0, H*0.40, W, H*0.10, rgb("#FFFFFF"))
draw_rectangle(ctx, W*0.32, 0, W*0.06, H, rgb("#00205B"))
draw_rectangle(ctx, 0, H*0.42, W, H*0.06, rgb("#00205B"))
save(s, "norway.png")
quiz.append(["norway.png", "Which flag is red with a blue-white cross?", "Norway"])

# ------------ ROMANIA ------------
s, ctx = new_canvas()
stripe = W/3
draw_rectangle(ctx, 0, 0, stripe, H, rgb("#002B7F"))
draw_rectangle(ctx, stripe, 0, stripe, H, rgb("#FCD116"))
draw_rectangle(ctx, stripe*2, 0, stripe, H, rgb("#CE1126"))
save(s, "romania.png")
quiz.append(["romania.png", "Which flag is blue-yellow-red vertical stripes?", "Romania"])

# ------------ AUSTRALIA ------------
s, ctx = new_canvas()

blue = rgb("#00008B")
white = rgb("#FFFFFF")
red = rgb("#FF0000")

draw_rectangle(ctx, 0, 0, W, H, blue)
ux_w = W * 0.5
ux_h = H * 0.5

draw_rectangle(ctx, 0, 0, ux_w, ux_h, blue)

ctx.set_source_rgb(*white)
ctx.rectangle(0, ux_h/2 - ux_h*0.07, ux_w, ux_h*0.14)
ctx.fill()

ctx.rectangle(ux_w/2 - ux_w*0.07, 0, ux_w*0.14, ux_h)
ctx.fill()

ctx.set_source_rgb(*red)
ctx.rectangle(0, ux_h/2 - ux_h*0.04, ux_w, ux_h*0.08)
ctx.fill()

ctx.rectangle(ux_w/2 - ux_w*0.04, 0, ux_w*0.08, ux_h)
ctx.fill()

ctx.set_source_rgb(*white)
ctx.set_line_width(ux_h * 0.12)
ctx.move_to(0, 0)
ctx.line_to(ux_w, ux_h)
ctx.stroke()

ctx.move_to(0, ux_h)
ctx.line_to(ux_w, 0)
ctx.stroke()

ctx.set_source_rgb(*red)
ctx.set_line_width(ux_h * 0.06)
ctx.move_to(0, 0)
ctx.line_to(ux_w, ux_h)
ctx.stroke()

ctx.move_to(0, ux_h)
ctx.line_to(ux_w, 0)
ctx.stroke()

def draw_star(ctx, cx, cy, r_outer, points, rotation=0, color=white):
    r_inner = r_outer * 0.45
    ctx.set_source_rgb(*color)
    ctx.new_path()
    for i in range(points * 2):
        angle = rotation + i * math.pi / points
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.close_path()
    ctx.fill()

draw_star(ctx, W*0.25, H*0.72, H*0.10, 7)
draw_star(ctx, W*0.75, H*0.25, H*0.04, 7)
draw_star(ctx, W*0.82, H*0.40, H*0.05, 7)
draw_star(ctx, W*0.70, H*0.45, H*0.03, 7)
draw_star(ctx, W*0.80, H*0.60, H*0.04, 7)
draw_star(ctx, W*0.72, H*0.70, H*0.025, 7)

save(s, "australia.png")
quiz.append([
    "australia.png",
    "Which country's flag has the Union Jack and the Southern Cross constellation?",
    "Australia"
])

# -------- SAVE QUIZ --------
with open(os.path.join(OUT_DIR, "quiz.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["file", "question", "answer"])
    w.writerows(quiz)

print("\nAll flags generated! Check folder:", OUT_DIR)