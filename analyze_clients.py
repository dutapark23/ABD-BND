import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import os

# ── RAW DATA ────────────────────────────────────────────────────────────────
raw = [
    ("Kevin Dale","971568770949","23.03","Answer","YES","","",""),
    ("Jamie Barr","971585713015","23.03","Answer","YES","","",""),
    ("Andrew Dunbar","971504507463","23.03","Answer","YES","","",""),
    ("Cristine","971568022359","25.03","Answer","YES","","",""),
    ("Ibrahim Igbarie","971521885659","25.03","Answer","YES","","",""),
    ("Tracy Harmoush","971 50 738 3414","25.03","Answer","YES","","",""),
    ("Enzo Bedok","971 58 592 3428","25.03","Answer","YES","","",""),
    ("Alber Alsst","971 55 990 4075","25.03","Answer","YES","","",""),
    ("Mokhamed Adnan","971 52 719 9352","25.03","Answer","YES","","",""),
    ("Raghu","971585393677","25.03","Answer","YES","","",""),
    ("Ambreen","971503832994","25.03","Answer","YES","","",""),
    ("Jai","971503017210","25.03","Answer","YES","","",""),
    ("Andrei Sidorka","971585151675","25.03","Answer","YES","he'll be back in 5 months","did not answer",""),
    ("Moda","971564297138","25.03","Answer","YES","","",""),
    ("Gabby","971 52 227 3467","25.03","Answer","YES","","",""),
    ("Mathilda","971 50 655 4091","25.03","Answer","YES","","",""),
    ("Carlota","971 55 314 0086","25.03","Answer","YES","","",""),
    ("Dr. Laiiba","97158915894","25.03","Answer","YES","","",""),
    ("Marisa Fernandes","971525193078","25.03","Answer","YES","","",""),
    ("Adem","971 58 231 1176","25.03","Phone is off","","","",""),
    ("Brice Roman","971586717986","25.03","No answer","","","",""),
    ("Lazat","971561644177","25.03","No answer","","","",""),
    ("Alessandro Brovelli","971 56 298 6464","25.03","Phone is off","","","",""),
    ("Patrick","971505417085","25.03","No answer","","","",""),
    ("Alessandro Gioia","971 58 531 3245","25.03","Phone is off","","","",""),
    ("Emanuele","971553858608","25.03","Phone is off","","","",""),
    ("Kaan Aslan","971 58 576 7943","25.03","No answer","","","",""),
    ("Julius","971506549368","25.03","No answer","","","",""),
    ("Ibrahim Jabri","971505073316","25.03","No answer","","","",""),
    ("Shivani","971557976203","25.03","No answer","","","",""),
    ("Benn","447376912917","25.03","Answer","NO","10th April","UK",""),
    ("Omar Ghanem","971566915970","25.03","No answer","","","",""),
    ("Amir M","971 58 511 6966","25.03","Answer","YES","","",""),
    ("Kamini Naik","971 58 912 1864","25.03","No answer","","","",""),
    ("Tina Ruiz","971 55 903 9012","25.03","No answer","","","",""),
    ("Karin Lopez","971 54 566 9868","25.03","No answer","","","",""),
    ("Irene Ashraf","971 50 566 3460","25.03","Answer","YES","","",""),
    ("Anthea Rabahie","971 55 211 1579","25.03","No answer","","","",""),
    ("Alima","998 90 811 43 83","25.03","Phone is off","","","",""),
    ("Jasmine","1 (647) 929-7755","25.03","Phone is off","","","",""),
    ("Abtine Monavvari","1 (647) 297-5013","25.03","No answer","","","",""),
    ("Michael Kussani","33 6 50 30 40 38","25.03","No answer","","","",""),
    ("Stanley Samadhi","41 76 269 35 77","25.03","Phone is off","","","",""),
    ("Gulnara Omar","1 (236) 514-4778","25.03","Phone is off","","","",""),
    ("Eelco Huudeman","31 6 41116983","25.03","Phone is off","","","",""),
    ("Molli Llyod","44 7865 294110","25.03","Answer","No","anytime soon","UK",""),
    ("Gagaan Singh","91 96505 60787","25.03","No answer","","","",""),
    ("Oriel","972546209889","25.03","No answer","","","",""),
    ("Maddy Christina","971526332035","25.03","","","","",""),
    ("Cleo","32468340668","25.03","No answer","","","",""),
    ("Cosmin Petrescu","40737783878","25.03","No answer","","","",""),
    ("Anshula","+91 91 3771 649 4","25.03","No answer","","","",""),
    ("Marvin","971558576327","25.03","No answer","","","",""),
    ("Pratz","971525503316","25.03","No answer","","","",""),
    ("Anna Cruz","34654785373","25.03","No answer","","","",""),
    ("Set Comp","971561254563","25.03","No answer","","","",""),
    ("Ebrahim","44 7447 477491","25.03","Phone is off","","","",""),
    ("James Sellu","971 50 935 8513","25.03","Answer","Yes","","",""),
    ("Bruno","49 1512 8752004","25.03","Phone is off","","","",""),
    ("Kenneth Beller","971 56 990 7103","25.03","Phone is off","","","",""),
    ("Patrick Hong","971 58 188 2864","25.03","No answer","","","",""),
    ("Xavier Cafrey","1 (647) 779-4315","25.03","Phone is off","","","",""),
    ("Josh Bridgman","971 55 225 1516","25.03","Phone is off","","","",""),
    ("Tamara OShaughessy","1 (705) 817-7400","25.03","No answer","","","",""),
    ("Alexander Gatej","971 50 229 1750","25.03","No answer","","","",""),
    ("Maribel Franchesca","971 58 509 5831","25.03","Phone is off","","","",""),
    ("Irtaza","44 7395 255000","25.03","Phone is off","","","",""),
    ("Bailey Nicole","971 58 594 8516","25.03","No answer","","","",""),
    ("Ferhat","971 52 978 6179","25.03","No answer","","","",""),
    ("Harry Knights","971 58 528 5820","25.03","No answer","","","",""),
    ("Zoheb","971 50 646 4158","25.03","Answer","Yes","","",""),
    ("Anna Kovaleva","971 58 977 7684","25.03","No answer","","","",""),
    ("Shako Lokman","971 50 180 5921","25.03","Phone is off","","","",""),
    ("Valeriya","971 50 605 7884","25.03","Answer","Yes","","",""),
    ("Stuart Carter","971 55 443 6190","25.03","Answer","Yes","","",""),
    ("Alex Alleyne","971 58 556 2488","25.03","Answer","Yes","","",""),
    ("Adham Kemel","971 50 940 0519","26.03","Answer","No","will be back on Saturday","",""),
    ("Lauren","971585696743","26.03","Answer","Yes","","",""),
    ("David Allen","971562884820","26.03","Answer","Yes","","",""),
    ("Qvie","971588331202","26.03","Answer","Yes","","",""),
    ("NATABOU Junior","971 52 235 8137","26.03","No answer","","","",""),
    ("Nadine Samara","971 56 683 8030","26.03","No answer","","","",""),
    ("Nervi","971786229801","26.03","Phone is off","","","",""),
    ("Antoine Blanco","971 58 532 1859","26.03","Phone is off","","","",""),
    ("Mohammed Suliaman","+971 55 691 2308","26.03","Answer","No","after a month","Abu Dhabi",""),
    ("SYMPOSIUM GROUP S.R.L.","+971 58 510 2346","26.03","Phone is off","","","",""),
    ("Fabio Lavalle","+971 50 188 6685","26.03","Answer","No","not anymore","did not answer",""),
    ("Anastasiia Stoiatska","+971 52 206 8408","26.03","No answer","","","",""),
    ("Diana Mamonong","+971 58 594 5809","26.03","Phone is off","","","",""),
    ("Jonathan Ma","+971 55 554 6039","26.03","Answer","No","in 2 weeks","France",""),
    ("Essa Rasool","+971 50 886 2228","26.03","Answer","Yes","","",""),
    ("Aisha Al muhairy","+971 50 656 5665","26.03","No answer","","","",""),
    ("Alfredo","505312857","26.03","Answer","Yes","","",""),
    ("alexander dowie","+971 58 528 8421","26.03","No answer","","","",""),
    ("Imrane","+971 58 547 3327","26.03","No answer","","","",""),
    ("Charlotte A Edgar","556401606","26.03","Answer","Yes","","",""),
    ("Daniel leese","+971 55 991 5990","26.03","Phone is off","","","",""),
    ("Joe Cross","+971 58 500 6150","26.03","Phone is off","","","",""),
    ("Rustam Rylskiy","+971 50 317 0603","26.03","Answer","Yes","","",""),
    ("Cardin Loic","+971 50 885 0696","26.03","Phone is off","","","",""),
    ("Moustafa Hamouda","585146733","26.03","Answer","Yes","","",""),
    ("Charey Ryatt","+971 52 699 0312","26.03","No answer","","","",""),
    ("Mohit Gupta","+971 50 610 3804","26.03","Phone is off","","","",""),
    ("Queensy Harris","+971 50 373 0297","26.03","Phone is off","","","",""),
    ("Miles McGilvery","+44 7706 771162","26.03","Answer","No","no exact date yet","UK",""),
    ("amar Llcus","+971 55 176 8177","26.03","Phone is off","","","",""),
    ("Cynthia","971506856145","26.03","Answer","Yes","","",""),
    ("Karen Abuan","971505475910","26.03","Phone is off","","","",""),
    ("Sarah Halls","971585209029","26.03","Answer","Yes","","",""),
    ("Ciaran finn","447722136384","26.03","Phone is off","","","",""),
    ("Mohammad Almarzouq","509416800","26.03","No answer","","","",""),
    ("Matias Molina","971506026529","26.03","Phone is off","","","",""),
    ("Fabian Orietz","4915737896664","26.03","Answer","did not answer","","",""),
    ("Zainab","557331910","26.03","Phone is off","","","",""),
    ("Maurice Pauli","588378403","27.03","Phone is off","","","",""),
    ("Margo Cunego","33611613536","27.03","Phone is off","","","",""),
    ("Jake Heath","585926412","27.03","No answer","","","",""),
    ("Milla","447391858354","26.03","Answer","Yes","","",""),
    ("Christine","971568022359","27.03","Answer","Yes","","",""),
    ("Nahla Al Malki","971544409565","27.03","Answer","Yes","","",""),
    ("James Reynolds","971585923289","27.03","Answer","Yes","","",""),
    ("Vexatrade","+971 58 574 1107","27.03","No answer","","","",""),
    ("Candice","+971 58 527 3608","27.03","Answer","No","no definite time","did not answer",""),
    ("Felix","+33 6 49 62 47 78","27.03","Answer","No","no definite time","France",""),
    ("VideoGrown","+971 50 562 7041","27.03","","","","",""),
    ("Bastien","+971 50 959 6982","27.03","Answer","Yes","","",""),
    ("Redouanne","+971 50 701 6426","27.03","Phone is off","","","",""),
    ("Richard Grannon","+971 58 589 1771","27.03","Phone is off","","","",""),
    ("Tanja","+49 162 5964969","27.03","No answer","","","",""),
    ("Govind","+971 55 680 4200","27.03","Answer","Yes","","",""),
    ("JoeCom","+971 55 554 6039","27.03","No answer","","","",""),
    ("Aylin Kormali","+971 58 566 1745","27.03","Phone is off","","","",""),
    ("Stefanos Christou","+357 96 206994","27.03","","","","",""),
    ("Manish","971502724882","27.03","Answer","Yes","","",""),
    ("Cocospark","+971 52 633 2035","27.03","Phone is off","","","",""),
    ("Brian Choi","+971 54 552 9537","27.03","No answer","","","",""),
    ("Kivanc","+971 50 328 2564","27.03","Phone is off","","","",""),
    ("Kirollos Samy","+971 58 573 5206","27.03","Answer","Yes","","",""),
    ("Relife Academy","+971 50 276 8831","27.03","","","","",""),
    ("Marina Nady","+971 55 355 6226","27.03","","","","",""),
    ("Bellonie","+971 52 916 5886","27.03","","","","",""),
    ("Reem Khaddam","971509158287","27.03","Answer","Yes","","","metro podcast studio"),
    ("Adan Boukra","9715847798","27.03","Answer","Yes","","",""),
    ("Vincent Ernst","+971 58 598 5530","27.03","","","","",""),
    ("Muhammed Ali Erkan","+971 52 392 1329","27.03","","","","",""),
    ("Cleo","32468340668","27.03","Answer","Yes","","",""),
    ("Wayne Malcolm","971547617788","27.03","Answer","Yes","","",""),
    ("Joseph Dinlot","971508427541","27.03","Answer","Yes","","",""),
    ("Nicholas Jowett","447498674994","27.03","No answer","","","",""),
    ("Rivals Gym","971585499212","27.03","Answer","Yes","","",""),
    ("Adrian","34689813273","27.03","No answer","","","",""),
    ("Althea","971505523948","27.03","Answer","Yes","","",""),
    ("Vlad Puscas","40787281615","27.03","Answer","Yes","","",""),
    ("Dirk Kreuter","971528895913","27.03","Answer","Yes","","",""),
    ("Mehdi Louiz","33751073266","27.03","No answer","","","",""),
    ("Jamie Innovation AI","971521522309","28.03","Answer","Yes","","","Dimension"),
    ("Hardeep","+971 55 329 4544","28.03","No answer","","","",""),
    ("Kamil Ravin","+44 7504 002199","28.03","No answer","","","",""),
    ("Pavel","971553653712","28.03","Answer","Yes","","",""),
    ("Hossam","971508899416","28.03","Answer","Yes","","",""),
    ("Rami Ismael","+45 52 36 64 79","28.03","No answer","","","",""),
    ("Charles Andrews","+971 58 561 7109","28.03","Answer","Yes","","",""),
    ("Kevin Sanz","971507289140","30.03","Answer","Yes","","",""),
    ("James Sahota","971501022533","30.03","Answer","Yes","","",""),
    ("Brinelle","971505523948","30.03","Answer","Yes","","",""),
    ("Inquiry","971506558745","30.03","Answer","Yes","","",""),
    ("Car Rentals","971503081670","30.03","Answer","Yes","","",""),
    ("Zee","971502146650","30.03","Answer","Yes","","",""),
    ("Moroccan guy","212778011586","30.03","Answer","Yes","","",""),
    ("Norman David","971569618886","30.03","Answer","Yes","","",""),
    ("Medhi","33751073266","30.03","Answer","Yes","","",""),
    ("Alex","82340110905","30.03","Answer","Yes","","",""),
    ("Javier Oliver","34662309355","30.03","Answer","Yes","","",""),
    ("Alfredo","971505312857","30.03","Answer","Yes","","",""),
    ("Maksyms","380663061995","30.03","No answer","","","",""),
    ("Revi Realty","971508288648","31.03","Answer","Yes","","",""),
    ("Kiro Ashraf","971507350420","31.03","Answer","Yes","","",""),
    ("Julia","9715011147101","31.03","Answer","Yes","","",""),
    ("Qvie","97158331202","31.03","Answer","Yes","","",""),
    ("Tony","971508589930","31.03","Answer","Yes","","",""),
    ("Danis Latypov","97150286084","31.03","Answer","Yes","","",""),
    ("Omri Ben","971566224229","31.03","Answer","Yes","","",""),
    ("Divinom Healing","971507005910","31.03","Answer","Yes","","",""),
    ("Zaid Imran","971508288648","31.03","Answer","Yes","","",""),
    ("Julia","971501147101","31.03","Answer","Yes","","",""),
    ("Sarah H","971567586587","31.03","Answer","Yes","","",""),
    ("Inquiry","971552677987","31.03","Answer","Yes","","",""),
    ("Nick","447498674994","31.03","Answer","Yes","","",""),
    ("Alaa Sawaf","971569554911","1.04","Answer","Yes","","",""),
    ("Mohamed","971564645979","1.04","Answer","Yes","","",""),
    ("Muhammad Zulfiqar","971585669028","1.04","Answer","Yes","","",""),
    ("","971585815644","1.04","No answer","","","",""),
    ("Karim Molvani","971526887589","1.04","Answer","Yes","","",""),
    ("Nick Santo","77078505587","2.04","Phone is off","","","",""),
    ("Bial","971527898783","2.04","Answer","Yes","","",""),
    ("Abdul Basit","971568677883","2.04","Answer","Yes","","",""),
    ("Nicolas Corbin","971585286351","2.04","No answer","","","",""),
    ("Spintman","31646967499","2.04","No answer","","","",""),
    ("Karen Mattar","971 52 710 1347","2.04","No answer","","","",""),
    ("SocMed byKaren","971 50 547 5910","2.04","No answer","","","",""),
    ("Houda","971505501382","2.04","No answer","","","",""),
    ("Vlad","97154299888","2.04","Answer","Yes","","",""),
    ("Uswah","971581759326","2.04","Answer","Yes","","",""),
    ("Dilip Kumar","919953800577","2.04","No answer","","","",""),
    ("Akash","447534531551","2.04","No answer","","","",""),
    ("Qvie","97158331202","2.04","Answer","Yes","","",""),
    ("Ahmet Midyat","905325576207","2.04","No answer","","","",""),
    ("Andrea","971585018298","2.04","","","","",""),
    ("Zak","971507250385","2.04","No answer","","","",""),
    ("Alex Mulder","971523014981","2.04","Phone is off","","","",""),
    ("Lucas Faria","5513991493711","2.04","No answer","","","",""),
    ("Tomi","971585475146","2.04","Answer","Yes","","",""),
    ("Karma","971505622650","3.04","No answer","","","",""),
    ("ResultMentors","9715690114552","3.04","Phone is off","","","",""),
    ("Aneeka","447517226406","3.04","No answer","","","",""),
    ("Shila","971525029741","3.04","No answer","","","",""),
    ("Ibrahim Ward","971545574375","3.04","No answer","","","",""),
    ("Step Global","971553849215","3.04","No answer","","","",""),
    ("Gabi","971559190219","3.04","Answer","","","",""),
    ("Jaymie AI company","971521522309","3.04","Answer","","","",""),
    ("Marcus Lawrence","971585983627","3.04","No answer","","","",""),
    ("Krystel Abi Assi","585521989","3.04","No answer","","","",""),
    ("Lewis Welsh","44 7921 502439","3.04","Answer","Yes","","",""),
    ("Monica Perna","+971 58 518 1846","3.04","Phone is off","","","",""),
    ("Negin","+971 58 557 7267","3.04","Answer","Yes","","",""),
    ("Danjal","+971 54 577 1432","3.04","Answer","No","in 2 weeks","did not answer",""),
    ("Jano Garro","+971 50 784 5323","3.04","No answer","","","",""),
    ("Anthony Omenya","5145061029","3.04","Phone is off","","","",""),
    ("AbdelRahman","971544578080","3.04","No answer","","","",""),
    ("Zakaria","+971 58 570 2687","3.04","Phone is off","","","",""),
    ("Pranav Kumar","+971 50 318 1421","3.04","Answer","Yes","","",""),
    ("Dirk","+971 52 889 5913","3.04","Answer","Yes","","",""),
    ("Sabrina","+971 52 381 5528","3.04","Phone is off","","","",""),
    ("Laura Roche","+971 50 274 2950","3.04","Phone is off","","","",""),
    ("Luka","+971 55 935 3922","3.04","Answer","Yes","","",""),
    ("Minoru","+34 634 10 52 47","3.04","Answer","Yes","","",""),
    ("Amedeo","+971 52 959 9614","3.04","Phone is off","","","",""),
    ("Josh Bridgman","+971 55 370 5753","3.04","Answer","Yes","","",""),
    ("Steve Cronin","+971 50 708 7260","3.04","Phone is off","","","",""),
    ("Andre","+971 50 504 3159","3.04","Answer","Yes","","",""),
    ("Sophia","+971 55 182 5620","3.04","No answer","No","","",""),
    ("Austin","+971 58 519 7604","3.04","Answer","Yes","","",""),
    ("Martina","+971 56 230 8383","3.04","No answer","","","",""),
    ("Usef Kamal","+971 56 800 1888","6.04","No answer","","","",""),
    ("Amin","+971 56 491 6536","6.04","Answer","Yes","","",""),
    ("Killian","+971 58 577 0601","6.04","No answer","","","",""),
    ("Jeremy","+971 58 199 8661","6.04","No answer","","","",""),
    ("Adrien","+971 50 733 2744","6.04","No answer","","","",""),
    ("Shona Laws","+971 56 573 4203","6.04","No answer","","","",""),
    ("Hardeep Singh","+971 55 329 4544","6.04","Phone is off","","","",""),
    ("Sam Smith","+971 58 561 7109","6.04","Phone is off","","","",""),
    ("Kamil Ravin","+44 7504 002199","6.04","No answer","","","",""),
    ("Andrew Dunbar","+971 50 450 7463","6.04","Answer","Yes","","",""),
    ("Abner Lobo","971564066116","3.04","No answer","","","",""),
    ("Sultan","971505822220","6.04","Answer","","","",""),
    ("Armaan","971585949806","6.04","Answer","","","",""),
    ("Adan Bourka","971585847798","6.04","Answer","","","",""),
    ("Abeer Abdeen","971507257622","6.04","Answer","","","",""),
    ("Melda","+971 55 628 1005","6.04","No answer","","","",""),
    ("Matias Molina","+971 50 602 6529","6.04","Phone is off","","","",""),
    ("George Hovanishan","+971 55 955 4267","6.04","No answer","","","",""),
    ("Enguerrand","+97105421183741","6.04","Phone is off","","","",""),
    ("Ramiro Cubria","+971 50 963 8915","6.04","Phone is off","","","",""),
    ("Royal Oasis","+971 55 881 5719","6.04","Answer","","","",""),
    ("Aitor Ferreria","+971 55 774 6423","6.04","Answer","","","",""),
    ("David Rupp","+971 52 898 5107","6.04","No answer","","","",""),
    ("Arthur","+971 55 636 0998","6.04","Phone is off","","","",""),
    ("Joseph Atalla","+971 52 701 1992","6.04","No answer","","","",""),
    ("MaxSell","+971 58 967 9003","6.04","Phone is off","","","",""),
    ("Julius Aeroe","+971 50 654 9368","6.04","Phone is off","","","",""),
    ("Louise Lambert","+971 55 724 8175","6.04","Answer","Yes","","",""),
    ("Trevisan Lambert","+971 58 578 4895","6.04","Phone is off","","","",""),
    ("Luke King","+44 7764 495043","6.04","","","","",""),
    ("Zeina Hassan","971529217724","6.04","Answer","Yes","","",""),
    ("Kori","+971 58 590 4610","6.04","Phone is off","","","",""),
    ("Ameer","+971 52 503 3538","6.04","No answer","","","",""),
    ("Cannelle Maricux","+971 56 665 6866","6.04","Phone is off","","","",""),
    ("Mahan Java","+971 52 415 5699","6.04","No answer","","","",""),
    ("Shubi Zaidi","+971 50 865 3039","6.04","Answer","Yes","","",""),
    ("Katie Orr","+971 56 459 8037","6.04","Phone is off","","","",""),
    ("Haris","+971 54 588 7777","6.04","Answer","Yes","","",""),
    ("Omar","971566915970","6.04","Answer","Yes","","",""),
    ("Dorian","3381653599288","6.04","Answer","Yes","","",""),
    ("Caroline","971 55 295 5634","7.04","Answer","Yes","","",""),
    ("Anil","971 55 956 4344","7.04","Answer","Yes","","",""),
    ("Jack Davy","44 7850 354241","7.04","Answer","Yes","","",""),
    ("Jaymie Amarante","971563791641","8.04","Answer","Yes","","",""),
    ("Karina","79234809298","8.04","Answer","Yes","","",""),
    ("Tehan","971569602565","8.04","Answer","Yes","","",""),
    ("Rustam","+971 50 317 0603","8.04","No answer","","","",""),
    ("Cardin Loic","+971 50 885 0696","8.04","No answer","","","",""),
    ("Lea Kiwan","+971 50 534 2114","8.04","No answer","","","",""),
    ("Leander","+971 58 667 7059","8.04","No answer","","","",""),
    ("Kevin","+971 58 559 2800","8.04","No answer","","","",""),
    ("IMPI","380507594535","8.04","Answer","Yes","","",""),
    ("S.C.","971525172205","8.04","Answer","Yes","","",""),
    ("Antonia","62881038314750","8.04","Answer","Yes","","",""),
    ("Lemya","+971 50 480 7802","9.04","Phone is off","","","",""),
    ("Hugo","+971 58 582 0173","9.04","Answer","Yes","","",""),
    ("Masun Avci","+971 55 523 3728","9.04","Phone is off","","","",""),
    ("Amin","971585431677","9.04","No answer","","","",""),
    ("Mattia Ruta","+971 58 549 4581","9.04","Phone is off","","","",""),
    ("Mohamed Murrane","+971 50 555 4707","9.04","Answer","Yes","","",""),
    ("Meghna Vadera","+971 58 507 3327","9.04","Answer","Yes","","",""),
    ("Butrus Said","+971 52 624 2712","9.04","No answer","","","",""),
    ("Alber","+971 55 990 4075","9.04","Answer","Yes","","",""),
    ("Shaheen","+971 52 420 3664","9.04","No answer","","","",""),
    ("Ayarpi","+971 56 378 4521","9.04","No answer","","","",""),
    ("River Jangda","+971 50 682 3990","9.04","Answer","Yes","","",""),
    ("Segilola","+971 58 627 6220","9.04","Phone is off","","","",""),
    ("Elie Daher","+971 50 189 1930","9.04","Answer","Yes","","",""),
    ("Zak Dhiba","+971 50 725 0385","9.04","No answer","","","",""),
    ("Majra","+971 52 382 4567","9.04","","","","",""),
    ("Gustavo","+971 56 234 1660","9.04","No answer","","","",""),
    ("Impact Nexus","+971 52 188 1237","9.04","Phone is off","","","",""),
    ("Areesh","+971 56 744 9727","9.04","No answer","","","",""),
    ("Alyssa Bagatsing","971567494715","9.04","Answer","Yes","","",""),
    ("Lana Almatt","962798496572","9.04","Answer","Yes","","",""),
    ("James Sellu","447984404213","9.04","Answer","Yes","","",""),
    ("Estate Invest","971581662024","9.04","Answer","Yes","","",""),
    ("Martin","971542553337","9.04","Answer","Yes","","",""),
    ("Shivani","971557976203","9.04","No answer","","","",""),
    ("Adham Kemel","971 50 940 0519","9.04","Answer","Yes","","",""),
    ("Omar Ghanem","971566915970","11.04","No answer","","","",""),
    ("Hardeep","971553294544","11.04","Phone is off","","","",""),
    ("Yaser Alhmoudi","971 52 800 0065","11.04","No answer","","","",""),
    ("Kori","971585904610","11.04","Phone is off","","","",""),
    ("Ibrahim Alkurd","971508267043","11.04","No answer","","","",""),
    ("Kamil Marciszewski","971 58 584 2787","11.04","No answer","","","",""),
    ("Alex","971585006591","11.04","Answer","Yes","","",""),
    ("Joshua Kaats","971 55 955 4267","11.04","Phone is off","","","",""),
    ("Florian","971561633955","11.04","Answer","Yes","","",""),
    ("Colins","971501193536","11.04","Phone is off","","","",""),
    ("Mark","447920883667","11.04","No answer","","","",""),
    ("Bryan","971504840593","11.04","No answer","","","",""),
    ("Mattia","971 52 704 3700","11.04","Phone is off","","","",""),
    ("Drew","971525780160","11.04","No answer","","","",""),
    ("Anas","923098487100","11.04","Phone is off","","","",""),
    ("Adam","971585976402","11.04","Phone is off","","","",""),
    ("Sandra Shediak","971 54 995 7747","11.04","Answer","You","","","https://www.imventstudios.com/"),
    ("David Bragg","971 50 848 6004","11.04","No answer","","","",""),
    ("Adrian","971509860193","11.04","No answer","","","",""),
    ("James Selu","971 50 935 8513","11.04","Answer","Yes","","",""),
    ("Mohamed","971569732794","13.04","Phone is off","","","",""),
    ("Saad El Soussi","971585590040","13.04","No answer","","","",""),
    ("Borawi Hajri","971 50 272 0550","13.04","Answer","","","",""),
    ("Vincent Istrael","971521335493","13.04","Answer","Yes","","",""),
    ("Melissa","971 55 713 6203","13.04","Phone is off","","","",""),
    ("Alina Ratusnyak","971 58 598 0295","13.04","Phone is off","","","",""),
    ("Kyran O'neil","971 58 510 5778","13.04","Answer","Yes","","",""),
    ("Manoah","33 6 45 39 52 16","13.04","","","","",""),
    ("Hamid Al Ali","971 55 420 0779","13.04","Answer","No","","Abu Dhabi",""),
    ("Agathe Krotky","971 58 589 5200","13.04","","","","",""),
    ("Philip Pich","61 424 871 982","13.04","No answer","","","",""),
    ("Aitor Galvez","34 693 77 33 35","13.04","","","","",""),
    ("Marko","971 58 590 5126","13.04","Phone is off","","","",""),
    ("Tom","971 55 684 1993","13.04","Answer","Yes","","",""),
    ("Lurii","971 50 234 0725","13.04","Answer","Yes","","",""),
    ("David Wunderink","31 6 18357181","13.04","","","","",""),
    ("Anthony Trevisan","33 7 72 13 56 35","13.04","","","","",""),
    ("Zak","971 50 725 0385","13.04","No answer","","","",""),
    ("Sophia Delavari","971 55 182 5620","13.04","Phone is off","","","",""),
    ("Stone Invest","971 50 126 7249","13.04","","","","",""),
    ("Moayad Fahmawi","971 55 552 3507","13.04","No answer","","","",""),
    ("Andrey Siridenko","971 54 388 3224","13.04","No answer","","","",""),
    ("Amin","971 56 491 6536","13.04","Answer","Yes","","",""),
    ("Vikash Morjaria","971 50 945 8811","13.04","Answer","Yes","","",""),
    ("Mohamed Almarzoqou","1 (303) 667-8764","13.04","","","","",""),
    ("Anas","39 351 312 3765","13.04","Phone is off","","","",""),
    ("Nico","49 1515 3583580","13.04","No answer","","","",""),
    ("Javier Angoso","49 162 7800631","13.04","No answer","No","","Spain",""),
    ("Tarek Berjaoui","971 58 678 2050","13.04","Answer","Yes","","",""),
    ("Deepak Sharma","1 (786) 710-1470","13.04","","","","",""),
    ("Othmane","971 52 316 1654","13.04","Phone is off","","","",""),
    ("Nicola Napolitano","971 52 575 1968","13.04","Phone is off","","","",""),
    ("River Jangda","971 50 682 3990","13.04","Answer","Yes","","",""),
    ("Hamid Kennou","971 54 393 9752","13.04","No answer","","","",""),
    ("Niggi","971566789176","13.04","Answer","Yes","","",""),
    ("Mariam","971585409986","13.04","Answer","Yes","","",""),
    ("Ali","971582654607","13.04","Answer","Yes","","",""),
    ("Cynthia Chong","971553588660","13.04","Answer","Yes","","",""),
    ("Yaz","971507994352","13.04","Answer","Yes","","",""),
    ("Nikki Cowell","971585522109","13.04","Answer","Yes","","",""),
    ("GVTM","50760585006591","14.04","Answer","No","","Panama",""),
    ("Tan","+971 58 593 7071","14.04","Phone is off","","","",""),
    ("Erika Jane","+63 908 758 0457","14.04","Phone is off","","","",""),
    ("Iwona Laub","+971 56 803 8887","14.04","Answer","Yes","","","procast studio"),
    ("Calvin","+971 55 457 6577","14.04","Phone is off","","","",""),
    ("Mia","+1 203-228-4715","14.04","Phone is off","","","",""),
    ("Daniel","2029776754","14.04","Phone is off","","","",""),
    ("Dasha Adrianova","+971 58 817 7123","14.04","Phone is off","","","",""),
    ("Sarah","+971 58 520 9029","14.04","Answer","Yes","","",""),
    ("Ahmet","+90 532 557 62 07","14.04","Answer","","","",""),
    ("Brahim","+971 55 912 8574","14.04","Phone is off","","","",""),
    ("Kuldeep","+44 7779 536211","14.04","No answer","","","",""),
    ("Davit","+49 1512 1899255","14.04","Answer","No","","Germany",""),
    ("Dilip Kumar","+47 93 98 52 77","14.04","No answer","","","",""),
    ("Roussel Hugo","+33 6 23 33 49 96","14.04","Answer","","","",""),
    ("Priyanjali Guha","+39 329 079 2014","14.04","Answer","No","","France",""),
    ("Amir","+971 58 501 3255","14.04","No answer","","","",""),
    ("Irah Samantha Mellijor","+971 56 314 7908","14.04","Phone is off","","","",""),
    ("Erik","+376 668 011","14.04","Phone is off","","","",""),
    ("Kristine Adante","971561703874","14.04","Answer","Yes","","",""),
    ("Rania Shamas","971506966046","14.04","Phone is off","","","",""),
    ("Alice Maudret","33664870732","14.04","No answer","","","",""),
    ("Danil Vasyukov","971 55 589 8027","14.04","Phone is off","","","",""),
    ("Robin Bouman","31 6 48532015","14.04","No answer","","","",""),
    ("Eduardo Barrecheguren","971 58 502 3899","14.04","Phone is off","","","",""),
    ("Tuomas Kivioja","971564982660","14.04","No answer","","","",""),
    ("Medhi Souci","33786917519","14.04","No answer","","","",""),
    ("Roslan","971 54 291 8992","14.04","Phone is off","","","",""),
    ("Ibrahim Igbarie","971521885659","14.04","No answer","","","",""),
    ("Victor Bazil","971 56 555 8806","14.04","No answer","","","",""),
    ("Mustafa Fashir","971585448172","14.04","No answer","","","",""),
    ("Farjah","971585775709","14.04","Answer","Yes","","",""),
    ("Jody Cavali","971585273608","14.04","No answer","","","",""),
    ("Gaspard","971 55 756 9011","14.04","No answer","","","",""),
    ("Mr Isaac","971554211379","14.04","Phone is off","","","",""),
    ("Mohammed","971545653758","14.04","","","","",""),
    ("Nathan","971 52 603 8327","14.04","Phone is off","","","",""),
    ("Aladin Gasanin","971547786494","14.04","Phone is off","","","",""),
    ("Aashna","971 58 578 2726","14.04","Phone is off","","","",""),
    ("Namrata","971558968618","14.04","No answer","","","",""),
    ("Yuyu","971 55 959 7448","14.04","No answer","","","",""),
    ("Servane Collete","971 50 699 5950","14.04","No answer","","","",""),
    ("Tamer","971 54 457 8080","14.04","No answer","","","",""),
    ("Sufian","971509241414","14.04","No answer","","","",""),
    ("Pablo Ginestar","34 674 49 47 56","14.04","Phone is off","","","",""),
    ("Khaled Mohamed","971 50 991 3621","14.04","","","","",""),
    ("Polina Sybina","058 547 2434","14.04","Answer","Yes","","",""),
    ("Sherry Faller","971 58 669 0809","14.04","No answer","","","",""),
    ("NEV real estate","971564049750","14.04","Phone is off","","","",""),
    ("Ralph Haddad","971568547799","14.04","Answer","Yes","","",""),
    ("Matjaz Vidmar","971 58 561 9840","14.04","Answer","No","","",""),
    ("Til Lichtinger","49 172 9041469","14.04","Phone is off","","","",""),
    ("Gary Blowers","971 55 795 7053","14.04","No answer","","","",""),
    ("Rebien","37254353609","14.04","Phone is off","","","",""),
    ("Hidde","31 6 40223557","14.04","Phone is off","","","",""),
    ("Iclicksee fzco","+971 54 533 3089","14.04","Phone is off","","","",""),
    ("Dennis","+49 1511 4169166","14.04","Phone is off","","","",""),
    ("Luca","+971 52 776 1774","14.04","Phone is off","","","",""),
    ("Sabri","+971 58 534 5874","14.04","Answer","Yes","","",""),
    ("Alexis","+33 6 18 59 79 30","14.04","No answer","","","",""),
    ("Rami","+971 50 708 4732","14.04","Answer","Yes","","",""),
    ("Mariam","+971 50 838 3839","14.04","No answer","","","",""),
    ("Guoda","+971 55 431 6611","14.04","Answer","No","","",""),
    ("Brand","+1 469-461-4333","14.04","Answer","No","","Texas",""),
    ("Quentin","+971 56 778 1399","14.04","Answer","Yes","","",""),
    ("Alena","+971 52 409 2165","14.04","Answer","Yes","","",""),
    ("Youssef","+971 55 773 7960","14.04","Answer","Yes","","",""),
    ("Soheil","+1 416-455-8709","14.04","No answer","","","",""),
    ("Skye","+971 58 593 3581","15.04","Phone is off","","","",""),
    ("John","+971 50 829 3979","15.04","Answer","Yes","","",""),
    ("Irina","+971 58 670 7002","15.04","Phone is off","","","",""),
    ("Pallavi","+971 58 949 2461","15.04","Answer","Yes","","",""),
    ("Charlie","+971 58 568 1810","15.04","Answer","Yes","","",""),
    ("Alexey","9630407512","15.04","Phone is off","","","",""),
    ("Emile","+97156246191","15.04","Phone is off","","","",""),
    ("Ahmad","+971 54 573 5515","15.04","Answer","Yes","","",""),
    ("Wei Shaun","+60 17-253 9171","15.04","No answer","","","",""),
    ("Roman","+971 56 939 9953","15.04","Answer","Yes","","",""),
    ("Lazreg","+971 52 953 5328","15.04","Phone is off","","","",""),
    ("Mohamed","+971 55 150 0200","15.04","","","","",""),
    ("Rachid","+971 58 507 9495","15.04","No answer","","","",""),
    ("Zena","+1506165720","15.04","Phone is off","","","",""),
    ("Nabil","+971 50 767 5812","15.04","No answer","","","",""),
    ("Fraser","+44 7531 090912","15.04","No answer","","","",""),
    ("Najma","+971 58 553 9438","15.04","Phone is off","","","",""),
    ("Sofiane","+971 58 548 0298","15.04","No answer","","","",""),
    ("Devaux","+971 56 372 6552","15.04","Phone is off","","","",""),
    ("Corinna","+971 56 861 0024","15.04","No answer","","","",""),
    ("Saba","+971 52 746 4336","15.04","Answer","","","",""),
    ("Roland","+971 56 385 3146","15.04","Answer","No","","",""),
    ("Kareem","+971 50 168 7608","15.04","Phone is off","","","",""),
    ("Gachar","+971 58 599 3683","15.04","Phone is off","","","",""),
    ("Elias","+971 58 583 6211","15.04","No answer","","","",""),
    ("Dori","+971 50 347 7151","15.04","Answer","Yes","","",""),
    ("Salim","+971 52 220 0094","15.04","Answer","Yes","","",""),
    ("ANNA MARIA","+34 655 86 97 84","15.04","No answer","","","",""),
    ("Lucatelli","+39 388 936 9290","15.04","No answer","","","",""),
    ("Gary","+97158561144","15.04","Phone is off","","","",""),
    ("Bachir","561367514","15.04","No answer","","","",""),
    ("Dr. Azri","+44 7593 323385","15.04","Answer","Yes","","",""),
    ("Ch ali","+971 58 265 4607","15.04","Answer","Yes","","",""),
    ("Evgeniya","+7 916 735-14-74","15.04","No answer","","","",""),
    ("Ahmad","+9715620515757","15.04","Phone is off","","","",""),
    ("Moustafa","+971 50 384 0619","15.04","Phone is off","","","",""),
    ("Ivan","+971 58 564 3883","15.04","No answer","","","",""),
    ("Gabriel","+971 58 531 0304","15.04","No answer","","","",""),
    ("Ruslan","+971 56 155 4075","15.04","No answer","","","",""),
    ("Jonathan","+971 58 530 6163","15.04","No answer","","","",""),
    ("Patrick","506228659","23.04","No answer","","","",""),
    ("Basel","97332323939","23.04","Answer","No","no schedule yet","Bahrain",""),
    ("Nour","+971 58 118 7459","23.04","Phone is off","","","",""),
    ("Yousef","+971 52 300 6375","23.04","No answer","","","",""),
    ("Tatiana","+971 54 411 2174","23.04","No answer","","","",""),
    ("CAPSULE CORP","34648155195","23.04","No answer","","","",""),
    ("Jim","+971 56 977 3511","23.04","No answer","","","",""),
    ("Danny","+971 50 117 0458","23.04","Answer","Yes","","",""),
    ("Lewis","+971 54 734 7960","23.04","Phone is off","","","",""),
    ("Mahreen","+971 56 368 8898","23.04","Answer","Yes","","",""),
    ("Mohammad","+971 50 941 6800","23.04","No answer","","","",""),
    ("Egor","+971 58 522 0052","23.04","Answer","Yes","","",""),
    ("Farah","+971 56 345 9337","23.04","No answer","","","",""),
    ("James","+971 52 999 9055","23.04","No answer","","","",""),
    ("Philipp","+971 58 554 3600","23.04","Phone is off","","","",""),
    ("Maksim","+47 97 41 44 24","23.04","No answer","","","",""),
    ("Diana","+971 58 594 5809","23.04","Phone is off","","","",""),
    ("Mouadh","+971 58 589 8417","23.04","Phone is off","","","",""),
    ("Advantage Exam Preparation","+44 7599 675382","23.04","Answer","No","no schedule yet","UK",""),
    ("Alber","+971 55 990 4075","23.04","Answer","Yes","","",""),
    ("LG-Ecom","+33 6 28 93 20 03","23.04","No answer","","","",""),
    ("George","+33 7 87 05 26 49","23.04","No answer","","","",""),
    ("Maik","+49 1514 1666868","23.04","Answer","Yes","he didn't know yet","Germany",""),
    ("Joseph","+971 52 701 1992","23.04","No answer","","","",""),
    ("Jordan","+972 53-708-1161","23.04","Phone is off","","","",""),
    ("Antoine","+971 58 532 1859","23.04","Phone is off","","","",""),
    ("Yusuf","+971 58 161 9933","23.04","Answer","Yes","","",""),
    ("MaxSell","+971 58 967 9003","23.04","No answer","","","",""),
    ("Nikolett","542183001","23.04","Phone is off","","","",""),
    ("Namsheed","+973 3417 1888","23.04","Answer","No","no schedule yet","Bahrain",""),
    ("Julius","+971 50 654 9368","23.04","Phone is off","","","",""),
    ("Espace","+33 6 47 48 95 26","23.04","Phone is off","","","",""),
    ("Louise","+971 55 724 8175","23.04","Answer","Yes","","",""),
    ("sarah","+971 58 542 5826","23.04","Answer","Yes","","","Podster"),
    ("BR","+971 52 264 4249","23.04","Phone is off","","","",""),
    ("Khaled","+971 50 991 3621","23.04","No answer","","","",""),
    ("George","+971 50 238 7280","23.04","No answer","","","",""),
    ("TREVISAN","+971 58 578 4895","23.04","Phone is off","","","",""),
    ("Luke","+44 7764 495043","23.04","No answer","","","",""),
    ("Kori","+971 58 590 4610","23.04","Phone is off","","","",""),
    ("Katia","+971 58 979 3486","23.04","Answer","No","she didn't want to answer","",""),
    ("Ameer","+971 52 503 3538","23.04","No answer","","","",""),
    ("CANNELLE","+971 56 665 6866","23.04","Phone is off","","","",""),
    ("Hamid Al","+971 50 388 5642","23.04","Answer","Yes","","",""),
    ("Mahan","+971 52 415 5699","23.04","No answer","","","",""),
    ("Shubi","+971 50 865 3039","23.04","Answer","Yes","","",""),
    ("Katie","+971 56 459 8037","23.04","Phone is off","","","",""),
    ("Haris","+971 54 588 7777","23.04","Answer","Yes","","",""),
    ("Mitchell","+1 919-236-9803","23.04","No answer","","","",""),
    ("Michaela","+971 58 880 1490","23.04","Phone is off","","","",""),
    ("Clue","+971 55 334 3790","23.04","Answer","No","1st week of May","Egypt",""),
    ("billy","+971 56 293 8798","23.04","Answer","No","who knows, no definite date","Europe",""),
    ("Kyran","+971 58 510 5778","23.04","No answer","","","",""),
    ("Poppy","+971 58 546 2649","23.04","No answer","","","",""),
    ("Nicola","+971 52 110 0425","23.04","No answer","","","",""),
    ("Ahmad Samhan","799288881111","23.04","Answer","No","maybe september","Russia",""),
    ("Gaillan","971552755882","23.04","Answer","Yes","","",""),
    ("Dan Ngo","61412764845","23.04","Answer","Yes","","",""),
    ("Mufida","971526786442","23.04","Answer","Yes","","",""),
    ("Makh","971585407009","23.04","Answer","Yes","","",""),
    ("Anzhelika","375296106800","25.04","Answer","","","",""),
    ("Jeremy","+971 58 199 8661","25.04","No answer","","","",""),
    ("Adrien","+971 50 733 2744","25.04","No answer","","","",""),
    ("Georgiana","+971 58 582 6831","25.04","Answer","Yes","she just got back few days ago","",""),
    ("Sohaib","+971 58 557 8685","25.04","Answer","Yes","","",""),
    ("Jess","+971 52 748 8494","25.04","Answer","Yes","","",""),
    ("Nim","+971 50 305 2531","25.04","Answer","Yes","","",""),
    ("Eva","+971 50 498 1445","25.04","Answer","Yes","","",""),
    ("Neerav","507739084","25.04","Answer","Yes","","",""),
    ("Arun","447841194919","4.05","Answer","No","no sched yet","UK",""),
    ("Wanner Aarts","31642703282","4.05","Answer","No","later this year","Bali",""),
    ("Wesley Van Der Male","4741333105","4.05","Answer","No","this weekend","",""),
    ("Vera Firman","971585189766","4.05","Answer","No","end of June","",""),
    ("Gael Angouola","2250574038383","4.05","Answer","Yes","","",""),
    ("Stefan","491736487563","5.05","Answer","","","",""),
    ("Saeed Altamimi","971501996964","5.05","Answer","","","",""),
    ("Mark Strathern","447883669244","5.05","Answer","","","",""),
    ("Antoine Blanco","971585321859","5.05","Answer","","","",""),
    ("Paul Welch","447787535992","5.05","Answer","No","","London",""),
    ("Kevin","6583676782","5.05","Answer","No","","Singapore",""),
    ("Sabita Rajesh","9713578437","6.05","Answer","Yes","","",""),
    ("Hilal Medini","971 58 624 7584","","Answer","No","","Morocco",""),
    ("Sarah","971585425826","5.05","Answer","Yes","","",""),
    ("Hassine Elgharbi","971581093859","6.05","Answer","","","",""),
    ("Bilal","33683763279","6.05","Answer","Yes","","","Upod"),
    ("Faiz","971552400115","7.05","Answer","Yes","","",""),
    ("Schenelle","971509277832","7.05","Answer","Yes","","",""),
    ("George Skimmer","971585534287","7.05","Answer","Yes","","",""),
    ("Houda Abdulrahman","971 50 550 1382","7.05","Answer","","","",""),
    ("Gabriela Tomaskova","971 52 156 8546","7.05","Answer","Yes","","",""),
    ("Marianne Munoz","971 52 114 8707","7.05","Answer","Yes","","",""),
    ("Anna Ursalova","971 58 511 2906","7.05","Answer","Yes","","",""),
    ("Yehia","971555092346","8.05","Answer","Yes","","",""),
    ("Viktor","79832733763","8.05","Answer","Yes","","",""),
    ("Nadia Bissar","971551122240","8.05","Answer","Yes","","",""),
    ("Ritu","971555743879","8.05","Answer","Yes","","",""),
    ("Lisa","971501381436","8.05","Answer","Yes","","",""),
    ("Salvatore","971554394103","8.05","Answer","Yes","","",""),
    ("Nasif","971507895810","8.05","Answer","Yes","","",""),
    ("Ishaqh Mohamed","971525230750","8.05","Answer","Yes","","",""),
    ("Moez Khelifi","971553208419","8.05","Answer","Yes","","",""),
    ("Karim Ibrahim","971524147798","8.05","Answer","Yes","","",""),
    ("Ali Mac","971568577148","8.05","Answer","Yes","","",""),
    ("Kholoud","971506776743","8.05","Answer","Yes","","",""),
    ("Mohamed Ayman","971589378139","8.05","Answer","Yes","","",""),
    ("Dominique","436603733587","8.05","Answer","No","","",""),
    ("Puja Tiwar","971585981991","8.05","Answer","Yes","","",""),
    ("Hicham El Amrani","971529957792","8.05","Answer","Yes","","",""),
    ("Farah Hassan","971563459337","8.05","Answer","","","",""),
    ("Suzana","971552750542","8.05","Answer","","","",""),
    ("Santiago Amado","971588400196","8.05","Answer","","","",""),
    ("Rayan","971585562464","8.05","Answer","","","",""),
    ("Conor Healey","971505901820","11.05","Answer","","","",""),
    ("Francois","97155951470","11.05","Answer","","","",""),
    ("Deepesh Sanduja","61410184708","11.05","Answer","","","",""),
    ("Clement Talmo","33624835980","12.05","Answer","Yes","","",""),
    ("Soufiane","971585997267","13.05","Answer","Yes","","",""),
    ("Melissa Jeffrey","447769179643","13.05","Answer","Yes","","",""),
    ("Dina Alhamdan","971525165235","13.05","Answer","Yes","","",""),
    ("Olga","971565485089","13.05","Answer","Yes","","",""),
    ("Bint Azad","971508898015","13.05","Answer","Yes","","",""),
    ("Adham Kamel","9719400519","13.05","Answer","Yes","","",""),
    ("Wafa","971509128925","13.05","Answer","Yes","","",""),
    ("Roza","971505937035","13.05","Answer","Yes","","",""),
    ("Anandhu Rajaji","971508016296","13.05","Answer","Yes","","",""),
    ("Elshafey","971569801749","13.05","Answer","Yes","","",""),
    ("Antoine","971503056672","13.05","Answer","Yes","","",""),
    ("Usama Wali","971558290124","13.05","Answer","Yes","","",""),
    ("Abu Yassin","9715855390040","13.05","Answer","Yes","","",""),
    ("Nazia","18609389429","14.05","Answer","Yes","","",""),
    ("Alaa Sawaf","971569554911","","Answer","Yes","","",""),
    ("Asma Ahmad","971507249096","","Answer","Yes","","",""),
    ("Mia","12032284715","","Answer","Yes","","LA",""),
    ("Radwa Elattar","971553343790","","Answer","Yes","","",""),
    ("Denise (Jaqui's PA)","447469155610","","Answer","No","next week","UK",""),
]

