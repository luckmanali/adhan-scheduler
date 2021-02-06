"""
Configuration for adhan-scheduler
"""

ADHANS = [
    # ADD YOUR ADHAN LINKS HERE ...
    "https://github.com/luckmanali/adhan-collection/blob/main/Masjid%20Al-Haram.mp3?raw=true",
]

# Supported CLI Media Players
CLI_MEDIA_PLAYERS = {
    'mplayer',
    'omxplayer'
}


# 0 for Shafi.
# 1 for Hanafi.
SCHOOL = 1


"""
The following calculation methods are supported:
1. Muslim World League
2. Islamic Society of North America
3. Egyptian General Authority of Survey
4. Umm Al-Qura University, Makkah
5. University of Islamic Sciences, Karachi
6. Institute of Geophysics, University of Tehran
7. Shia Ithna-Ashari, Leva Institute, Qum
8. Gulf Region
9. Kuwait
10. Qatar
11. Majlis Ugama Islam Singapura, Singapore
12. Union Organization islamic de France
13. Diyanet İşleri Başkanlığı, Turkey
14. Spiritual Administration of Muslims of Russia

For more details please visit: https://aladhan.com/calculation-methods
"""
METHOD = 1


# You can tune the results to match your local mosque using the OFFSET variable.
# Index order: "Fajr, Zhuhr, Asr, Maghrib, Isha"
# Example: OFFSET = [-45, 0, 4, 0, -29]
OFFSET = None
