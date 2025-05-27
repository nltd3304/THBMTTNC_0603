class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I") # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set
        ]
        matrix = list(key)

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
        
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        encrypted_text = ""

        # Xử lý văn bản để đảm bảo cặp ký tự hợp lệ
        processed_plain_text = ""
        i = 0
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 < len(plain_text):
                char2 = plain_text[i+1]
                if char1 == char2:
                    processed_plain_text += char1 + "X"
                    i += 1
                else:
                    processed_plain_text += char1 + char2
                    i += 2
            else:
                processed_plain_text += char1 + "X" # Nếu số lượng ký tự lẻ, thêm 'X'
                i += 1
        
        # Nếu sau khi xử lý vẫn còn lẻ, thêm 'X' cuối cùng
        if len(processed_plain_text) % 2 != 0:
            processed_plain_text += "X"

        for i in range(0, len(processed_plain_text), 2):
            pair = processed_plain_text[i:i+2]
            
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        banro = ""
        # Loại bỏ ký tự 'X' nếu nó là ký tự cuối cùng và là ký tự được thêm vào
        for i in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + "" + decrypted_text[i+1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2]
            banro += decrypted_text[-1]
        return banro