cols = ["name","phone","date","call_status","in_dubai","return_when","country","studio"]
df = pd.DataFrame(raw, columns=cols)

# ── NORMALISE ────────────────────────────────────────────────────────────────
def norm_status(s):
    s = str(s).strip().lower()
    if s in ("answer","answered"): return "Answer"
    if "off" in s: return "Phone Off"
    if "no answer" in s: return "No Answer"
    return "Unknown/Blank"

def norm_dubai(s):
    s = str(s).strip().lower()
    if s in ("yes","you"): return "In Dubai"
    if s == "no": return "Not in Dubai"
    return "Unknown"

df["status"] = df["call_status"].apply(norm_status)
df["dubai_status"] = df["in_dubai"].apply(norm_dubai)

# ── STATS ────────────────────────────────────────────────────────────────────
total = len(df)
status_counts = df["status"].value_counts()
answered = status_counts.get("Answer", 0)
no_ans = status_counts.get("No Answer", 0)
phone_off = status_counts.get("Phone Off", 0)
unknown = status_counts.get("Unknown/Blank", 0)

answered_df = df[df["status"] == "Answer"]
dubai_counts = answered_df["dubai_status"].value_counts()
in_dubai = dubai_counts.get("In Dubai", 0)
not_dubai = dubai_counts.get("Not in Dubai", 0)
dubai_unknown = dubai_counts.get("Unknown", 0)

