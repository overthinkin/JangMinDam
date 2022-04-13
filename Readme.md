# 허프만 코드 알고리즘

------

팀: Team C

팀원: 정민성, 백도담, 장진이

------

- 파일에 빈번하게 나타나는 문자에는 짧은 이진코드를 할당하고, 

  드물게 나타나는 문자에는 긴 이진코드를 할당하는 파일 압축 방법

- 허프만 압축 방법으로 변환시킨 문자 코드들 사이에는 접두부 특성이 존재
  - 접두부 특성이란, 각 문자에 할당된 이진코드는 어떤 다른 문자에 할당된 이진 코드의 접두부가 되지 않는 것
  - 접두부 특성 장점: 코드와 코드 사이를 구분할 특별한 코드가 필요 없음

#### 허프만코딩 알고리즘의 시간복잡도

- O(nlogn)

------

## 코드 분석 목차

#### 1) 허프만 코드와 노드의 구조

#### 2) 허프만 인코딩에 필요한 함수

​	make_frequncy_dict, make_heap, make_codes_helper, make_codes, get_encoded_text

#### 3) .bin 파일에 넣기 위한 노력

​	padding_encode, get_byte_arr, compress, remove_padding

#### 4) .bin파일을 해독(decoding)하는데에 필요한 함수

​	decode_text, decompress

#### 5) 실제 txt 파일을 압축한 결과

------



## 1) 허프만 코드와 노드의 구조

```python
import heapq

class HuffmanCoding:
    def __init__(self, path):
        self.heap = []
        self.codes = {}
        self.path = path

    class HeapNode:
        def __init__(self, char, freq): # char: 문자 , freq: 빈도수
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq
        # 다른 빈도수가 더 크면 true, 작으면 false 리턴

        def __eq__(self, other):
            if other == None:
                return False
            if not instance(other, HeapNode):
                return False
            return self.freq == ohter.freq
```

codes는 각 문자의 이진코드를 담는 dictionary입니다

heap에 들어갈 노드는 문자와 빈도수를 가지고 있고 디폴트 값으로 왼쪽, 오른쪽은 비어있게 됩니다.

_ _ lt _ _ 함수와 _ _ eq _ _ 함수는 어떤 노드가 작거나 같은지 빈도수를 기준으로 비교하게끔 재정의 하는 함수입니다.





------

## 2) 허프만 인코딩에 필요한 함수

### 	(1) make_frequency_dict(self, text)

```python
def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency
```

문자의 빈도수를 저장할 딕셔너리를 만드는 함수입니다.
text 문자열을 하나씩 순회하며
frequency 배열에 문자가 존재하면 각 문자에 대한 빈도수를 증가시킵니다.



### 	(2) make_heap(self, frequency)

```python
def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
```

heap에 노드를 넣는 함수입니다.
heapq모듈을 사용하여 문자열 발생 빈도수가 적은 순으로 heap에 node가 삽입됩니다(최소힙).



### 	(3) marge_nodes(self)

```python
def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)
```

![](https://user-images.githubusercontent.com/80513292/163229152-69775756-3c90-42d5-b4c0-0f47b4f7b5f1.jpg)

2번부터 6번에 해당하는 코드로

가장 작은 빈도수를 가지고있는 노드를 heap에서부터 추출하여 새로운 노드를 만드는 함수입니다.

이 때, 새로운 노드는 문자는 갖지 않으며 두 노드의 빈도수를 합한 빈도수를 가지고 있게됩니다.

왼쪽에 오른쪽보다 더 낮은 빈도수의 노드가 연결됩니다.

합한 노드를 다시 heap에 넣어주면서 이진 트리를 완성하게 됩니다.



### 	(4) make_codes_helper(self, root, current_code)

```python
def make_codes_helper(self, root, current_code):
        if root == None:
            return
        if root.char != None:
            self.codes[root.char] = current_code
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")
```

![](https://user-images.githubusercontent.com/80513292/163229010-2b3ac36c-6c79-4b64-8816-474175f3952b.png)

codes라는 딕셔너리에 key값은 문자 value값은 코드 형식으로 넣어주는 코드입니다.

ex) {'t':'0000', 'e':'0001', ... , 'i' : '111'}

왼쪽으로 타고 내려갈 때는 0, 오른쪽으로 타고 내려갈 때는 1을 current_code에 추가해주는 방식입니다.



### 	(5) make_codes(self)

```python
def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
        print(self.codes)
        heapq.heappush(self.heap, root)
```

위에 설명했던 make_codes_helper를 호출하는 함수입니다.

heap에 들어있는 root 노드와 빈문자열을 처음에 매개변수로 넘겨줍니다.

잘 들어갔는지 확인하기 위해 codes 딕셔너리를 출력해보았고, 후에 디코딩할 때 root노드가 또 필요하기 때문에

한 번더 넣어주는 코드를 추가하였습니다.



### 	(6) get_encoded_text(self, text)

```python
def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text
```

변환하고 싶은 text를 codes딕셔너리를 참조해 허프만 코드로 바꿔주는 코드입니다.

ex) "Hello" -> "0001111110"





------

## 3)  .bin 파일에 넣기 위한 노력

문자열로 저장된 0과 1의 허프만 코드를 bin 파일에 현실적으로 압축하려면 

패딩과 패딩인포를 추가하여 바이트를 비트로 바꿔줘야 합니다.



### 	(1) padding_encode(self, encoded_text)

