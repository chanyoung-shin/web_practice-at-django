# english.ver
# Sejong Web Project

[**Google Drive Link**](https://drive.google.com/file/d/1p0GZTfjaLX204CJcR64Sfdo_YRLNgrET/view?usp=sharing)  
This link leads to a file for the **Sejong University Website Improvement Project** from the first semester of 2024.

**Context**: The project aimed to enhance the **Jiphyeon Campus** website (used for online coursework at Sejong University). The improvements focused on four main areas:  
1. **Login system**  
2. **Web design**  
3. **Lecture summarization system**  
4. **Assignment & lecture deadline reminders**  

My role primarily involved **improving the login system**, which was previously reliant on manual password entry—both inconvenient and vulnerable to security risks.

---

## How Is the Structure Organized?

1. **Webcam Input**  
   The user’s webcam captures an image of their face, which is sent to the server along with their user ID.

2. **YOLO Detection**  
   - The YOLO model checks for security threats (e.g., electronic devices, printer photos, etc.).  
   - If it detects no threats and only a human face is present, it crops the face area for further processing.  
   - If any security threat is detected, the process terminates with a “Security threat detected” message.

3. **Siamese Network**  
   - The user ID determines which Siamese Network model to use (or which reference data to compare against).  
   - The cropped face image is fed into the Siamese Network.

4. **Model Decision**  
   - If the Siamese Network confirms the user (face match), login is granted.  
   - Otherwise, the process repeats (unless YOLO detects a threat).

---

## YOLOv8

**YOLO** serves two purposes:
1. **Identify Security Threats** (e.g., other devices, printed photos, masks, tablets, etc.).
2. **Crop Only the Face** to provide the Siamese Network with a clean input, thereby improving accuracy.

I used **YOLOv8** from Ultralytics, trained on a custom dataset from **Roboflow** (which currently isn’t publicly accessible due to dataset removal by the owner).

![image](https://github.com/user-attachments/assets/1475a0b6-f253-45ce-9c91-3114aa36891e)

Ultralytics provides a user-friendly interface for training YOLOv8 models with minimal effort.

---

## Siamese Network

A **Siamese Network** consists of two identical neural networks (with shared weights and structure) that each process one input; their outputs are then compared. Initially described in 2005 by Yann LeCun’s team, it was further refined in 2015 into a neural-based Siamese model.

### One-Shot Learning

A key concept in understanding Siamese Networks is **One-shot learning**, a form of **few-shot learning**.  
- Traditional deep learning requires large amounts of data due to the numerous parameters.  
- Humans, by contrast, can often recognize something new from minimal examples.  
- One-shot learning aims to replicate human-like learning from a single example.

![image](https://github.com/user-attachments/assets/a8a8b0a1-d8e9-442c-a01c-ef80c57657b7)  
> Source: [Velog Post on Siamese Networks](https://velog.io/@jy_/Siamese-Network)

In the above diagram, two images are passed through the same network, and the outputs are compared to compute a similarity score. If the **Euclidean distance** between the embeddings is sufficiently small, the images are deemed similar.

### Applying Siamese Network to User Authentication

- A Siamese Network receives two images:
  1. **Reference image** (stored as the user’s registered face)  
  2. **Incoming webcam image**  
- The network outputs a **distance**; the smaller the distance, the more similar the two faces are.  
- If the distance is below a chosen **threshold**, we accept the login as valid.  

To **minimize false positives**, we used the validation distribution of distances so that the threshold is set near the point where **FP (false positives) ≈ 0**. Consequently, the model is highly cautious in verifying the user’s identity.

![image](https://github.com/user-attachments/assets/03fd4c99-cf6e-4b82-b885-6f0a0e14fc0a)  
The black vertical line in the distribution acts as our threshold.

---

### Training Process

We used:
- **My own face images** (anchor folder).  
- **Subset of the LFW (Labelled Faces in the Wild)** dataset (contains multiple celebrities).  

1. **Data Preparation**  
   - Because a Siamese Network learns by comparing two images at a time, the number of images in each folder (my face vs. LFW) must be balanced.  
   - If needed, we duplicate paths in the smaller set until both sets are equal in size.

2. **Data Loading & Preprocessing**  
   - Convert images to resolution **120×120**.  
   - Apply standard transformations (e.g., normalization, tensor conversion).  
   - Batch the data via **DataLoader** (e.g., batch size of 32).

3. **Loss Function**  
   - A contrastive loss or similar metric-based loss is often used to train the Siamese Network.

4. **Model Architecture**  
   - We combined **MobileNet** with Siamese principles.  
   - Performed **transfer learning**, freezing most layers of MobileNet and training only the final layers.

![image](https://github.com/user-attachments/assets/acf32733-6346-4e2e-974e-8e56b6446af7)

After training, the model successfully differentiates between my face and others with high accuracy.

---

## Django

**Django** is a Python-based web framework designed for rapid, secure development. Two key reasons developers favor Django:

1. **Fast Development**  
   - Simple setup and straightforward learning curve.  
   - Provides a practical structure for common web development tasks.

2. **Security**  
   - Django defends against **XSS** by escaping user input in templates.  
   - Protects against **CSRF** attacks by encrypting session tokens.

### How Django Works (MTV Pattern)

Django uses the **MTV (Model–Template–View)** pattern:
- **Model (M)**: Manages database interactions.  
- **Template (T)**: Renders dynamic HTML for the user.  
- **View (V)**: Core application logic.  

![image](https://github.com/user-attachments/assets/17572fab-9059-41d3-a1d6-cffb0945f58f)

**Basic Flow**:
1. A user requests a URL → **urls.py** routes to the appropriate app-level urls.py.  
2. The app’s urls.py points to a **view function**.  
3. The view can return a response directly or may need to query/update the database via **models**.  
4. The final data is rendered into **templates** (HTML) and sent to the user.

---

# korean.ver
## Core Structure

Below are some crucial Django files from the project:

### 1. HTML (Template)

![image](https://github.com/user-attachments/assets/98d0c2ad-75a4-44c7-97e9-1eae249f6d15)

- Captures the user’s webcam input.  
- Sends the captured image to the server.

### 2. Views (Server Logic)

![image](https://github.com/user-attachments/assets/b8f18d92-6c03-463e-bc8f-3a3fac552815)

- Receives the image from the client.  
- Runs YOLO to detect devices or other threats:
  - If a threat is detected, returns “detect device” and stops.  
  - Otherwise, crops the face and sends it to the **Siamese Network**.  
  - If the Siamese Network confirms the user, returns “Done”; otherwise, it returns a prompt to retry.

### 3. HTML Response Handling

![image](https://github.com/user-attachments/assets/98d0c2ad-75a4-44c7-97e9-1eae249f6d15)

- If the server’s response is “Done,” redirects the user to the logged-in page.  
- Otherwise, displays messages such as “Face not recognized” or “Security threat detected.”


# sejong web project

https://drive.google.com/file/d/1p0GZTfjaLX204CJcR64Sfdo_YRLNgrET/view?usp=sharing
이링크는 2024 1학기에 진행하였던 세종 웹사이트 개선 프로젝트 파일이다. 

세종대에서 온라인으로 학습할 때 이용하는 집현캠퍼스라는 사이트를 개선하는 프로젝트였다. 개선점은 크게 4가지로 로그인 시스템 개선, 웹 디자인 개선, 강의 요약 시스템 추가, 과제, 강의등 마감시간 알림 개선이다.

내가 맡은 역할은 로그인 시스템 개선이다. 기존 로그인 시스템은 직접 비밀번호를 쳐야해서 번거롭고 비밀번호 유출 보안 문제도 있다. 그러나 이 로그인 시스템을 사용하면 앞선 두가지 문제를 완화할 수 있다.

## How is the structure structured?
1.먼저 사용자의 웹캠을 이용하여 사용자의 얼굴 이미지와 사용자의 id가 서버로 들어온다

2.이후 YOLO를 이용해 보안위협(device,프린터된 사진)이 있는지 검출하고 만약 보안위협이 감지되지않고 사람의 얼굴만 감지 된다면 사람의 얼굴을 crop하여 Siamese Network 모델로 보낸다.

3.id를 대조하여 그 사람에 맞는 Siamese Network 모델을 찾고 Siamese Network에 받은 사진을 입력한다.

4.Siamese Network가 이사람이 맞다고 판단하면 로그인이 허락되고 만약 그렇지 않다면 이 1~4까지의 과정을 반복한다. 그러나 보안 위협이 감지되면, "보안 위협이 감지되었습니다."라는 메세지와 함께 반복을 멈춘다.

## YOLOv8
YOLO는 먼저 보안위협을 검출하고 배경정보를 없애 siamese network내의 정확도를 높이기 위해서 얼굴만 crop 시키는 역할을 한다. 나는 YOLOv8 모델을 사용했으며  데이터 셋은 디바이스, 진짜 얼굴, 인쇄물, 마스크, 태블릿등의 사진이 있는 파일을 Roboflow에서 가져왔다.(현재는 데이터셋의 주인이 데이터셋을 내려서 링크를 제공할 수 없다.)

![image](https://github.com/user-attachments/assets/1475a0b6-f253-45ce-9c91-3114aa36891e)

YOLO는 사진과 같은 ultralytics 패키지를 지원하기 때문에 학습하기 굉장히 쉽다.

## Siamese Network
Siamese Network 가중치와 구조가 같은 인공 신경망에 두 입력을 넣은 뒤 출력을 비교하는 인공 신경망이다. 이 네트워크 구조 자체는 2005년 에 Yann LeCun이라는 교수 연구팀에 의해 발표되었다. 그리고 2015년에 이 네트워크에 신경망을 접목시킨 샴 신경망이 발표되었다. 

샴 네트워크를 이해하기 위해서는 One-shot learning 뭔지 알아야한다.
딥러닝은 기존 모델들에 비해 강력한 모델이다. 그러나 이 딥러닝 모델을 학습시키기 위해 정말 많은 양의 파라미터를 생성하고 학습시켜야 한다. 이를 위해서는 많은 데이터도 필요하다. 반면 사람은 적은 데이터로도 학습이 가능하다. 딥러닝 모델이 인간처럼 소량의 데이터 만으로 학습할 수 있개하는 것이 Few-shot learning이고 극단적으로 한 장의 데이터 만으로 학습 할 수 있게 하는 것을 One-shot learning이라고 한다.

![image](https://github.com/user-attachments/assets/a8a8b0a1-d8e9-442c-a01c-ef80c57657b7)

source:https://velog.io/@jy_/Siamese-Network

위의 사진은 샴 네트워크의 구조를 그림으로 표현한 것이다. 위 사진의 과정을 설명하자면 다른 두 사진을 모델에 입력하고 모델의 출력값을 이용해 이 두 사진이 얼마나 유사한지 출력한다.

Siamese Network의 출력값은 두 사진의 유클리디안 벡터의 거리이다. 이거리가 짧으면 짧을 수록 두 사진이 비슷하다는 것을 의미한다. 따라서 거리가 어느정도 이하이면 사용자를 로그인 시킬지 정할 수 있다. 이것을 우리는 thresould이라고 칭하였다.

Siamese Network는 사진의 얼굴이 진짜 사용자의 얼굴인지 확인한다. Siamese Network는 두가지의 사진을 받아 두사진의 유사도를 측정한다. 이 원리를 이용하여 기존 사용자의 얼굴 이미지와 현재 서버에 들어오는 이미지를 분석하여 사용자 인지 아닌지 판단한다. 

이 과정에서 보안상의 이유로 다른 사람인데 사용자라고 인식하는 경우를 거의 0에 수렴하도록 만들어야한다. 모델을 학습할 때 validation의 출력값(두사진 사이의 거리)의 분포를 이용해 다른 사람을 사용자라고 인식하는 즉 FP(1종 오류)가 0인 지점을 threshold로 지정하였다. 즉 Siamese Network의 출력값이 이 thereshold 보다 작아야지만 로그인된다.

<img width="284" alt="KakaoTalk_20250106_15560422116" src="https://github.com/user-attachments/assets/03fd4c99-cf6e-4b82-b885-6f0a0e14fc0a" />

즉 사진의 분포에서 검은 줄로 표시된 값이 threshold로 설정된다.

학습과정은 다음과 같다.

먼저 데이터셋은 나의 얼굴 사진과 lfw데이터 중 일부를 사용하였다. lfw데이터는 여러 유명인의 얼굴이 모여있는 데이터 셋이다.

먼저 학습과 데이터 전처리를 위한 라이브러리들을 불러 와준다.

![image](https://github.com/user-attachments/assets/dffb9908-4a86-43b3-8a96-8867c3243b78)

내가 준비한 데이터를 파이썬에서 쉽게 접근할 수 있게 Dataset클래스를 정의해 준다.
![image](https://github.com/user-attachments/assets/63e10252-3312-43bd-a871-c652ec1ef673)

 샴네트워크 모델을 학습시킬떄 두 폴더(anchor(my face), lfw)의 데이터의 수가 다르면 안된다. 왜냐하면 샴네트워크의 원리가 신경망을 통과시킨 두 결과 값의 벡터값을 이용하여 가중치를 업데이트하는 방식이기 때문이다. 따라서 두 폴더의 데이터수를 맞추기 위해 수가 부족한 폴더의 경로 리스트에다 개수가 같아질 때까지 똑같은 경로를 복사해주었다.

이렇게 만들어진 경로를 이용해 모델이 이미지를 요청하면 경로를 이용해 이미지를 불러온다음 transform을 이용하여 전처리를 하고 이미지를 반환해준다.

![image](https://github.com/user-attachments/assets/3000f7e2-5651-4b1c-b0ad-82f894dbad10)

준비된 이미지 데이터 셋을 모델에 학습 시키기 위해 120*120의 해상도로 맞추고 텐서 형태로 바꿔 준다. 또한 미니 배치를 사용해기위해 DataLoder로 32개씩 묶어준다.

![image](https://github.com/user-attachments/assets/80875850-db3a-4024-a98e-8443f2b52f7b)

학습에 쓸 손실함수를 정의해준다.

![image](https://github.com/user-attachments/assets/50248f20-1d77-4941-820d-51892550c155)

모바일 넷과 샴네트워크를 결합한 신경망이다. 우리는 컴퓨터 리소스 자원이 부족하여 완전연결층만 학습시키는 전이학습을 하였다.

![image](https://github.com/user-attachments/assets/acf32733-6346-4e2e-974e-8e56b6446af7)

학습 시킨 결과물이다. 위의 사진처럼 잘 구별하는 모습을 보여준다.

## Django
 장고는 파이썬 웹 애플리케이션을 효율적으로 빠르게 개발할 수 있는 소프트웨어이다. 장고는 다음 2가지의 특성 때문에 개발자 사이에서 많이 쓰인다.

1.개발 속도
 장고 프레임 워크는 설치 및 학습이 간단하므로 몇시간 내에 자신의 장고 프로젝트를 만들 수 있다. 장고는 타 프레임워크에 비해 신속한 개발과 실용적인 디자인을 제공한다. 또한 장고는 몇 가지 일반적인 웹 개발 테스크에 즉시 사용할 수 있는 구조를 제공하기 때문에 몇 줄 만으로도 코드를 작성할 수 있다.

2. 보안
 장고는 3가지의 보안 공격을 막을 수 있다. 첫 번째는 XSS공격이다. XSS 공격은 웹사이트 사용자가 브라우저에 악성코드를 삽입하는 공격이다. 하지만 장고는 이러한 공격을 escape처리하거나 무시하여 이러한 공격으로부터 사용자를 보호한다.
 두 번째는 CSRF(크로스 사이트 요청 위조)이다. 이공격은 해커가 사용자의 보안 인증 정보를 훔치기 위해 웹 앱에 무단 요청을 전송할 때 발생한다. 장고는 사용자의 정보를 암호화하여 정보를 보호한다.

### Django의 작동 원리

 장고는 MTV 패턴을 통해 설계가 이루어진다. MTV는 Model(모델), Template(템플릿), View(뷰)의 약자이다. 여기서 M은 DB와 상호작용하는 부분이고, T는 사용자들의 눈에 보이는 부분(ex html) , V는 웹서비스 내부의 동작 논리를 담당하는 부분이다.

![image](https://github.com/user-attachments/assets/17572fab-9059-41d3-a1d6-cffb0945f58f)

위의 사진은 장고의 작동원리를 나타낸 그림이다.

장고 프로젝트의 urls.py에 사용자가 접근하면 urls.py는 적절한 app의 urls.py로 보낸다. 이 urls.py는 또 다시 적절합 app내의 view의 함수로 내보낸다. 이 def 함수에서 받은 것을 처리해 사용자에게 반환할 수도 있지만 사용자가 데이터베이스에 접근할 때는 model을 통해 Database로 접근해 정보를 사용자에게 반환한다.

## 핵심 구조
 다음은 내가 작성한 장고의 핵심이 되는 파일들이다.

![image](https://github.com/user-attachments/assets/98d0c2ad-75a4-44c7-97e9-1eae249f6d15)

먼저 html파일이다 이 파일은 사용자에게 웹캠을 요청하고 사진을 따오는 것을 목적으로 한다. 사용자의 사진을 따오고 서버로 사진을 보내준다,

![image](https://github.com/user-attachments/assets/b8f18d92-6c03-463e-bc8f-3a3fac552815)

이 코드는 받은 사진을 처리하는 서버의 view.py 파일이다. 사진을 받으면 YOLO를 이용해 자르고 자른사진을 Siamese Network에 입력한다, 사용자가 맞다고 판단되면 Done을 html에 반환한다. 또한 디바이스나 보안 위협을 감지하였다면 "detect dvice"를 반환한다.

![image](https://github.com/user-attachments/assets/98d0c2ad-75a4-44c7-97e9-1eae249f6d15)

다시 html 파일을 살펴보자 만약 done을 받으면 사용자의 로그인 페이지로 이동한다, 그렇지 않다면 사용자에게 text로 "얼굴이 인식되지 않았습니다."를 반환하거나 "디바이스 감지 및 부정 행위 감지"를 반환한다..