# Countries of non-Dubai clients
not_in_dubai_df = answered_df[answered_df["dubai_status"] == "Not in Dubai"]
countries = not_in_dubai_df["country"].replace("", "Not Specified").value_counts()

# Studios
studios = df[df["studio"].str.strip() != ""]["studio"].value_counts()

# Daily call volume
df["date_clean"] = df["date"].str.replace(r"[,\s]","",regex=True)
date_map = {
    "23.03":"Mar 23","24.03":"Mar 24","25.03":"Mar 25","26.03":"Mar 26","27.03":"Mar 27",
    "28.03":"Mar 28","30.03":"Mar 30","31.03":"Mar 31","1.04":"Apr 1","2.04":"Apr 2",
    "3.04":"Apr 3","6.04":"Apr 6","7.04":"Apr 7","8.04":"Apr 8","9.04":"Apr 9",
    "11.04":"Apr 11","13.04":"Apr 13","14.04":"Apr 14","15.04":"Apr 15","23.04":"Apr 23",
    "25.04":"Apr 25","4.05":"May 4","5.05":"May 5","6.05":"May 6","7.05":"May 7",
    "8.05":"May 8","11.05":"May 11","12.05":"May 12","13.05":"May 13","14.05":"May 14",
}
df["date_label"] = df["date_clean"].map(date_map).fillna("Other")
daily = df.groupby("date_label")["status"].value_counts().unstack(fill_value=0)

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────
C_DARK   = "#1a1a2e"
C_MID    = "#16213e"
C_ACCENT = "#e94560"
C_GOLD   = "#f5a623"
C_GREEN  = "#27ae60"
C_BLUE   = "#2980b9"
C_GREY   = "#7f8c8d"
C_LIGHT  = "#ecf0f1"

