from pprint import pprint
from prettytable import PrettyTable

def euklid(a, b):
    result = {}
    if a < b:
        a, b = b, a
    step = 1
    while b != 0:
        result[step] = {
            'a': a,
            'b': b,
            'q': a // b,
            'r': a % b,
        }
        tmp = b
        b = a % b
        a = tmp
        step += 1
    result["result"] = a
    return result


def extended_euklid(a, b):
    result = euklid(a, b)
    step = len(result.keys()) - 1

    x, y = 0, 1
    while step > 0:
        result[step].update({"x": x, "y": y})
        if step == 1:
            break
        x = y
        y = result[step]["x"] - result[step - 1]["q"] * y
        step -= 1


    result["result"] = result["result"], x, y
    return result

def main():
    a, b = 23, 17

    result = euklid(a, b)
    table = PrettyTable(["i", "a", "b", "q", "r"])
    for i, value in result.items():
        if i == "result":
            continue
        table.add_row([i, *value.values()])
    print(table)
    print(f"ggt{a, b} = {result['result']}")


    result_extended = extended_euklid(a, b)
    table = PrettyTable(["i", "a", "b", "q", "r", "x", "y"])
    for i, value in result_extended.items():
        if isinstance(i, int):
            x_val = value.get('x', '')
            y_val = value.get('y', '')
            table.add_row([i, value['a'], value['b'], value['q'], value['r'], x_val, y_val])

    print("--- Erweiterter Euklidischer Algorithmus ---")
    print(table)

    ggt, x, y = result_extended['result']
    print(f"ggt({a}, {b}) = {ggt}")
    print(f"{ggt} = {a} * {x} + {b} * {y}")

if __name__ == '__main__':
    main()
