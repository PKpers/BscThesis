a = { "f" : 4, "rad" : [5, 3]}
keys = a.keys()

if "r" in keys or 'rad' in keys:
    b = a.get("r")
    if not b:
        b = a.get("rad")
    #
#
print(b)
if "f" in keys:
    print("ok")
#
def test(a, **kwargs):
    if not kwargs:
        print('ok')
        return
   # 
    print('kwargs')
    return
#
'''
a, b, c, d = [None for i in range(4)]
for i in range(10):
    if i == 0 :
        a = 3
    elif i == 2 or i == 3:
        b = 4
    print(a, b ,c, d)
'''    
test(3, n=None)