# ── HELPER: save fig to BytesIO ───────────────────────────────────────────────
def fig_to_img(fig, dpi=150):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Call Status Donut
# ═══════════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5,4), facecolor=C_DARK)
ax1.set_facecolor(C_DARK)
labels1 = ["Answered","No Answer","Phone Off","Unknown/Blank"]
vals1   = [answered, no_ans, phone_off, unknown]
clrs1   = [C_GREEN, C_ACCENT, C_GOLD, C_GREY]
wedges, texts, autotexts = ax1.pie(
    vals1, labels=None, colors=clrs1, autopct="%1.1f%%",
    startangle=140, pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor=C_DARK, linewidth=2))
for t in autotexts:
    t.set_color("white"); t.set_fontsize(9); t.set_fontweight("bold")
ax1.legend(wedges, [f"{l} ({v})" for l,v in zip(labels1,vals1)],
           loc="lower center", bbox_to_anchor=(0.5,-0.12),
           ncol=2, fontsize=8, frameon=False,
           labelcolor="white")
ax1.set_title("Call Status Breakdown", color="white", fontsize=12, fontweight="bold", pad=10)
buf1 = fig_to_img(fig1); plt.close(fig1)

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Dubai Status (of answered)
# ═══════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5,4), facecolor=C_DARK)
ax2.set_facecolor(C_DARK)
labels2 = ["In Dubai","Not in Dubai","Unknown"]
vals2   = [in_dubai, not_dubai, dubai_unknown]
clrs2   = [C_BLUE, C_ACCENT, C_GREY]
wedges2, texts2, auto2 = ax2.pie(
    vals2, labels=None, colors=clrs2, autopct="%1.1f%%",
    startangle=90, pctdistance=0.75,
    wedgeprops=dict(width=0.5, edgecolor=C_DARK, linewidth=2))
