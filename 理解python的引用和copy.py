b = {"a":"b"}
end = []
for i in range(10):
    a = b
    a["num"] = i
    end.append(a)
print(end)
print("------------------------")
end = []
for i in range(10):
    a = b.copy()
    a["num"] = i
    end.append(a)
print(end)