```python
	def padding_encode(self, encoded_text): 
        extra_padding = 8 - len(encoded_text) % 8 
        for i in range(extra_padding):      
            encoded_text += "0"            

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text  

```

encoded_text: 문자열 '0'과 '1'로 허프만 코딩된 전체 텍스트

허프만 텍스트의 길이를 8로 나눴을 때 8의 배수가 아니면 

맨 뒤에 0을 추가하여 바이트를 정확히 맞춥니다.

padded_info: 뒤에 추가한 0의 개수가 몇개인지 8비트로 표현해줍니다.

패딩 정보를 허프만 코드에 추가합니다.



### 	(2) get_byte_arr(self, padded_encod)

```python
    def get_byte_arr(self, padded_encod): 
        if(len(padded_encod) % 8 != 0): #코드가 8의 배수가 아니면
            print("Encoded text not padded properly")  #에러 문구 출력하고 함수 종료
            exit(0)

        b = bytearray() 
        for i in range(0, len(padded_encod), 8):
            byte = padded_encod[i:i+8] 
            b.append(int(byte, 2))
        return b 
```

byte_array: 1바이트 단위의 값을 연속적으로 저장하는 자료형

byte_array로 저장하기 위해 padding_encode 함수를 통해 패딩을 추가했습니다. (정확하게 떨어지기 위해)

bytearray 생성해서 8자리씩 끊어낸 내용을 byte array인 b에 저장합니다.



### 	(3) compress(self)

```python
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
```

파일을 읽어와 앞서 설명했던 빈도수를 얻고, 그에 따른 heap을 만들고, 노드를 합치고, 각 문자에 맞는 허프만 코드를 만들고, 인코딩하고 싶은 text를 인코딩하는 함수를 호출하는 함수입니다.

인코딩 된 텍스트에 extra padding을 넣기 위해 함수를 실행하고 binary 파일로 압축시켜줍니다.



### 	(4) remove_padding(self, padded_encoded_text)

```python
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text
```

패딩과 패딩인포를 추가하여 만든 bin 파일을 문자열로 돌려야 합니다

remove_padding 함수의 코드 순서는 다음과 같습니다

패딩인포 읽기 >> 패딩 제거하기 >> 'encoded_text'에 뒤에 붙어 있던 패딩을 제거한 코드를 저장하기





------

## 4) .bin파일을 해독(decoding)하는데에 필요한 함수

### 	(1) decode_text(self, code)

```python
def decode_text(self, code):
        root = heapq.heappop(self.heap)
        tmp = root
        original = ""
        for i in range(len(code)):
            if code[i] == "0":
                if root.left == None:
                    original += root.char
                    root = tmp.left
                else:
                    root = root.left
            if code[i] == "1":
                if root.right == None:
                    original += root.char
                    root = tmp.right
                else:
                    root = root.right
        original += root.char

        return original
```

![](https://user-images.githubusercontent.com/80513292/163229253-7bf62e7c-0d33-488a-85d2-f95c80188a1c.png)

![](https://user-images.githubusercontent.com/80513292/163229256-31dc903a-8f8d-4a90-9efe-ad195aabdd58.png)

허프만 코드는 중복되는 prefix를 갖지 않기 때문에 순차적으로 읽으면서 해당 문자열을 찾을 수 있습니다.

0일 때는 왼쪽, 1일 때는 오른쪽으로 가며 문자를 찾다가 더이상 연결된 노드가 없으면 해당 문자를 가져옵니다.

ex) 0다음에 0이 오는데 a에 왼쪽에 연결된 노드가 없음 -> a를 가져옴

​      1다음에 0이 있어 왼쪽으로 가고 또 0이 있어 왼쪽으로 가고 그다음에 또 0이 있어서 왼쪽으로 가야하는데

​       b에는 왼쪽에 연결된 노드가 없음 -> b를 가져옴



### 	(2) decompress(self, input_path)

```python
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
```

bin파일을 불러와 다시 string 형식으로 바꾸고 extra padding을 없애고 decode_text 함수를 실행시켜 원 파일로 압축해제하는 함수입니다.





------

## 5) 실제 txt 파일을 압축한 결과

txt 파일 자료 출처: [aeon)'Why evolution is not a tree of life but a fuzzy network'](https://aeon.co/essays/why-evolution-is-not-a-tree-of-life-but-a-fuzzy-network)

![원본파일](https://user-images.githubusercontent.com/80513292/163229469-14e362a3-7bbc-4d44-ab36-10a38b858d85.png)

UTF-8로 작성된 원본 파일의 용량은 22.2KB (22,779 바이트)

![실행화면](https://user-images.githubusercontent.com/80513292/163229473-86c2f787-2b6f-4359-adf7-a32042065445.png)

실행 후 허프만 코드가 저장된 위치에 가면 압축된 파일과 압축해제된 파일이 새로 생긴다

![3](https://user-images.githubusercontent.com/80513292/163229477-2837327f-746c-4464-90da-ed502eb9777d.png)

압축된 bin 파일의 용량은 12.2KB (12,559 바이트)

![](https://user-images.githubusercontent.com/80513292/163229479-5a443a68-5093-4b2d-81e1-49e63c8a6caf.png)

압축 해제된 파일과 원본 파일의 내용을 직접 비교했을 때도 특수문자나 엔터까지 잘 디코딩 된 것을 확인할 수 있습니다.

![](https://user-images.githubusercontent.com/80513292/163230119-c306d18a-a424-41db-a080-b7476a7d03d5.png)