for t in auto2:
    t.set_color("white"); t.set_fontsize(9); t.set_fontweight("bold")
ax2.legend(wedges2, [f"{l} ({v})" for l,v in zip(labels2,vals2)],
           loc="lower center", bbox_to_anchor=(0.5,-0.12),
           ncol=2, fontsize=8, frameon=False, labelcolor="white")
ax2.set_title("Client Location (Answered Only)", color="white", fontsize=12, fontweight="bold", pad=10)
buf2 = fig_to_img(fig2); plt.close(fig2)

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Countries of absent clients
# ═══════════════════════════════════════════════════════════════════════════════
top_countries = countries.head(10)
fig3, ax3 = plt.subplots(figsize=(7,4), facecolor=C_DARK)
ax3.set_facecolor(C_DARK)
bars = ax3.barh(top_countries.index[::-1], top_countries.values[::-1],
               color=C_ACCENT, edgecolor=C_DARK)
for bar, val in zip(bars, top_countries.values[::-1]):
    ax3.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
             str(val), va="center", color="white", fontsize=9)
ax3.set_xlabel("Clients", color=C_LIGHT, fontsize=9)
ax3.set_title("Absent Clients by Country", color="white", fontsize=12, fontweight="bold")
ax3.tick_params(colors=C_LIGHT, labelsize=9)
ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_color(C_GREY); ax3.spines["left"].set_color(C_GREY)
ax3.set_xlim(0, top_countries.values.max()*1.25)
buf3 = fig_to_img(fig3); plt.close(fig3)

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4 — Daily call activity
# ═══════════════════════════════════════════════════════════════════════════════
date_order = [v for v in date_map.values() if v in df["date_label"].values]
daily2 = df[df["date_label"].isin(date_order)].groupby("date_label")["status"].value_counts().unstack(fill_value=0)
daily2 = daily2.reindex(date_order, fill_value=0)

