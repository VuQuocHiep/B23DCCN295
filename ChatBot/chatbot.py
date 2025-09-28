import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Text, Button
import threading
import time
import json
import os
import unicodedata
import difflib

DATA_FILE = "answers.json"

default_answers = {
    "đơn đồ thị vô hướng": "Đơn đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là các cạnh.",
    "đa đồ thị vô hướng": "Đa đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là tập các cạnh. e1 ∈ E, e2 ∈ E được gọi là cạnh bội nếu chúng cùng tương ứng với một cặp đỉnh.",
    "giả đồ thị vô hướng": "Giả đồ thị vô hướng G=<V,E> bao gồm V là tập đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử (hai phần tử không nhất thiết phải khác nhau) trong V được gọi là các cạnh. Cạnh e được gọi là khuyên nếu có dạng e = (u,u).",
    "đơn đồ thị có hướng": "Đơn đồ thị có hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp có thứ tự gồm hai phần tử của V gọi là các cung.",
    "đa đồ thị có hướng": "Đa đồ thị có hướng G=<V,E> bao gồm V là tập đỉnh, E là họ các cặp có thứ tự gồm hai phần tử khác nhau của V được gọi là các cung. Hai cung e1, e2 tương ứng với cùng một cặp đỉnh được gọi là cung lặp.",
    "đồ thị vô hướng": "Đơn đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là tập các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là các cạnh.",
    "đồ thị có hướng": "Đa đồ thị vô hướng G=<V,E> bao gồm V là tập các đỉnh, E là họ các cặp không có thứ tự gồm hai phần tử khác nhau của V gọi là tập các cạnh. e1 ∈ E, e2 ∈ E được gọi là cạnh bội nếu chúng cùng tương ứng với một cặp đỉnh.",
    "Bậc của đỉnh": "VHai đỉnh 𝑢 và 𝑣 của đồ thị vô hướng 𝐺 = <𝑉,𝐸 > được gọi là kề nhau nếu (𝑢,𝑣)là cạnh thuộc đồ thị 𝐺. Nếu 𝑒 = (𝑢,𝑣)là cạnh của đồ thị 𝐺 thì ta nói cạnh này liên thuộc với hai đỉnh 𝑢 và 𝑣, hoặc ta nói cạnh 𝑒 nối đỉnh 𝑢 với đỉnh 𝑣, đồng thời các đỉnh 𝑢 và 𝑣 sẽ được gọi là đỉnh đầu của cạnh (𝑢,𝑣).",
    "Định lý về tổng bậc các đỉnh": "Giả sử 𝐺 =< 𝑉,𝐸 > là đồ thị vô hướng với 𝑚cạnh, khi đó: Tổng deg𝑣 =2𝑚.",
    "Đường đi": " Đường đi độ dài 𝑛 từ đỉnh 𝑢 đến đỉnh 𝑣 trên đồ thị vô hướng 𝐺 =< 𝑉,𝐸 >là dãy x0, 𝑥1,.. . , 𝑥𝑛−1,𝑥𝑛, trong đó 𝑛 là số nguyên dương, 𝑥0 = 𝑢, 𝑥𝑛 = 𝑣,(𝑥𝑖,𝑥𝑖+1) ∈ 𝐸, 𝑖 = 0,1,2,...,𝑛 − 1.",
    "chu trình": " Đường đi có đỉnh đầu trùng với đỉnh cuối (𝑢 = 𝑣) ",
    "Liên thông": "Đồ thị vô hướng được gọi là liên thông  nếu luôn tìm được đường đi giữa hai đỉnh bất kỳ của nó",
    "Cạnh Cầu": " Cạnh 𝑒 ∈ 𝐸 được gọi là cầu nếu loại bỏ e làm tăng thành phần liên thông của đồ thị. Đỉnh 𝑢 ∈ 𝑉 được gọi là đỉnh trụ nếu loại bỏ 𝑢 cùng với các cạnh nối với 𝑢 làm tăng thành phần liên thông của đồ thị.",
    "Đỉnh trụ": " Là đỉnh trụ nếu loại bỏ 𝑢 cùng với các cạnh nối với 𝑢 làm tăng thành phần liên thông của đồ thị.",
    "Bán bậc của đỉnh": "Nếu 𝑒 =(𝑢,𝑣) là cung của đồ thị có hướng 𝐺 thì ta nói hai đỉnh 𝑢 và 𝑣 là kề nhau, và nói cung (𝑢,𝑣) nối đỉnh 𝑢 với đỉnh 𝑣, hoặc nói cung này đi ra khỏi đỉnh 𝑢 và đi vào đỉnh 𝑣. Đỉnh 𝑢 được gọi là đỉnh đầu, đỉnh 𝑣 được gọi là đỉnh cuối của cung (𝑢,𝑣).",
    " bán bậc ra": "Số cung của đồ thị đi ra khỏi 𝑣 và ký hiệu là 𝑑𝑒𝑔+(𝑣).",
    " bán bậc vào ": "là số cung của đồ thị đi vào 𝑣 và ký hiệu là 𝑑𝑒𝑔−(𝑣).",
    "liên thông mạnh": " nếu giữa hai đỉnh bất kỳ 𝑢 ∈ 𝑉,𝑣 ∈ 𝑉 đều  có đường đi từ 𝑢 đến 𝑣. ",
    "liên thông yếu": "nếu đồ thị vô hướng tương ứng với nó là liên thông.",
    "Định chiều được": " nếu ta có thể biến đổi các cạnh trong 𝐺 thành các cung tương ứng để nhận được một đồ thị có hướng liên thông mạnh. ",
    " Đồ thị đầy đủ": " 𝑛 đỉnh, ký hiệu là 𝐾𝑛, là đơn đồ thị vô  hướng mà giữa hai đỉnh bất kỳ của nó đều có cạnh nối",
    "Đồ thị vòng": "𝑛 đỉnh, ký hiệu là 𝐶𝑛 (𝑛 ≥ 3) là đơn đồ thị  vô hướng gồm các cạnh (1,2),(2,3),…,(𝑛 − 1,𝑛),(𝑛,1)",
    " Đồ thị bánh xe": "𝑛 đỉnh, ký hiệu là 𝑊𝑛 là đồ thị thu được bằng cách bổ sung một đỉnh nối với tất cả các đỉnh của đồ thị vòng 𝐶𝑛−1.",
    "Đồ thị hai phía": "tập đỉnh 𝑉 của nó có thể phân hoạch thành hai tập 𝑋 và 𝑌 sao cho mỗi cạnh của đồ thị chỉ có dạng (𝑥,𝑦), trong đó x ∈ 𝑋 và 𝑦 ∈ 𝑌.",
    "Ma trận kề của đồ thị vô hướng": " ma trận 𝑛 × 𝑛 có các phần tử hoặc bằng 0 hoặc bằng 1 theo qui định như sau: 𝐴={𝑎𝑖𝑗:𝑎𝑖𝑗 = 1 𝑛ế𝑢 (𝑖,𝑗) ∈ 𝐸,𝑎𝑖𝑗 = 0 𝑛ế𝑢 (𝑖,𝑗) ∉ 𝐸; 𝑖,𝑗 = 1, 2,. . . , 𝑛}.",
    "Ma trận trọng số ": "Mỗi cạnh 𝑒 = (𝑢,𝑣) của đồ thị được gán bởi một số (𝑒) = 𝑐(𝑢,𝑣) gọi là trọng số của cạnh 𝑒 Đồ thị trong trường hợp như vậy gọi là đồ thị trọng số  Ma trận trọng số 𝑐 = 𝑐[𝑖,𝑗], 𝑐[𝑖,𝑗] = 𝑐(𝑖,𝑗) nếu (𝑖,𝑗) ∈ 𝐸, �[𝑖, 𝑗] = 𝜃 nếu (𝑖,𝑗) ∉ 𝐸. 𝜃 nhận các giá trị: 0,∞,−∞ tuỳ theo từng tình huống cụ thể của thuật toán ",
    "Ma trận liên thuộc Đồ thị vô hướng": "Xét đồ thị vô hướng 𝐺 = (𝑉,𝐸),𝑉 = {1,2,…,𝑛}, 𝐸 ={𝑒1, 𝑒2, …,𝑒𝑚}. Ma trận liên thuộc đỉnh-cạnh của 𝐺 là ma trận kích thước 𝑛 ×𝑚 được xây dựng như sau: a𝑖𝑗 = 1, nế𝑢 đỉ𝑛ℎ 𝑖 𝑙𝑖ê𝑛 𝑡ℎ𝑢ộ𝑐 𝑣ớ𝑖 𝑐ạ𝑛ℎ 𝑗 0, 𝑛ế𝑢 đỉ𝑛ℎ 𝑖 𝑘ℎô𝑛𝑔 𝑙𝑖ê𝑛 𝑡ℎ𝑢ộ𝑐 𝑣ớ𝑖 𝑐ạ𝑛ℎ 𝑗",
    "Ma trận liên thuộc Đồ thị có hướng": "Xét đồ thị có hướng 𝐺 = (𝑉,𝐸),𝑉 = {1,2,…,𝑛}, 𝐸 = {𝑒1, 𝑒2, …,𝑒𝑚}. Ma trận liên thuộc đỉnh-cung của 𝐺 là ma rận kích thước 𝑛 ×𝑚 được xây dựng như sau: 1, 𝑛ế𝑢 𝑖 𝑙à đỉ𝑛ℎ đầ𝑢 𝑐ủ𝑎 𝑐𝑢𝑛𝑔 𝑒𝑗  −1,𝑛ế𝑢 𝑖 𝑙à đỉ𝑛ℎ 𝑐𝑢ố𝑖 𝑐ủ𝑎 𝑐𝑢𝑛𝑔 𝑒𝑗 0, 𝑛ế𝑢 𝑖 𝑘ℎô𝑛𝑔 𝑙à đầ𝑢 𝑚ú𝑡 𝑐ủ𝑎 𝑐𝑢𝑛𝑔 𝑒�",
    "Ưu và nhược điểm của danh sách kề ": "Ưu điểm o Dễ dàng duyệt tất cả các đỉnh của một danh sách kề Dễ dàng duyệt các cạnh của đồ thị trong mỗi danh sách kề Tối ưu về phương pháp biểu diễn Nhược điểm Khó khăn cho người đọc có kỹ năng lập trình yếu ",
    "Ưu và nhược điểm của danh sách cạnh": "Ưu điểm o Trong trường hợp đồ thị thưa (𝑚 < 6𝑛), biểu diễn bằng danh sách cạnh tiết kiệm được không gian nhớ o Thuận lợi cho một số thuật toán chỉ quan tâm đến các cạnh của đồ thị Nhược điểm  Khi cần duyệt các đỉnh kề với đỉnh 𝑢 bắt buộc phải duyệt tất cả các cạnh của đồ thị Điều này làm cho thuật toán có chi phí tính toán cao",
    "Thuật toán DFS": "DFS(u):\n"
                      "  Bước 1: Khởi tạo\n"
                      "    stack = ∅\n"
                      "    push(stack, u)\n"
                      "    <Thăm đỉnh u>\n"
                      "    chuaXet[u] = false\n"
                      "\n"
                      "  Bước 2: Lặp\n"
                      "    while stack ≠ ∅:\n"
                      "      s = pop(stack)\n"
                      "      for t ∈ Ke(s):\n"
                      "        if chuaXet[t]:\n"
                      "          <Thăm đỉnh t>\n"
                      "          chuaXet[t] = false\n"
                      "          push(stack, s)\n"
                      "          push(stack, t)\n"
                      "          break\n"
                      "\n"
                      "  Bước 3: Trả lại kết quả\n"
                      "    return <tập đỉnh đã duyệt>",
    "Độ phức tạp thuật toán DFS": """Biểu diễn đồ thị bằng ma trận kề:
                                  - Độ phức tạp: O(n^2), với n là số đỉnh.
                                Biểu diễn đồ thị bằng danh sách cạnh:
                                  - Độ phức tạp: O(n * m), với n là số đỉnh, m là số cạnh.
                                Biểu diễn đồ thị bằng danh sách kề:
                                  - Độ phức tạp: O(max(n, m)), với n là số đỉnh, m là số cạnh.""",
    "Thuật toán BFS": """BFS(u):
                        Bước 1: Khởi tạo
                          queue = ∅
                          push(queue, u)
                          chuaXet[u] = false
                        Bước 2: Lặp
                          while queue ≠ ∅:
                            s = pop(queue)
                            <Thăm đỉnh s>
                            for t ∈ Ke(s):
                              if chuaXet[t]:
                                push(queue, t)
                                chuaXet[t] = false
                        Bước 3: Trả lại kết quả
                          return <tập đỉnh đã duyệt>""",
    "Độ phức tạp thuật toán BFS": """Biểu diễn bằng ma trận kề:
      Độ phức tạp O(n^2), với n là số đỉnh.
    Biểu diễn bằng danh sách cạnh:
      Độ phức tạp O(n.m), với n là số đỉnh, m là số cạnh.
    Biểu diễn bằng danh sách kề:
      Độ phức tạp O(max(n, m)), với n là số đỉnh, m là số cạnh.""",
    "Thuật toán duyệt thành phần liên thông ": """Duyet-TPLT() {
    Bước 1: Khởi tạo
      soTPLT = 0   // số thành phần liên thông
    Bước 2: Lặp
      for u ∈ V:        // duyệt tất cả các đỉnh
        if chuaXet[u]:
          soTPLT = soTPLT + 1   // tăng số TPLT
          BFS(u)   // hoặc DFS(u)
          <Ghi nhận các đỉnh thuộc TPLT>
    Bước 3: Trả lại kết quả
      return <các TPLT>
    }""",
    "Thuật toán DFS tìm đường đi giữa các đỉnh": """DFS(s) {

    Bước 1: Khởi tạo
      stack = ∅
      push(stack, s)
      chuaXet[s] = false
    Bước 2: Lặp
      while stack ≠ ∅:
        u = pop(stack)        // lấy đỉnh từ ngăn xếp
        for v ∈ Ke(u):
          if chuaXet[v]:      // nếu v chưa được duyệt
            chuaXet[v] = false    // đánh dấu v đã duyệt
            push(stack, u)        // đưa u trở lại ngăn xếp
            push(stack, v)        // đưa v vào ngăn xếp
            truoc[v] = u          // ghi nhận đường đi: v đến từ u
            break                 // chỉ xét một đỉnh
    Bước 3: Trả lại kết quả
      return <tập đỉnh đã duyệt>
    }""",
    "Thuật toán kiểm tra tính liên thông mạnh": """Strong_Connected(G = <V, E>) {
    Bước 1: Khởi tạo
      ReInit()        // ∀u ∈ V: chuaXet[u] = true
    Bước 2: Lặp
      for u ∈ V:
        if BFS(u) ≠ V    // hoặc DFS(u)
          return false   // đồ thị không liên thông mạnh
        else
          ReInit()       // khởi tạo lại mảng chuaXet[]
    Bước 3: Trả lại kết quả
      return true        // đồ thị liên thông mạnh
    }""",
    "Thuật toán duyệt các đỉnh trụ": """Duyet_Tru(G = <V, E>) {

    Bước 1: Khởi tạo
      ReInit()    // ∀u ∈ V: chuaXet[u] = true

    Bước 2: Lặp
      for u ∈ V:              // lấy mỗi đỉnh u
        chuaXet[u] = false    // cấm BFS/DFS duyệt u
        if BFS(v) ≠ V \ {u}   // hoặc DFS(v)
          <Ghi nhận u là đỉnh trụ>
        ReInit()              // khởi tạo lại mảng chuaXet[]

    Bước 3: Trả lại kết quả
      return <tập các đỉnh trụ>
    }""",
    "Thuật toán duyệt các cạnh cầu": """Duyet_Cau(G = <V, E>) {
    Bước 1: Khởi tạo
      ReInit()    // ∀u ∈ V: chuaXet[u] = true
    Bước 2: Lặp
      for e ∈ E:                // lấy mỗi cạnh e
        E = E \ {e}             // loại bỏ cạnh e khỏi đồ thị
        if BFS(1) ≠ V           // hoặc DFS(1), kiểm tra từ đỉnh 1
          <Ghi nhận e là cạnh cầu>
        E = E ∪ {e}             // hoàn trả cạnh e
        ReInit()                // khởi tạo lại mảng chuaXet[]
    Bước 3: Trả lại kết quả
      return <tập các cạnh cầu>
    }""",
    # Chương 4
    "Chu trình Euler": "Chu trình đơn trong đồ thị G đi qua tất cả các cạnh của nó được gọi là chu trình Euler.",
    "Đường đi Euler": "Đường đi đơn trong đồ thị G đi qua tất cả các cạnh của nó được gọi là đường đi Euler.",
    "Đồ thị Euler": "Đồ thị được gọi là đồ thị Euler nếu nó có chu trình Euler.",
    "Đồ thị nửa Euler": "Đồ thị được gọi là đồ thị nửa Euler nếu nó có đường đi Euler.",
    "Điều kiện cần và đủ để đồ thị là Euler": """Với đồ thị vô hướng:
    - Đồ thị vô hướng liên thông 𝐺 =< 𝑉, 𝐸 > là đồ thị Euler khi và chỉ khi mọi đỉnh của 𝐺 đều có bậc chẵn.
    - Với đồ thị có hướng:
    Đồ thị có hướng liên thông yếu 𝐺 =< 𝑉, 𝐸 > là đồ thị Euler khi và chỉ khi tất cả các đỉnh của nó đều có bán bậc ra bằng bán bậc vào (điều này làm cho đồ thị là liên thông mạnh).""",
    "Chứng minh đồ thị là Euler": """Với đồ thị vô hướng:
    - Kiểm tra đồ thị có liên thông hay không?
      + Kiểm tra 𝐷𝐹𝑆(𝑢) = 𝑉 hoặc 𝐵𝐹𝑆(𝑢) = 𝑉?
    - Kiểm tra bậc của tất cả cả đỉnh có phải số chẵn hay không?
      + Với ma trận kề, tổng các phần tử của hàng 𝑢 (cột 𝑢) là bậc của đỉnh 𝑢.

    Với đồ thị có hướng
    - Kiểm tra đồ thị có liên thông yếu hay không?
      + Kiểm tra đồ thị vô hướng tương ứng là liên thông, hoặc
      + Kiểm tra nếu tồn tại đỉnh 𝑢 ∈ 𝑉 để 𝐷𝐹𝑆(𝑢) = 𝑉 hoặc 𝐵𝐹𝑆 𝑢 = 𝑉?
    - Kiểm tra tất cả các đỉnh có thỏa mãn bán bậc ra bằng bán bậc vào hay không?
      + Với ma trận kề, bán bậc ra của đỉnh 𝑢 là 𝑑𝑒𝑔+(𝑢) là số các số 1 của hàng 𝑢, bán bậc vào của đỉnh 𝑢 là 𝑑𝑒𝑔−(𝑢) là số các số 1 của cột 𝑢.""",
    "Thuật toán tìm chu trình Euler": """Euler-Cycle(𝑢){
      // Bước 1: Khởi tạo
      𝑠𝑡𝑎𝑐𝑘 = ∅; //khởi tạo 𝑠𝑡𝑎𝑐𝑘 là ∅
      𝐶𝐸 = ∅; //khởi tạo mảng 𝐶𝐸 là ∅
      p𝑢𝑠ℎ(𝑠𝑡𝑎𝑐𝑘, 𝑢); //đưa đỉnh 𝑢 vào ngăn xếp
      // Bước 2: Lặp
      while(𝑠𝑡𝑎𝑐𝑘 ≠ ∅){
        𝑠 = 𝒈𝒆𝒕(𝑠𝑡𝑎𝑐𝑘); //lấy đỉnh ở đầu ngăn xếp
        if(𝐾𝑒(𝑠) ≠ ∅){
          𝑡 = <đỉnh đầu tiên trong 𝐾𝑒(𝑠)>;
          p𝑢𝑠ℎ(𝑠𝑡𝑎𝑐𝑘, 𝑡); //đưa đỉnh 𝑡 vào ngăn xếp
          𝐸 = 𝐸\{(𝑠, 𝑡)}; //loại bỏ cạnh (𝑠, 𝑡)
        }
        else{
          𝑠 = p𝑜𝑝(𝑠𝑡𝑎𝑐𝑘); //loại bỏ s khỏi ngăn xếp
          𝑠 ⇒ 𝐶𝐸; //đưa s sang 𝐶𝐸
        }
      }
      // Bước 3: Trả lại kết quả
      <lật ngược lại các đỉnh trong 𝐶𝐸 ta được chu trình Euler>;
    }""",
    "Điều kiện cần và đủ để đồ thị là nửa Euler": """Với đồ thị vô hướng:
      - Đồ thị vô hướng liên thông 𝐺 =< 𝑉, 𝐸 > là đồ thị nửa Euler khi và chỉ khi 𝐺 có 0 hoặc 2 đỉnh bậc lẻ.
        + G có 2 đỉnh bậc lẻ: đường đi Euler xuất phát tại một đỉnh bậc lẻ và kết thúc tại đỉnh bậc lẻ còn lại.
        + G có 0 đỉnh bậc lẻ: G chính là đồ thị Euler.

    Với đồ thị có hướng:
      - Đồ thị có hướng liên thông yếu 𝐺 =< 𝑉, 𝐸 > là đồ thị nửa Euler khi và chỉ khi:
        + Tồn tại đúng hai đỉnh 𝑢, 𝑣 ∈ 𝑉 sao cho 𝑑𝑒𝑔+ (𝑢) − 𝑑𝑒𝑔− (𝑢) = 𝑑𝑒𝑔− (𝑣) − 𝑑𝑒𝑔+ (𝑣) = 1.
        + Các đỉnh 𝑠 ≠ 𝑢, 𝑠 ≠ 𝑣 còn lại có 𝑑𝑒𝑔+ (𝑠) = 𝑑𝑒𝑔− (𝑠).
        + Đường đi Euler sẽ xuất phát tại đỉnh 𝑢 và kết thúc tại đỉnh 𝑣.""",
    "Chứng minh đồ thị là nửa Euler": """Với đồ thị vô hướng:
      - Chứng tỏ đồ thị đã cho liên thông.
        + Sử dụng hai thủ tục 𝐷𝐹𝑆(𝑢) hoặc 𝐵𝐹𝑆(𝑢).
      - Có 0 hoặc 2 đỉnh bậc lẻ.
        + Sử dụng tính chất của các phương pháp biểu diễn đồ thị để tìm ra bậc của mỗi đỉnh.

    Với đồ thị có hướng:
      - Chứng tỏ đồ thị đã cho liên thông yếu.
        + Sử dụng hai thủ tục 𝐷𝐹𝑆(𝑢) hoặc 𝐵𝐹𝑆(𝑢).
      - Có hai đỉnh 𝑢, 𝑣 ∈ 𝑉 thỏa mãn:
          𝑑𝑒𝑔+ (𝑢) − 𝑑𝑒𝑔− (𝑢) = 𝑑𝑒𝑔− (𝑣) − 𝑑𝑒𝑔+ (𝑣) = 1.
      - Các đỉnh 𝑠 ≠ 𝑢, 𝑠 ≠ 𝑣 còn lại có 𝑑𝑒𝑔+ (𝑠) = 𝑑𝑒𝑔− (𝑠).""",
    "Thuật toán tìm đường đi Euler": """Thuật toán tìm đường đi Euler gần giống hệt thuật toán tìm chu trình Euler:
    - Tìm chu trình Euler:
      + Đầu vào thuật toán là đỉnh 𝑢 ∈ 𝑉 bất kỳ.
    - Tìm đường đi Euler:
      + Đồ thị vô hướng:
        ++ Đầu vào thuật toán là đỉnh 𝑢 ∈ 𝑉 có bậc lẻ đầu tiên (trường hợp có 0 bậc lẻ thì dùng đỉnh bất kỳ).
      + Đồ thị có hướng:
        ++ Đầu vào thuật toán là đỉnh 𝑢 ∈ 𝑉 thỏa mãn 𝑑𝑒𝑔+ (𝑢) − 𝑑𝑒𝑔− (𝑢) = 1.""",
    "Đường đi Hamilton": "Đường đi qua tất cả các đỉnh của đồ thị, mỗi đỉnh đúng một lần được gọi là đường đi Hamilton.",
    "Chu trình Hamilton": "Chu trình bắt đầu tại một đỉnh 𝑣 nào đó, qua tất cả các đỉnh còn lại mỗi đỉnh đúng một lần, sau đó quay trở lại 𝑣, được gọi là chu trình Hamilton.",
    "Đồ thị Hamilton": "Đồ thị được gọi là đồ thị Hamilton nếu có chu trình Hamilton.",
    "Đồ thị nửa Hamilton": "Đồ thị được gọi là đồ thị nửa Hamilton nếu có đường đi Hamilton.",
    "Tiêu chuẩn nhận biết đồ thị Hamilton:": "Cho đến nay, chưa tìm ra được một tiêu chuẩn để nhận biết một đồ thị có phải là đồ thị Hamilton hay không.",
    "Kiểm tra một đồ thị có phải là đồ thị Hamilton": "Cho đến nay, cũng vẫn chưa có thuật toán hiệu quả để kiểm tra một đồ thị có phải là đồ thị Hamilton hay không.",
    "Thuật toán tìm chu trình Hamilton": """Thuật toán liệt kê tất cả các chu trình Hamilton bắt đầu tại đỉnh thứ 𝑘:
    Hamilton(int k){
      for(𝑦 ∈ 𝐾𝑒(𝑋[𝑘 − 1])){
        if((𝑘 == 𝑛 + 1) && (𝑦 == 𝑣0))
          Ghinhan(𝑋[1], 𝑋[2], … , 𝑋[𝑛], 𝑣0);
        else if(𝑐ℎ𝑢𝑎𝑥𝑒𝑡 𝑦 == 𝒕𝒓𝒖𝒆){
          𝑋 𝑘 = 𝑦;
          𝑐ℎ𝑢𝑎𝑥𝑒𝑡 𝑦 = 𝒇𝒂𝒍𝒔𝒆;
          Hamilton(𝑘 + 1);
          𝑐ℎ𝑢𝑎𝑥𝑒𝑡 𝑦 = 𝒕𝒓𝒖𝒆;
        }
      }
    }
    Hamilton-Cycle(𝑣0){
      //Khởi tạo các đỉnh là chưa xét
      for(𝑣 ∈ 𝑉)
        𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑣] = 𝒕𝒓𝒖𝒆;
      X[1] = 𝑣0; //𝑣0 là một đỉnh nào đó của đồ thị
      𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑣0] = 𝒇𝒂𝒍𝒔𝒆; //Đánh dấu 𝑣0 đã xét
      Hamilton(2); //Gọi thủ tục duyệt
    }""",
    # chương 5
    "Cây": "Cây là một đồ thị vô hướng, liên thông, không có chu trình.",
    "Rừng": "Rừng là một đồ thị vô hướng, không có chu trình.\nNhư vậy rừng là một đồ thị mà mỗi thành phần liên thông của nó là một cây.",
    "Các tính chất của cây": """Giả sử 𝑇 =< 𝑉, 𝐸 > là đồ thị vô hướng 𝑛 đỉnh, khi đó những khẳng định sau là tương đương:
    1) 𝑇 là một cây.
    2) 𝑇 không có chu trình và có 𝑛 − 1 cạnh.
    3) 𝑇 liên thông và có đúng 𝑛 − 1 cạnh.
    4) 𝑇 liên thông và mỗi cạnh của nó đều là cầu.
    5) Giữa hai đỉnh bất kỳ của 𝑇 được nối với nhau bởi đúng một đường đi đơn.
    6) 𝑇 không chứa chu trình nhưng hễ cứ thêm vào nó một cạnh ta thu được đúng một chu trình.""",
    "Cây khung": """Cho 𝐺 là đồ thị vô hướng liên thông. Ta gọi đồ thị con 𝑇 của 𝐺 là một cây khung của 𝐺 (Cây bao trùm) nếu 𝑇 thoả mãn hai điều kiện:
    - 𝑇 là một cây.
    - Tập đỉnh của 𝑇 bằng tập đỉnh của 𝐺.""",
    "Xây dựng cây khung của đồ thị": """Cách xây dựng một cây khung của đồ thị bắt đầu tại đỉnh 𝑢:
    - Sử dụng thuật toán duyệt DFS hoặc BFS.
    - Mỗi khi ta đến được đỉnh 𝑣 (tức 𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑣] = 𝑡𝑟𝑢𝑒) từ đỉnh 𝑢 thì cạnh (𝑢, 𝑣) được kết nạp vào cây khung.""",
    "Xây dựng cây khung của đồ thị sử dụng thuật toán DFS": """Thuật toán tạo cây khung từ một đỉnh 𝒖:
    Tree-DFS(𝑢){
      cℎ𝑢𝑎𝑥𝑒𝑡[𝑢] = 𝑓𝑎𝑙𝑠𝑒; //đánh dấu đỉnh 𝑢 đã duyệt
      for(𝑣 ∈ 𝐾𝑒(𝑢)){
        if(𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑣]){ //nếu 𝑣 chưa được duyệt
          𝑇 = 𝑇 ∪ { 𝑢, 𝑣 }; //hợp cạnh (u, 𝑣) vào cây khung
          Tree-DFS(𝑣); //duyệt theo chiều sâu từ 𝑣
        }
      }
    }
    Thuật toán xây dựng cây khung:
    Tree-Graph-DFS( ){
      //Khởi tạo các đỉnh đều chưa xét
      for(𝑢 ∈ 𝑉)
        cℎ𝑢𝑎𝑥𝑒𝑡[𝑢] = 𝑡𝑟𝑢𝑒;
      𝑟𝑜𝑜𝑡 = < đỉ𝑛ℎ 𝑏ấ𝑡 𝑘ỳ 𝑐ủ𝑎 đồ 𝑡ℎị >; //Lấy một đỉnh bất kỳ làm gốc
      𝑇 = ∅; //Cây ban đầu chưa có cạnh nào
      Tree-DFS(root); //Gọi thuật toán tạo cây khung từ một đỉnh
      if(𝑇 < 𝑛 − 1)
        <đồ thị không liên thông>;
      else
        <ghi nhận tập cạnh của cây khung 𝑇>;
    }""",
    "Xây dựng cây khung của đồ thị sử dụng thuật toán BFS": """
    Tree-BFS(𝑢){
      //Bước 1: Khởi tạo
      T = ∅; 𝑞𝑢𝑒𝑢𝑒 = ∅; p𝑢𝑠ℎ(𝑞𝑢𝑒𝑢𝑒, 𝑢); 𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑢] = 𝑓𝑎𝑙𝑠𝑒;
      //Bước 2: Lặp
      while(𝑞𝑢𝑒𝑢𝑒 ≠ ∅){
        𝑠 = p𝑜𝑝(𝑞𝑢𝑒𝑢𝑒);
        for(𝑡 ∈ 𝐾𝑒(𝑠)){
          if(𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑡]){
            p𝑢𝑠ℎ(𝑞𝑢𝑒𝑢𝑒, 𝑡);
            T = T ∪ { 𝑠, 𝑡 };
            𝑐ℎ𝑢𝑎𝑥𝑒𝑡[𝑡] = 𝑓𝑎𝑙𝑠𝑒;
          }
        }
      }
      //Bước 3: Trả lại kết quả
      if( 𝑇 < 𝑛 − 1) <đồ thị không liên thông>;
      else <ghi nhận tập cạnh của cây khung 𝑇>;
    }""",
    "Thuật toán Kruskal": """Kruskal(){
    //Bước 1 (khởi tạo):
    𝑇 = ∅; //Ban đầu tập cạnh cây khung là rỗng
    𝑑 𝐻 = 0; //Ban đầu độ dài cây khung là 0
    //Bước 2 (sắp xếp):
    <sắp xếp các cạnh đồ thị theo thứ tự tăng dần của trọng số>;
    //Bước 3 (lặp):
    while(|𝑇| < 𝑛 − 1 && 𝐸 ≠ ∅ ){
      𝑒 = <Cạnh có độ dài nhỏ nhất>;
      𝐸 = 𝐸\{𝑒}; //Loại cạnh 𝑒 ra khỏi tập cạnh
      if (𝑇 ∪ {𝑒} không tạo nên chu trình ){
        T = 𝑇 ∪ {𝑒}; //Đưa 𝑒 vào cây khung
        𝑑(H) = 𝑑(H) + 𝑑(𝑒); //cập nhật độ dài cây khung
      }
    }
    //Bước 4 (trả lại kết quả):
    if(|𝑇| < 𝑛 − 1) <Đồ thị không liên thông>;
    else return (T, d(H));
    }""",
    "Thuật toán Prim": """Prim(s){
    //Bước 1 (khởi tạo):
    𝑉𝐻 = {𝑠}; //Ban đầu 𝑉𝐻 chỉ chứa 𝑠
    𝑉 = 𝑉\{𝑠}; //Loại 𝑠 ra khỏi 𝑉
    𝑇 = ∅; //Cây khung ban đầu chưa có cạnh nào
    𝑑(H) = 0; //Độ dài cây khung ban đầu bằng 0
    //Bước 2 (lặp):
    while(V ≠ ∅ ){
      𝑒 = (𝑢, 𝑣); //Cạnh có độ dài nhỏ nhất với 𝑢 ∈ 𝑉, v ∈ 𝑉𝐻
      if(𝑘ℎô𝑛𝑔 𝑡ì𝑚 đượ𝑐 𝑒)
        return <Đồ thị không liên thông>;
      T = 𝑇 ∪ {𝑒}; //Đưa 𝑒 vào cây khung
      𝑑(H) = 𝑑(H) + 𝑑(𝑒); //Cập nhật độ dài cây khung
      𝑉𝐻 = 𝑉𝐻 ∪ {𝑢}; //Đưa 𝑢 vào 𝑉𝐻
      V = V\ 𝑢 ; //Loại 𝑢 ra khỏi 𝑉
    }
    //Bước 3 (trả lại kết quả):
    return (T, d(H));
    }""",
    "Độ dài đường đi": """Xét đồ thị G = <V, E> với tập đỉnh V và tập cạnh E.
    - Với mỗi cạnh (u, v) ∈ E, ta gán một số thực a(u, v) gọi là trọng số của cạnh.
    - Nếu (u, v) ∉ E thì đặt a(u, v) = ∞.
    - Nếu dãy v0, v1, ..., vk là một đường đi trên G thì độ dài của đường đi đó là:
        Σ (i = 1 → k) a(vi-1, vi).
    """,
    "Trường hợp s cố định t thay đổi": """ 
    - Tìm đường đi ngắn nhất từ s đến tất cả các đỉnh còn lại. 
    - Nếu trọng số không âm: dùng thuật toán Dijkstra. 
    - Nếu có trọng số âm nhưng không có chu trình âm: dùng Bellman-Ford. 
    - Nếu có chu trình âm: bài toán không có lời giải.
    """,
    "Trường hợp s thay đổi t thay đổi": """ 
    - Tìm đường đi ngắn nhất giữa mọi cặp đỉnh. 
    - Nếu trọng số không âm: thực hiện n lần thuật toán Dijkstra. 
    - Nếu không có chu trình âm: dùng thuật toán Floyd.
    """,
    "Thuật toán Dijkstra": """Dijkstra(s) {
    Bước 1 (Khởi tạo):
      d[s] = 0              // gán nhãn đỉnh s bằng 0
      T = V \ {s}           // T là tập đỉnh có nhãn tạm thời
      for v ∈ V:
        d[v] = a(s, v)
        truoc[v] = s
    Bước 2 (Lặp):
      while T ≠ ∅:
        chọn u ∈ T sao cho d[u] = min{ d[z] | z ∈ T }
        T = T \ {u}         // cố định nhãn đỉnh u
        for v ∈ T:
          if d[v] > d[u] + a(u, v):
            d[v] = d[u] + a(u, v)    // gán lại nhãn cho v
            truoc[v] = u
    }""",
    "Thuật toán Bellman-Ford": """Bellman-Ford(s) {
    Bước 1 (Khởi tạo):
      for v ∈ V:
        d[v] = a(s, v)
        truoc[v] = s
      d[s] = 0
    
    Bước 2 (Lặp):
      for k = 1 → n-1:
        for v ∈ V \ {s}:
          for u ∈ V:
            if d[v] > d[u] + a(u, v):
              d[v] = d[u] + a(u, v)
              truoc[v] = u
    }""",
    "Thuật toán Floyd": """Floyd() {
    Bước 1 (Khởi tạo):
      for i = 1 → n:
        for j = 1 → n:   // xét từng cặp đỉnh
          d[i, j] = a(i, j)
          if a[i, j] != ∞:
            next[i, j] = j
          else:
            next[i, j] = null
    Bước 2 (Lặp):
      for k = 1 → n:
        for i = 1 → n:
          for j = 1 → n:
            if d[i, j] > d[i, k] + d[k, j]:
              d[i, j] = d[i, k] + d[k, j]
              next[i, j] = next[i, k]
    }""",
    "Mạng là đồ thị có hướng": """
    - Có duy nhất một đỉnh s không có cung đi vào gọi là điểm phát.
    - Có duy nhất một đỉnh t không có cung đi ra gọi là điểm thu.
    - Mỗi cung e = (u, v) ∈ E được gán với một số thực không âm c_e = c(u, v) gọi là khả năng thông qua (băng thông) của cung.
    - Quy ước: Nếu không có cung (u, v) thì khả năng thông qua được gán bằng 0.
    """,
    "Luồng trong mạng": """
    1) Luồng trên mỗi cung e ∈ E không vượt quá khả năng thông qua của nó:
       0 ≤ f_e ≤ c_e
    2) Điều kiện cân bằng luồng trên mỗi đỉnh của mạng:
       - Tổng luồng trên các cung đi vào đỉnh v bằng tổng luồng trên các cung đi ra khỏi đỉnh v 
         với mọi v ≠ s, t:
           ∑ f(u, v), u ∈ Γ⁻(v) = ∑ f(v, u), u ∈ Γ⁺(v)
       Trong đó:
       - Γ⁻(v): tập các đỉnh kề trước (có cạnh đi vào v).
       - Γ⁺(v): tập các đỉnh kề sau (có cạnh đi ra từ v).
    3) Giá trị của luồng f được định nghĩa là:
       val(f) = ∑ f(s, u), u ∈ Γ⁺(s)
              = ∑ f(u, t), u ∈ Γ⁻(t)
    """,
    "Lát cắt trong mạng": """
    - Lát cắt (X, X*) là một cách phân hoạch tập đỉnh V của mạng thành hai tập X và X*, 
      trong đó s ∈ X và t ∈ X*.
    - Khả năng thông qua của lát cắt (X, X*) được định nghĩa là:
        c(X, X*) = ∑ c(v, w), với v ∈ X, w ∈ X*
    - Lát cắt với khả năng thông qua nhỏ nhất được gọi là lát cắt hẹp nhất.
    """,
    "Tăng luồng trong mạng": """
    - Nếu e = (v, w) ∈ E với f(v, w) = 0 
      → (v, w) ∈ Ef với trọng số c(v, w).
    - Nếu e = (v, w) ∈ E với f(v, w) = c(v, w) 
      → (w, v) ∈ Ef với trọng số c(v, w).
    - Nếu e = (v, w) ∈ E với 0 < f(v, w) < c(v, w) 
      → (v, w) ∈ Ef với trọng số c(v, w) - f(v, w),
      → (w, v) ∈ Ef với trọng số f(v, w).
    """,
    "Thuật toán Ford-Fulkerson": """
    1. Bắt đầu từ một luồng f bất kỳ (có thể là luồng 0).
    2. Xây dựng đồ thị tăng luồng Gf.
    3. Tìm một đường tăng luồng P trong Gf:
       - Nếu không có đường tăng luồng nào → thuật toán kết thúc.
       - Nếu có đường tăng luồng P:
           + Cập nhật luồng mới f' theo P.
           + Lặp lại bước 2 cho đến khi không tìm thêm được đường tăng luồng.
    """

}

