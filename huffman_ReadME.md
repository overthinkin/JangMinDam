### marge_nodes(self)

```
def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

```

![](C:\Users\민됴이\Desktop\huf.jpg)

2번부터 6번에 해당하는 코드로

가장 작은 빈도수를 가지고있는 노드를 heap에서부터 추출하여 새로운 노드를 만드는 함수입니다.

이 때, 새로운 노드는 문자는 갖지 않으며 두 노드의 빈도수를 합한 빈도수를 가지고 있게됩니다.

왼쪽에 오른쪽보다 더 낮은 빈도수의 노드가 연결됩니다.

합한 노드를 다시 heap에 넣어주면서 이진 트리를 완성하게 됩니다.



### make_codes_helper(self, root, current_code)

```
def make_codes_helper(self, root, current_code):
        if root == None:
            return
        if root.char != None:
            self.codes[root.char] = current_code
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

```

![](C:\Users\민됴이\Desktop\jj.png)

codes라는 딕셔너리에 key값은 문자 value값은 코드 형식으로 넣어주는 코드입니다.

ex) {'t':'0000', 'e':'0001', ... , 'i' : '111'}

왼쪽으로 타고 내려갈 때는 0, 오른쪽으로 타고 내려갈 때는 1을 current_code에 추가해주는 방식입니다.

### make_codes(self)

```
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

### get_encoded_text(self, text)

```
def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

```

변환하고 싶은 text를 codes딕셔너리를 참조해 허프만 코드로 바꿔주는 코드입니다.

ex) "Hello" -> "0001111110"

### compress(self, text)

```
def compress(self, text):
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)

        return encoded_text

```

위에 설명했던 빈도수를 얻고, 그에 따른 heap을 만들고, 노드를 합치고, 각 문자에 맞는 허프만 코드를 만들고, 인코딩하고 싶은 text를 인코딩하는 함수를 호출하는 함수입니다.

### decompress(self, code)

```
def decompress(self, code):
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

![](C:\Users\민됴이\Desktop\R.png)

![](C:\Users\민됴이\Desktop\R (1).png)

허프만 코드는 중복되는 prefix를 갖지 않기 때문에 순차적으로 읽으면서 해당 문자열을 찾을 수 있습니다.

0일 때는 왼쪽, 1일 때는 오른쪽으로 가며 문자를 찾다가 더이상 연결된 노드가 없으면 해당 문자를 가져옵니다.

ex) 0다음에 0이 오는데 a에 왼쪽에 연결된 노드가 없음 -> a를 가져옴

​      1다음에 0이 있어 왼쪽으로 가고 또 0이 있어 왼쪽으로 가고 그다음에 또 0이 있어서 왼쪽으로 가야하는데

​       b에는 왼쪽에 연결된 노드가 없음 -> b를 가져옴