fig4, ax4 = plt.subplots(figsize=(12,4), facecolor=C_DARK)
ax4.set_facecolor(C_DARK)
x = np.arange(len(daily2.index))
w = 0.25
for i,(col,clr) in enumerate(zip(["Answer","No Answer","Phone Off"],[C_GREEN,C_ACCENT,C_GOLD])):
    if col in daily2.columns:
        ax4.bar(x+i*w, daily2[col], w, label=col, color=clr, alpha=0.85)
ax4.set_xticks(x+w)
ax4.set_xticklabels(daily2.index, rotation=45, ha="right", color=C_LIGHT, fontsize=7)
ax4.set_ylabel("# Contacts", color=C_LIGHT, fontsize=9)
ax4.set_title("Daily Call Activity (Mar – May)", color="white", fontsize=12, fontweight="bold")
ax4.tick_params(colors=C_LIGHT)
ax4.legend(frameon=False, labelcolor="white", fontsize=8)
ax4.spines["top"].set_visible(False); ax4.spines["right"].set_visible(False)
ax4.spines["bottom"].set_color(C_GREY); ax4.spines["left"].set_color(C_GREY)
buf4 = fig_to_img(fig4); plt.close(fig4)

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Return timeline segmentation
# ═══════════════════════════════════════════════════════════════════════════════
def classify_return(row):
    ret = str(row["return_when"]).strip().lower()
    if row["dubai_status"] != "Not in Dubai": return None
    if ret in ("","nan","did not answer"): return "Unspecified"
    if any(k in ret for k in ["not anymore","not coming","never"]): return "Lost Client"
    if any(k in ret for k in ["weekend","week","april","may","few days","saturday","this week","soon"]): return "Short-term (<1 mo)"
    if any(k in ret for k in ["month","june","july"]): return "Mid-term (1–3 mo)"
    if any(k in ret for k in ["september","later this year","5 months"]): return "Long-term (3+ mo)"
    return "No Definite Date"