# Load dữ liệu từ file hoặc tạo mới
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        custom_answers = json.load(f)
else:
    custom_answers = default_answers.copy()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_answers, f, ensure_ascii=False, indent=2)

# Biến toàn cục
training_mode = False
pending_question = ""
history = []
dark_mode = False
BG_COLOR = "#ffffff"
USER_COLOR = "#A3D8F4"
BOT_COLOR = "#FDE2E4"


# ------------------- Hàm lưu dữ liệu -------------------
def save_answers():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_answers, f, ensure_ascii=False, indent=2)


# ------------------- Cập nhật màu -------------------
def update_colors():
    global BG_COLOR, USER_COLOR, BOT_COLOR
    if dark_mode:
        BG_COLOR = "#2E2E2E"
        USER_COLOR = "#4A90E2"
        BOT_COLOR = "#FF6F61"
    else:
        BG_COLOR = "#ffffff"
        USER_COLOR = "#A3D8F4"
        BOT_COLOR = "#FDE2E4"
    root.configure(bg=BG_COLOR)
    chat_canvas.configure(bg=BG_COLOR)
    chat_frame.configure(bg=BG_COLOR)


# ------------------- Hiển thị tin nhắn -------------------
def add_message(msg, sender="bot"):
    bubble = Frame(chat_frame, bg=BG_COLOR)
    avatar = tk.Label(bubble, text="🤖" if sender == "bot" else "🧑", font=("Arial", 14), bg=BG_COLOR)
    avatar.pack(side="left" if sender == "bot" else "right", padx=5)
    color = BOT_COLOR if sender == "bot" else USER_COLOR
    lbl = tk.Label(
        bubble, text=msg, bg=color, fg="black",
        padx=12, pady=8, wraplength=400,
        font=("Segoe UI", 11), justify="left", bd=0, relief="flat"
    )
    lbl.pack(side="left" if sender == "bot" else "right", padx=5)
    bubble.pack(anchor="w" if sender == "bot" else "e", fill="x", pady=3, padx=10)
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)
    history.append(f"{'Bot' if sender == 'bot' else 'Bạn'}: {msg}")


