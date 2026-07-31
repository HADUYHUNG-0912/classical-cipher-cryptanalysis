"""CLI menu chính — chọn hệ mật mã để phá."""
from caesar.attack import break_caesar
from vigenere.attack import break_vigenere
from playfair.attack import break_playfair


def main():
    print("=== Cryptanalysis Toolkit ===")
    print("1. Caesar cipher")
    print("2. Vigenère cipher")
    print("3. Playfair cipher")
    choice = input("Chọn hệ mật mã cần phá (1-3): ")

    ciphertext = input("Nhập ciphertext: ")

    if choice == "1":
        plaintext, key = break_caesar(ciphertext)
    elif choice == "2":
        plaintext, key = break_vigenere(ciphertext)
    elif choice == "3":
        plaintext, key = break_playfair(ciphertext)
    else:
        print("Lựa chọn không hợp lệ.")
        return

    print(f"\nKhóa tìm được: {key}")
    print(f"Plaintext: {plaintext}")


if __name__ == "__main__":
    main()