not_in_dubai_df2 = answered_df[answered_df["dubai_status"] == "Not in Dubai"].copy()
not_in_dubai_df2["return_seg"] = not_in_dubai_df2.apply(classify_return, axis=1)
ret_seg = not_in_dubai_df2["return_seg"].value_counts()

fig5, ax5 = plt.subplots(figsize=(6,4), facecolor=C_DARK)
ax5.set_facecolor(C_DARK)
seg_colors = {"Short-term (<1 mo)":C_GREEN,"Mid-term (1–3 mo)":C_GOLD,
              "Long-term (3+ mo)":C_ACCENT,"No Definite Date":C_GREY,
              "Unspecified":"#8e44ad","Lost Client":"#c0392b"}
clrs5 = [seg_colors.get(k, C_GREY) for k in ret_seg.index]
ax5.bar(ret_seg.index, ret_seg.values, color=clrs5, edgecolor=C_DARK)
ax5.set_xticklabels(ret_seg.index, rotation=20, ha="right", color=C_LIGHT, fontsize=8)
ax5.set_ylabel("Clients", color=C_LIGHT, fontsize=9)
ax5.set_title("Absent Clients: Return Timeline", color="white", fontsize=12, fontweight="bold")
ax5.tick_params(colors=C_LIGHT)
ax5.spines["top"].set_visible(False); ax5.spines["right"].set_visible(False)
ax5.spines["bottom"].set_color(C_GREY); ax5.spines["left"].set_color(C_GREY)
for i,(idx,val) in enumerate(ret_seg.items()):
    ax5.text(i, val+0.1, str(val), ha="center", color="white", fontsize=9, fontweight="bold")
buf5 = fig_to_img(fig5); plt.close(fig5)

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ═══════════════════════════════════════════════════════════════════════════════
pdf_path = "/home/user/ABD-BND/Dubai_Podcast_Studio_Marketing_Report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        leftMargin=1.5*cm, rightMargin=1.5*cm,
                        topMargin=1.5*cm, bottomMargin=1.5*cm)

styles = getSampleStyleSheet()
W = A4[0] - 3*cm

def style(name, parent="Normal", **kwargs):
    s = ParagraphStyle(name, parent=styles[parent], **kwargs)
    return s

S_title    = style("title2",    fontSize=22, textColor=colors.HexColor(C_ACCENT),
                   spaceAfter=4, fontName="Helvetica-Bold", alignment=TA_CENTER)
S_sub      = style("sub",       fontSize=11, textColor=colors.HexColor(C_GOLD),
                   spaceAfter=2, fontName="Helvetica-Bold", alignment=TA_CENTER)
S_date     = style("date",      fontSize=9,  textColor=colors.HexColor(C_GREY),
                   spaceAfter=12, alignment=TA_CENTER)
S_h2       = style("h2",        fontSize=13, textColor=colors.HexColor(C_GOLD),
                   spaceBefore=14, spaceAfter=4, fontName="Helvetica-Bold")
S_h3       = style("h3",        fontSize=10, textColor=colors.HexColor(C_ACCENT),
                   spaceBefore=8, spaceAfter=3, fontName="Helvetica-Bold")
S_body     = style("body",      fontSize=9,  textColor=colors.HexColor(C_LIGHT),
                   spaceAfter=4, leading=14)
S_bullet   = style("bullet2",   fontSize=9,  textColor=colors.HexColor(C_LIGHT),
                   spaceAfter=3, leading=14, leftIndent=12, bulletIndent=0)
S_kpi_val  = style("kpiv",      fontSize=26, textColor=colors.HexColor(C_ACCENT),
                   alignment=TA_CENTER, fontName="Helvetica-Bold")
S_kpi_lbl  = style("kpil",      fontSize=8,  textColor=colors.HexColor(C_GREY),
                   alignment=TA_CENTER)

story = []

# ── COVER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("DUBAI PODCAST STUDIO", S_title))
story.append(Paragraph("Client Database — Marketing Intelligence Report", S_sub))
story.append(Paragraph("Reporting Period: March 23 – May 14, 2025  |  Generated: May 15, 2025", S_date))
story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor(C_ACCENT)))
story.append(Spacer(1, 0.4*cm))

# ── EXEC SUMMARY ─────────────────────────────────────────────────────────────
story.append(Paragraph("EXECUTIVE SUMMARY", S_h2))
story.append(Paragraph(
    f"Between <b>March 23 and May 14, 2025</b>, the studio assistant completed a full outreach "
    f"campaign across <b>{total} client contact records</b>. The exercise was specifically designed "
    f"to gauge the impact of <b>regional conflict</b> and the approaching <b>summer season</b> on "
    f"client presence and booking intent in Dubai. The data reveals a market that remains "
    f"predominantly active locally, but with a notable segment of clients either currently abroad "
    f"or uncertain about their return — directly informing how the studio should allocate its "
    f"marketing budget and messaging for June–August.", S_body))
story.append(Spacer(1, 0.3*cm))

# ── KPI ROW ──────────────────────────────────────────────────────────────────
contact_rate = round(answered/total*100,1)
dubai_rate   = round(in_dubai/answered*100,1) if answered else 0
absent_rate  = round(not_dubai/answered*100,1) if answered else 0

kpi_data = [
    [Paragraph(str(total), S_kpi_val),
     Paragraph(f"{answered} ({contact_rate}%)", S_kpi_val),
     Paragraph(str(in_dubai), S_kpi_val),
     Paragraph(str(not_dubai), S_kpi_val)],
    [Paragraph("Total Records", S_kpi_lbl),
     Paragraph("Reached (Contact Rate)", S_kpi_lbl),
     Paragraph("Confirmed In Dubai", S_kpi_lbl),
     Paragraph("Currently Absent", S_kpi_lbl)],
]
kpi_table = Table(kpi_data, colWidths=[W/4]*4)
kpi_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(C_MID)),
    ("BOX",        (0,0), (-1,-1), 1, colors.HexColor(C_ACCENT)),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.HexColor(C_GREY)),
    ("ALIGN",      (0,0), (-1,-1), "CENTER"),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1),8),
]))
story.append(kpi_table)
story.append(Spacer(1, 0.5*cm))

# ── SECTION 1: CALL PERFORMANCE ──────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("1. OUTREACH PERFORMANCE", S_h2))

row1 = [[Image(buf1, width=W*0.47, height=W*0.35),
         Image(buf2, width=W*0.47, height=W*0.35)]]
t1 = Table(row1, colWidths=[W*0.5, W*0.5])
t1.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
story.append(t1)
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("Key Findings:", S_h3))
story.append(Paragraph(
    f"• <b>Contact rate of {contact_rate}%</b> ({answered}/{total}) — a strong baseline for a "
    f"cold-recall campaign.", S_bullet))
story.append(Paragraph(
    f"• <b>{phone_off} numbers ({round(phone_off/total*100,1)}%) were switched off</b> — "
    f"likely clients who have temporarily or permanently left the region.", S_bullet))
story.append(Paragraph(
    f"• <b>{no_ans} no-answers ({round(no_ans/total*100,1)}%)</b> represent a recoverable segment "
    f"via WhatsApp/SMS follow-up.", S_bullet))
story.append(Paragraph(
    f"• Of those reached, <b>{dubai_rate}% confirmed they are in Dubai</b>, while "
    f"<b>{absent_rate}% are currently outside</b> the country.", S_bullet))

# ── SECTION 2: GEOGRAPHIC DISPERSION ─────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("2. GEOGRAPHIC DISPERSION OF ABSENT CLIENTS", S_h2))
story.append(Image(buf3, width=W*0.85, height=W*0.38))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("Key Findings:", S_h3))
story.append(Paragraph(
    "• The <b>UK dominates</b> as the top destination for absent clients — suggesting a strong "
    "British expat segment that travels home during the summer.", S_bullet))
story.append(Paragraph(
    "• <b>France and Germany</b> follow, confirming a significant Western European clientele.", S_bullet))
story.append(Paragraph(
    "• <b>Bahrain and Abu Dhabi</b> appearances suggest some regional displacement — these clients "
    "may return quickly and should be priority-targeted.", S_bullet))
story.append(Paragraph(
    "• <b>Russia, Spain, Egypt, Panama, Bali, Singapore, Morocco</b> all represented — "
    "the studio has a genuinely international client base.", S_bullet))

# ── SECTION 3: DAILY ACTIVITY ─────────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("3. OUTREACH VOLUME OVER TIME", S_h2))
story.append(Image(buf4, width=W, height=W*0.33))
story.append(Spacer(1,0.2*cm))
story.append(Paragraph("Key Findings:", S_h3))
story.append(Paragraph(
    "• The campaign peaked in <b>late March / early April</b> with the heaviest single-day volumes, "
    "suggesting proactive follow-up immediately after the regional conflict escalation.", S_bullet))
story.append(Paragraph(
    "• A notable <b>April 14 surge</b> (highest single-day record) likely reflects a systematic "
    "sweep of the full database.", S_bullet))
story.append(Paragraph(
    "• Activity levels in <b>May 2025 dropped</b> — indicating either saturation of the reachable "
    "pool or a shift to other tasks. Fresh outreach waves are recommended.", S_bullet))

# ── SECTION 4: RETURN TIMELINE ───────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("4. ABSENT CLIENT RETURN TIMELINE SEGMENTATION", S_h2))
story.append(Image(buf5, width=W*0.75, height=W*0.33))
story.append(Spacer(1,0.2*cm))

short_n = ret_seg.get("Short-term (<1 mo)", 0)
mid_n   = ret_seg.get("Mid-term (1–3 mo)", 0)
long_n  = ret_seg.get("Long-term (3+ mo)", 0)
no_date = ret_seg.get("No Definite Date", 0)
lost    = ret_seg.get("Lost Client", 0)

