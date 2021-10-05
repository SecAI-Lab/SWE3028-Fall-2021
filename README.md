## SWE3028
Capstone Design Project (Fall 2021)


### Team Building
* Team A [jjangdol]: YOON SEONGBIN (윤성빈), NAM DEUKYUN (남득윤), WEE SUNGEUN (위성은), and LEE DASOL (이다솔)
* Team B [bTeam]: Jisu Kim (김지수), Jinhwan Kim (김진환), Seyeon Park (박세연), and Mujin Gwak (곽무진)
* Team C [coturnix]: Seonghyun Ban (반성현), Dongyoung Choi(최동영), and Minseung Lee (이민승)
* Team D [EDITH]: Oinar Chingis (칭기즈), Kim Eunmin (김은민), Park Soohun (박수헌), and Gong He (공허)
* Team E [Exponential]: Pavlov Borislav Georgiev, KIM MINJAE (김민재), KIM YOUNGOH (김영오), and PARK GUERYANG (박거량)
* Team F [Fancy]: CHA MINJI (차민지), LEE EUNJI (이은지), JO DAEYEOL (조대열), and KIM DAEHEE (김대희)
* Team G [cookie&cream]: NAMKOONG BOMIN (남궁보민), KIM HANGYU (김한규), SUH JUWON (서주원), CHO GYEONGHYEON (조경현), and CHOI JAEHYUK (최재혁)
* Team H [The outsiders]: CHE SEUNGYUN (채승윤), UHM JIYONG (엄지용), LEE JISEOP (이지섭), JEONG CHAEWON (정채원), and HONG SEONGJUN (홍성준)


### Team Proposals
* Team A [jjangdol]: [GANdan-fontmaker: Web Service for Handwritten-Hangul Font Generation](https://github.com/dasollee2525/Capstone-project)
* Team B [bTeam]: [S-Gether: Web Application for Sharing Goal](https://github.com/7ZXU/SWE3028-TeamB)
* Team C [coturnix]: [Explainable AI model for Stock Trading](https://github.com/leeminseung/coturnix)
* Team D [EDITH]: [AI-Powered Anime Character Editing Web App](https://github.com/chingisooinar/CDP_EDITH)
* Team E [Exponential]: [Stock-loss Prevention: Mobile Application with CNN-LSTM Model for Predicting Sharp Rises and Falls in Stock Price](https://github.com/borislavvp/SWE3028-Exponential)
* Team F [Fancy]: [Review Note Auto Generation Application](https://github.com/deinm/Capstone_Design_Project)
* Team G [cookie&cream]: [Deep Learning Based Fashion Recommendation Application](https://github.com/eee-min20/cookieNcream)
* Team H [The outsiders]: [CNN based Location Image Search and its Adaptation to Social Network](https://github.com/Outsider-H/PINPLACE)


#### Common considerations for AI-based projects
 - Supervised or unsupervised?
 - Dataset you want to utilize for training?
    - Manual dataset preparation for labeling?
    - Number of dataset
    - Number of labels (supervised)
    - Ratio (training/validation/test)
 - Goal (e.g., classifier)
    - Clarify the objective of the model
    - Narrow down your scope if too broad -> constraints
    - Set up the objective function (min/max)
 - Algorithm or model
    - Reasoning that you choose that model?
    - CNN-based, RNN-based?, GAN, ensembles?
    - Difference between your model and prior work
    - Applying the existing model (as it is) might not work for your goal
 - Input and output form
    - Input form to be fed into a model
    - e.g., words must be converted into vectors (like word2vec) in NLP
    - pre-processing of raw inputs
    - output: classified category (e.g., softmax) or others?
 - Defining unique challenges for your own problem
 - Existing techniques to take advantage of
    - Open sources
    - e.g., OCR (optical character recognition) for recognizing chars
 - Limitations (every work has limitations)
    - Constraints
    - Out of scope
 - Evaluation 
    - Evaluation metrics? F1 (with FPR/FNR), accuracy or AUC? (supervised)
    - Assessment on GAN outputs?
    - Comparison with another model at least one comparison: performance comparison with previous approaches
	  - Availability of comparing models (open source?)
 - Computation resource (e.g., GPU)
    - Out of scope; you should find your own
    - Cloud GPU?
