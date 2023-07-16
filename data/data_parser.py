import json


def check_json(obj):
    if isinstance(obj, dict):
        return sorted((k, check_json(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(check_json(x) for x in obj)
    else:
        return obj


today = '''
📅 Monday (2023-02-13):

⏰ 09:00 AM - 10:30 AM: Data Structures and Algorithms (lec) by Nikolay Kudasov (🏢 Room: 108)
⏰ 10:40 AM - 12:10 PM: Data Structures and Algorithms (tut) by Nikolay Kudasov (🏢 Room: 108)
⏰ 02:20 PM - 03:50 PM: Data Structures and Algorithms (lab) by Khaled Ismaeel (🏢 Room: 303)
'''

week = '''
📅 Monday (2023-02-13):

⏰ 09:00 AM - 10:30 AM: Data Structures and Algorithms (lec) by Nikolay Kudasov (🏢 Room: 108)
⏰ 10:40 AM - 12:10 PM: Data Structures and Algorithms (tut) by Nikolay Kudasov (🏢 Room: 108)
⏰ 02:20 PM - 03:50 PM: Data Structures and Algorithms (lab) by Khaled Ismaeel (🏢 Room: 303)

📅 Tuesday (2023-02-14):

⏰ 09:00 AM - 10:30 AM: Software Systems Analysis and Design (lec) by Evgeni Zouev (🏢 Room: 108)
⏰ 10:40 AM - 12:10 PM: Software Systems Analysis and Design (tut) by Imam Muwaffaq (💻 Room: ONLINE)
⏰ 12:40 PM - 02:10 PM: Software Systems Analysis and Design (lab) by Fahima Mokhtari (🏢 Room: 303)
⏰ 02:20 PM - 03:50 PM: English for Academic Purposes I by Gelvanovsky, Kruglova, Rednikova, Melnikova, Saduov, Marouf (🏢 Room: 105/314/313/318/320/421)
⏰ 04:00 PM - 05:30 PM: English for Academic Purposes I by Gelvanovsky, Kruglova, Rednikova, Melnikova, Saduov, Marouf (🏢 Room: 105/314/313/318/320/421)

📅 Wednesday (2023-02-15):

⏰ 10:40 AM - 12:10 PM: Theoretical Computer Science (lec) by Manuel Mazzara (🏢 Room: 108)
⏰ 02:20 PM - 03:50 PM: Theoretical Computer Science (lab) by Andrey Frolov (🏢 Room: 321)

📅 Thursday (2023-02-16):

⏰ 10:40 AM - 12:10 PM: Analytical Geometry and Linear Algebra II (lec) by Yaroslav Kholodov (🏢 Room: 108)
⏰ 04:00 PM - 05:30 PM: Analytical Geometry and Linear Algebra II (lab) by Ivan Konyukhov (🏢 Room: 314)

📅 Friday (2023-02-17):

⏰ 09:00 AM - 10:30 AM: Mathematical Analysis II (lec) by Oleg Kiselev (🏢 Room: 108)
⏰ 10:40 AM - 12:10 PM: Mathematical Analysis II (tut) by Imre Delgado (🏢 Room: 108)
⏰ 12:40 PM - 02:10 PM: Mathematical Analysis II (lab) by Zlata Shchedrikova (🏢 Room: 301)
⏰ 02:20 PM - 03:50 PM: English for Academic Purposes I by Gelvanovsky, Kruglova, Rednikova, Melnikova, Saduov, Marouf (🏢 Room: 314/313/316/318/320/421)
⏰ 04:00 PM - 05:30 PM: English for Academic Purposes I by Gelvanovsky, Kruglova, Rednikova, Melnikova, Saduov, Marouf (🏢 Room: 314/313/318/320/421)
'''
