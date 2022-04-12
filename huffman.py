from ctypes import sizeof
import heapq
import os

class HuffmanCoding:
    def __init__(self, path):
        self.heap = []
        self.codes = {}
        self.path = path



    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other == None:
                return False
            if not instance(other, HeapNode):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root == None:
            return
        if root.char != None:
            self.codes[root.char] = current_code
            return

        self.make_codes_helper(root.left, current_code + '0')
        self.make_codes_helper(root.right, current_code + '1')

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
        print(self.codes)
        heapq.heappush(self.heap, root)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text
#문자열로 저장된 0과 1의 허프만 코드를 
# bin 파일에 현실적으로 압축하려면 
#패딩과 패딩인포를 추가하여 바이트를 비트로 바꿔야한다

    def padding_encode(self, encoded_text): #encoded_text: 문자열 '0'과 '1'로 허프만코딩된 전체 텍스트
        extra_padding = 8 - len(encoded_text) % 8 #허프만 텍스트의 길이를 
        for i in range(extra_padding):     #8로 나눴을 때 8의 배수가 아니면 맨뒤에 
            encoded_text += "0"            #0을 추가하여 바이트를 정확히 맞춘다

        padded_info = "{0:08b}".format(extra_padding) #패딩인포: 뒤에 추가한 0의 개수가 몇개인지 8비트로 표현한다
        encoded_text = padded_info + encoded_text #패딩 정보를 허프만 코드에 추가한다
        return encoded_text  

    def get_byte_arr(self, padded_encod): #byte_array: 1바이트 단위의 값을 연속적으로 저장하는 자료형
        if(len(padded_encod) % 8 != 0): #byte_array로 저장하기 위해 패딩을 추가했음-정확하게 떨어지기 위해
            print("Encoded text not padded properly") #허프만 코드가 8의 배수가 아니면 bytearray에 넣을 수 없으므로 오류 출력
            exit(0)

        b = bytearray() #bytearray 생성
        for i in range(0, len(padded_encod), 8):
            byte = padded_encod[i:i+8] #8자리씩 끊어서 배열에 저장
            b.append(int(byte, 2))
        return b #byte array를 내보냄
        
    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin" #binary 파일로 저장하기 위해 확장자 추가 

        file = open(self.path,'r',encoding='utf-8')
        output = open(output_path, 'wb')
        text = file.read()
        text = text.rstrip()
        #허프만 압축 함수 실행
        frequency = self.make_frequency_dict(text) 
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.padding_encode(encoded_text)

        b = self.get_byte_arr(padded_encoded_text)
        output.write(bytes(b))
    
        file.close()
        output.close()
    
        print("압축 완료")
        return output_path #저장위치
    
    #패딩,패딩인포를 추가하여 만든 bin 파일을 문자열로 돌려야함
    #1. 패딩인포 읽기 >> 2. 패딩 제거하기 >> 3. 0과 1을 하나씩 새로운 파일에 저장하기

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, code): #char인 상태로 돌려서 해독하기
        root = heapq.heappop(self.heap)
        tmp = root
        original = ""
        for i in range(len(str(code))):
            if code[i] == '0':
                if root.left == None:
                    original += root.char
                    root = tmp.left
                else:
                    root = root.left
            if code[i] == '1':
                if root.right == None:
                    original += root.char
                    root = tmp.right
                else:
                    root = root.right
        original += root.char
        return original
    
    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w',encoding='utf-8') as output:
            bit_string = ""

            byte = file.read(1)
            while(byte != b''):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
                

            encoded_text = self.remove_padding(bit_string)
            
            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

            print("Decompressed")
        return output_path
