def caesar_cipher(text, shift):
    result = ""
    for char in text:
        new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        result += new_char
    return "加密后的字符串:" + result

def main():
    while True:
        text = input("输入一个字符串（只能是大写字母）:")
        if text.isupper() and text:
            break
        else:
            print("输入无效，请重新输入。")
        
    while True:
        try:
            shift = int(input("请输入1-26的整数作为偏移量:"))
            if 1 <= shift <= 26:
                break
            else:
                print("输入无效，请输入1-26的整数。")
        except ValueError:
            print("输入无效，请重新输入。")

    encrypted_text = caesar_cipher(text, shift)
    print("Encrypted string:", encrypted_text)

if __name__ == '__main__':
    main()