story.append(Paragraph("Key Findings:", S_h3))
story.append(Paragraph(
    f"• <b>{short_n} clients short-term (<1 month)</b> — immediate re-engagement priority. "
    f"These clients are returning imminently and should receive booking incentive offers NOW.", S_bullet))
story.append(Paragraph(
    f"• <b>{mid_n} clients mid-term (1–3 months)</b> — target with June/July 'book before you arrive' "
    f"campaigns.", S_bullet))
story.append(Paragraph(
    f"• <b>{long_n} clients long-term (3+ months)</b> — low summer priority; nurture with newsletter "
    f"content and autumn re-engagement.", S_bullet))
story.append(Paragraph(
    f"• <b>{no_date} clients gave no definite return date</b> — monitor and ping in 30–45 days.", S_bullet))
story.append(Paragraph(
    f"• <b>{lost} clients indicated they are no longer based in Dubai</b> — consider archiving "
    f"or targeting with remote/virtual studio services.", S_bullet))

# ── SECTION 5: STUDIO PREFERENCES ───────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("5. STUDIO BRAND MENTIONS", S_h2))
studio_rows = [[Paragraph("<b>Studio</b>", S_body),
                Paragraph("<b>Mentions</b>", S_body)]]
for s, c in studios.items():
    studio_rows.append([Paragraph(str(s), S_body), Paragraph(str(c), S_body)])
st_table = Table(studio_rows, colWidths=[W*0.7, W*0.25])
st_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(C_ACCENT)),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor(C_MID)),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("TEXTCOLOR",  (0,1), (-1,-1), colors.HexColor(C_LIGHT)),
    ("BOX",        (0,0), (-1,-1), 1, colors.HexColor(C_GREY)),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.HexColor(C_GREY)),
    ("ALIGN",      (1,0), (1,-1), "CENTER"),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6),
]))
story.append(st_table)
story.append(Spacer(1,0.2*cm))
story.append(Paragraph(
    "Studios explicitly named by clients include <b>Dimension, Metro Podcast Studio, "
    "Podster, Procast Studio, and Upod</b>. These are competitive studios the clients "
    "are aware of or have used — key intelligence for positioning and differentiation.", S_body))

# ── SECTION 6: RISK ASSESSMENT ───────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("6. RISK ASSESSMENT — WAR IMPACT + SUMMER EFFECT", S_h2))

risk_data = [
    ["Risk Factor","Severity","Evidence","Recommended Action"],
    ["Regional conflict\nclient exodus","MEDIUM",
     f"{phone_off} phones off\n({round(phone_off/total*100,1)}% of database)",
     "Retain Dubai-based clients with loyalty\noffers; don't over-invest in departed"],
    ["Summer seasonal\ndecline","HIGH",
     f"{not_dubai} clients confirmed\noutside Dubai",
     "Shift budget to retention + 'coming back'\ncampaigns targeting UK/EU"],
    ["Unreachable pool","MEDIUM",
     f"{no_ans+phone_off} ({round((no_ans+phone_off)/total*100,1)}%)\nnot reached",
     "WhatsApp/email retargeting with a\npersonalised message"],
    ["Competitor studio\nawareness","LOW-MEDIUM",
     "5 competitor studios\nnamed by clients",
     "Benchmark pricing & services vs.\nDimension, Podster, Metro"],
    ["Long-term absent\nclients","LOW",
     f"{long_n} returning\nin 3+ months",
     "Autumn re-engagement campaign\nlaunched in Aug/Sep"],
]
risk_table = Table(risk_data, colWidths=[W*0.2, W*0.12, W*0.26, W*0.36])
risk_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(C_ACCENT)),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor(C_MID)),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("TEXTCOLOR",  (0,1), (-1,-1), colors.HexColor(C_LIGHT)),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("BOX",        (0,0), (-1,-1), 1, colors.HexColor(C_GREY)),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.HexColor(C_GREY)),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
    # severity colours
    ("BACKGROUND", (1,2), (1,2), colors.HexColor("#c0392b")),  # HIGH
    ("BACKGROUND", (1,1), (1,1), colors.HexColor(C_GOLD)),     # MEDIUM
    ("BACKGROUND", (1,3), (1,3), colors.HexColor(C_GOLD)),
    ("BACKGROUND", (1,4), (1,4), colors.HexColor("#16a085")),  # LOW-MEDIUM
    ("BACKGROUND", (1,5), (1,5), colors.HexColor(C_BLUE)),     # LOW
    ("TEXTCOLOR",  (1,1), (1,-1), colors.white),
    ("FONTNAME",   (1,1), (1,-1), "Helvetica-Bold"),
    ("ALIGN",      (1,0), (1,-1), "CENTER"),
]))
story.append(risk_table)

# ── SECTION 7: MARKETING RECOMMENDATIONS ─────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("7. MARKETING STRATEGY & BUDGET RECOMMENDATIONS", S_h2))

story.append(Paragraph("JUNE 2025 — PRIORITY ACTIONS", S_h3))
rec_data = [
    ["#","Action","Target Segment","Budget Priority","Channel"],
    ["1","'Welcome Back' campaign with\nbooking discount for returning clients",
     f"Short-term returnees\n({short_n} clients)","★★★★★","WhatsApp / Direct call"],
    ["2","Dubai-based client retention:\nMonthly subscription / loyalty pack",
     f"In-Dubai confirmed\n({in_dubai} clients)","★★★★☆","Email + Instagram"],
    ["3","WhatsApp blast to no-answer list\nwith offer + studio tour video",
     f"Unreached ({no_ans+phone_off} contacts)","★★★☆☆","WhatsApp"],
    ["4","UK/Europe geo-targeted social ads\n'Coming back to Dubai? Book your pod'",
     "UK, France, Germany\nexpat communities","★★★☆☆","Meta Ads"],
    ["5","Competitor differentiation content\n(vs. Dimension, Podster, Metro)",
     "All active + returning clients","★★★☆☆","Instagram / YouTube"],
    ["6","Autumn nurture sequence (email)",
     f"Long-term absent ({long_n})\n+ no-date ({no_date})","★★☆☆☆","Email"],
]
rec_table = Table(rec_data, colWidths=[W*0.04, W*0.30, W*0.22, W*0.14, W*0.24])
rec_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(C_ACCENT)),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor(C_MID)),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("TEXTCOLOR",  (0,1), (-1,-1), colors.HexColor(C_LIGHT)),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("BOX",        (0,0), (-1,-1), 1, colors.HexColor(C_GREY)),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.HexColor(C_GREY)),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("ALIGN",      (0,0),(0,-1),"CENTER"),
    ("ALIGN",      (3,0),(3,-1),"CENTER"),
]))
story.append(rec_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("BUDGET ALLOCATION GUIDANCE (% of Monthly Marketing Budget)", S_h3))
budget_data = [
    ["Channel / Campaign","Allocation","Rationale"],
    ["Direct WhatsApp / SMS outreach\n(returning clients + unreached list)","30%",
     "Highest conversion — personal touch;\nlow cost, high impact"],
    ["Meta Ads (UK, France, Germany geo-targeting)","25%",
     "Capture expats before they return;\nbuild anticipation"],
    ["Instagram organic + Reels\n(competitor differentiation)","15%",
     "Brand awareness; differentiate\nvs. named competitors"],
    ["Email nurture sequences\n(mid/long-term absent)","10%",
     "Low cost; keeps studio top of mind\nfor autumn return"],
    ["Loyalty / retention offers\nfor in-Dubai clients","15%",
     "Prevent churn of confirmed\nactive clients"],
    ["Content production\n(studio tour, testimonials)","5%",
     "Once-off asset; high reuse value\nacross all channels"],
]
bud_table = Table(budget_data, colWidths=[W*0.38, W*0.12, W*0.44])
bud_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(C_GOLD)),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor(C_MID)),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.HexColor(C_DARK)),
    ("TEXTCOLOR",  (0,1), (-1,-1), colors.HexColor(C_LIGHT)),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8),
    ("BOX",        (0,0), (-1,-1), 1, colors.HexColor(C_GREY)),
    ("INNERGRID",  (0,0), (-1,-1), 0.5, colors.HexColor(C_GREY)),
    ("ALIGN",      (1,0),(1,-1),"CENTER"),
    ("FONTNAME",   (1,1),(1,-1),"Helvetica-Bold"),
    ("TEXTCOLOR",  (1,1),(1,-1),colors.HexColor(C_GOLD)),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(bud_table)

# ── SECTION 8: ACTION CHECKLIST ──────────────────────────────────────────────
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_GREY)))
story.append(Paragraph("8. IMMEDIATE ACTION CHECKLIST (NEXT 2 WEEKS)", S_h2))
actions = [
    ("TODAY", "Export all 'Short-term returnee' contacts and assign to sales for personal follow-up call"),
    ("TODAY", "Draft WhatsApp template for unreached clients (no-answer + phone-off list)"),
    ("THIS WEEK", f"Create a 'Coming back to Dubai?' offer — minimum 10% booking discount or free add-on"),
    ("THIS WEEK", "Set up Meta Ads campaign targeting UK, France, Germany with UAE podcast/content creator interest"),
    ("THIS WEEK", "Audit pricing and services vs. Dimension, Podster, Metro Podcast Studio, Procast, Upod"),
    ("NEXT WEEK", "Send loyalty offer to all confirmed in-Dubai clients (email + WhatsApp)"),
    ("NEXT WEEK", "Build email automation for mid/long-term absent clients (6-week nurture sequence)"),
    ("END OF JUNE", "Re-run outreach call campaign on all unreached records — situation may have changed"),
]
for timing, task in actions:
    story.append(Paragraph(f"<b>[{timing}]</b> {task}", S_bullet))

# ── FOOTER ───────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(C_ACCENT)))
story.append(Paragraph(
    "Dubai Podcast Studio | Client Intelligence Report | Confidential | May 2025",
    style("footer", fontSize=8, textColor=colors.HexColor(C_GREY), alignment=TA_CENTER)))

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved to: {pdf_path}")
print(f"Total records: {total}")
print(f"Answered: {answered} ({contact_rate}%)")
print(f"In Dubai: {in_dubai} | Absent: {not_dubai}")