# ------------------- Animation bot gõ -------------------
def bot_typing_animation(reply):
    bubble = Frame(chat_frame, bg=BG_COLOR)
    avatar = tk.Label(bubble, text="🤖", font=("Arial", 14), bg=BG_COLOR)
    avatar.pack(side="left", padx=5)
    lbl = tk.Label(
        bubble, text="", bg=BOT_COLOR, fg="black",
        padx=12, pady=8, wraplength=400,
        font=("Segoe UI", 11), justify="left", bd=0, relief="flat"
    )
    lbl.pack(side="left", padx=5)
    bubble.pack(anchor="w", fill="x", pady=3, padx=10)
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)
    displayed = ""
    for char in reply:
        displayed += char
        lbl.config(text=displayed)
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1.0)
        time.sleep(0.02)


# ------------------- Chuẩn hóa text -------------------
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def normalize_text(text):
    text = remove_accents(text.lower())
    text = ' '.join(text.split())
    return text


# ------------------- Bot trả lời -------------------
def bot_reply(user_input):
    global training_mode, pending_question
    norm_input = normalize_text(user_input)
    found = False
    best_match = None
    highest_ratio = 0
    for k, v in custom_answers.items():
        norm_key = normalize_text(k)
        ratio = difflib.SequenceMatcher(None, norm_input, norm_key).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = v
    if highest_ratio > 0.6:
        bot_typing_animation(best_match)
        found = True
    if not found:
        training_mode = True
        pending_question = user_input.strip()
        bot_typing_animation(
            f"❓ Mình chưa biết trả lời thế nào cho '{user_input}'. Hãy nhập câu trả lời để mình học nhé!")


