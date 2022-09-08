import sys

ini = sys.argv[1]
ini = ini.split("&")
a = ini[0].split("=")[1]
op = ini[1].split("=")[1]
b = ini[2].split("=")[1]

res = ""
with open("cgi-bin/calculator.html", "r", encoding="utf-8") as f:
    for line in f:
        res += line
res = res.replace("$num1", a)
res = res.replace("$num2", b)
# res = res.replace("$option", op)
if(op == "add"):
    res = res.replace("$option", "+")
    res = res.replace("$ans", str(float(a) + float(b)))
elif(op == "sub"):
    res = res.replace("$option", "-")
    res = res.replace("$ans", str(float(a) - float(b)))
elif(op == "mul"):
    res = res.replace("$option", "*")
    res = res.replace("$ans", str(float(a) * float(b)))
else:
    res = res.replace("$option", "/")
    res = res.replace("$ans", str(float(a) / float(b)))

res = res.replace("$hostname", sys.argv[2])
res = res.replace("$port", sys.argv[3])
print(res)