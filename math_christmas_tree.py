def christmas_tree(x: int = 7) -> str:
    output = ""
    liste = [str(x)]
    blueprints = ["√({})"]

    for i in range(5):
        liste.append(blueprints[-1].format(x**2))
        liste.append(blueprints[-1].format(f"1+{x ** 2 - 1}"))
        liste.append(blueprints[-1].format(f"1+{x - 1}*{(x ** 2 - 1) // (x - 1)}"))
        blueprints.append(blueprints[-1].format(f"1+{x - 1}*" + "√({})"))
        x += 1


    for i in liste:
        output += " "*((len(blueprints[-1]) - len(i)) // 2) + i + " " + "\n"

    last_len = len(blueprints[-1])
    for i in range(3):
        output += " "*(last_len//2 - 3) + "|" + " "*4 + "|" + " "*(last_len//2 - 3) + "\n"
    return output


def main():
    print(christmas_tree())

if __name__ == "__main__":
    main()