# ------------------- Gửi tin nhắn -------------------
def send_message(event=None):
    global training_mode, pending_question
    user_input = entry.get("1.0", tk.END).strip()
    if not user_input:
        return
    add_message(user_input, sender="user")
    entry.delete("1.0", tk.END)

    if training_mode:
        # Người dùng nhập câu trả lời cho câu hỏi chưa biết
        custom_answers[pending_question] = user_input
        save_answers()
        add_message("✅ Cảm ơn bạn! Mình đã học xong câu trả lời mới.", sender="bot")
        training_mode = False
        pending_question = ""
    else:
        threading.Thread(target=bot_reply, args=(user_input,), daemon=True).start()


# ------------------- Nhấn Enter -------------------
def on_enter(event):
    if event.state & 0x0001:
        return
    send_message()
    return "break"


# ------------------- Chế độ Dark/Light -------------------
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_colors()


# ------------------- Reset training -------------------
def reset_training():
    global custom_answers
    custom_answers = default_answers.copy()
    save_answers()
    add_message("♻️ Mình đã reset toàn bộ câu trả lời đã học, trở về trạng thái ban đầu.", sender="bot")


# ------------------- GUI -------------------
root = tk.Tk()
root.title("🤖 Chatbot Toán Rời Rạc 2")
root.geometry("650x700")
root.configure(bg=BG_COLOR)

chat_canvas = Canvas(root, bg=BG_COLOR, highlightthickness=0)
scrollbar = Scrollbar(root, orient="vertical", command=chat_canvas.yview)
chat_frame = Frame(chat_canvas, bg=BG_COLOR)

chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=scrollbar.set)

chat_canvas.pack(side="top", fill="both", expand=True, padx=5, pady=5)
scrollbar.pack(side="right", fill="y")

entry = Text(root, font=("Segoe UI", 12), height=3, wrap="word")
entry.pack(side="top", fill="x", padx=10, pady=(0, 5), ipady=5)

send_button = Button(root, text="Gửi", command=send_message,
                     bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), padx=20, pady=5)
send_button.pack(side="top", pady=(0, 5))

dark_button = Button(root, text="🌙/☀️", command=toggle_dark_mode,
                     bg="#555555", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=3)
dark_button.place(x=10, y=650)

reset_button = Button(root, text="Reset Training", command=reset_training,
                      bg="#FF5722", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=3)
reset_button.place(x=90, y=650)

entry.bind("<Return>", on_enter)

add_message("Chào bạn 👋! Mình là Chatbot – trợ lý thông minh giúp bạn học Toán Rời Rạc.", sender="bot")

root.mainloop()
